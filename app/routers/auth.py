from uuid import UUID
import logging

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.core.rbac import get_permissions_for_role
from app.core.security import hash_password, verify_password, create_access_token
from app.dependencies import get_db, get_current_user
from app.models.rol import Roles
from app.models.usuario import Usuarios

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Auth"])
DEFAULT_SIGNUP_ROLE_NAME = "Usuario"


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    usuario_id: UUID
    rol_id: UUID | None = None
    rol_nombre: str | None = None
    permissions: list[str] = []


class CurrentUserResponse(BaseModel):
    usuario_id: UUID
    email: str
    rol_id: UUID | None = None
    rol_nombre: str | None = None
    permissions: list[str] = []


class SignUpRequest(BaseModel):
    email: str
    password: str
    nombre: str | None = None


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Endpoint de login. Retorna un token JWT si las credenciales son correctas.
    
    Args:
        request: Email y contraseña
        db: Sesión de base de datos
        
    Returns:
        Token JWT y ID del usuario
        
    Raises:
        HTTPException: Si email o contraseña son incorrectos
    """
    usuario = db.query(Usuarios).filter(
        Usuarios.email == request.email
    ).first()
    
    if not usuario or not verify_password(request.password, usuario.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos"
        )
    
    access_token = create_access_token(data={"sub": str(usuario.id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "usuario_id": usuario.id,
        "rol_id": usuario.rol_id,
        "rol_nombre": usuario.rol.nombre if usuario.rol else None,
        "permissions": get_permissions_for_role(usuario.rol.nombre if usuario.rol else None),
    }


@router.post("/signup", response_model=LoginResponse)
def signup(request: SignUpRequest, db: Session = Depends(get_db)):
    """
    Endpoint de registro. Crea un nuevo usuario y retorna un token JWT.
    
    Args:
        request: Email, contraseña y nombre
        db: Sesión de base de datos
        
    Returns:
        Token JWT y ID del nuevo usuario
        
    Raises:
        HTTPException: Si el email ya existe o hay error en BD
    """
    try:
        # Verificar si el email ya existe
        existing_user = db.query(Usuarios).filter(
            Usuarios.email == request.email
        ).first()
        
        if existing_user:
            logger.warning(f"Intento de signup con email duplicado: {request.email}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El email ya está registrado"
            )

        default_role = db.query(Roles).filter(Roles.nombre == DEFAULT_SIGNUP_ROLE_NAME).first()
        if not default_role:
            default_role = db.query(Roles).order_by(Roles.nombre).first()

        if not default_role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No hay roles disponibles para crear usuarios"
            )
        
        # Crear nuevo usuario
        nuevo_usuario = Usuarios(
            email=request.email,
            password_hash=hash_password(request.password),
            nombre=request.nombre or request.email.split("@")[0],
            apellido=request.nombre or request.email.split("@")[0],
            rol_id=default_role.id,
            activo=True
        )
        
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        
        logger.info(f"Nuevo usuario registrado: {nuevo_usuario.id} ({nuevo_usuario.email})")
        
        # Generar token
        access_token = create_access_token(data={"sub": str(nuevo_usuario.id)})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "usuario_id": nuevo_usuario.id,
            "rol_id": nuevo_usuario.rol_id,
            "rol_nombre": nuevo_usuario.rol.nombre if nuevo_usuario.rol else None,
            "permissions": get_permissions_for_role(nuevo_usuario.rol.nombre if nuevo_usuario.rol else None),
        }
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        logger.warning(f"IntegrityError en signup: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El email ya está registrado o violación de restricción"
        )
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error en signup: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al registrar usuario"
        )


@router.get("/me", response_model=CurrentUserResponse)
def me(current_user: Usuarios = Depends(get_current_user)):
    """Retorna el usuario autenticado actual con su rol."""
    return {
        "usuario_id": current_user.id,
        "email": current_user.email,
        "rol_id": current_user.rol_id,
        "rol_nombre": current_user.rol.nombre if current_user.rol else None,
        "permissions": get_permissions_for_role(current_user.rol.nombre if current_user.rol else None),
    }

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.core.rbac import has_any_permission
from app.core.security import decode_access_token
from app.models.usuario import Usuarios

security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Usuarios:
    """
    Obtiene el usuario actual a partir del token JWT.
    
    Args:
        credentials: Credenciales HTTP (token Bearer)
        db: Sesión de la base de datos
        
    Returns:
        Objeto Usuarios autenticado
        
    Raises:
        HTTPException: Si el token es inválido o el usuario no existe
    """
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )
    
    usuario_id = payload.get("sub")
    if not usuario_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
    
    usuario = db.query(Usuarios).filter(Usuarios.id == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )
    
    return usuario


def require_roles(*allowed_roles: str):
    """Crea una dependencia que exige que el usuario tenga uno de los roles permitidos."""
    normalized_roles = {role.strip().lower() for role in allowed_roles if role.strip()}

    def dependency(current_user: Usuarios = Depends(get_current_user)) -> Usuarios:
        user_role = (current_user.rol.nombre if current_user.rol else "").strip().lower()
        if user_role not in normalized_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tenés permisos para realizar esta acción"
            )
        return current_user

    return dependency


def require_permissions(*required_permissions: str):
    """Crea una dependencia que exige que el usuario tenga algún permiso requerido."""
    normalized_required_permissions = [permission.strip() for permission in required_permissions if permission.strip()]

    def dependency(current_user: Usuarios = Depends(get_current_user)) -> Usuarios:
        user_role = current_user.rol.nombre if current_user.rol else None
        if not has_any_permission(user_role, normalized_required_permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tenés permisos para realizar esta acción"
            )
        return current_user

    return dependency

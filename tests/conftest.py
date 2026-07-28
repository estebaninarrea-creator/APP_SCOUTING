from collections.abc import Generator
from dataclasses import dataclass
from dataclasses import field

import pytest
from fastapi.testclient import TestClient

from app.database import SessionLocal
from app.models.jugador import Jugadores
from app.models.liga import Ligas
from app.models.posicion import Posiciones
from app.models.rol import Roles
from app.models.usuario import Usuarios
from app.dependencies import get_current_user
from app.main import app


@dataclass
class TestRole:
    nombre: str


@dataclass
class TestUser:
    id: str = 'test-user-id'
    nombre: str = 'Test'
    apellido: str = 'User'
    email: str = 'test@example.com'
    rol: TestRole = field(default_factory=lambda: TestRole(nombre='Admin'))


@pytest.fixture(scope='session', autouse=True)
def bootstrap_minimum_test_data() -> Generator[None, None, None]:
    """Asegura datos base para tests que consultan registros existentes."""
    db = SessionLocal()
    try:
        admin_role = db.query(Roles).filter(Roles.nombre == 'Admin').first()
        if not admin_role:
            admin_role = Roles(nombre='Admin', descripcion='Rol admin para testing')
            db.add(admin_role)

        scout_role = db.query(Roles).filter(Roles.nombre == 'Scout').first()
        if not scout_role:
            scout_role = Roles(nombre='Scout', descripcion='Rol scout para testing')
            db.add(scout_role)

        user_role = db.query(Roles).filter(Roles.nombre == 'Usuario').first()
        if not user_role:
            user_role = Roles(nombre='Usuario', descripcion='Rol usuario para testing')
            db.add(user_role)

        db.flush()

        liga = db.query(Ligas).order_by(Ligas.created_at.desc()).first()
        if not liga:
            liga = Ligas(nombre='Liga Test')
            db.add(liga)

        posicion = db.query(Posiciones).order_by(Posiciones.orden.asc()).first()
        if not posicion:
            posicion = Posiciones(codigo='TEST', nombre='Posicion Test', orden=1)
            db.add(posicion)

        jugador = db.query(Jugadores).order_by(Jugadores.created_at.desc()).first()
        if not jugador:
            jugador = Jugadores(
                apellido='Jugador',
                nombre='Test',
                documento='TEST-JUGADOR-BASE',
                activo=True,
            )
            db.add(jugador)

        usuario = db.query(Usuarios).filter(Usuarios.email == 'test-admin@local.dev').first()
        if not usuario:
            usuario = Usuarios(
                rol_id=admin_role.id,
                nombre='Admin',
                apellido='Test',
                email='test-admin@local.dev',
                password_hash='not-used-in-tests',
                activo=True,
            )
            db.add(usuario)

        db.commit()
        yield
    finally:
        db.close()


@pytest.fixture()
def authorized_user() -> TestUser:
    return TestUser()


@pytest.fixture(autouse=True)
def override_current_user(authorized_user: TestUser):
    app.dependency_overrides[get_current_user] = lambda: authorized_user
    try:
        yield
    finally:
        app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)

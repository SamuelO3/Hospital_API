import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi import status

from main import app
from database.config import Base, get_db

# Configuración de la base de datos de prueba
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear tablas
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Sobrescribir la dependencia de la base de datos
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

# Fixtures para datos de prueba
@pytest.fixture
def test_user():
    return {
        "user": {
            "username": "test@example.com",
            "email": "test@example.com",
            "rol_user": "patient",
            "password": "testpassword123"
        },
        "user_information": {
            "first_name_user": "test",
            "second_name_user": "test",
            "first_lastname_user": "test",
            "second_lastname_user": "test",
            "birth_date_user": "2025-11-27",
            "gender_user": "test",
            "phone_number_user": "string",
            "document_number_user": "string",
            "id_user": "string"
        }
    }
@pytest.fixture
def test_admin_user():
    return {
        "user": {
            "username": "admin@example.com",
            "email": "admin@example.com",
            "rol_user": "admin",
            "password": "adminpassword123"
        },
        "user_information": {
            "first_name_user": "testAdmin",
            "second_name_user": "test",
            "first_lastname_user": "test",
            "second_lastname_user": "test",
            "birth_date_user": "2025-11-27",
            "gender_user": "test",
            "phone_number_user": "string",
            "document_number_user": "string",
            "id_user": "string"
        }
    }

@pytest.fixture
def test_user_info():
    return {
        "first_name": "Test",
        "last_name": "User",
        "phone_number": "+1234567890",
        "address": "123 Test St"
    }

@pytest.fixture
def admin_auth_headers(client, test_admin_user, test_user_info):
    """Fixture que devuelve los headers de autenticación para un usuario administrador"""
    # Crear la estructura de datos esperada por la API
    admin_data = {
        "user": {
            "username": test_admin_user["email"].split('@')[0],
            "email": test_admin_user["email"],
            "password": test_admin_user["password"],
            "rol_user": test_admin_user["role"]
        },
        "user_information": test_user_info
    }
    
    # Registrar el usuario administrador
    response = client.post("/auth/register", json=admin_data)
    
    # Si el usuario ya existe, intentar hacer login
    if response.status_code != status.HTTP_201_CREATED:
        login_data = {
            "email": test_admin_user["email"],
            "password": test_admin_user["password"]
        }
    else:
        # Hacer login con el usuario recién creado
        login_data = {
            "email": test_admin_user["email"],
            "password": test_admin_user["password"]
        }
    
    # Iniciar sesión
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == status.HTTP_200_OK
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

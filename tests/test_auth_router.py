import pytest
from fastapi import status
from fastapi.testclient import TestClient
from main import app
from sqlalchemy.orm import Session
from database.config import get_db

client = TestClient(app)

def get_auth_headers(client: TestClient, email: str, password: str):
    """Helper function to get authentication headers"""
    login_data = {
        "email": email,
        "password": password,
    }
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == status.HTTP_200_OK
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_register_user(client, test_user, test_user_info):
    """Test para el registro de un nuevo usuario"""
    # Crear la estructura de datos esperada por la API
    user_data = {
        "user": {
            "username": test_user["user"]["username"].split('@')[0],
            "email": test_user["user"]["email"],
            "password": test_user["user"]["password"],
            "rol_user": test_user["user"]["rol_user"]
        },
        "user_information": test_user_info
    }
    
    # Hacer la petición
    response = client.post("/auth/register", json=user_data)
    
    # Verificar respuesta
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "user" in data
    assert "user_information" in data
    assert data["user"]["email"] == test_user["email"]
    assert data["user_information"]["first_name"] == test_user_info["first_name"]

def test_login_success(client, test_user, test_user_info):
    """Test para el inicio de sesión exitoso"""
    # Primero registrar un usuario
    user_data = {
        "user": {
            "username": test_user["email"].split('@')[0],
            "email": test_user["email"],
            "password": test_user["password"],
            "rol_user": test_user["role"]
        },
        "user_information": test_user_info
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    # Intentar iniciar sesión
    login_data = {
        "email": test_user["email"],
        "password": test_user["password"]
    }
    response = client.post("/auth/login", json=login_data)
    
    # Verificar respuesta
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"
    assert "user" in data

def test_login_invalid_credentials(client, test_user, test_user_info):
    """Test para credenciales inválidas en inicio de sesión"""
    # Primero registrar un usuario
    user_data = {
        "user": {
            "username": test_user["email"].split('@')[0],
            "email": test_user["email"],
            "password": test_user["password"],
            "rol_user": test_user["role"]
        },
        "user_information": test_user_info
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    # Intentar iniciar sesión con contraseña incorrecta
    login_data = {
        "email": test_user["email"],
        "password": "wrongpassword"
    }
    response = client.post("/auth/login", json=login_data)
    
    # Verificar respuesta de error
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Incorrect email or password" in response.json()["detail"]
    
    # Intentar con un email que no existe
    login_data = {
        "email": "nonexistent@example.com",
        "password": test_user["password"]
    }
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_register_duplicate_email(client, test_user, test_user_info):
    """Test para intentar registrar un email ya existente"""
    # Crear datos de usuario con la estructura correcta
    user_data = {
        "user": {
            "username": test_user["user"]["email"].split('@')[0],
            "email": test_user["user"]["email"],
            "password": test_user["user"]["password"],
            "rol_user": test_user["user"]["rol_user"]
        },
        "user_information": test_user_info
    }
    
    # Registrar usuario por primera vez
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    # Intentar registrar el mismo email de nuevo
    response = client.post("/auth/register", json=user_data)
    
    # Verificar respuesta de error
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Email already registered" in response.json()["detail"]

@pytest.fixture
def auth_headers(client, test_user, test_user_info):
    """Fixture que devuelve los headers de autenticación para un usuario de prueba"""
    # Registrar usuario
    user_data = {
        "user": {
            "username": test_user["user"]["email"].split('@')[0],
            "email": test_user["user"]["email"],
            "password": test_user["user"]["password"],
            "rol_user": test_user["user"]["rol_user"]
        },
        "user_information": test_user_info
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    # Iniciar sesión
    login_data = {
        "email": test_user["email"],
        "password": test_user["password"]
    }
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == status.HTTP_200_OK
    
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_protected_route(client, auth_headers):
    """Test para verificar que las rutas protegidas requieren autenticación"""
    # Intentar acceder sin token
    response = client.get("/auth/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    # Acceder con token válido
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert "email" in response.json()

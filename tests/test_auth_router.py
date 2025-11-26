import pytest
from fastapi import status
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register_user(client, test_user, test_user_info):
    """Test para el registro de un nuevo usuario"""
    # Combinar datos de usuario y su información
    user_data = {"user": test_user, "user_information": test_user_info}
    
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
    user_data = {"user": test_user, "user_information": test_user_info}
    client.post("/auth/register", json=user_data)
    
    # Intentar iniciar sesión
    login_data = {
        "email": test_user["email"],
        "password": test_user["password"]
    }
    response = client.post("/auth/login", data=login_data)
    
    # Verificar respuesta
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client):
    """Test para credenciales inválidas en inicio de sesión"""
    login_data = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    }
    response = client.post("/auth/login", data=login_data)
    
    # Verificar respuesta de error
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Incorrect email or password" in response.json()["detail"]

def test_register_duplicate_email(client, test_user, test_user_info):
    """Test para intentar registrar un email ya existente"""
    # Registrar usuario por primera vez
    user_data = {"user": test_user, "user_information": test_user_info}
    client.post("/auth/register", json=user_data)
    
    # Intentar registrar el mismo email de nuevo
    response = client.post("/auth/register", json=user_data)
    
    # Verificar respuesta de error
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Email already registered" in response.json()["detail"]

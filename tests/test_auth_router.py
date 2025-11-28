import pytest
from fastapi import status
from fastapi.testclient import TestClient
from main import app
from sqlalchemy.orm import Session
from database.config import get_db
from uuid import uuid4

client = TestClient(app)

def test_register_user(client):
    """Test para registrar un usuario correctamente"""
    test_uuid = str(uuid4())

    user_data = {
        "user": {
            "username": "testuser",
            "email": "testuser@example.com",
            "rol_user": "patient",
            "password": "strongpassword123"
        },
        "user_information": {
            "first_name_user": "John",
            "second_name_user": "Michael",
            "first_lastname_user": "Doe",
            "second_lastname_user": "Smith",
            "birth_date_user": "2025-11-28",
            "gender_user": "Male",
            "phone_number_user": "123456",
            "document_number_user": "ABC123",
            "id_user": test_uuid
        }
    }

    response = client.post("/auth/register", json=user_data)

    assert response.status_code == 201
    result = response.json()

    assert "user" in result
    assert "user_information" in result
    assert result["user"]["email"] == "testuser@example.com"
    assert result["user_information"]["first_name_user"] == "John"


def test_login_success(client):
    """Test para login exitoso"""
    test_uuid = str(uuid4())

    # Primero registrar
    user_data = {
        "user": {
            "username": "loginuser",
            "email": "login@example.com",
            "rol_user": "patient",
            "password": "mypassword123"
        },
        "user_information": {
            "first_name_user": "Alice",
            "second_name_user": "Q",
            "first_lastname_user": "Brown",
            "second_lastname_user": "Smith",
            "birth_date_user": "2025-11-28",
            "gender_user": "Female",
            "phone_number_user": "123",
            "document_number_user": "XYZ999",
            "id_user": test_uuid
        }
    }
    client.post("/auth/register", json=user_data)

    # Hacer login
    login_data = {
        "email": "login@example.com",
        "password": "mypassword123"
    }

    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.fixture
def auth_headers(client, test_user):
    """Fixture que devuelve los headers de autenticación para un usuario de prueba"""
    # Registrar usuario
    user_data = {
        "user": {
            "username": test_user["username"],
            "email": test_user["email"],
            "rol_user": test_user["rol_user"],
            "password": test_user["password"]
        },
        "user_information": test_user["payload"]["user_information"]
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

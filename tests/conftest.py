import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi import status
from uuid import uuid4

from main import app

# from main import app
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
    test_uuid = str(uuid4())
    payload = {
        "user": {
            "username": "test",
            "email": "test@example.com",
            "rol_user": "patient",
            "password": "testpassword123",
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
            "id_user": test_uuid,
        },
    }
    user_flat = {
        "username": payload["user"]["username"],
        "email": payload["user"]["email"],
        "rol_user": payload["user"]["rol_user"],
        "password": payload["user"]["password"],
        "payload": payload,
    }
    return user_flat


@pytest.fixture
def test_admin_user():
    test_uuid = str(uuid4())
    payload = {
        "user": {
            "username": "admin",
            "email": "admin@example.com",
            "rol_user": "admin",
            "password": "adminpassword123",
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
            "id_user": test_uuid,
        },
    }
    admin_flat = {
        "username": payload["user"]["username"],
        "email": payload["user"]["email"],
        "rol_user": payload["user"]["rol_user"],
        "password": payload["user"]["password"],
        "payload": payload,
    }
    return admin_flat


@pytest.fixture
def test_user_info():
    test_uuid = str(uuid4())
    return {
        "first_name_user": "Test",
        "second_name_user": "User",
        "first_lastname_user": "Example",
        "second_lastname_user": "Example2",
        "birth_date_user": "2025-11-27",
        "gender_user": "Other",
        "phone_number_user": "+123456789",
        "document_number_user": "ABC123",
        "id_user": test_uuid,
    }


@pytest.fixture
def admin_auth_headers(client, test_admin_user):
    admin_data = {
        "user": {
            "username": test_admin_user["username"],
            "email": test_admin_user["email"],
            "password": test_admin_user["password"],
            "rol_user": test_admin_user["rol_user"],
        },
        "user_information": test_admin_user["payload"]["user_information"],
    }

    # Registrar
    response = client.post("/auth/register", json=admin_data)

    # Hacer login
    login_data = {
        "email": test_admin_user["email"],
        "password": test_admin_user["password"],
    }

    response = client.post("/auth/login", json=login_data)
    assert response.status_code == status.HTTP_200_OK

    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def nurse_user(client):
    """
    Registra un usuario y devuelve:
    - id_user
    - id_user_information
    """

    uid = str(uuid4())

    user_payload = {
        "user": {
            "username": f"user_{uid}",
            "email": f"user_{uid}@example.com",
            "rol_user": "nurse",  # o 'medic', según cómo lo manejes en tu sistema
            "password": "password123"
        },
        "user_information": {
            "first_name_user": "Test",
            "second_name_user": "Nurse",
            "first_lastname_user": "User",
            "second_lastname_user": "Role",
            "birth_date_user": "2025-11-28",
            "gender_user": "Male",
            "phone_number_user": "000111",
            "document_number_user": f"DOC999nurse{uid}",
            "id_user": uid
        }
    }

    r = client.post("/auth/register", json=user_payload)
    assert r.status_code == status.HTTP_201_CREATED

    data = r.json()

    return {
        "id_user": data["user"]["id_user"],
        "id_user_information": data["user_information"]["id_user_information"],
        "email": data["user"]["email"],
        "password": "password123"
    }


@pytest.fixture
def medic_user(client):
    """
    Registra un usuario y devuelve:
    - id_user
    - id_user_information
    """
    uid = str(uuid4())

    user_payload = {
        "user": {
            "username": f"user_{uid}",
            "email": f"user_{uid}@example.com",
            "rol_user": "medic",
            "password": "password123"
        },
        "user_information": {
            "first_name_user": "Test",
            "second_name_user": "Medic",
            "first_lastname_user": "User",
            "second_lastname_user": "Role",
            "birth_date_user": "2025-11-28",
            "gender_user": "Male",
            "phone_number_user": "000111",
            "document_number_user": f"DOC999medic{uid}",
            "id_user": uid
        }
    }

    r = client.post("/auth/register", json=user_payload)
    assert r.status_code == 201

    data = r.json()

    return {
        "id_user": data["user"]["id_user"],
        "id_user_information": data["user_information"]["id_user_information"],
        "email": data["user"]["email"],
        "password": "password123"
    }


@pytest.fixture
def patient_user(client):
    """
    Registra un usuario y devuelve:
    - id_user
    - id_user_information
    - email
    - password
    """
    uid = str(uuid4())

    user_payload = {
        "user": {
            "username": f"patient_{uid}",
            "email": f"patient_{uid}@example.com",
            "rol_user": "user",
            "password": "password123",
        },
        "user_information": {
            "first_name_user": "Test",
            "second_name_user": "Patient",
            "first_lastname_user": "User",
            "second_lastname_user": "Role",
            "birth_date_user": "2025-11-28",
            "gender_user": "Male",
            "phone_number_user": "000111",
            "document_number_user": f"DOC999patient{uid}",
            "id_user": uid,
        },
    }

    r = client.post("/auth/register", json=user_payload)
    assert r.status_code == status.HTTP_201_CREATED

    data = r.json()

    return {
        "id_user": data["user"]["id_user"],
        "id_user_information": data["user_information"]["id_user_information"],
        "email": data["user"]["email"],
        "password": "password123",
    }

#     # Iniciar sesión
#     response = client.post("http:/d/127.0.0.1:8000/auth/login", json=login_data)
#     assert response.status_code == status.HTTP_200_OK
#     token = response.json()["access_token"]
#     return {"Authorization": f"Bearer {token}"}

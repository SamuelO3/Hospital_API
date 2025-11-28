import pytest
from fastapi import status
from uuid import uuid4
from datetime import date

# Import the auth_headers fixture from test_auth_router
from conftest import admin_auth_headers
import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    return TestClient(app)


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

def test_create_medic(client, medic_user, admin_auth_headers):
    """
    Prueba crear un médico usando un usuario con rol MEDIC
    """

    medic_payload = {
        "specialty": "Cardiology",
        "id_user_information": medic_user["id_user_information"]
    }

    r = client.post("/medics/", json=medic_payload, headers=admin_auth_headers)
    assert r.status_code == 201
    

    data = r.json()

    assert data["specialty"] == "Cardiology"
    assert data["id_user_information"] == medic_user["id_user_information"]


def test_get_medics(client, admin_auth_headers):
    r = client.get("/medics/", headers=admin_auth_headers)

    assert r.status_code in (200, 404)


def test_get_medic_by_id(client, medic_user, admin_auth_headers):
    # Primero lo creamos
    payload = {
        "specialty": "Pediatrics",
        "id_user_information": medic_user["id_user_information"]
    }
    r = client.post("/medics/", json=payload, headers=admin_auth_headers)
    medic_id = r.json()["id_medic"]

    # Lo obtenemos
    r = client.get(f"/medics/{medic_id}", headers=admin_auth_headers)

    assert r.status_code == 200


def test_delete_medic(client, medic_user, admin_auth_headers):
    # Primero lo creamos
    payload = {
        "specialty": "Pediatrics",
        "id_user_information": medic_user["id_user_information"]
    }
    r = client.post("/medics/", json=payload, headers=admin_auth_headers)
    medic_id = r.json()["id_medic"]

    # Lo eliminamos
    r = client.delete(f"/medics/delete/{medic_id}", headers=admin_auth_headers)

    assert r.status_code == 200




# ========================= Si se necesitan mocks =========================
# from unittest.mock import MagicMock
# from controllers.medic_controller import create_medic
# from schemas.medic_schema import Medic

# def test_create_medic_unit():
#     db = MagicMock()

#     medic_payload = Medic(
#         specialty="Cardiology",
#         id_user_information="uuid-123"
#     )

#     # La función modifica el objeto así que solo validamos que se llame a add/commit
#     create_medic(db, medic_payload)

#     db.add.assert_called_once()
#     db.commit.assert_called_once()

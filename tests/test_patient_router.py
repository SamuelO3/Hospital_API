from fastapi import status
import pytest
from fastapi.testclient import TestClient
from uuid import uuid4
from main import app

from conftest import admin_auth_headers


@pytest.fixture
def client():
    return TestClient(app)


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


# ==================== TESTS CREATE PATIENT ====================


def test_create_patient(client, patient_user, admin_auth_headers):
    """
    Prueba crear un paciente usando un usuario con rol PATIENT
    """
    patient_payload = {
        "blood_type": "O+",
        "id_user_information": patient_user["id_user_information"],
    }

    r = client.post("/patient/", json=patient_payload, headers=admin_auth_headers)
    assert r.status_code == status.HTTP_200_OK

    data = r.json()
    assert data["blood_type"] == "O+"
    assert data["id_user_information"] == patient_user["id_user_information"]
    assert "id_patient" in data


def test_create_patient_duplicate_user_info_fails(
    client, patient_user, admin_auth_headers
):
    """
    Prueba que no se puede crear dos pacientes con el mismo id_user_information
    """
    patient_payload = {
        "blood_type": "A+",
        "id_user_information": patient_user["id_user_information"],
    }

    # Crear el primer paciente
    r = client.post("/patient/", json=patient_payload, headers=admin_auth_headers)
    assert r.status_code == status.HTTP_200_OK

    # Intentar crear otro con el mismo id_user_information
    r = client.post("/patient/", json=patient_payload, headers=admin_auth_headers)
    assert r.status_code == status.HTTP_400_BAD_REQUEST


# # ==================== TESTS GET PATIENTS ====================


def test_get_all_patients(client, admin_auth_headers):
    """
    Prueba obtener todos los pacientes
    """
    r = client.get("/patient/all", headers=admin_auth_headers)
    assert r.status_code in (status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST)

    if r.status_code == status.HTTP_200_OK:
        data = r.json()
        assert isinstance(data, list)


def test_get_patients_pagination(client, admin_auth_headers):
    """
    Prueba la paginación de pacientes
    """
    # Crear varios pacientes
    for i in range(5):
        uid = str(uuid4())
        user_payload = {
            "user": {
                "username": f"patient_{uid}",
                "email": f"patient_{uid}@example.com",
                "rol_user": "patient",
                "password": "password123",
            },
            "user_information": {
                "first_name_user": f"Patient{i}",
                "second_name_user": "Test",
                "first_lastname_user": "User",
                "second_lastname_user": "Pagination",
                "birth_date_user": "1990-01-01",
                "gender_user": "Male",
                "phone_number_user": f"555-000{i}",
                "document_number_user": f"DOCPAGE{uid}",
                "id_user": uid,
            },
        }

        r = client.post("/auth/register", json=user_payload)
        id_user_info = r.json()["user_information"]["id_user_information"]

        patient_payload = {"blood_type": "O+", "id_user_information": id_user_info}
        client.post("/patient/", json=patient_payload, headers=admin_auth_headers)

    # Obtener con paginación
    limit = 3
    skip = 0
    r = client.get(
        f"/patient/all?limit={limit}&skip={skip}", headers=admin_auth_headers
    )
    assert r.status_code == status.HTTP_200_OK
    data = r.json()
    assert len(data) <= 3


def test_get_patient_by_id(client, patient_user, admin_auth_headers):
    """
    Prueba obtener un paciente por ID
    """
    # Primero lo creamos
    payload = {
        "blood_type": "B+",
        "id_user_information": patient_user["id_user_information"],
    }
    r = client.post("/patient/", json=payload, headers=admin_auth_headers)
    patient_id = r.json()["id_patient"]

    # Lo obtenemos por ID
    r = client.get(f"/patient/{patient_id}", headers=admin_auth_headers)
    # Debug: ver qué responde la API si falla
    if r.status_code != 201:
        print(f"\nStatus Code: {r.status_code}")
        print(f"Response: {r.json()}")

    assert r.status_code == status.HTTP_200_OK

    data = r.json()
    assert data["id_patient"] == patient_id
    assert data["blood_type"] == "B+"


def test_get_patient_by_id_not_found(client, admin_auth_headers):
    """
    Prueba obtener un paciente que no existe
    """
    non_existent_id = str(uuid4())
    r = client.get(f"/patient/{non_existent_id}", headers=admin_auth_headers)
    assert r.status_code == status.HTTP_400_BAD_REQUEST


# # ==================== TESTS UPDATE PATIENT ====================


def test_update_patient(client, patient_user, admin_auth_headers):
    """
    Prueba actualizar un paciente
    """
    # Crear paciente
    payload = {
        "blood_type": "O-",
        "id_user_information": patient_user["id_user_information"],
    }
    r = client.post("/patient/", json=payload, headers=admin_auth_headers)
    patient_id = r.json()["id_patient"]

    # Actualizar
    update_payload = {"blood_type": "AB+"}
    r = client.put(
        f"/patient/update/{patient_id}", json=update_payload, headers=admin_auth_headers
    )
    assert r.status_code == status.HTTP_200_OK

    data = r.json()
    assert data["blood_type"] == "AB+"
    assert data["id_patient"] == patient_id


def test_update_patient_not_found(client, admin_auth_headers):
    """
    Prueba actualizar un paciente que no existe
    """
    non_existent_id = str(uuid4())
    update_payload = {"blood_type": "A-"}
    r = client.put(
        f"/patient/update/{non_existent_id}",
        json=update_payload,
        headers=admin_auth_headers,
    )
    assert r.status_code == status.HTTP_400_BAD_REQUEST


# # ==================== TESTS DELETE PATIENT ====================


def test_delete_patient(client, patient_user, admin_auth_headers):
    """
    Prueba eliminar un paciente
    """
    # Crear paciente
    payload = {
        "blood_type": "A+",
        "id_user_information": patient_user["id_user_information"],
    }
    r = client.post("/patient/", json=payload, headers=admin_auth_headers)
    patient_id = r.json()["id_patient"]

    # Eliminar
    r = client.delete(f"/patient/delete/{patient_id}", headers=admin_auth_headers)
    assert r.status_code == status.HTTP_200_OK

    # Verificar que ya no existe
    r = client.get(f"/patient/{patient_id}", headers=admin_auth_headers)
    assert r.status_code == status.HTTP_400_BAD_REQUEST


def test_delete_patient_not_found(client, admin_auth_headers):
    """
    Prueba eliminar un paciente que no existe
    """
    non_existent_id = str(uuid4())
    r = client.delete(f"/patient/delete/{non_existent_id}", headers=admin_auth_headers)
    assert r.status_code == status.HTTP_400_BAD_REQUEST

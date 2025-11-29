import pytest
from fastapi import status
from uuid import uuid4
from fastapi.testclient import TestClient
from main import app

# Si ya tienes client y admin_auth_headers en conftest, puedes omitir esto
from conftest import admin_auth_headers


@pytest.fixture
def client():
    # Solo si NO lo tienes ya en conftest
    return TestClient(app)


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
def test_create_nurse(client, nurse_user, admin_auth_headers):
    """
    Prueba crear una enfermera usando un usuario registrado
    """

    nurse_payload = {
        "speciality": "Cardiology",  # campo del schema
        "id_user_information": nurse_user["id_user_information"]
    }

    r = client.post("/nurse/", json=nurse_payload, headers=admin_auth_headers)

    # Ajusta según tu router: 201 si pusiste status_code en el POST
    assert r.status_code == status.HTTP_201_CREATED

    data = r.json()

    # Aquí depende de cómo responda tu endpoint exactamente
    assert data["speciality"] == "Cardiology" or data["speciality"] == "Cardiology"
    assert str(data["id_user_information"]) == nurse_user["id_user_information"]


def test_get_nurses(client, admin_auth_headers):
    """
    Prueba obtener el listado de enfermeras
    """

    r = client.get("/nurse/", headers=admin_auth_headers)
    # podría ser 200 aunque no haya enfermeras, simplemente lista vacía
    assert r.status_code == status.HTTP_200_OK


def test_get_nurse_by_id(client, nurse_user, admin_auth_headers):
    """
    Crea una enfermera y la obtiene por id
    """

    payload = {
        "speciality": "Pediatrics",
        "id_user_information": nurse_user["id_user_information"]
    }

    # Crear
    r = client.post("/nurse/", json=payload, headers=admin_auth_headers)
    assert r.status_code == status.HTTP_201_CREATED
    nurse_id = r.json()["id_nurse"]

    # Obtener por id
    r = client.get(f"/nurse/byid/{nurse_id}", headers=admin_auth_headers)

    assert r.status_code == status.HTTP_200_OK
    data = r.json()
    assert data["id_nurse"] == nurse_id


def test_update_nurse(client, nurse_user, admin_auth_headers):
    """
    Crea una enfermera y actualiza su especialidad
    """

    # Crear primero
    payload = {
        "speciality": "Pediatrics",
        "id_user_information": nurse_user["id_user_information"]
    }
    r = client.post("/nurse/", json=payload, headers=admin_auth_headers)
    assert r.status_code == status.HTTP_201_CREATED
    nurse_id = r.json()["id_nurse"]

    # Actualizar
    update_payload = {
        "speciality": "ICU"
    }

    r = client.put(
        f"/nurse/update/{nurse_id}",
        json=update_payload,
        headers=admin_auth_headers
    )

    assert r.status_code == status.HTTP_200_OK
    data = r.json()
    assert data["message"] == "Enfermera actualizada correctamente."
    assert data["nurse"]["speciality"] == "ICU" or data["nurse"]["speciality"] == "ICU"


def test_delete_nurse(client, nurse_user, admin_auth_headers):
    """
    Crea una enfermera y luego la elimina
    """

    # Crear primero
    payload = {
        "speciality": "Pediatrics",
        "id_user_information": nurse_user["id_user_information"]
    }
    r = client.post("/nurse/", json=payload, headers=admin_auth_headers)
    assert r.status_code == status.HTTP_201_CREATED
    nurse_id = r.json()["id_nurse"]

    # Eliminar
    r = client.delete(f"/nurse/delete/{nurse_id}", headers=admin_auth_headers)

    assert r.status_code == status.HTTP_200_OK
    data = r.json()
    assert data["message"] == "Enfermera eliminada correctamente."

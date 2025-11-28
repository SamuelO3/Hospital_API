from fastapi import status
import pytest
from fastapi.testclient import TestClient
from uuid import uuid4
from datetime import date, timedelta
from main import app

# Import the auth_headers fixture from conftest
from conftest import admin_auth_headers


@pytest.fixture
def client():
    return TestClient(app)


def create_test_diagnosis_data():
    """
    Helper para crear datos de diagnóstico de prueba
    """
    return {
        "diagnosis_date": str(date.today()),
        "diagnosis_description": "Diagnóstico de prueba - Paciente presenta síntomas controlados",
    }


# ==================== TESTS CREATE DIAGNOSIS ====================


def test_create_diagnosis(client, admin_auth_headers):
    """
    Prueba crear un diagnóstico
    """
    diagnosis_payload = create_test_diagnosis_data()

    r = client.post("/diagnosis/", json=diagnosis_payload, headers=admin_auth_headers)

    if r.status_code != status.HTTP_200_OK:
        print(f"\nStatus Code: {r.status_code}")
        print(f"Response: {r.json()}")

    assert r.status_code == status.HTTP_200_OK

    data = r.json()
    assert data["diagnosis_description"] == diagnosis_payload["diagnosis_description"]
    assert "id_diagnosis" in data


# ==================== TESTS GET DIAGNOSIS ====================


def test_get_all_diagnosis_pagination(client, admin_auth_headers):
    """
    Prueba la paginación de diagnósticos
    """
    # Crear varios diagnósticos
    for i in range(5):
        diagnosis_payload = {
            "diagnosis_date": str(date.today()),
            "diagnosis_description": f"Diagnóstico de prueba #{i+1}",
        }
        client.post("/diagnosis/", json=diagnosis_payload, headers=admin_auth_headers)

    # Obtener con paginación
    limit = 3
    skip = 0

    r = client.get(
        f"/diagnosis/all?limit={limit}&skip={skip}", headers=admin_auth_headers
    )
    assert r.status_code == status.HTTP_200_OK
    data = r.json()
    assert len(data) <= 3


def test_get_diagnosis_by_id(client, admin_auth_headers):
    """
    Prueba obtener un diagnóstico por ID
    """
    # Crear diagnóstico
    diagnosis_payload = create_test_diagnosis_data()
    r = client.post("/diagnosis/", json=diagnosis_payload, headers=admin_auth_headers)
    diagnosis_id = r.json()["id_diagnosis"]

    # Obtener por ID
    r = client.get(f"/diagnosis/{diagnosis_id}", headers=admin_auth_headers)
    assert r.status_code == status.HTTP_200_OK

    data = r.json()
    assert data["id_diagnosis"] == diagnosis_id


def test_get_diagnosis_by_id_not_found(client, admin_auth_headers):
    """
    Prueba obtener un diagnóstico que no existe
    """
    non_existent_id = str(uuid4())
    r = client.get(f"/diagnosis/{non_existent_id}", headers=admin_auth_headers)

    assert r.status_code == status.HTTP_404_NOT_FOUND


# # ==================== TESTS UPDATE DIAGNOSIS ====================


def test_update_diagnosis(client, admin_auth_headers):
    """
    Prueba actualizar un diagnóstico
    """
    # Crear diagnóstico
    diagnosis_payload = create_test_diagnosis_data()
    r = client.post("/diagnosis/", json=diagnosis_payload, headers=admin_auth_headers)
    diagnosis_id = r.json()["id_diagnosis"]

    # Actualizar
    update_payload = {
        "diagnosis_description": "Diagnóstico actualizado - Mejoría notable"
    }
    r = client.put(
        f"/diagnosis/update/{diagnosis_id}",
        json=update_payload,
        headers=admin_auth_headers,
    )
    assert r.status_code == status.HTTP_200_OK

    data = r.json()
    assert data["diagnosis_description"] == update_payload["diagnosis_description"]


def test_update_diagnosis_not_found(client, admin_auth_headers):
    """
    Prueba actualizar un diagnóstico que no existe
    """
    non_existent_id = str(uuid4())
    update_payload = {"diagnosis_description": "No debería funcionar"}
    r = client.put(
        f"/diagnosis/update/{non_existent_id}",
        json=update_payload,
        headers=admin_auth_headers,
    )
    assert r.status_code == status.HTTP_404_NOT_FOUND


# # ==================== TESTS DELETE DIAGNOSIS ====================


def test_delete_diagnosis(client, admin_auth_headers):
    """
    Prueba eliminar un diagnóstico
    """
    # Crear diagnóstico
    diagnosis_payload = create_test_diagnosis_data()
    r = client.post("/diagnosis/", json=diagnosis_payload, headers=admin_auth_headers)
    diagnosis_id = r.json()["id_diagnosis"]

    # Eliminar
    r = client.delete(f"/diagnosis/delete/{diagnosis_id}", headers=admin_auth_headers)
    assert r.status_code == status.HTTP_200_OK

    # Verificar que ya no existe
    r = client.get(f"/diagnosis/{diagnosis_id}", headers=admin_auth_headers)
    assert r.status_code == status.HTTP_404_NOT_FOUND


def test_delete_diagnosis_not_found(client, admin_auth_headers):
    """
    Prueba eliminar un diagnóstico que no existe
    """
    non_existent_id = str(uuid4())
    r = client.delete(
        f"/diagnosis/delete/{non_existent_id}", headers=admin_auth_headers
    )
    assert r.status_code == status.HTTP_404_NOT_FOUND

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from uuid import uuid4
from main import app
from conftest import admin_auth_headers


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def basic_patient_and_appointment(client, admin_auth_headers):
    """
    Crea un patient + medical_appointment mínimos para poder crear una factura.
    Ajusta esto según tus rutas reales.
    """
    uid = str(uuid4())

    # 1. Crear paciente
    patient_payload = {
        "first_name": "Test",
        "first_lastname": "User",
        "birth_date": "1990-01-01",
        "gender": "Male",
        "phone_number": "000111",
        "document_number": f"DOC{uid}",
    }

    rp = client.post("/patients/", json=patient_payload, headers=admin_auth_headers)
    assert rp.status_code in (200, 201)
    patient = rp.json()
    id_patient = patient["id_patient"]

    # 2. Crear cita médica
    appointment_payload = {
        "id_patient": id_patient,
        "date_appointment": "2025-01-01",
        "time_appointment": "10:00",
        "reason": "Test Reason",
    }

    ra = client.post("/medicalAppointment/", json=appointment_payload, headers=admin_auth_headers)
    assert ra.status_code in (200, 201)
    appointment = ra.json()

    return {
        "id_patient": id_patient,
        "id_medical_appointment": appointment["id_medical_appointment"]
    }


def test_create_bill(client, basic_patient_and_appointment, admin_auth_headers):
    payload = {
        "total": 150.0,
        "id_patient": basic_patient_and_appointment["id_patient"],
        "id_medical_appointment": basic_patient_and_appointment["id_medical_appointment"]
    }

    r = client.post("/bill/", json=payload, headers=admin_auth_headers)
    assert r.status_code in (200, 201)

    data = r.json()
    assert "id_bill" in data
    assert data["total"] == 150.0


def test_get_bill_by_id(client, basic_patient_and_appointment, admin_auth_headers):
    # Crear primero
    payload = {
        "total": 99.0,
        "id_patient": basic_patient_and_appointment["id_patient"],
        "id_medical_appointment": basic_patient_and_appointment["id_medical_appointment"]
    }
    r = client.post("/bill/", json=payload, headers=admin_auth_headers)
    bill_id = r.json()["id_bill"]

    # Obtener
    r = client.get(f"/bill/{bill_id}", headers=admin_auth_headers)
    assert r.status_code == 200
    assert r.json()["id_bill"] == bill_id


def test_update_bill(client, basic_patient_and_appointment, admin_auth_headers):
    payload = {
        "total": 80.0,
        "id_patient": basic_patient_and_appointment["id_patient"],
        "id_medical_appointment": basic_patient_and_appointment["id_medical_appointment"]
    }
    r = client.post("/bill/", json=payload, headers=admin_auth_headers)
    bill_id = r.json()["id_bill"]

    update_payload = {
        "total": 120.0,
        "generation_date": "2024-01-01",
        "generation_hour": "12:00",
        "id_patient": basic_patient_and_appointment["id_patient"],
        "id_medical_appointment": basic_patient_and_appointment["id_medical_appointment"]
    }

    r = client.put(f"/bill/update/{bill_id}", json=update_payload, headers=admin_auth_headers)
    assert r.status_code == 200
    assert r.json()["total"] == 120.0


def test_delete_bill(client, basic_patient_and_appointment, admin_auth_headers):
    payload = {
        "total": 50.0,
        "id_patient": basic_patient_and_appointment["id_patient"],
        "id_medical_appointment": basic_patient_and_appointment["id_medical_appointment"]
    }
    r = client.post("/bill/", json=payload, headers=admin_auth_headers)
    bill_id = r.json()["id_bill"]

    r = client.delete(f"/bill/delete/{bill_id}", headers=admin_auth_headers)
    assert r.status_code == 200
    assert "Response" in r.json()

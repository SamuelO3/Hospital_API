from fastapi import status
import pytest
from fastapi.testclient import TestClient
from uuid import uuid4
from main import app

from conftest import admin_auth_headers
from medic_router import test_create_medic
from patient_router import test_create_patient
from diagnosis_router import test_create_diagnosis


@pytest.fixture
def client():
    return TestClient(app)


def test_create_medical_appointment(client, test_create_medic, test_create_patient, test_create_diagnosis, admin_auth_headers):

    payload = {
        "appointment_date": "2025-11-29",
        "appointment_hour": "09:30:00",
        "location": "Consultorio 203",
        "id_medic": medic["id_medic"],
        "id_nurse": nurse["id_nurse"],
        "id_patient": patient["id_patient"],
        "id_diagnosis": diagnosis["id_diagnosis"]
    }

    r = client.post("/medical_appointment/", json=payload, headers=admin_auth_headers)

    assert r.status_code == 201
    data = r.json()

    assert data["location"] == "Consultorio 203"
    assert data["id_medic"] == medic["id_medic"]

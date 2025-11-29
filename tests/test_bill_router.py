import pytest
from uuid import uuid4
from fastapi.testclient import TestClient
from main import app
from conftest import admin_auth_headers

client = TestClient(app)


@pytest.fixture
def patient_user(admin_auth_headers):
    """
    Crea un usuario y su user_information para poder usarlo en Patient.
    Ajusta campos según tu /auth/register real.
    """
    uid = str(uuid4())

    payload = {
        "user": {
            "username": f"patient_{uid}",
            "email": f"patient_{uid}@example.com",
            "rol_user": "user",
            "password": "password123"
        },
        "user_information": {
            "first_name_user": "Test",
            "second_name_user": "Patient",
            "first_lastname_user": "User",
            "second_lastname_user": "Role",
            "birth_date_user": "1990-01-01",
            "gender_user": "Male",
            "phone_number_user": "000111",
            "document_number_user": f"DOC_PAT_{uid}",
            "id_user": uid
        }
    }

    r = client.post("/auth/register", json=payload)
    assert r.status_code in (200, 201)
    data = r.json()

    return {
        "id_user_information": data["user_information"]["id_user_information"]
    }


@pytest.fixture
def basic_patient_and_appointment(patient_user, admin_auth_headers):
    """
    Crea:
    - un Patient (usa PatientCreate)
    - una Medical_Appointment (usa MedicalAppointmentCreate)

    Devuelve id_patient e id_medical_appointment.
    """

    # 1. Crear paciente con el SCHEMA REAL:
    patient_payload = {
        "blood_type": "O+",
        "id_user_information": patient_user["id_user_information"],
    }

    rp = client.post("/patient/", json=patient_payload, headers=admin_auth_headers)
    print("RESP PATIENT:", rp.status_code, rp.text)
    assert rp.status_code in (200, 201)
    patient = rp.json()
    id_patient = patient["id_patient"]

    # 2. Crear cita médica con el SCHEMA REAL:
    from uuid import uuid4
    appointment_payload = {
        "appointment_date": "2025-11-29",
        "appointment_hour": "00:49:07.051Z",
        "location": "Consultorio 101",
        # por ahora usamos UUIDs random; si tu DB tiene FK estrictas,
        # luego tendremos que crear realmente medic/nurse/diagnosis.
        "id_medic": str(uuid4()),
        "id_nurse": str(uuid4()),
        "id_patient": id_patient,
        "id_diagnosis": str(uuid4()),
    }

    ra = client.post(
        "/medical_appointment/",
        json=appointment_payload,
        headers=admin_auth_headers,
    )
    print("RESP APPOINTMENT:", ra.status_code, ra.text)
    assert ra.status_code in (200, 201)
    appointment = ra.json()

    return {
        "id_patient": id_patient,
        "id_medical_appointment": appointment["id_medical_appointment"],
    }

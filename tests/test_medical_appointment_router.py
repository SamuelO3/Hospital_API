# import pytest
# from fastapi.testclient import TestClient
# from uuid import uuid4
# from main import app


# # ================================================================
# # CLIENT
# # ================================================================
# @pytest.fixture
# def client():
#     return TestClient(app)


# # ================================================================
# # ADMIN USER + TOKEN
# # ================================================================
# @pytest.fixture
# def test_admin_user():
#     uid = str(uuid4())

#     payload = {
#         "user": {
#             "username": "admin_user",
#             "email": f"admin_{uid}@example.com",
#             "rol_user": "admin",
#             "password": "adminpassword123"
#         },
#         "user_information": {
#             "first_name_user": "Admin",
#             "second_name_user": "Sys",
#             "first_lastname_user": "Root",
#             "second_lastname_user": "User",
#             "birth_date_user": "1999-01-01",
#             "gender_user": "Other",
#             "phone_number_user": "00012345",
#             "document_number_user": f"ADMIN_DOC_{uid}",
#             "id_user": uid
#         }
#     }

#     return {
#         "payload": payload,
#         "email": payload["user"]["email"],
#         "password": payload["user"]["password"],
#         "username": payload["user"]["username"]
#     }


# @pytest.fixture
# def admin_auth_headers(client, test_admin_user):

#     # Registrar admin
#     r = client.post("/auth/register", json=test_admin_user["payload"])
#     assert r.status_code == 201

#     # Login
#     login = {
#         "email": test_admin_user["email"],
#         "password": test_admin_user["password"]
#     }

#     r = client.post("/auth/login", json=login)
#     assert r.status_code == 200

#     token = r.json()["access_token"]

#     return {"Authorization": f"Bearer {token}"}


# # ================================================================
# # GENERIC USER CREATION (REUSABLE)
# # ================================================================
# def register_user(client, role):
#     uid = str(uuid4())

#     payload = {
#         "user": {
#             "username": f"{role}_{uid}",
#             "email": f"{role}_{uid}@example.com",
#             "rol_user": role,
#             "password": "password123"
#         },
#         "user_information": {
#             "first_name_user": f"{role.capitalize()}Name",
#             "second_name_user": "Test",
#             "first_lastname_user": "Lastname",
#             "second_lastname_user": "Role",
#             "birth_date_user": "1990-05-10",
#             "gender_user": "Other",
#             "phone_number_user": "999000",
#             "document_number_user": f"DOC_{role}_{uid}",
#             "id_user": uid
#         }
#     }

#     r = client.post("/auth/register", json=payload)
#     assert r.status_code == 201

#     data = r.json()

#     return {
#         "id_user": data["user"]["id_user"],
#         "id_user_information": data["user_information"]["id_user_information"],
#         "email": data["user"]["email"],
#         "password": "password123"
#     }


# # ================================================================
# # FIXTURES: MEDIC, NURSE, PATIENT, DIAGNOSIS
# # ================================================================
# @pytest.fixture
# def test_create_medic(client, admin_auth_headers):
#     user = register_user(client, "medic")

#     payload = {
#         "specialty": "Cardiology",
#         "id_user_information": user["id_user_information"]
#     }

#     r = client.post("/medics/", json=payload, headers=admin_auth_headers)
#     assert r.status_code == 201

#     return r.json()


# @pytest.fixture
# def test_create_nurse(client, admin_auth_headers):
#     user = register_user(client, "nurse")

#     payload = {
#         "speciality": "Emergency",
#         "id_user_information": user["id_user_information"]
#     }

#     r = client.post("/nurses/", json=payload, headers=admin_auth_headers)
#     assert r.status_code == 201

#     return r.json()


# @pytest.fixture
# def test_create_patient(client, admin_auth_headers):
#     user = register_user(client, "patient")

#     payload = {
#         "blood_type": "A+",
#         "id_user_information": user["id_user_information"]
#     }

#     r = client.post("/patients/", json=payload, headers=admin_auth_headers)
#     assert r.status_code == 201

#     return r.json()


# @pytest.fixture
# def test_create_diagnosis(client, admin_auth_headers):
#     payload = {
#         "name_diagnosis": "Hypertension",
#         "description_diagnosis": "Blood pressure condition"
#     }

#     r = client.post("/diagnosis/", json=payload, headers=admin_auth_headers)
#     assert r.status_code == 201

#     return r.json()


# # ================================================================
# # MEDICAL APPOINTMENT FIXTURE
# # ================================================================
# @pytest.fixture
# def test_create_medical_appointment(
#     client,
#     test_create_medic,
#     test_create_nurse,
#     test_create_patient,
#     test_create_diagnosis,
#     admin_auth_headers
# ):

#     payload = {
#         "appointment_date": "2025-11-29",
#         "appointment_hour": "09:30:00",
#         "location": "Consultorio 203",
#         "id_medic": test_create_medic["id_medic"],
#         "id_nurse": test_create_nurse["id_nurse"],
#         "id_patient": test_create_patient["id_patient"],
#         "id_diagnosis": test_create_diagnosis["id_diagnosis"]
#     }

#     r = client.post("/medical_appointment/", json=payload, headers=admin_auth_headers)
#     assert r.status_code == 201

#     return r.json()

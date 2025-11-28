# import pytest
# from fastapi import status
# from uuid import uuid4
# from datetime import date

# # Import the auth_headers fixture from test_auth_router
# from test_auth_router import auth_headers

# # Datos de prueba para médicos
# @pytest.fixture
# def test_medic_data():
#     return {
#         "specialty": "Cardiología",
#         "license_number": "MED12345",
#         "user_id": str(uuid4())  # ID de usuario existente
#     }

# # Fixture para crear un médico de prueba
# @pytest.fixture
# def create_test_medic(client, test_medic_data, admin_auth_headers):
#     response = client.post("/medics/", json=test_medic_data, headers=admin_auth_headers)
#     assert response.status_code == status.HTTP_201_CREATED
#     return response.json()

# # Test para crear un médico
# def test_create_medic(client, test_medic_data, admin_auth_headers, test_user, test_user_info):
#     """Test para crear un nuevo médico (requiere rol de administrador)"""
#     # Intentar crear médico sin autenticación
#     response = client.post("/medics/", json=test_medic_data)
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
#     # Crear un usuario normal (no administrador)
#     regular_user = test_user.copy()
#     regular_user.update(test_user_info)
#     response = client.post("/auth/register", json=regular_user)
#     assert response.status_code == status.HTTP_201_CREATED
    
#     # Iniciar sesión como usuario normal
#     login_data = {
#         "username": test_user["email"],
#         "password": test_user["password"]
#     }
#     response = client.post("/auth/login", data=login_data)
#     assert response.status_code == status.HTTP_200_OK
#     regular_token = response.json()["access_token"]
#     regular_headers = {"Authorization": f"Bearer {regular_token}"}
    
#     # Intentar crear médico como usuario normal (debería fallar)
#     response = client.post("/medics/", json=test_medic_data, headers=regular_headers)
#     assert response.status_code == status.HTTP_403_FORBIDDEN
    
#     # Crear el médico con el token de administrador
#     response = client.post("/medics/", json=test_medic_data, headers=admin_auth_headers)
    
#     # Verificar la respuesta
#     assert response.status_code == status.HTTP_201_CREATED
#     data = response.json()
#     assert "id" in data
#     assert data["specialty"] == test_medic_data["specialty"]
#     assert data["license_number"] == test_medic_data["license_number"]

# # Test para obtener un médico por ID
# def test_get_medic_by_id(client, create_test_medic, admin_auth_headers):
#     """Test para obtener un médico por su ID"""
#     # Obtener el ID del médico creado por el fixture
#     medic_id = create_test_medic["id"]
    
#     # Obtener el médico por ID
#     response = client.get(f"/medics/{medic_id}", headers=admin_auth_headers)
    
#     # Verificar la respuesta
#     assert response.status_code == status.HTTP_200_OK
#     data = response.json()
#     assert data["id"] == medic_id
#     assert data["specialty"] == create_test_medic["specialty"]

# # Test para obtener todos los médicos
# def test_get_medics(client, create_test_medic, admin_auth_headers):
#     """Test para obtener todos los médicos"""
#     # Obtener todos los médicos
#     response = client.get("/medics/", headers=admin_auth_headers)
    
#     # Verificar la respuesta
#     assert response.status_code == status.HTTP_200_OK
#     medics = response.json()
#     assert isinstance(medics, list)
#     assert len(medics) > 0
#     assert any(medic["id"] == create_test_medic["id"] for medic in medics)

# # Test para actualizar un médico
# def test_update_medic(client, create_test_medic, admin_auth_headers):
#     """Test para actualizar un médico existente"""
#     medic_id = create_test_medic["id"]
    
#     # Datos actualizados
#     updated_data = {
#         "specialty": "Neurología",
#         "license_number": "UPDATED123",
#         "user_id": create_test_medic["user_id"]  # Incluir el user_id requerido
#     }
    
#     # Actualizar el médico
#     response = client.put(f"/medics/{medic_id}", json=updated_data, headers=admin_auth_headers)
    
#     # Verificar la respuesta
#     assert response.status_code == status.HTTP_200_OK
#     data = response.json()
#     assert data["specialty"] == "Neurología"
#     assert data["license_number"] == "UPDATED123"

# # Test para eliminar un médico
# def test_delete_medic(client, create_test_medic, admin_auth_headers):
#     """Test para eliminar un médico"""
#     medic_id = create_test_medic["id"]
    
#     # Eliminar el médico
#     response = client.delete(f"/medics/{medic_id}", headers=admin_auth_headers)
    
#     # Verificar que se eliminó correctamente
#     assert response.status_code == status.HTTP_200_OK
    
#     # Verificar que ya no existe
#     response = client.get(f"/medics/{medic_id}", headers=admin_auth_headers)
#     assert response.status_code == status.HTTP_404_NOT_FOUND

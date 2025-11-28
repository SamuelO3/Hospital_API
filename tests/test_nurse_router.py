# import pytest
# from fastapi import status
# from uuid import uuid4

# # Datos de prueba para enfermeros/as
# @pytest.fixture
# def test_nurse_data():
#     return {
#         "license_number": "ENF54321",
#         "specialty": "Enfermería General",
#         "user_id": str(uuid4())  # ID de usuario existente
#     }

# # Test para obtener todos los enfermeros/as
# def test_get_nurses(client):
#     """Test para obtener la lista de enfermeros/as"""
#     # No se requiere autenticación para este endpoint según el router
#     response = client.get("/nurse/")
    
#     # Verificar la respuesta
#     assert response.status_code == status.HTTP_200_OK
#     assert isinstance(response.json(), list)

# # Test para crear un nuevo enfermero/a
# def test_create_nurse(client, test_nurse_data):
#     """Test para crear un nuevo registro de enfermero/a"""
#     # Obtener token de administrador
#     login_data = {"username": "admin@example.com", "password": "adminpassword123"}
#     login_response = client.post("/auth/login", data=login_data)
#     token = login_response.json()["access_token"]
#     headers = {"Authorization": f"Bearer {token}"}
    
#     # Crear el enfermero/a
#     response = client.post("/nurse/", json=test_nurse_data, headers=headers)
    
#     # Verificar la respuesta
#     assert response.status_code == status.HTTP_201_CREATED
#     data = response.json()
#     assert "id" in data
#     assert data["license_number"] == test_nurse_data["license_number"]
#     assert data["specialty"] == test_nurse_data["specialty"]

# # Test para obtener un enfermero/a por ID
# def test_get_nurse_by_id(client, test_nurse_data):
#     """Test para obtener un enfermero/a por su ID"""
#     # Obtener token de administrador
#     login_data = {"username": "admin@example.com", "password": "adminpassword123"}
#     login_response = client.post("/auth/login", data=login_data)
#     token = login_response.json()["access_token"]
#     headers = {"Authorization": f"Bearer {token}"}
    
#     # Crear un enfermero/a primero
#     create_response = client.post("/nurse/", json=test_nurse_data, headers=headers)
#     nurse_id = create_response.json()["id"]
    
#     # Obtener el enfermero/a por ID
#     response = client.get(f"/nurse/byid/{nurse_id}", headers=headers)
    
#     # Verificar la respuesta
#     assert response.status_code == status.HTTP_200_OK
#     data = response.json()
#     assert data["id"] == nurse_id
#     assert data["license_number"] == test_nurse_data["license_number"]

# # Test para actualizar un enfermero/a
# def test_update_nurse(client, test_nurse_data):
#     """Test para actualizar la información de un enfermero/a"""
#     # Obtener token de administrador
#     login_data = {"username": "admin@example.com", "password": "adminpassword123"}
#     login_response = client.post("/auth/login", data=login_data)
#     token = login_response.json()["access_token"]
#     headers = {"Authorization": f"Bearer {token}"}
    
#     # Crear un enfermero/a primero
#     create_response = client.post("/nurse/", json=test_nurse_data, headers=headers)
#     nurse_id = create_response.json()["id"]
    
#     # Datos de actualización
#     update_data = {"specialty": "Enfermería Pediátrica"}
    
#     # Actualizar el enfermero/a
#     response = client.put(f"/nurse/update/{nurse_id}", json=update_data, headers=headers)
    
#     # Verificar la respuesta
#     assert response.status_code == status.HTTP_200_OK
#     data = response.json()
#     assert data["specialty"] == update_data["specialty"]
#     assert data["license_number"] == test_nurse_data["license_number"]  # No debería cambiar

# # Test para eliminar un enfermero/a
# def test_delete_nurse(client, test_nurse_data):
#     """Test para eliminar un enfermero/a"""
#     # Obtener token de administrador
#     login_data = {"username": "admin@example.com", "password": "adminpassword123"}
#     login_response = client.post("/auth/login", data=login_data)
#     token = login_response.json()["access_token"]
#     headers = {"Authorization": f"Bearer {token}"}
    
#     # Crear un enfermero/a primero
#     create_response = client.post("/nurse/", json=test_nurse_data, headers=headers)
#     nurse_id = create_response.json()["id"]
    
#     # Eliminar el enfermero/a
#     response = client.delete(f"/nurse/delete/{nurse_id}", headers=headers)
    
#     # Verificar la respuesta
#     assert response.status_code == status.HTTP_200_OK
    
#     # Verificar que el enfermero/a ya no existe
#     get_response = client.get(f"/nurse/byid/{nurse_id}", headers=headers)
#     assert get_response.status_code == status.HTTP_404_NOT_FOUND

# # Test para verificar los permisos de acceso
# def test_nurse_permissions(client, test_nurse_data):
#     """Test para verificar los permisos de acceso a los endpoints de enfermeros/as"""
#     # Intentar crear un enfermero sin autenticación
#     response = client.post("/nurse/", json=test_nurse_data)
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
#     # Crear un usuario no administrador
#     user_data = {
#         "user": {
#             "email": "user@example.com",
#             "password": "userpassword123",
#             "role": "user"
#         },
#         "user_information": {
#             "first_name": "Regular",
#             "last_name": "User",
#             "phone_number": "+1234567890",
#             "address": "456 User St"
#         }
#     }
#     client.post("/auth/register", json=user_data)
    
#     # Iniciar sesión como usuario regular
#     login_data = {"username": "user@example.com", "password": "userpassword123"}
#     login_response = client.post("/auth/login", data=login_data)
#     token = login_response.json()["access_token"]
#     headers = {"Authorization": f"Bearer {token}"}
    
#     # Intentar crear un enfermero como usuario regular
#     response = client.post("/nurse/", json=test_nurse_data, headers=headers)
#     assert response.status_code == status.HTTP_403_FORBIDDEN

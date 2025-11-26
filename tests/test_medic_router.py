import pytest
from fastapi import status
from uuid import uuid4
from datetime import date

# Datos de prueba para médicos
@pytest.fixture
def test_medic_data():
    return {
        "specialty": "Cardiología",
        "license_number": "MED12345",
        "user_id": str(uuid4())  # ID de usuario existente
    }

# Test para crear un médico
def test_create_medic(client, test_medic_data):
    """Test para crear un nuevo médico"""
    # Necesitamos un token de administrador para esta prueba
    # Primero, crear un usuario administrador y obtener su token
    admin_user = {
        "email": "admin@example.com",
        "password": "adminpassword123",
        "role": "admin"
    }
    admin_info = {
        "first_name": "Admin",
        "last_name": "User",
        "phone_number": "+1234567890",
        "address": "123 Admin St"
    }
    
    # Registrar el usuario administrador
    client.post("/auth/register", json={"user": admin_user, "user_information": admin_info})
    
    # Iniciar sesión para obtener el token
    login_data = {
        "username": admin_user["email"],
        "password": admin_user["password"]
    }
    login_response = client.post("/auth/login", data=login_data)
    token = login_response.json()["access_token"]
    
    # Crear el médico con el token de autenticación
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/medics/", json=test_medic_data, headers=headers)
    
    # Verificar la respuesta
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "id" in data
    assert data["specialty"] == test_medic_data["specialty"]
    assert data["license_number"] == test_medic_data["license_number"]

# Test para obtener un médico por ID
def test_get_medic_by_id(client, test_medic_data):
    """Test para obtener un médico por su ID"""
    # Primero necesitamos crear un médico para obtenerlo
    # (asumiendo que ya tenemos un admin logueado de la prueba anterior)
    login_data = {"username": "admin@example.com", "password": "adminpassword123"}
    login_response = client.post("/auth/login", data=login_data)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Crear el médico
    create_response = client.post("/medics/", json=test_medic_data, headers=headers)
    medic_id = create_response.json()["id"]
    
    # Obtener el médico por ID
    response = client.get(f"/medics/{medic_id}", headers=headers)
    
    # Verificar la respuesta
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == medic_id
    assert data["specialty"] == test_medic_data["specialty"]

# Test para obtener todos los médicos
def test_get_medics(client):
    """Test para obtener todos los médicos"""
    # Obtener token de administrador
    login_data = {"username": "admin@example.com", "password": "adminpassword123"}
    login_response = client.post("/auth/login", data=login_data)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Obtener todos los médicos
    response = client.get("/medics/", headers=headers)
    
    # Verificar la respuesta
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

# Test para actualizar un médico
def test_update_medic(client, test_medic_data):
    """Test para actualizar un médico existente"""
    # Obtener token de administrador
    login_data = {"username": "admin@example.com", "password": "adminpassword123"}
    login_response = client.post("/auth/login", data=login_data)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Crear un médico para actualizar
    create_response = client.post("/medics/", json=test_medic_data, headers=headers)
    medic_id = create_response.json()["id"]
    
    # Datos de actualización
    update_data = {"specialty": "Neurología"}
    
    # Actualizar el médico
    response = client.put(f"/medics/{medic_id}", json=update_data, headers=headers)
    
    # Verificar la respuesta
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["specialty"] == update_data["specialty"]
    assert data["license_number"] == test_medic_data["license_number"]  # No debería cambiar

# Test para eliminar un médico
def test_delete_medic(client, test_medic_data):
    """Test para eliminar un médico"""
    # Obtener token de administrador
    login_data = {"username": "admin@example.com", "password": "adminpassword123"}
    login_response = client.post("/auth/login", data=login_data)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Crear un médico para eliminar
    create_response = client.post("/medics/", json=test_medic_data, headers=headers)
    medic_id = create_response.json()["id"]
    
    # Eliminar el médico
    response = client.delete(f"/medics/{medic_id}", headers=headers)
    
    # Verificar la respuesta
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Medic deleted successfully"}
    
    # Verificar que el médico ya no existe
    get_response = client.get(f"/medics/{medic_id}", headers=headers)
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

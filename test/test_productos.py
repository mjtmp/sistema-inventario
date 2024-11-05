import pytest
from httpx import Client
from backend.main import app

# Fixture para crear un producto
@pytest.fixture
def create_producto():
    with Client(app=app, base_url="http://test") as client:
        data = {
            "nombre": "Producto inicial",
            "descripcion": "Descripción inicial",
            "precio": 100.0,
            "proveedor_id": 1  # Asegúrate de que este ID es válido
        }
        response = client.post("/productos/", json=data)
        assert response.status_code == 201
        return response.json()

def test_create_producto(create_producto):
    with Client(app=app, base_url="http://test") as client:
        data = {
            "nombre": "Producto de prueba",
            "descripcion": "Descripción de prueba",
            "precio": 100.0,
            "proveedor_id": create_producto["proveedor_id"]
        }
        response = client.post("/productos/", json=data)
    assert response.status_code == 201
    assert response.json()["nombre"] == "Producto de prueba"

def test_update_producto(create_producto):
    with Client(app=app, base_url="http://test") as client:
        data = {
            "nombre": "Producto actualizado",
            "descripcion": "Descripción actualizada",
            "precio": 150.0,
            "proveedor_id": create_producto["proveedor_id"]
        }
        response = client.put(f"/productos/{create_producto['id']}", json=data)
    assert response.status_code == 200
    assert response.json()["nombre"] == "Producto actualizado"

def test_delete_producto(create_producto):
    with Client(app=app, base_url="http://test") as client:
        response = client.delete(f"/productos/{create_producto['id']}")
    assert response.status_code == 200


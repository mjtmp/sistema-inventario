# tests/test_main.py
from httpx import AsyncClient
import pytest
from backend.main import app  # Ruta de importación

@pytest.mark.asyncio
async def test_example():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/example")
    assert response.status_code == 200
    assert response.json() == {"message": "This is an example"}




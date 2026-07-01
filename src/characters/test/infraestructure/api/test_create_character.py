from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_character_and_returns_200():
    response = client.post(
        "/characters/",
        json={
            "name": "Tanjiro Kamado",
            "state": "alive",
            "img": "https://example.com/tanjiro.jpg"
        }
    )
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["name"] == "Tanjiro Kamado"
    assert response.json()["state"] == "alive"
    assert response.json()["img"] == "https://example.com/tanjiro.jpg"
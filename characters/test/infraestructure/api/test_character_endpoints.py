from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_all_characters_returns_list():
    response = client.get("/characters/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_character_by_id_returns_200():
    # Primero creamos uno
    create = client.post(
        "/characters/",
        json={
            "name": "Tanjiro Kamado",
            "state": "alive",
            "img": "https://example.com/tanjiro.jpg",
        },
    )
    character_id = create.json()["id"]

    # Lo recuperamos por id
    response = client.get(f"/characters/{character_id}")
    assert response.status_code == 200
    assert response.json()["id"] == character_id
    assert response.json()["name"] == "Tanjiro Kamado"


def test_get_character_by_id_not_found():
    response = client.get("/characters/999999")
    assert response.status_code == 404


def test_update_character_returns_200():
    create = client.post(
        "/characters/",
        json={
            "name": "Tanjiro Kamado",
            "state": "alive",
            "img": "https://example.com/tanjiro.jpg",
        },
    )
    character_id = create.json()["id"]

    response = client.put(
        f"/characters/{character_id}",
        json={
            "name": "Tanjiro Kamado",
            "state": "dead",
            "img": "https://example.com/tanjiro-v2.jpg",
        },
    )
    assert response.status_code == 200
    assert response.json()["state"] == "dead"
    assert response.json()["img"] == "https://example.com/tanjiro-v2.jpg"


def test_update_character_not_found():
    response = client.put(
        "/characters/999999",
        json={
            "name": "Tanjiro Kamado",
            "state": "alive",
            "img": "https://example.com/tanjiro.jpg",
        },
    )
    assert response.status_code == 404


def test_delete_character_returns_200():
    create = client.post(
        "/characters/",
        json={
            "name": "Tanjiro Kamado",
            "state": "alive",
            "img": "https://example.com/tanjiro.jpg",
        },
    )
    character_id = create.json()["id"]

    response = client.delete(f"/characters/{character_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Character deleted successfully"


def test_delete_character_not_found():
    response = client.delete("/characters/999999")
    assert response.status_code == 404
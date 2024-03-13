from fastapi.testclient import TestClient
from main import app
import pytest

@pytest.fixture
def client():
    return TestClient(app)

def test_create_meal(client):
    response = client.post("/meals", params={"text": "Chicken Salad", "cal_value": 500.0})
    assert response.status_code == 200
    assert "meal_id" in response.json()

def test_update_meal(client):
    meal_id = create_meal(client, "Pasta", 700.0)
    response = client.put(f"/meals/{meal_id}", params={"text": "Spaghetti", "cal_value": 800.0})
    assert response.status_code == 200

def test_delete_meal(client):
    meal_id = create_meal(client, "Pizza", 1000.0)
    response = client.delete(f"/meals/{meal_id}")
    assert response.status_code == 200

def test_get_meal(client):
    meal_id = create_meal(client, "Burger", 800.0)
    response = client.get(f"/meals/{meal_id}")
    assert response.status_code == 200

def test_get_all_meals(client):
    create_meal(client, "Salmon", 600.0)
    create_meal(client, "Steak", 900.0)

    response = client.get("/meals")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def create_meal(client, text, cal_value):
    response = client.post("/meals", params={"text": text, "cal_value": cal_value})
    assert response.status_code == 200
    return response.json().get("meal_id")

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_create_order():
    response = client.post(
        "/orders/",
        json={"customer_name": "Test Customer", "total_amount": 100.0}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["customer_name"] == "Test Customer"
    assert data["total_amount"] == 100.0
    assert data["status"] == "PENDING"

def test_get_orders():
    response = client.get("/orders/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

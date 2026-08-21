import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_add_to_cart_invalid_quantity():
    response = client.post("/cart", params={"product_id": 1, "quantity": 0})
    assert response.status_code == 400
    assert "Quantity must be greater than 0" in response.json()["detail"]


def test_order_exceeds_inventory_stock():
    client.post("/cart", params={"product_id": 1, "quantity": 999})
    response = client.post("/orders")
    assert response.status_code == 400
    assert "Not enough stock" in response.json()["detail"]
def create_category(client, admin_token):
    response = client.post(
        "/categories/",
        json={"name": "Electronics", "description": "Gadgets"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    return response.json()["id"]

def create_product(client, admin_token, category_id, stock=10):
    response = client.post(
        "/products/",
        json={"name": "Laptop", "price": 999.99, "stock": stock, "category_id": category_id},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    return response.json()["id"]

def get_user_token(client, username="shopper"):
    client.post("/auth/register", json={
        "username": username,
        "email": f"{username}@test.com",
        "password": "test1234"
    })
    login_response = client.post("/auth/login", data={
        "username": username,
        "password": "test1234"
    })
    return login_response.json()["access_token"]

def test_add_to_cart_invalid_quantity(client, admin_token):
    category_id = create_category(client, admin_token)
    product_id = create_product(client, admin_token, category_id)
    user_token = get_user_token(client)

    response = client.post(
        "/cart",
        params={"product_id": product_id, "quantity": 0},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 400
    assert "Quantity must be greater than 0" in response.json()["detail"]

def test_order_exceeds_inventory_stock(client, admin_token):
    category_id = create_category(client, admin_token)
    product_id = create_product(client, admin_token, category_id, stock=5)
    user_token = get_user_token(client)

    client.post(
        "/cart",
        params={"product_id": product_id, "quantity": 999},
        headers={"Authorization": f"Bearer {user_token}"}
    )

    response = client.post(
        "/orders",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 400
    assert "Not enough stock" in response.json()["detail"]

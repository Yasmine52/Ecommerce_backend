def create_category(client, admin_token):
    response = client.post(
        "/categories/",
        json={"name": "Electronics", "description": "Gadgets"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    return response.json()["id"]

def test_create_product_success(client, admin_token):
    category_id = create_category(client, admin_token)

    response = client.post(
        "/products/",
        json={
            "name": "Laptop",
            "description": "A powerful laptop",
            "price": 999.99,
            "stock": 10,
            "category_id": category_id
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Laptop"
    assert data["category_id"] == category_id

def test_create_product_invalid_category(client, admin_token):
    response = client.post(
        "/products/",
        json={
            "name": "Laptop",
            "description": "A powerful laptop",
            "price": 999.99,
            "stock": 10,
            "category_id": 999
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 404

def test_create_product_as_customer_forbidden(client, admin_token):
    category_id = create_category(client, admin_token)

    client.post("/auth/register", json={
        "username": "henry",
        "email": "henry@test.com",
        "password": "test1234"
    })
    login_response = client.post("/auth/login", data={
        "username": "henry",
        "password": "test1234"
    })
    token = login_response.json()["access_token"]

    response = client.post(
        "/products/",
        json={
            "name": "Laptop",
            "price": 999.99,
            "stock": 10,
            "category_id": category_id
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403

def test_get_products_list(client, admin_token):
    category_id = create_category(client, admin_token)
    client.post(
        "/products/",
        json={"name": "Laptop", "price": 999.99, "stock": 10, "category_id": category_id},
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Laptop"

def test_get_single_product(client, admin_token):
    category_id = create_category(client, admin_token)
    create_response = client.post(
        "/products/",
        json={"name": "Laptop", "price": 999.99, "stock": 10, "category_id": category_id},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    product_id = create_response.json()["id"]

    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Laptop"

def test_get_product_not_found(client):
    response = client.get("/products/999")
    assert response.status_code == 404

def test_update_product(client, admin_token):
    category_id = create_category(client, admin_token)
    create_response = client.post(
        "/products/",
        json={"name": "Laptop", "price": 999.99, "stock": 10, "category_id": category_id},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    product_id = create_response.json()["id"]

    response = client.put(
        f"/products/{product_id}",
        json={"price": 899.99},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["price"] == 899.99

def test_delete_product(client, admin_token):
    category_id = create_category(client, admin_token)
    create_response = client.post(
        "/products/",
        json={"name": "Laptop", "price": 999.99, "stock": 10, "category_id": category_id},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    product_id = create_response.json()["id"]

    response = client.delete(
        f"/products/{product_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 204

    get_response = client.get(f"/products/{product_id}")
    assert get_response.status_code == 404

def test_products_search_filter(client, admin_token):
    category_id = create_category(client, admin_token)
    client.post(
        "/products/",
        json={"name": "Gaming Laptop", "price": 1200, "stock": 5, "category_id": category_id},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    client.post(
        "/products/",
        json={"name": "Office Chair", "price": 150, "stock": 20, "category_id": category_id},
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    response = client.get("/products/?search=laptop")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Gaming Laptop"

def test_products_price_filter(client, admin_token):
    category_id = create_category(client, admin_token)
    client.post(
        "/products/",
        json={"name": "Cheap Item", "price": 10, "stock": 5, "category_id": category_id},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    client.post(
        "/products/",
        json={"name": "Expensive Item", "price": 500, "stock": 5, "category_id": category_id},
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    response = client.get("/products/?min_price=100&max_price=1000")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Expensive Item"

def test_products_pagination(client, admin_token):
    category_id = create_category(client, admin_token)
    for i in range(5):
        client.post(
            "/products/",
            json={"name": f"Product {i}", "price": 10, "stock": 5, "category_id": category_id},
            headers={"Authorization": f"Bearer {admin_token}"}
        )

    response = client.get("/products/?skip=0&limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2

    response2 = client.get("/products/?skip=2&limit=2")
    assert response2.status_code == 200
    assert len(response2.json()) == 2

def test_get_products_populates_cache(client, admin_token):
    from core.cache import redis_client
    category_id = create_category(client, admin_token)
    client.post(
        "/products/",
        json={"name": "Laptop", "price": 999.99, "stock": 10, "category_id": category_id},
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    keys_before = redis_client.keys("products:*")
    assert keys_before == []

    response = client.get("/products/")
    assert response.status_code == 200

    keys_after = redis_client.keys("products:*")
    assert len(keys_after) == 1

def test_create_product_invalidates_cache(client, admin_token):
    from core.cache import redis_client
    category_id = create_category(client, admin_token)
    client.post(
        "/products/",
        json={"name": "Laptop", "price": 999.99, "stock": 10, "category_id": category_id},
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    client.get("/products/")
    assert len(redis_client.keys("products:*")) == 1

    client.post(
        "/products/",
        json={"name": "Mouse", "price": 19.99, "stock": 50, "category_id": category_id},
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert redis_client.keys("products:*") == []

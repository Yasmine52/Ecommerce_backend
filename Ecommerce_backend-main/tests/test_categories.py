def test_create_category_success(client, admin_token):
    response = client.post(
        "/categories/",
        json={"name": "Electronics", "description": "Gadgets and devices"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Electronics"
    assert "id" in data

def test_get_categories_list(client, admin_token):
    client.post(
        "/categories/",
        json={"name": "Electronics", "description": "Gadgets"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    response = client.get("/categories/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Electronics"

def test_create_category_as_customer_forbidden(client):
    client.post("/auth/register", json={
        "username": "frank",
        "email": "frank@test.com",
        "password": "test1234"
    })
    login_response = client.post("/auth/login", data={
        "username": "frank",
        "password": "test1234"
    })
    token = login_response.json()["access_token"]

    response = client.post(
        "/categories/",
        json={"name": "Electronics", "description": "Gadgets"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403

def test_get_single_category(client, admin_token):
    create_response = client.post(
        "/categories/",
        json={"name": "Electronics", "description": "Gadgets"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    category_id = create_response.json()["id"]

    response = client.get(f"/categories/{category_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Electronics"

def test_get_category_not_found(client):
    response = client.get("/categories/999")
    assert response.status_code == 404

def test_update_category(client, admin_token):
    create_response = client.post(
        "/categories/",
        json={"name": "Electronics", "description": "Gadgets"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    category_id = create_response.json()["id"]

    response = client.put(
        f"/categories/{category_id}",
        json={"name": "Updated Electronics"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Electronics"

def test_delete_category_as_admin(client, admin_token):
    create_response = client.post(
        "/categories/",
        json={"name": "Electronics", "description": "Gadgets"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    category_id = create_response.json()["id"]

    response = client.delete(
        f"/categories/{category_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 204

    get_response = client.get(f"/categories/{category_id}")
    assert get_response.status_code == 404

def test_delete_category_as_customer_forbidden(client, admin_token):
    create_response = client.post(
        "/categories/",
        json={"name": "Electronics", "description": "Gadgets"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    category_id = create_response.json()["id"]

    client.post("/auth/register", json={
        "username": "grace",
        "email": "grace@test.com",
        "password": "test1234"
    })
    login_response = client.post("/auth/login", data={
        "username": "grace",
        "password": "test1234"
    })
    token = login_response.json()["access_token"]

    response = client.delete(
        f"/categories/{category_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403

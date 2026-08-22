def test_register_user_success(client):
    response = client.post("/auth/register", json={
        "username": "bob",
        "email": "bob@test.com",
        "password": "test1234"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "bob"
    assert data["email"] == "bob@test.com"
    assert data["role"] == "customer"

def test_register_duplicate_user(client):
    client.post("/auth/register", json={
        "username": "bob",
        "email": "bob@test.com",
        "password": "test1234"
    })
    response = client.post("/auth/register", json={
        "username": "bob",
        "email": "bob@test.com",
        "password": "test1234"
    })
    assert response.status_code == 400

def test_login_success(client):
    client.post("/auth/register", json={
        "username": "alice",
        "email": "alice@test.com",
        "password": "test1234"
    })
    response = client.post("/auth/login", data={
        "username": "alice",
        "password": "test1234"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client):
    client.post("/auth/register", json={
        "username": "charlie",
        "email": "charlie@test.com",
        "password": "correctpassword"
    })
    response = client.post("/auth/login", data={
        "username": "charlie",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_login_nonexistent_user(client):
    response = client.post("/auth/login", data={
        "username": "ghostuser",
        "password": "whatever123"
    })
    assert response.status_code == 401

def test_create_category_without_token(client):
    response = client.post("/categories/", json={
        "name": "Books",
        "description": "All books"
    })
    assert response.status_code == 401

def test_create_category_as_customer_forbidden(client):
    client.post("/auth/register", json={
        "username": "dave",
        "email": "dave@test.com",
        "password": "test1234"
    })
    login_response = client.post("/auth/login", data={
        "username": "dave",
        "password": "test1234"
    })
    token = login_response.json()["access_token"]

    response = client.post(
        "/categories/",
        json={"name": "Books", "description": "All books"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403

def test_create_category_as_admin_success(client, admin_token):
    response = client.post(
        "/categories/",
        json={"name": "Books", "description": "All books"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 201

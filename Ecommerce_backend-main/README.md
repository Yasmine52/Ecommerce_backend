# Ecommerce Backend (FastAPI)

A backend system for an e-commerce application built with **FastAPI**. The project provides authentication, role-based authorization, product and category management, cart and order functionality, inventory management, Redis caching, logging, monitoring, and automated API testing.

## Features

### Authentication & Authorization
- User registration and login
- JWT-based authentication
- Role-based access control
- Admin-protected endpoints

### Products & Categories
- Create, read, update, and delete products
- Category management
- Product search
- Category filtering
- Price filtering
- Pagination

### Cart & Orders
- Add and manage cart items
- Create orders
- Order item management
- Stock validation during ordering

### Inventory & Validation
- Inventory management
- Stock checking
- Quantity validation
- Business-rule validation
- Proper HTTP error responses

### Redis Caching
- Cache-Aside pattern for product listing
- Redis cache keys based on search and filter parameters
- 60-second cache expiration
- Cache invalidation after product creation, update, or deletion

### Logging & Monitoring
- Request logging using Loguru
- HTTP status and response-time logging
- Prometheus metrics
- Monitoring dashboard
- Redis and database health checks

### Automated Testing
- Pytest test suite
- FastAPI TestClient
- Authentication tests
- Product tests
- Category tests
- Inventory tests
- Cache-related tests

## Tech Stack

- **FastAPI** - Backend API framework
- **SQLAlchemy** - Database ORM
- **SQLite** - Database
- **JWT** - Authentication and authorization
- **Redis / Memurai** - Caching
- **Loguru** - Application logging
- **Prometheus** - API monitoring and metrics
- **Pytest** - Automated testing
- **Pydantic** - Data validation

## Project Structure

```text
Ecommerce_backend-main/
│
├── core/
│   ├── cache.py
│   ├── dependencies.py
│   └── security.py
│
├── models/
│   ├── user.py
│   ├── product.py
│   ├── category.py
│   ├── cart.py
│   ├── orders.py
│   └── order_items.py
│
├── routers/
│   ├── auth.py
│   ├── products.py
│   ├── categories.py
│   ├── cart.py
│   ├── orders.py
│   ├── orderitems.py
│   └── dashboard.py
│
├── schemas/
│
├── services/
│   └── inventory.py
│
├── tests/
│   ├── test_auth.py
│   ├── test_products.py
│   ├── test_categories.py
│   └── test_inventory.py
│
├── database.py
├── main.py
├── benchmark_cache.py
├── pytest.ini
├── requirements.txt
└── README.md
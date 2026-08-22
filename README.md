# Ecommerce Backend (FastAPI)

A backend system for an e-commerce application built with **FastAPI**, featuring authentication, product management, cart and orders flow, inventory control, and monitoring.

 # Features
1. Users + JWT + Roles Auth
   - User registration and login
   - Role-based access (User / Admin)
2. Products + Categories
   - Search, filter, and pagination
3. Cart + Orders + OrderItems
   - Complete order flow
4. Inventory + Validation
   - Stock management
   - Error handling and business logic
5. Redis + Logging + Monitoring
   - Performance optimization
   - API monitoring dashboard
   - Automated testing

# Tech Stack
- FastAPI (Backend framework)
- SQLAlchemy + SQLite (Database ORM)
- JWT (Authentication & Authorization)
- Redis (Caching & Session Management)
- Pytest (Testing)
# Project Structure
 main.py              # Entry point
 database.py          # Database configuration
 models/              # SQLAlchemy models
 routers/             # API routes (users, products, cart, orders, inventory)
 utils/               # Validation, business logic, helpers
 tests/               # Pytest test cases
 requirements.txt     # Dependencies

 # Some API Endpoints 
POST /users/login → Login

POST /products/ → Add product (Admin only)

GET /products/ → List products

POST /cart/ → Add to cart

POST /orders/ → Create order

GET /inventory/ → Check stock

# Testing
Run tests with:
Pytest

# Contributors
Yasmine, Muhamed, Basmala, Roaa, Menna
Team Members (Inventory, Products, Orders, Monitoring)

 Notes
Use an Admin JWT Token for product and inventory endpoints.

Redis and monitoring dashboard run on 127.0.0.1:8000/dashboard

from fastapi import FastAPI
from database import Base, engine
from models import cart, orders, order_items, user, product, category
from routers import products, categories

Base.metadata.create_all(bind=engine)

app = FastAPI()

from routers import cart as cart_router
from routers import orders as orders_router
from routers import orderitems as orderitems_router
from routers import auth as auth_router

app.include_router(cart_router.router)
app.include_router(orders_router.router)
app.include_router(orderitems_router.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(auth_router.router)
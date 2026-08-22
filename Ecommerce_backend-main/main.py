import time
from routers import dashboard as dashboard_router
from fastapi import FastAPI, Request
from loguru import logger
from prometheus_fastapi_instrumentator import Instrumentator

from database import Base, engine
from models import cart, orders, order_items, user, product, category
from routers import (
    cart as cart_router,
    orders as orders_router,
    orderitems as orderitems_router,
    categories,
    products,
    auth as auth_router,
)

logger.add("logs/app.log", rotation="10 MB", level="INFO")

Base.metadata.create_all(bind=engine)

app = FastAPI()

Instrumentator().instrument(app).expose(app)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = (time.time() - start_time) * 1000

    logger.info(
        f"{request.method} {request.url.path} | "
        f"Status: {response.status_code} | "
        f"Duration: {duration:.2f}ms"
    )
    return response

app.include_router(cart_router.router)
app.include_router(orders_router.router)
app.include_router(orderitems_router.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(auth_router.router)
app.include_router(dashboard_router.router)
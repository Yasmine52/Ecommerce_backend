from fastapi import HTTPException
from models.product import Product


def check_stock(product: Product, quantity: int):
    if quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than 0"
        )

    if product.stock < quantity:
        raise HTTPException(
            status_code=400,
            detail=f"Not enough stock for product '{product.name}'"
        )


def decrease_stock(product: Product, quantity: int):
    check_stock(product, quantity)
    product.stock -= quantity


def restore_stock(product: Product, quantity: int):
    product.stock += quantity
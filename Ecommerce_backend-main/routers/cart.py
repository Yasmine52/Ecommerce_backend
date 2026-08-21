from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.cart import Cart
from models.user import User
from models.product import Product
from core.dependencies import get_current_user

router = APIRouter()

@router.post("/cart")
def add_to_cart(
    product_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than 0"
        )

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    cart_item = Cart(
        user_id=current_user.id,
        product_id=product_id,
        quantity=quantity
    )

    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)

    return {
        "message": "Item added to cart",
        "cart_item": cart_item
    }
@router.get("/cart")
def get_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items = db.query(Cart).filter(Cart.user_id == current_user.id).all()
    return {"cart_items": items}

@router.delete("/cart/{item_id}")
def delete_cart_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = db.query(Cart).filter(Cart.id == item_id, Cart.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Item deleted successfully"}
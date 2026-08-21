from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.order_items import OrderItem

router = APIRouter()

@router.get("/orders/{order_id}/items")
def get_order_items(order_id: int, db: Session = Depends(get_db)):
    items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
    if not items:
        return {"message": "No items found for this order"}
    return {
        "order_items": [
            {"product_id": item.product_id, "quantity": item.quantity}
            for item in items
        ]
    }

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.orders import Order
from models.order_items import OrderItem
from models.cart import Cart
from models.user import User, UserRole
from core.dependencies import get_current_user, require_role
from datetime import datetime
from models.product import Product
from services.inventory import check_stock, decrease_stock, restore_stock

router = APIRouter()

@router.post("/orders")
def create_order(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cart_items = db.query(Cart).filter(Cart.user_id == current_user.id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    for item in cart_items:
        product = db.query(Product).filter(
            Product.id == item.product_id
        ).first()

        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product {item.product_id} not found"
            )

        check_stock(product, item.quantity)

    order = Order(user_id=current_user.id, status="pending", created_at=datetime.utcnow())
    
    db.add(order)
    db.flush()
    

    for item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(order_item)
        product = db.query(Product).filter(Product.id == item.product_id).first()
        decrease_stock(product, item.quantity)

    db.query(Cart).filter(Cart.user_id == current_user.id).delete()
    db.commit()
    db.refresh(order)

    return {"message": "Order created successfully", "order_id": order.id}


@router.get("/orders")
def get_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role == UserRole.admin:
        orders = db.query(Order).all()
    else:
        orders = db.query(Order).filter(Order.user_id == current_user.id).all()

    if not orders:
        return {"message": "No orders found"}
    return {"orders": orders}


@router.get("/orders/{order_id}")
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if current_user.role != UserRole.admin and order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this order")

    return {"order": order}


@router.put("/orders/{order_id}/status")
def update_order_status(
    order_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.admin)),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    valid_statuses = ["pending", "shipped", "delivered"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")

    order.status = status
    db.commit()
    db.refresh(order)
    return {"message": "Order status updated", "order_id": order.id, "new_status": order.status}


@router.delete("/orders/{order_id}")
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.admin)),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status != "pending":
        raise HTTPException(
            status_code=400,
            detail="Only pending orders can be cancelled"
        )
    for item in order.items:
        product = db.query(Product).filter(
            Product.id == item.product_id
        ).first()

        if product:
            restore_stock(product, item.quantity)
    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}
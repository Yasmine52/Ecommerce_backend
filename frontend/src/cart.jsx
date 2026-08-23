import { useState, useEffect } from "react";
import api from "./api";

function Cart() {
  const [cartItems, setCartItems] = useState([]);
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetchCart();
  }, []);

  const fetchCart = async () => {
    try {
      const response = await api.get("/cart");
      setCartItems(response.data.cart_items || []);
    } catch (err) {
      setMessage("Failed to load cart");
    }
  };

  const removeItem = async (itemId) => {
    try {
      await api.delete(`/cart/${itemId}`);
      fetchCart();
    } catch (err) {
      setMessage("Failed to remove item");
    }
  };

  const placeOrder = async () => {
    try {
      await api.post("/orders");
      setMessage("Order placed successfully!");
      setCartItems([]);
    } catch (err) {
      setMessage(err.response?.data?.detail || "Failed to place order");
    }
  };

  return (
    <div className="page-container">
      <h2 className="page-title">Your Cart</h2>
      {message && <p className="success-text">{message}</p>}

      {cartItems.length === 0 ? (
        <p className="empty-state">Your cart is empty.</p>
      ) : (
        <>
          {cartItems.map((item) => (
            <div key={item.id} className="cart-item">
              <span className="cart-item-info">
                Product #{item.product_id} — Qty: {item.quantity}
              </span>
              <button onClick={() => removeItem(item.id)} className="remove-btn">
                Remove
              </button>
            </div>
          ))}
          <button onClick={placeOrder} className="btn" style={{ marginTop: "16px" }}>
            Place Order
          </button>
        </>
      )}
    </div>
  );
}

export default Cart;

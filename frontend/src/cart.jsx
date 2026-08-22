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
    <div style={{ maxWidth: "600px", margin: "40px auto", fontFamily: "sans-serif" }}>
      <h2>Your Cart</h2>
      {message && <p style={{ color: message.includes("success") ? "green" : "red" }}>{message}</p>}

      {cartItems.length === 0 ? (
        <p>Your cart is empty.</p>
      ) : (
        <>
          <ul style={{ listStyle: "none", padding: 0 }}>
            {cartItems.map((item) => (
              <li
                key={item.id}
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  borderBottom: "1px solid #eee",
                  padding: "10px 0",
                }}
              >
                <span>Product #{item.product_id} — Qty: {item.quantity}</span>
                <button onClick={() => removeItem(item.id)}>Remove</button>
              </li>
            ))}
          </ul>
          <button onClick={placeOrder} style={{ marginTop: "16px", padding: "10px 20px" }}>
            Place Order
          </button>
        </>
      )}
    </div>
  );
}

export default Cart;
import { useState, useEffect } from "react";
import api from "./api";

function Products() {
  const [products, setProducts] = useState([]);
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await api.get("/products/");
      setProducts(response.data);
    } catch (err) {
      setMessage("Failed to load products");
    }
  };

  const addToCart = async (productId) => {
    try {
      await api.post("/cart", null, {
        params: { product_id: productId, quantity: 1 },
      });
      setMessage("Added to cart!");
      setTimeout(() => setMessage(""), 2000);
    } catch (err) {
      setMessage(err.response?.data?.detail || "Failed to add to cart");
    }
  };

  return (
    <div style={{ maxWidth: "800px", margin: "40px auto", fontFamily: "sans-serif" }}>
      <h2>Products</h2>
      {message && <p style={{ color: "green" }}>{message}</p>}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))", gap: "16px" }}>
        {products.map((product) => (
          <div
            key={product.id}
            style={{ border: "1px solid #ccc", borderRadius: "8px", padding: "16px" }}
          >
            <h3>{product.name}</h3>
            <p>{product.description}</p>
            <p><strong>${product.price}</strong></p>
            <p>Stock: {product.stock}</p>
            <button onClick={() => addToCart(product.id)} style={{ padding: "8px 16px" }}>
              Add to Cart
            </button>
          </div>
        ))}
      </div>
      {products.length === 0 && <p>No products found.</p>}
    </div>
  );
}

export default Products;

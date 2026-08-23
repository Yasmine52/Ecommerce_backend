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
    <div className="page-container">
      <h2 className="page-title">Products</h2>
      {message && <p className="success-text">{message}</p>}

      {products.length === 0 ? (
        <p className="empty-state">No products found.</p>
      ) : (
        <div className="grid">
          {products.map((product) => (
            <div key={product.id} className="card">
              <div className="product-name">{product.name}</div>
              <div className="product-desc">{product.description}</div>
              <div className="product-price">${product.price}</div>
              <div className="product-stock">Stock: {product.stock}</div>
              <button onClick={() => addToCart(product.id)} className="btn">
                Add to Cart
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Products;

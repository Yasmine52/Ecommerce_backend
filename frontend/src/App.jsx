import { BrowserRouter, Routes, Route, Link, Navigate } from "react-router-dom";
import Login from "./Login";
import Products from "./Products";
import Cart from "./Cart";

function isLoggedIn() {
  return !!localStorage.getItem("token");
}

function ProtectedRoute({ children }) {
  return isLoggedIn() ? children : <Navigate to="/login" />;
}

function App() {
  const loggedIn = isLoggedIn();

  const handleLogout = () => {
    localStorage.removeItem("token");
    window.location.href = "/login";
  };

  return (
    <BrowserRouter>
      <nav style={{ padding: "16px", borderBottom: "1px solid #ccc", fontFamily: "sans-serif" }}>
        <Link to="/products" style={{ marginRight: "16px" }}>Products</Link>
        <Link to="/cart" style={{ marginRight: "16px" }}>Cart</Link>
        {loggedIn ? (
          <button onClick={handleLogout}>Logout</button>
        ) : (
          <Link to="/login">Login</Link>
        )}
      </nav>

      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          path="/products"
          element={
            <ProtectedRoute>
              <Products />
            </ProtectedRoute>
          }
        />
        <Route
          path="/cart"
          element={
            <ProtectedRoute>
              <Cart />
            </ProtectedRoute>
          }
        />
        <Route path="/" element={<Navigate to="/products" />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
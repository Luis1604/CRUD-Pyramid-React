import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import ProductsPage from "./pages/ProductsPage";
import OrdersPage from "./pages/OrdersPage";
import AdminPage from "./pages/AdminPage";
import LoginGooglePage from "./pages/LoginGooglePage";
import RegisterGooglePage from "./pages/RegisterGooglePage";
import { AuthProvider } from "./context/AuthContext";

function App() {
    return (
        <AuthProvider>
                <Router>
                <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/admin" element={<AdminPage />} />
                    <Route path="/register" element={<RegisterPage />} />
                    <Route path="/products" element={<ProductsPage />} />
                    <Route path="/orders" element={<OrdersPage />} />
                    <Route path="/loging" element={<LoginGooglePage />} />
                    <Route path="/registerg" element={<RegisterGooglePage />} />
                </Routes>
            </Router>
        </AuthProvider>
        
    );
}

export default App;

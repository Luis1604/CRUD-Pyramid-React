import { useNavigate } from "react-router-dom";
import "../styles/admin.css";
import { AuthContext } from "../context/AuthContext";
import React, { useContext, useEffect, useCallback } from "react";

const AdminPage = () => {
    const { vrfToken, logout } = useContext(AuthContext);
    const navigate = useNavigate();

    // Verifica la autenticación
    useEffect(() => {
        if (!vrfToken()) {
            console.log("Usuario no autenticado, redirigiendo...");
            navigate("/");
        } else {
            console.log("Usuario autenticado en admin");
        }
    }, [vrfToken, navigate]);

    // Manejo de clic en las opciones del panel
    const handleOptionClick = useCallback((option) => {
        if (option.action) {
            option.action();
        } else if (option.path) {
            navigate(option.path);
        }
    }, [navigate]);

    const options = [
        { path: "/register", label: "Crear Usuario", icon: "👤" },
        { path: "/products", label: "Crear Producto", icon: "📦" },
        { path: "/orders", label: "Crear Orden", icon: "🛒" },
        { label: "Cerrar Sesión", icon: "🚪", action: logout }
    ];

    return (
        <div className="admin-container">
            <h2>Panel de Administración</h2>
            <div className="admin-grid">
                {options.map((option, index) => (
                    <div 
                        key={index} 
                        className="admin-card" 
                        onClick={() => handleOptionClick(option)}
                    >
                        <span className="admin-icon">{option.icon}</span>
                        <h3>{option.label}</h3>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default AdminPage;

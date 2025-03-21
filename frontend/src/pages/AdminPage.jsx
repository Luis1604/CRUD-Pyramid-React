import { useNavigate } from "react-router-dom";
import "../styles/admin.css";
import { AuthContext } from "../context/AuthContext";
import React, { useContext, useEffect, useCallback } from "react";

const AdminPage = () => {
    const { vrfToken, logout } = useContext(AuthContext);
    const navigate = useNavigate();
    const vrf = useCallback(() => !!vrfToken(), [vrfToken]); 
    
    useEffect(() => {
        const interval = setInterval(() => {
            if (!vrf()) {
                console.log("Usuario no autenticado, redirigiendo...");
                navigate("/");
            }else{
                console.log("Usuario autenticado Admin");
            }
        }, 1000);

        return () => clearInterval(interval);
    }, [vrf, navigate]);

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
        <>
            <nav>
                <div className="logo">Panel de Administración</div>
                <ul>
                    <li><a href="/admin">Administracíon</a></li>
                    <li><a href="/register">Usuarios</a></li>
                    <li><a href="/products">Productos</a></li>
                    <li><a href="/orders">Órdenes</a></li>
                    <li><a href="/" onClick={() => logout()} >Cerrar Sesión</a></li>
                </ul>
            </nav>
            <div className="admin-container">
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
            <footer>
                &copy; 2025 CRUD App - Todos los derechos reservados.
            </footer>

        </>
    );
};

export default AdminPage;

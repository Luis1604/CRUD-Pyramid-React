import React, { createContext, useState, useEffect, useCallback } from "react";

// Crear el contexto de autenticación
export const AuthContext = createContext();
const TOKEN_EXPIRATION_TIME = 3600 * 1000; // 1 hora
// Crear el proveedor de autenticación
export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);

    // Función para obtener datos del usuario
    const fetchUserData = useCallback(async (token) => {
        if (!token) return logout(); // Si no hay token, cerrar sesión

        try {
            const response = await fetch("http://localhost:6543/api/dashboard", {
                method: "GET",
                headers: { Authorization: `Bearer ${token}` },
            });

            if (!response.ok) throw new Error("Error en la validación del token");

            const data = await response.json();
            if (data.success) {
                console.log("Usuario autenticado:", data.name);
                setUser(data);
            } else {
                logout();
            }
        } catch (error) {
            console.error("Error al obtener datos del usuario:", error);
            logout();
        }
    }, []);

    // Verifica el token al cargar el componente
    useEffect(() => {
        const token = localStorage.getItem("token");
        if (token) fetchUserData(token);
    }, [fetchUserData]);

    // Función para iniciar sesión y almacenar el token
    const login = (token) => {
        localStorage.setItem("token", token);
        fetchUserData(token);
        setTimeout(() => logout(), TOKEN_EXPIRATION_TIME);
    };

    // Función para cerrar sesión
    const logout = () => {
        localStorage.removeItem("token");
        console.log("Token eliminado, cerrando sesión...");
        setUser(null);
    };

    // Validación del token
    const vrfToken = () => !!localStorage.getItem("token");

    return (
        <AuthContext.Provider value={{ user, login, logout, vrfToken }}>
            {children}
        </AuthContext.Provider>
    );
};

import axios from "axios";

const API_URL = "http://localhost:6543";

// Instancia de axios con configuración predeterminada
export const api = axios.create({
    baseURL: API_URL,
    headers: { "Content-Type": "application/json" }
});

// Función para obtener el token desde localStorage
export const getToken = () => localStorage.getItem("token");

// Función para guardar el token en localStorage
export const saveToken = (token) => localStorage.setItem("token", token);

// Función para eliminar el token (logout)
export const logout = () => {
    localStorage.removeItem("token");
    window.location.href = "/login"; // Redirigir al login tras cerrar sesión
};

// Función para iniciar sesión
export const login = async (email, password) => {
    try {
        const { data } = await api.post("/api/login", { email, password });
        saveToken(data.token);
        return data;
    } catch (error) {
        console.error("Error en login:", error);
        throw error.response?.data || { error: "Error al iniciar sesión" };
    }
};

// Función para registrar un nuevo usuario
export const registerUser = async (name, email, password) => {
    try {
        console.log("Enviando solicitud a createuser:", { name, email, password });
        const response = await api.post("/api/createuser", { name, email, password });
        console.log("Datos enviados");

        // Asegurarse de que la respuesta contenga 'message' y 'name'
        if (!response.data || !response.data.message || !response.data.name) {
            throw new Error(response.data?.error || "Respuesta inesperada del servidor.");
        }

        console.log("Usuario registrado con éxito:", response.data.message, response.data.name);
        return response.data; // Regresar toda la respuesta con mensaje y nombre
    } catch (error) {
        console.error("Error en el registro:", error);

        if (error.response) {
            // Si la respuesta del servidor tiene un error
            console.error("Respuesta del servidor:", error.response);
            if (error.response.data?.error) {
                return Promise.reject({ error: error.response.data.error });
            }
        } else if (error.request) {
            // Si no hubo respuesta del servidor (ej. error de red)
            console.error("No se recibió respuesta del servidor:", error.request);
        } else {
            // Cualquier otro error
            console.error("Error inesperado:", error.message);
        }

        // Si ocurre un error inesperado
        return Promise.reject({ error: "Error inesperado. Inténtelo más tarde." });
    }
};

// Función para obtener productos con autenticación
export const getProducts = async () => {
    try {
        const token = getToken();
        const response = await api.get("/api/products", {
            headers: { Authorization: `Bearer ${token}` }
        });
        return response.data;
    } catch (error) {
        throw error.response?.data || { error: "Error al obtener productos" };
    }
};

// Función para obtener órdenes con autenticación
export const getOrders = async () => {
    try {
        const token = getToken();
        const response = await api.get("/api/orders", {
            headers: { Authorization: `Bearer ${token}` }
        });
        return response.data;
    } catch (error) {
        throw error.response?.data || { error: "Error al obtener órdenes" };
    }
};
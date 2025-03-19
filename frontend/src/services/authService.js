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
export const login_ = async (mail, pass) => {
    console.log("Enviando solicitud a login:", { mail, pass });
    const res = await fetch("http://localhost:6543/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email:mail, password:pass}),
        mode: "cors",
    });
    console.log("Datos recibidos");
    const data = await res.json();
    if (data.success) {
        localStorage.setItem("token", data.token);
        saveToken(data.token);
        console.log("Sesión iniciada:");
        return data;
    }else{
        console.error("Error en el token recibido", data.error)
        return data;
    }
        
};

// Función para registrar un nuevo usuario
export const registerUser = async (name, email, password) => {
    try {
        console.log("Enviando solicitud a createuser:", { name, email });
        const resp = await fetch("http://localhost:6543/api/createuser", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name: name, email:email, password:password}),
            mode: "cors",
        });
        const data = await resp.json();
        if (data.success) {
            localStorage.setItem("token", data.token);
            saveToken(data.token);
            console.log("Usuario registrado con éxito:", data.name);
            return data;
        }else{
            console.error("Error en el registro:", data.error);
            return data;
        }
    } catch (error) {
        console.error("Error en el registro:", error);

        if (error.response) {
            // Si la respuesta del servidor tiene un error
            console.error("Respuesta del servidor:", error.response);
            if (error.resp.data?.error) {
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
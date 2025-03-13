import axios from "axios";

const API_URL = "http://localhost:6543";

export const api = axios.create({
    baseURL: API_URL,
    headers: { "Content-Type": "application/json" }
});

export const login = (email, password) => api.post("/api/login", { email, password });

export const registerUser = (name, email, password) => api.post("/api/createuser", { name, email, password });

export const getProducts = () => api.get("/api/products");

export const getOrders = () => api.get("/api/orders");

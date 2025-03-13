import { createContext, useState } from "react";
import { login } from "../services/api";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);

    const handleLogin = async (email, password) => {
        const response = await login(email, password);
        localStorage.setItem("token", response.data.token);
        setUser({ email });
    };

    return <AuthContext.Provider value={{ user, handleLogin }}>{children}</AuthContext.Provider>;
};
import React, { useContext, useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { login_ } from "../services/authService"; // Servicio de autenticación
import { FaEye, FaEyeSlash } from "react-icons/fa";
import "../styles/login.css";
import { AuthContext } from "../context/AuthContext";

const LoginPage = () => {
    const { login, vrfToken } = useContext(AuthContext);
    const navigate = useNavigate();
    const [credentials, setCredentials] = useState({ email: "", password: "" });
    const [showPassword, setShowPassword] = useState(false);
    const [error, setError] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const vrf = useCallback(() => !!vrfToken(), [vrfToken]); 
    
    useEffect(() => {
        const timeout = setTimeout(() => {
            if (vrf()) {
                console.log("Usuario autenticado, redirigiendo...");
                navigate("/admin");
            }
        }, 1000);
        return () => clearTimeout(timeout);
    }, [vrf, navigate]);

    // Manejo de cambio en inputs
    const handleChange = (e) => {
        setCredentials({ ...credentials, [e.target.name]: e.target.value });
    };

    // Manejo de inicio de sesión
    const handleLogin = useCallback(async (e) => {
        e.preventDefault();
        setError("");
        setIsLoading(true);

        try {
            const data = await login_(credentials.email, credentials.password);
            if(data.success){
                login(data.token);
                navigate("/admin");
            }else{
                setError(data.error);
            }
            
        } catch (error) {
            setError(error?.error || "Error al iniciar sesión.");
        } finally {
            setIsLoading(false);
        }
    }, [credentials, login, navigate]);

    return (
        <div className="login-container">
            <div className="login-box">
                <h2 className="h2">Iniciar Sesión</h2>
                {error && <p className="error-message">{error}</p>}
                <form onSubmit={handleLogin}>
                    {/* Input de Email */}
                    <div className="input-group">
                        <input
                            type="email"
                            name="email"
                            autoComplete="username"
                            placeholder="Correo electrónico"
                            value={credentials.email}
                            onChange={handleChange}
                            required
                        />
                    </div>

                    {/* Input de Contraseña con Icono */}
                    <div className="input-group">
                        <input
                            type={showPassword ? "text" : "password"}
                            name="password"
                            autoComplete="current-password"
                            placeholder="Contraseña"
                            value={credentials.password}
                            onChange={handleChange}
                            required
                        />
                        <span className="toggle-password" onClick={() => setShowPassword(!showPassword)}>
                            {showPassword ? <FaEyeSlash /> : <FaEye />}
                        </span>
                    </div>

                    <button className="button" type="submit" disabled={isLoading}>
                        {isLoading ? "Cargando..." : "Ingresar"}
                    </button>
                </form>
            </div>
        </div>
    );
};

export default LoginPage;
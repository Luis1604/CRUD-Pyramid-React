import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../services/authService"; // Importamos el servicio de autenticación
import { FaEye, FaEyeSlash } from "react-icons/fa";
import "../styles/login.css";

const LoginPage = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [showPassword, setShowPassword] = useState(false);
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setError(""); // Limpiar error anterior

        try {
            login(email, password);
            navigate("/admin"); // Redirigir tras login exitoso
        } catch (error) {
            setError(error.error || "Error al iniciar sesión.");
        }
    };

    return (
        <div className="login-container">
            <div className="login-box">
                <h2>Iniciar Sesión</h2>
                {error && <p className="error-message">{error}</p>}
                <form onSubmit={handleLogin}>
                    {/* Input de Email */}
                    <div className="input-group">
                        <input 
                            type="email"
                            id="email"
                            autoComplete="username"
                            placeholder="Correo electrónico" 
                            value={email} 
                            onChange={(e) => setEmail(e.target.value)} 
                            required 
                        />
                    </div>

                    {/* Input de Contraseña con Icono */}
                    <div className="input-group">
                        <input
                            type={showPassword ? "text" : "password"}
                            id="password"
                            autoComplete="current-password"
                            placeholder="Contraseña"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                        <span
                            className="toggle-password"
                            onClick={() => setShowPassword(!showPassword)}
                        >
                            {showPassword ? <FaEyeSlash /> : <FaEye />}
                        </span>
                    </div>

                    <button type="submit">Ingresar</button>
                </form>
            </div>
        </div>
    );
};

export default LoginPage;

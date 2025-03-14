import { useState } from "react";
import { registerUser } from "../services/authService";
import "../styles/register.css";
import { FaEye, FaEyeSlash } from "react-icons/fa";

const RegisterPage = () => {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [showPassword, setShowPassword] = useState(false);
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");
    const [formErrors, setFormErrors] = useState({});

    const validateForm = () => {
        let errors = {};

        if (name.trim().length < 3) {
            errors.name = "El nombre debe tener al menos 3 caracteres.";
        }

        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email.trim())) {
            errors.email = "Ingrese un correo válido.";
        }

        if (password.length < 6) {
            errors.password = "La contraseña debe tener al menos 6 caracteres.";
        }

        setFormErrors(errors);
        return Object.keys(errors).length === 0; // Retorna true si no hay errores
    };

    const handleRegister = async (e) => {
        e.preventDefault();
        setError("");
        setSuccess("");

        if (!validateForm()) return; // Si hay errores, no envía el formulario

        try {
            const response = await registerUser(name.trim(), email.trim(), password);
            setSuccess("Usuario ",response.name," registrado con éxito.");
            setName("");
            setEmail("");
            setPassword("");
            setFormErrors({});
        } catch (error) {
            setError(error.error || "Error al registrar usuario.");
        }
    };

    return (
        <div className="register-container">
            <div className="register-box">
                <h2 className="h2">Registro de usuario</h2>
                {error && <p className="error-message">{error}</p>}
                {success && <p className="success-message">{success}</p>}
                <form onSubmit={handleRegister} noValidate>
                    <div className="input-group">
                        <input
                            type="text"
                            id="name"
                            placeholder="Nombre"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            minLength="3"
                            required
                        />
                    </div>

                    <div className="input-group">
                        <input
                            type="email"
                            id="email"
                            placeholder="Correo electrónico"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>

                    <div className="input-group">
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
                        {formErrors.name && <span className="error-message">{formErrors.name}</span>}
                        {formErrors.email && <span className="error-message">{formErrors.email}</span>}
                        {formErrors.password && <span className="error-message">{formErrors.password}</span>}
                    </div>

                    <button type="submit" disabled={Object.keys(formErrors).length > 0}>
                        Registrarse
                    </button>
                </form>
            </div>
        </div>
    );
};

export default RegisterPage;
import React, { useContext, useEffect, useCallback } from "react";
import { GoogleOAuthProvider, GoogleLogin } from "@react-oauth/google";
import { useNavigate } from "react-router-dom";
import "../styles/login.css";
import { AuthContext } from "../context/AuthContext";

const clientId = "223506677250-er5uug0l0i40cmpei06oevnvn5s6724i.apps.googleusercontent.com";

const LoginGooglePage = () => {
    const { login, vrfToken } = useContext(AuthContext);
    const navigate = useNavigate();

    // Redirigir si el usuario ya está autenticado
    useEffect(() => {
        if (vrfToken()) {
            console.log("Usuario autenticado con Google, redirigiendo...");
            navigate("/admin");
        }
    }, [vrfToken, navigate]);

    // Manejo de éxito en autenticación con Google
    const handleSuccess = useCallback(async (response) => {
        const idToken = response.credential;

        try {
            console.log("Enviando token de Google al backend...");

            const res = await fetch("http://localhost:6543/api/auth_google", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ token: idToken }),
                mode: "cors",
                credentials: "include",
            });

            if (!res.ok) throw new Error(`Error ${res.status}: ${res.statusText}`);

            const data = await res.json();

            if (data.success) {
                localStorage.setItem("token", data.token);
                login(data.token);
                console.log("Login con Google exitoso. Redirigiendo...");
                navigate("/admin");
            } else {
                console.error("Error en autenticación:", data.error);
            }
        } catch (error) {
            console.error("Error en la autenticación con Google:", error);
        }
    }, [login, navigate]);

    const handleFailure = () => console.log("Error al iniciar sesión con Google");

    return (
        <div className="login-container">
            <div className="login-box">
                <h2 className="h2">Iniciar Sesión con Google</h2>
                <GoogleOAuthProvider clientId={clientId}>
                    <GoogleLogin onSuccess={handleSuccess} onError={handleFailure} useOneTap />
                </GoogleOAuthProvider>
            </div>
        </div>
    );
};

export default LoginGooglePage;

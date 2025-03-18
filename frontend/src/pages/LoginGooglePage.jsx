import { GoogleOAuthProvider, GoogleLogin } from "@react-oauth/google";
import { useNavigate } from "react-router-dom";
import "../styles/login.css";

const clientId = "223506677250-er5uug0l0i40cmpei06oevnvn5s6724i.apps.googleusercontent.com";

const LoginGooglePage = () => {
    const navigate = useNavigate();

    const handleSuccess = async (response) => {
        const idToken = response.credential;
    
        try {
            // Enviar el token de Google al backend
            console.warn("Enviando token de Google al backend:");
            const res = await fetch("http://localhost:6543/api/auth_google", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ token: idToken }),
                mode: "cors", 
                credentials: "include",
            });
    
            // Manejo de error si la solicitud no se completa correctamente
            if (!res.ok) {
                console.error("Error en la respuesta del backend:", res.statusText);
                throw new Error(`Error ${res.status}: ${res.statusText}`);
            }
    
            const data = await res.json();
    
            if (data.success) {
                localStorage.setItem("token", data.token); // Guardar el JWT de sesión
                console.log("Login exitoso. Redirigiendo al dashboard...");
                navigate("/admin");
            } else {
                console.error("Error en autenticación:", data.error);
            }
        } catch (error) {
            console.error("Error en la solicitud de autenticación con Google:", error);
        }
    };

    const handleFailure = () => {
        console.log("Error al iniciar sesión con Google");
    };

    return (
        <div className="login-container">
            <div className="login-box">
                <h2 className="h2">Iniciar Sesión con Google</h2>
                <form>
                <GoogleOAuthProvider clientId={clientId}>
                    <GoogleLogin onSuccess={handleSuccess} onError={handleFailure} useOneTap />
                </GoogleOAuthProvider>
                </form>
            </div>
        </div>

    );
};

export default LoginGooglePage;

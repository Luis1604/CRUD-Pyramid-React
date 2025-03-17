import { GoogleOAuthProvider, GoogleLogin } from "@react-oauth/google";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import "../styles/login.css";

const clientId = "223506677250-er5uug0l0i40cmpei06oevnvn5s6724i.apps.googleusercontent.com";

const LoginGooglePage = () => {
    const navigate = useNavigate();
    const [otpRequired, setOtpRequired] = useState(false);
    const [otpCode, setOtpCode] = useState("");
    const [userToken, setUserToken] = useState(""); // Token de Google almacenado temporalmente

    const handleSuccess = async (response) => {
        const idToken = response.credential;
        setUserToken(idToken);

        try {
            // Enviar el token de Google al backend
            console.warn("Enviando token de Google al backend...");
            const res = await fetch("http://localhost:6543/api/auth_google", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ token: idToken }),
                mode: "cors", 
                credentials: "include",
            });

            if (!res.ok) {
                console.error("Error en la respuesta del backend:", res.statusText);
                throw new Error(`Error ${res.status}: ${res.statusText}`);
            }

            const data = await res.json();

            if (data.success) {
                if (data.otp_required) {
                    // Si el usuario tiene activado 2FA, pedir OTP
                    setOtpRequired(true);
                } else {
                    // Si no requiere OTP, iniciar sesión normalmente
                    localStorage.setItem("token", data.token);
                    console.log("Login exitoso. Redirigiendo al dashboard...");
                    navigate("/admin");
                }
            } else {
                console.error("Error en autenticación:", data.error);
            }
        } catch (error) {
            console.error("Error en la autenticación con Google:", error);
        }
    };

    const handleOtpSubmit = async (response) => {
        if (otpCode.trim()==="") {  
            console.error("Código de verificación vacío");
            return;
        }
        try {
            console.warn("Enviando 2fa al backend...");
            const res = await fetch("http://localhost:6543/api/auth_google", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ token: userToken, otp_code: otpCode }),
                mode: "cors",
                credentials: "include",
            });

            if (!res.ok) {
                console.error("Error en la respuesta del backend:", res.statusText);
                throw new Error(`Error ${res.status}: ${res.statusText}`);
            }

            const data = await res.json();

            if (data.success) {
                localStorage.setItem("token", data.token);
                console.log("Autenticación 2FA exitosa. Redirigiendo al dashboard...");
                navigate("/admin");
            } else {
                console.error("Código de verificación incorrecto");
            }
        } catch (error) {
            console.error("Error en la verificación de 2FA:", error);
        }
    };

    return (
        <div className="login-container">
            <div className="login-box">
                <h2 className="h2">Iniciar Sesión</h2>
                <form>
                    {!otpRequired ? (
                        <GoogleOAuthProvider clientId={clientId}>
                            <GoogleLogin onSuccess={handleSuccess} onError={() => console.log("Error al iniciar sesión con Google")} useOneTap />
                        </GoogleOAuthProvider>
                    ) : (
                        <div>
                            <p>Ingrese su código de verificación</p>
                            <input
                                type="text"
                                placeholder="Código de verificación"
                                value={otpCode}
                                onChange={(e) => setOtpCode(e.target.value)}
                            />
                            <button type="button" onClick={handleOtpSubmit}>Verificar Código</button>
                        </div>
                    )}
                </form>
            </div>
        </div>
    );
};

export default LoginGooglePage;

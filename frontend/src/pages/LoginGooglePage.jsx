import React, { useContext, useEffect, useCallback, useState } from "react";
import { GoogleOAuthProvider, GoogleLogin } from "@react-oauth/google";
import { useNavigate } from "react-router-dom";
import "../styles/login.css";
import { AuthContext } from "../context/AuthContext";

const clientId = "223506677250-er5uug0l0i40cmpei06oevnvn5s6724i.apps.googleusercontent.com";

const LoginGooglePage = () => {
    const { login, vrfToken } = useContext(AuthContext);
    const navigate = useNavigate();
    const [otpCode, setOtpCode] = useState("");
    const [otpRequired, setOtpRequired] = useState(false);
    const [mail, setMail] = useState(null);
    const vrf = useCallback(() => !!vrfToken(), [vrfToken]);

    useEffect(() => {
        const timeout = setTimeout(() => {
            if (vrf()) {
                console.log("Usuario autenticado, redirigiendo...");
                navigate("/admin");
            }
            else {
                console.log("No logueado")
            }
        }, 1000);
        return () => clearTimeout(timeout);
    }, [vrf, navigate]);
    

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
                if (data.otp_required) {
                    console.log("Se requiere OTP para continuar");
                    setMail(data.email);
                    setOtpRequired(true);
                } else {
                    login(data.token);
                    console.log("Login con Google exitoso sin 2FK. Redirigiendo...");
                    navigate("/admin");
                }
            } else {
                console.error("Error en autenticación:", data.error);
            }
        } catch (error) {
            console.error("Error en la autenticación con Google:", error);
        }
    }, [login, navigate]);

    const handleOtpSubmit = async (response) => {
        if (otpCode.trim() === "") {
            console.error("Código de verificación vacío");
            return;
        }
        try {
            if (mail === null) {
                console.error("Error en la verificación de 2FA: no se encontró el correo electrónico");
                return;
            } else {
                const res = await fetch("http://localhost:6543/api/two_steps", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ email: mail, otp_code: otpCode }),
                    mode: "cors",
                    credentials: "include",
                });

                if (!res.ok) {
                    console.error("Error en la respuesta del backend:", res.statusText);
                    throw new Error(`Error ${res.status}: ${res.statusText}`);
                }

                const data = await res.json();

                if (data.success) {
                    login(data.token);
                    console.log("Autenticación 2FA exitosa. Redirigiendo al dashboard...");
                    navigate("/admin");
                } else {
                    console.error("Código de verificación incorrecto");
                }
            }

        } catch (error) {
            console.error("Error en la verificación de 2FA:", error);
        }
    };

    return (
        <div className="login-container">
            <div className="login-box">

                <form>
                    {!otpRequired ? (
                        <>
                            <h2 className="h2-google">Iniciar Sesión con Google</h2>

                            <GoogleOAuthProvider 
                                clientId={clientId}
                                auto_select={true}
                                prompt="consent"
                                onScriptLoadSuccess={() => console.log("Google SDK cargado correctamente")}
                                onScriptLoadError={() => console.error("Error al cargar el SDK de Google")}
                            >
                                <GoogleLogin
                                    onSuccess={handleSuccess}
                                    onError={() => console.log("Error al iniciar sesión con Google")}
                                    useOneTap
                                    theme="filled_blue"
                                    size="large"         
                                    text="signin_with"
                                />
                            </GoogleOAuthProvider>
                        </>
                    ) : (
                        <>
                            <p className="h2-google">Ingrese su código de verificación</p>
                            <p className="code-duration">El código es válido por 5 minutos.</p>
                            <input
                                className="input-code"
                                type="text"
                                inputMode="numeric"
                                pattern="[0-9]*"
                                maxLength="6"
                                placeholder="------"
                                value={otpCode}
                                onChange={(e) => {
                                    const value = e.target.value.replace(/\D/g, ""); // Solo números
                                    setOtpCode(value);
                                }}
                            />
                            <button className="button" type="button" onClick={handleOtpSubmit}>Verificar Código</button>
                        </>
                    )}
                </form>
            </div>
        </div>
    );
};

export default LoginGooglePage;

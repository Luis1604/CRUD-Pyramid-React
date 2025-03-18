import { GoogleOAuthProvider, GoogleLogin } from "@react-oauth/google";
import { FcGoogle } from "react-icons/fc";
import { useNavigate } from "react-router-dom";
import "../styles/login.css";

const clientId = "223506677250-er5uug0l0i40cmpei06oevnvn5s6724i.apps.googleusercontent.com";

const LoginGooglePage = () => {
    const navigate = useNavigate();

    const handleSuccess = async (response) => {
        const idToken = response.credential;

        // Enviar el token al backend
        const res = await fetch("http://localhost:8000/api/auth/google", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ token: idToken }),
        });

        const data = await res.json();

        if (data.success) {
            localStorage.setItem("token", data.token); // Guardar el JWT de sesión
            navigate("/dashboard");
        }
    };

    const handleFailure = () => {
        console.log("Error al iniciar sesión con Google");
    };

    const CustomButton = ({ onClick, disabled, children }) => (
        <button
            onClick={onClick}
            disabled={disabled}
            className="flex items-center gap-2 px-4 py-2 bg-white text-gray-700 border border-gray-300 rounded-lg shadow hover:bg-gray-100 transition-all disabled:opacity-50"
        >
            {children}
        </button>
    );

    return (
        <div className="login-container">
            <div className="login-box">
                <h2 className="h2">Iniciar Sesión con Google</h2>
                <form>
                    <GoogleOAuthProvider clientId={clientId}>
                        <GoogleLogin
                            onSuccess={handleSuccess}
                            onError={handleFailure}
                            useOneTap
                            render={(renderProps) => (
                                <CustomButton onClick={renderProps.onClick} disabled={renderProps.disabled}>
                                    <FcGoogle className="text-xl" />
                                    Iniciar sesión con Google
                                </CustomButton>
                            )}
                        />
                    </GoogleOAuthProvider>
                </form>
            </div>
        </div>

    );
};

export default LoginGooglePage;

import { useNavigate } from "react-router-dom";
import "../styles/login.css";

const RegisterGooglePage = () => {
    const navigate = useNavigate();

    return (
        <div className="register-container">
            <div className="register-box">
                <h2 className="h2">Registro de usuario</h2>
                <form>
                <button 
                    onClick={() => navigate("/admin")} 
                    className="homepage-button google-button"
                >
                    Registrarse con Google
                </button>
                </form>
                    
            </div>
        </div>
    );
};

export default RegisterGooglePage;

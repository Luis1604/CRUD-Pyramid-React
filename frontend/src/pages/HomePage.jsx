import { useNavigate } from "react-router-dom";
import "../styles/homepage.css"; // Importa los estilos

const HomePage = () => {
    const navigate = useNavigate();

    return (
        <div className="homepage-container">
            <div className="homepage-content">
                <h1 className="homepage-title">Bienvenido a CRUD</h1>
                <p className="homepage-description">
                    Plataforma de administración de productos y órdenes.
                </p>
                <button 
                    onClick={() => navigate("/login")} 
                    className="homepage-button"
                >
                    Iniciar Sesión
                </button>
                <button 
                    onClick={() => navigate("/loging")} 
                    className="homepage-button google-button"
                >
                    Registrarse con Google
                </button>
                <button 
                    onClick={() => navigate("/loging")} 
                    className="homepage-button google-button"
                >
                    Iniciar sesión con Google
                </button>
            </div>
            <div className="homepage-footer">
                &copy; {new Date().getFullYear()} CRUD. Todos los derechos reservados.
            </div>
        </div>
    );
};

export default HomePage;

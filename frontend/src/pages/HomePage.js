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
            </div>
            <div className="homepage-footer">
                &copy; {new Date().getFullYear()} Academico. Todos los derechos reservados.
            </div>
        </div>
    );
};

export default HomePage;

import { useNavigate } from "react-router-dom";
import "../styles/homepage.css"; // Importa los estilos

const HomePage = () => {
    const navigate = useNavigate();

    return (
        <>
            <nav>
                <div className="logo">CRUD DEMO</div>
                <ul>
                    <li><a href="/">Inicio</a></li>
                </ul>
            </nav>

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
            </div>
            <footer>
                &copy; 2025 CRUD App - Todos los derechos reservados.
            </footer>
        </>
    );
};

export default HomePage;

import { useNavigate } from "react-router-dom";
import "../styles/admin.css";

const AdminPage = () => {
    const navigate = useNavigate();

    const options = [
        { path: "/register", label: "Crear Usuario", icon: "👤" },
        { path: "/create-product", label: "Crear Producto", icon: "📦" },
        { path: "/create-order", label: "Crear Orden", icon: "🛒" }
    ];

    return (
        <div className="admin-container">
            <h2>Panel de Administración</h2>
            <div className="admin-grid">
                {options.map((option, index) => (
                    <div key={index} className="admin-card" onClick={() => navigate(option.path)}>
                        <span className="admin-icon">{option.icon}</span>
                        <h3>{option.label}</h3>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default AdminPage;

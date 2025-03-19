import { useEffect, useState } from "react";
import axios from "axios";
import "../styles/products.css";
import { FaEdit, FaTrashAlt } from "react-icons/fa"; // Asegúrate de instalar react-icons si no lo tienes

const ProductsPage = () => {
    const [products, setProducts] = useState([]);
    const [error, setError] = useState(null);
    const [newProduct, setNewProduct] = useState({ name: "", description: "", price: "" });
    const [name, setName] = useState("");
    const [description, setDescription] = useState("");
    const [price, setPrice] = useState("");
    

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                const response = await axios.get("http://localhost:6543/api/products");
                setProducts(response.data);
            } catch (error) {
                console.error("Error al obtener productos:", error);
                setError("No se pudieron cargar los productos. Intente nuevamente más tarde.");
            }
        };
        fetchProducts();
    }, []);

    const handleModify = (id) => {
        console.log(`Modificar producto con ID: ${id}`);
    };

    const handleDelete = async (id) => {
        try {
            await axios.delete(`http://localhost:6543/api/products/${id}`);
            setProducts(products.filter(product => product.id !== id));
        } catch (error) {
            console.error("Error al eliminar producto:", error);
            setError("No se pudo eliminar el producto.");
        }
    };

    const handleAddProduct = async (e) => {
        e.preventDefault();
        if (!newProduct.name || !newProduct.description || !newProduct.price) {
            setError("Todos los campos son obligatorios.");
            return;
        }
        try {
            const resp = await fetch("http://localhost:6543/api/products", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name, description, price }),
                mode: "cors",
            });
            setProducts([...products, resp.data]);
            setNewProduct({ name: "Chocolate", description: "Chocolate blanco", price: "4" });
            setError(null);
        } catch (error) {
            console.error("Error al agregar producto:", error);
            setError("No se pudo agregar el producto.");
        }
    };

    return (
        <div className="products-container">
            <form className="register-box" onSubmit={handleAddProduct}>
                <h2 className="title">Agregar Producto</h2>
                <input type="text" name="name" placeholder="Nombre" value={newProduct.name} onChange={(e) => setName(e.target.value)} required />
                <input type="text" name="description" placeholder="Descripción" value={newProduct.description} onChange={(e) => setDescription(e.target.value)} required />
                <input type="number" name="price" placeholder="Precio" value={newProduct.price} onChange={(e) => setPrice(e.target.value)} required />
                <button type="submit">Agregar Producto</button>
            </form>

            {error && <p className="error-message">{error}</p>}

            <table className="styled-table">
                <thead>
                    <tr>
                        <th>Nombre</th>
                        <th>Descripción</th>
                        <th>Precio</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    {products.map((product) => (
                        <tr key={product.id}>
                            <td>{product.name}</td>
                            <td>{product.description}</td>
                            <td>${parseFloat(product.price).toFixed(2)}</td>
                            <td className="button-group">
                                <button className="modify-btn" onClick={() => handleModify(product.id)}>
                                    <FaEdit /> <span>Modificar</span>
                                </button>
                                <button className="delete-btn" onClick={() => handleDelete(product.id)}>
                                    <FaTrashAlt /> <span>Eliminar</span>
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default ProductsPage;

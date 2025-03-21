import React, { useContext, useEffect, useState, useCallback } from "react";
import { AuthContext } from "../context/AuthContext";
import "../styles/products.css";
import { useNavigate } from "react-router-dom";

const ProductsPage = () => {
    const { vrfToken, logout } = useContext(AuthContext);
    const navigate = useNavigate();
    const [showModal, setShowModal] = useState(false);
    const [newProduct, setNewProduct] = useState({ id: 0, name: "", description: "", price: "" });
    const [selectedId, setSelectedId] = useState(null);
    const [products, setProducts] = useState([
        { id: 1, name: '', description: '', price: '' },
    ]);
    const vrf = useCallback(() => !!vrfToken(), [vrfToken]);
    const [error, setError] = useState("");
    const handleOpenModal = () => setShowModal(true);
    const handleCloseModal = () => setShowModal(false);

    const handleChange = (e) => {
        setNewProduct({ ...newProduct, [e.target.name]: e.target.value });
    };

    const handleCreateProd = async (response) => {
        try {
            const res = await fetch("http://localhost:6543/api/createproduct", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(newProduct),
                mode: "cors",
                credentials: "include",
            });

            if (!res.ok) {
                console.error("Error en la respuesta del backend:", res.statusText);
                throw new Error(`Error ${res.status}: ${res.statusText}`);
            }
            const data = await res.json();
            if (data.success) {
                console.log("Producto creado con exito.");
                fetchData();
                handleCloseModal(true)
            } else {
                setError("Error al crear producto");
                console.error("Error al crear producto");
            }
        } catch (error) {
            console.error("Error al crear producto catch: ", error);
        }
    };
    const getProductNameById = (id) => {
        const product = newProduct.find(p => p.id === id);
        return product ? product.name : "Producto no encontrado";
    };
    
    const handleEliminate = async (response) => {
        try {
            if(selectedId===null){
                console.error("Seleccione un producto.");
                setError("Seleccione un producto");
            }else{
                console.log("Es array: ",newProduct); 
                const nam = getProductNameById(selectedId);
                const res = await fetch("http://localhost:6543/api/product", {
                    method: "DELETE",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({name:nam}),
                    mode: "cors",
                    credentials: "include",
                });
    
                if (!res.ok) {
                    console.error("Error en la respuesta del backend:", res.statusText);
                    throw new Error(`Error ${res.status}: ${res.statusText}`);
                }
                const data = await res.json();
                if (data.success) {
                    console.log("Producto eliminado con exito.");
                    fetchData();
                } else {
                    console.error("Error al eliminar producto", );
                    setError(data.error);
                }
            }
        } catch (error) {
            console.error("Error al crear producto catch: ", error);
        }
    };

    const fetchData = useCallback(async () => {
        try {
            const res = await fetch("http://localhost:6543/api/products", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
                mode: "cors",
                credentials: "include",
            });
    
            if (!res.ok) {
                console.error("Error en la respuesta del backend:", res.statusText);
                throw new Error(`Error ${res.status}: ${res.statusText}`);
            }
            const data = await res.json();
            if (data.success) {
                console.log("Productos listados con éxito.");
                setProducts(
                    data.products.map((product, index) => ({
                        ...product,
                        id: product.id || Date.now() + index, 
                    }))
                );
                handleCloseModal(true);
            } else {
                console.error("Error al crear producto");
            }
        } catch (error) {
            console.error("Error al crear producto catch: ", error);
        }
    }, [setProducts]);
    
    useEffect(() => {
        fetchData();
        const interval = setInterval(() => {
            if (!vrf()) {
                console.log("Usuario no autenticado, redirigiendo...");
                navigate("/");
            }
        }, 1000);
        return () => clearInterval(interval);
    }, [fetchData, vrf, navigate]);

    return (
        <>
            <nav>
                <div className="logo">Productos</div>
                <ul>
                    <li><a href="/admin">Administración</a></li>
                    <li><a href="/register">Usuarios</a></li>
                    <li><a href="/products">Productos</a></li>
                    <li><a href="/orders">Órdenes</a></li>
                    <li><a href="/" onClick={() => logout()}>Cerrar Sesión</a></li>
                </ul>
            </nav>

            <div className="products-container">
                {showModal && (
                    <div className="modal">
                        <div className="modal-content">
                            <h2 className="h2">Agregar Producto</h2>
                            <input type="text" name="name" placeholder="Nombre:" value={newProduct.name} onChange={handleChange} />
                            <input type="text" name="description" placeholder="Descripción:" value={newProduct.description} onChange={handleChange} />
                            <input type="number" name="price" placeholder="Precio:" value={newProduct.price} onChange={handleChange} />
                            <div className="modal-buttons">
                                <button onClick={handleCreateProd}>Guardar</button>
                                <button onClick={handleCloseModal}>Cancelar</button>
                            </div>
                        </div>
                    </div>
                )}
                <div className="table-container">
                    <table className="data-table">
                        <thead>
                            <tr>
                                <th></th>
                                <th>Nombre</th>
                                <th>Descripción</th>
                                <th>Precio</th>
                            </tr>
                        </thead>
                        <tbody>
                            {products.map((item) => (
                                <tr key={item.id} onClick={() => setSelectedId(item.id)}>
                                    <td>
                                        <input
                                            type="checkbox"
                                            checked={selectedId === item.id}
                                            onChange={() => setSelectedId(item.id)}
                                        />
                                    </td>
                                    <td>{item.name} </td>
                                    <td>{item.description}</td>
                                    <td>{item.price}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                    <div className="button-container">
                        {error && <p className="error-message">{error}</p>}
                        <button className="action-button" onClick={handleOpenModal}>Agregar</button>
                        <button className="action-button">Editar</button>
                        <button className="action-button" onClick={handleEliminate}>Eliminar</button>
                    </div>
                </div>
            </div>



            <footer>
                &copy; 2025 CRUD App - Todos los derechos reservados.
            </footer>
        </>
    );
};

export default ProductsPage;

import React, { useContext, useEffect, useState } from "react";
import { AuthContext } from "../context/AuthContext";
import "../styles/products.css";
import { useNavigate } from "react-router-dom";

const ProductsPage = () => {
    const { vrfToken, logout } = useContext(AuthContext);
    const navigate = useNavigate();
    useEffect(() => {
            if (!vrfToken()) {
                console.log("Usuario no autenticado, redirigiendo...");
                navigate("/");
            } else {
                console.log("Usuario autenticado en Productos");
            }
        }, [vrfToken, navigate]);

    const data = [
        { id: 1, name: 'Producto A', descr: 'Producto A', price: '$10' },
        { id: 2, name: 'Producto B', descr: 'Producto B', price: '$15' },
    ];
    return (
        <>
            <nav>
                <div className="logo">Productos</div>
                <ul>
                    <li><a href="/admin">Administracíon</a></li>
                    <li><a href="/register">Usuarios</a></li>
                    <li><a href="/products">Productos</a></li>
                    <li><a href="/orders">Órdenes</a></li>
                    <li><a href="/" onClick={() => logout()} >Cerrar Sesión</a></li>
                </ul>
            </nav>
            <div className="products-container">
                <div className="table-container">
                    <table className="data-table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Nombre</th>
                                <th>Descripción</th>
                                <th>Precio</th>
                            </tr>
                        </thead>
                        <tbody>
                            {data.map((item) => (
                                <tr key={item.id}>
                                    <td>{item.id}</td>
                                    <td>{item.name}</td>
                                    <td>{item.descr}</td>
                                    <td>{item.price}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                    <div className="button-container">
                        <button className="action-button">Agregar</button>
                        <button className="action-button">Editar</button>
                        <button className="action-button">Eliminar</button>
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

import { useEffect, useState } from "react";
import axios from "axios";

const ProductsPage = () => {
    const [products, setProducts] = useState([]);

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                const response = await axios.get("http://localhost:6543/api/products");
                setProducts(response.data);
            } catch (error) {
                console.error("Error al obtener productos", error);
            }
        };
        fetchProducts();
    }, []);

    return (
        <div>
            <h2>Productos</h2>
            <ul>
                {products.map((product) => (
                    <li key={product.id}>
                        {product.name} - ${product.price}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default ProductsPage;

import { useEffect, useState } from "react";
import axios from "axios";

const OrdersPage = () => {
    const [orders, setOrders] = useState([]);

    useEffect(() => {
        const fetchOrders = async () => {
            try {
                const response = await axios.get("http://localhost:6543/api/orders");
                setOrders(response.data);
            } catch (error) {
                console.error("Error al obtener órdenes", error);
            }
        };
        fetchOrders();
    }, []);

    return (
        <div>
            <h2>Órdenes</h2>
            <ul>
                {orders.map((order) => (
                    <li key={order.id}>
                        Orden #{order.id} - Usuario: {order.user_id}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default OrdersPage;

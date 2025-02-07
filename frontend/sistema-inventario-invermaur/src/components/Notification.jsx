import React, { useEffect, useState } from 'react';
import axios from 'axios';
import styles from '../styles/notification.module.css';

const Notification = ({ onRestock }) => {
    const [productos, setProductos] = useState([]);

    useEffect(() => {
        // Obtener productos con inventario bajo desde el backend
        const fetchProductosInventarioBajo = async () => {
            try {
                const response = await axios.get('http://localhost:8000/productos/inventario_bajo');
                console.log('Productos obtenidos:', response.data);
                setProductos(response.data);
            } catch (error) {
                console.error('Error al obtener productos con inventario bajo:', error);
            }
        };

        fetchProductosInventarioBajo();
    }, []);

    const handleRestockClick = async (producto) => {
        // Verificar el producto antes de la solicitud
        console.log('Producto:', producto);

        const cantidad = parseInt(prompt(`Ingrese la cantidad a reabastecer (Min: ${producto.cantidad_minima}, Max: ${producto.cantidad_maxima}):`), 10);
        if (!cantidad || cantidad <= 0) {
            alert('Por favor ingrese una cantidad válida.');
            return;
        }

        if (cantidad + producto.stock > producto.cantidad_maxima) {
            alert(`La cantidad total no puede exceder el stock máximo de ${producto.cantidad_maxima} unidades.`);
            return;
        }

        try {
            // Realizar la solicitud PUT al backend
            await axios.put(
                `http://localhost:8000/productos/reponer/${producto.producto_id}`,
                null,
                {
                    params: { cantidad: cantidad }, // Envía la cantidad como parámetro
                }
            );

            // Verificar el producto_id después de la solicitud
            console.log('Producto reabastecido ID:', producto.producto_id);

            alert('Producto reabastecido exitosamente');
            // Actualizar el estado de productos para eliminar el producto reabastecido
            setProductos(productos.filter(prod => prod.producto_id !== producto.producto_id));
            // Llama a la función para actualizar el estado de productos en el padre
            onRestock(producto.producto_id, cantidad);
        } catch (error) {
            console.error('Error al reponer producto:', error.response?.data || error.message);
            alert('Hubo un error al reponer el producto. Intente nuevamente.');
        }
    };

    return (
        <div className={`alert alert-warning mt-4 ${styles.notification}`} role="alert">
            🔔 Tienes productos con inventario bajo:
            <ul className={styles.productList}>
                {productos.map((producto) => (
                    <li key={producto.producto_id} className={styles.productItem}>
                        {producto.nombre} (Código: {producto.codigo}) - Stock: {producto.stock} unidades. Ubicación: {producto.ubicacion}
                        <button
                            className={`btn btn-primary ${styles.restockButton}`}
                            onClick={() => handleRestockClick(producto)} // Pasar el producto completo para validación
                        >
                            Reabastecer
                        </button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Notification;


























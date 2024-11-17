import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Sidebar from '../../components/Sidebar';
import Header from '../../layouts/Header';
import Footer from '../../layouts/Footer';
import 'bootstrap/dist/css/bootstrap.min.css';
import styles from './styles/listar-entradas.module.css';

const ListarEntradas = () => {
    const [entradas, setEntradas] = useState([]);

    useEffect(() => {
      // Obtener las entradas
      axios.get('http://localhost:8000/entradas_inventario')
        .then(response => {
          const entradasConDetalles = response.data.map(entrada => {
            // Hacer las solicitudes para obtener los detalles de producto y proveedor
            const productoRequest = axios.get(`http://localhost:8000/productos/${entrada.producto_id}`).catch((error) => {
              console.error('Error al obtener producto:', error);
              return { data: { nombre: 'No disponible' } }; // Asegurarse de que haya un valor por defecto
            });

            const proveedorRequest = axios.get(`http://localhost:8000/proveedores/${entrada.proveedor_id}`).catch((error) => {
              console.error('Error al obtener proveedor:', error);
              return { data: { nombre: 'No disponible' } }; // Asegurarse de que haya un valor por defecto
            });

            return Promise.all([productoRequest, proveedorRequest]).then(([productoRes, proveedorRes]) => {
              return {
                ...entrada,
                producto: productoRes.data,  // Producto con su nombre
                proveedor: proveedorRes.data, // Proveedor con su nombre
              };
            });
          });

          // Esperar a que todas las solicitudes se resuelvan y luego establecer las entradas
          Promise.all(entradasConDetalles).then(entradasConDetallesFinales => {
            setEntradas(entradasConDetallesFinales);
          });
        })
        .catch(error => console.error('Error al obtener entradas:', error));
    }, []);

  return (
    <div className={styles.container}>
      <Sidebar />
      <div className={styles.mainContent}>
        <Header />
        <div className="container mt-5">
          <h2 className={styles.title}>Listado de Entradas de Inventario</h2>
          <table className="table table-striped mt-4">
            <thead>
              <tr>
                <th>ID</th>
                <th>Producto</th>
                <th>Proveedor</th>
                <th>Cantidad</th>
                <th>Precio de Compra</th>
                <th>Fecha</th>
              </tr>
            </thead>
            <tbody>
              {entradas.map((entrada) => (
                <tr key={entrada.entrada_id}>
                  <td>{entrada.entrada_id}</td>
                  <td>{entrada.producto?.nombre || 'No disponible'}</td>  {/* Manejo de error */}
                  <td>{entrada.proveedor?.nombre || 'No disponible'}</td>  {/* Manejo de error */}
                  <td>{entrada.cantidad}</td>
                  <td>{entrada.precio_compra}</td>
                  <td>{new Date(entrada.fecha).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <Footer />
      </div>
    </div>
  );
};

export default ListarEntradas;


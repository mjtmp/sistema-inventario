import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Sidebar from '../../components/Sidebar';
import Header from '../../layouts/Header';
import Footer from '../../layouts/Footer';
import 'bootstrap/dist/css/bootstrap.min.css';
import styles from './styles/entrada-inventario.module.css';

const EntradaInventario = () => {
  const [entrada, setEntrada] = useState({
    producto_id: '',
    proveedor_id: '',
    cantidad: '',
    precio_compra: '',
    fecha: ''
  });

  const [productos, setProductos] = useState([]);
  const [proveedores, setProveedores] = useState([]);

  useEffect(() => {
    // Obtener lista de productos y proveedores para seleccionar en el formulario
    axios.get('http://localhost:8000/productos')
    .then(response => {
        console.log('Respuesta de productos:', response.data); // Imprime para verificar
        setProductos(response.data.productos); // Asegúrate de que "productos" existe en la respuesta
    })    
    .catch(error => console.error('Error al obtener productos:', error));

    axios.get('http://localhost:8000/proveedores')
    .then(response => {
      console.log('Respuesta de proveedores:', response.data); // Imprime para verificar
      setProveedores(response.data.proveedores); // Asegúrate de que "proveedores" existe en la respuesta
    })
    .catch(error => console.error('Error al obtener proveedores:', error));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:8000/entradas_inventario', entrada);
      alert('Entrada de inventario registrada con éxito');
      setEntrada({
        producto_id: '',
        proveedor_id: '',
        cantidad: '',
        precio_compra: '',
        fecha: ''
      });
    } catch (error) {
      console.error('Error al registrar la entrada de inventario:', error.response?.data || error.message);
      alert('Error al registrar la entrada de inventario');
    }
  };

  return (
    <div className={styles.container}>
      <Sidebar />
      <div className={styles.mainContent}>
        <Header />
        <div className="container mt-5 card">
          <h2 className={styles.title}>Registrar Entrada de Inventario</h2>
          <form onSubmit={handleSubmit} className={styles.formContainer}>
            <div className="form-group">
              <label>Producto</label>
              <select
                className="form-control"
                value={entrada.producto_id}
                onChange={(e) => setEntrada({ ...entrada, producto_id: e.target.value })}
                required
              >
                <option value="">Selecciona un producto</option>
                {productos.map((producto) => (
                  <option key={producto.producto_id} value={producto.producto_id}>
                    {producto.nombre}
                  </option>
                ))}
              </select>
            </div>
            <div className="form-group mt-3">
              <label>Proveedor</label>
              <select
                className="form-control"
                value={entrada.proveedor_id}
                onChange={(e) => setEntrada({ ...entrada, proveedor_id: e.target.value })}
                required
              >
                <option value="">Selecciona un proveedor</option>
                {proveedores.map((proveedor) => (
                  <option key={proveedor.proveedor_id} value={proveedor.proveedor_id}>
                    {proveedor.nombre}
                  </option>
                ))}
              </select>
            </div>
            <div className="form-group mt-3">
              <label>Cantidad</label>
              <input
                type="number"
                className="form-control"
                value={entrada.cantidad}
                onChange={(e) => setEntrada({ ...entrada, cantidad: e.target.value })}
                required
              />
            </div>
            <div className="form-group mt-3">
              <label>Precio de Compra</label>
              <input
                type="number"
                className="form-control"
                value={entrada.precio_compra}
                onChange={(e) => setEntrada({ ...entrada, precio_compra: e.target.value })}
                required
              />
            </div>
            <div className="form-group mt-3">
              <label>Fecha</label>
              <input
                type="date"
                className="form-control"
                value={entrada.fecha}
                onChange={(e) => setEntrada({ ...entrada, fecha: e.target.value })}
              />
            </div>
            <button type="submit" className="btn btn-primary mt-4">Registrar Entrada</button>
          </form>
        </div>
        <Footer />
      </div>
    </div>
  );
};

export default EntradaInventario;

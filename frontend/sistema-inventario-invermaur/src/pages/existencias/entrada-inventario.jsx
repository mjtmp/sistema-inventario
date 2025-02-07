import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Sidebar from '../../components/Sidebar';
import Header from '../../layouts/Header';
import Footer from '../../layouts/Footer';
import 'bootstrap/dist/css/bootstrap.min.css';
import styles from './styles/entrada-inventario.module.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBox, faTruck, faCalendarAlt, faDollarSign, faClipboardList } from '@fortawesome/free-solid-svg-icons';

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
  const [ordenesCompraCompletadas, setOrdenesCompraCompletadas] = useState([]);
  const [selectedOrdenCompra, setSelectedOrdenCompra] = useState('');
  const [detallesEntrada, setDetallesEntrada] = useState([]);
  const [usuarioId, setUsuarioId] = useState(null);

  useEffect(() => {
    const userId = localStorage.getItem('usuario_id');
    setUsuarioId(userId);

    axios.get('http://localhost:8000/productos')
      .then(response => {
        setProductos(response.data.productos);
      })
      .catch(error => console.error('Error al obtener productos:', error));

    axios.get('http://localhost:8000/proveedores')
      .then(response => {
        setProveedores(response.data.proveedores);
      })
      .catch(error => console.error('Error al obtener proveedores:', error));

    axios.get('http://localhost:8000/ordenes_compra?estado=completada')
      .then(response => {
        setOrdenesCompraCompletadas(response.data.ordenes_compra);
      })
      .catch(error => console.error('Error al obtener órdenes de compra completadas:', error));
  }, []);

  const handleOrdenCompraChange = (e) => {
    const selectedOrdenCompraId = e.target.value;
    setSelectedOrdenCompra(selectedOrdenCompraId);

    const selectedOrdenCompra = ordenesCompraCompletadas.find(orden => orden.orden_compra_id == selectedOrdenCompraId);
    if (selectedOrdenCompra && selectedOrdenCompra.detalles.length > 0) {
      const detalles = selectedOrdenCompra.detalles.map(detalle => ({
        producto_id: detalle.producto_id,
        proveedor_id: selectedOrdenCompra.proveedor_id,
        cantidad: detalle.cantidad,
        precio_compra: detalle.precio_unitario,
        fecha: new Date().toISOString().split('T')[0]
      }));

      setDetallesEntrada(detalles);
    } else {
      setDetallesEntrada([]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!usuarioId) {
      alert('No se pudo obtener el ID del usuario. Por favor, inicia sesión de nuevo.');
      return;
    }

    try {
      if (selectedOrdenCompra) {
        // Registrar múltiples detalles desde la orden de compra
        for (const detalle of detallesEntrada) {
          const entradaData = {
            ...detalle,
            usuario_id: usuarioId
          };

          await axios.post('http://localhost:8000/entradas_inventario', entradaData);
        }
      } else {
        // Registrar un producto individualmente
        const entradaData = {
          ...entrada,
          usuario_id: usuarioId
        };

        await axios.post('http://localhost:8000/entradas_inventario', entradaData);
      }

      alert('Entrada(s) de inventario registrada(s) con éxito');
      setEntrada({
        producto_id: '',
        proveedor_id: '',
        cantidad: '',
        precio_compra: '',
        fecha: ''
      });
      setSelectedOrdenCompra('');
      setDetallesEntrada([]);
    } catch (error) {
      console.error('Error al registrar las entradas de inventario:', error.response?.data || error.message);
      alert('Error al registrar las entradas de inventario');
    }
  };

  const getProveedorNombre = (proveedorId) => {
    const proveedor = proveedores.find(proveedor => proveedor.proveedor_id === proveedorId);
    return proveedor ? proveedor.nombre : '';
  };

  return (
    <div className={styles.container}>
      <Sidebar />
      <div className={styles.mainContent}>
        <Header />
        <div className={`container mt-5 ${styles.card}`}>
          <h2 className={styles.title}>
            <FontAwesomeIcon icon={faClipboardList} className={styles.titleIcon} /> Registrar Entrada de Inventario
          </h2>
          <form onSubmit={handleSubmit} className={styles.formContainer}>
            <div className="form-group">
              <label className={styles.boldLabel}>
                <FontAwesomeIcon icon={faBox} className={styles.icon} /> Orden de Pedido Completada
              </label>
              <select
                className="form-control"
                value={selectedOrdenCompra}
                onChange={handleOrdenCompraChange}
              >
                <option value="">Selecciona una orden de pedido</option>
                {ordenesCompraCompletadas.map((orden) => (
                  <option key={orden.orden_compra_id} value={orden.orden_compra_id}>
                    {`ID: ${orden.orden_compra_id} - Proveedor: ${getProveedorNombre(orden.proveedor_id)}`}
                  </option>
                ))}
              </select>
            </div>
            {detallesEntrada.map((detalle, index) => (
              <div key={index} className="form-group mt-3">
                <label className={styles.boldLabel}>
                  <FontAwesomeIcon icon={faBox} className={styles.icon} /> Producto
                </label>
                <select
                  className="form-control"
                  value={detalle.producto_id}
                  readOnly
                >
                  {productos.map((producto) => (
                    <option key={producto.producto_id} value={producto.producto_id}>
                      {producto.nombre}
                    </option>
                  ))}
                </select>
                <label className={styles.boldLabel} style={{ marginTop: '1rem' }}>
                  <FontAwesomeIcon icon={faTruck} className={styles.icon} /> Proveedor
                </label>
                <select
                  className="form-control"
                  value={detalle.proveedor_id}
                  readOnly
                >
                  {proveedores.map((proveedor) => (
                    <option key={proveedor.proveedor_id} value={proveedor.proveedor_id}>
                      {proveedor.nombre}
                    </option>
                  ))}
                </select>
                <label className={styles.boldLabel} style={{ marginTop: '1rem' }}>
                  <FontAwesomeIcon icon={faClipboardList} className={styles.icon} /> Cantidad
                </label>
                <input
                  type="number"
                  className="form-control"
                  value={detalle.cantidad}
                  readOnly
                />
                <label className={styles.boldLabel} style={{ marginTop: '1rem' }}>
                  <FontAwesomeIcon icon={faDollarSign} className={styles.icon} /> Precio de Compra (Bs)
                </label>
                <input
                  type="number"
                  className="form-control"
                  value={detalle.precio_compra}
                  readOnly
                />
                <label className={styles.boldLabel} style={{ marginTop: '1rem' }}>
                  <FontAwesomeIcon icon={faCalendarAlt} className={styles.icon} /> Fecha
                </label>
                <input
                  type="date"
                  className="form-control"
                  value={detalle.fecha}
                  readOnly
                />
              </div>
            ))}
            {!selectedOrdenCompra && (
              <>
                <div className="form-group mt-3">
                  <label className={styles.boldLabel}>
                    <FontAwesomeIcon icon={faBox} className={styles.icon} /> Producto
                  </label>
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
                  <label className={styles.boldLabel}>
                    <FontAwesomeIcon icon={faTruck} className={styles.icon} /> Proveedor
                  </label>
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
                  <label className={styles.boldLabel}>
                    <FontAwesomeIcon icon={faClipboardList} className={styles.icon} /> Cantidad
                  </label>
                  <input
                    type="number"
                    className="form-control"
                    value={entrada.cantidad}
                    onChange={(e) => setEntrada({ ...entrada, cantidad: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group mt-3">
                  <label className={styles.boldLabel}>
                    <FontAwesomeIcon icon={faDollarSign} className={styles.icon} /> Precio de Compra (Bs)
                  </label>
                  <input
                    type="number"
                    className="form-control"
                    value={entrada.precio_compra}
                    onChange={(e) => setEntrada({ ...entrada, precio_compra: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group mt-3">
                  <label className={styles.boldLabel}>
                    <FontAwesomeIcon icon={faCalendarAlt} className={styles.icon} /> Fecha
                  </label>
                  <input
                    type="date"
                    className="form-control"
                    value={entrada.fecha}
                    onChange={(e) => setEntrada({ ...entrada, fecha: e.target.value })}
                  />
                </div>
              </>
            )}
            <button type="submit" className={`${styles.btnPrimary} btn mt-4`}>Registrar Entrada</button>
          </form>
        </div>
        <Footer />
      </div>
    </div>
  );
};

export default EntradaInventario;

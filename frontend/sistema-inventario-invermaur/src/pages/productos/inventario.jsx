import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import Sidebar from '../../components/Sidebar';
import Header from '../../layouts/Header';
import Footer from '../../layouts/Footer';
import styles from './styles/inventario.module.css';

const Inventario = () => {
  // Estados para los productos y filtros
  const [productos, setProductos] = useState([]);
  const [reportes, setReportes] = useState([]);
  const [fechaInicio, setFechaInicio] = useState('');
  const [fechaFin, setFechaFin] = useState('');
  const [productoFiltro, setProductoFiltro] = useState('');
  const fechaCreacion = new Date(productos.fecha_creacion);  // Asegúrate de que esto esté bien
  const fechaActualizacion = new Date(productos.fecha_actualizacion);

  console.log(fechaCreacion);  // Verifica en consola si la fecha es válida

  // Si las fechas son correctas, formatea las fechas para mostrarlas
  const formattedFechaCreacion = fechaCreacion.toLocaleDateString();
  const formattedFechaActualizacion = fechaActualizacion.toLocaleDateString();

  useEffect(() => {
    axios.get('http://localhost:8000/productos')
      .then(response => {
        console.log('Datos del backend:', response.data);
        // Acceder al array de productos dentro de la respuesta
        setProductos(Array.isArray(response.data.productos) ? response.data.productos : []);
      })
      .catch(error => {
        console.error('Error al cargar los productos:', error);
      });
  }, []);

  // Función para cargar reportes de inventario filtrados
  const cargarReportes = () => {
    axios.get('http://localhost:8000/reportes-inventario', {
      params: {
        fecha_inicio: fechaInicio,
        fecha_fin: fechaFin,
        producto_id: productoFiltro,
      },
    })
      .then(response => {
        setReportes(response.data);
      })
      .catch(error => {
        console.error('Error al cargar los reportes:', error);
      });
  };

  return (
    <div className={styles.container}>
      <Sidebar />
      <div className={styles.mainContent}>
        <Header />
        <div className="container mt-5">
          <h2 className={styles.title}>Inventario</h2>
          
          {/* Filtros de Reportes */}
          <div className="row mb-4">
            <div className="col-md-3">
              <label>Fecha Inicio</label>
              <input 
                type="date" 
                className="form-control" 
                value={fechaInicio} 
                onChange={(e) => setFechaInicio(e.target.value)} 
              />
            </div>
            <div className="col-md-3">
              <label>Fecha Fin</label>
              <input 
                type="date" 
                className="form-control" 
                value={fechaFin} 
                onChange={(e) => setFechaFin(e.target.value)} 
              />
            </div>
            <div className="col-md-3">
              <label>Producto</label>
              <select 
                className="form-control" 
                value={productoFiltro} 
                onChange={(e) => setProductoFiltro(e.target.value)}
              >
                <option value="">Todos</option>
                {productos && productos.map(producto => (
                  <option key={producto.producto_id} value={producto.producto_id}>
                    {producto.nombre}
                  </option>
                ))}
              </select>
            </div>
            <div className="col-md-3 d-flex align-items-end">
              <button onClick={cargarReportes} className="btn btn-primary">Filtrar</button>
            </div>
          </div>

          {/* Tabla de productos */}
          <h3>Lista de Productos</h3>
          <table className="table table-bordered mt-3">
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Descripción</th>
                <th>Precio</th>
                <th>IVA</th>
                <th>Stock</th>
                <th>Proveedor</th>
                <th>Código de Barras</th>
                <th>Fecha de Creación</th>
                <th>Fecha de Actualización</th>
              </tr>
            </thead>
            <tbody>
              {productos.map(producto => (
                <tr key={producto.producto_id}>
                  <td>{producto.nombre}</td>
                  <td>{producto.descripcion}</td>
                  <td>{producto.precio}</td>
                  <td>{producto.tiene_iva ? 'Sí' : 'No'}</td>
                  <td>{producto.stock}</td>
                  <td>{producto.proveedor_id}</td>
                  <td>{producto.codigo_barras}</td>
                  <td>{formattedFechaCreacion}</td>
                  <td>{formattedFechaActualizacion}</td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* Tabla de reportes de inventario */}
          <h3>Reportes de Inventario</h3>
          <table className="table table-bordered mt-3">
            <thead>
              <tr>
                <th>Fecha</th>
                <th>Producto</th>
                <th>Stock</th>
              </tr>
            </thead>
            <tbody>
              {reportes.map(reporte => (
                <tr key={reporte.reporte_id}>
                  <td>{reporte.fecha}</td>
                  <td>{reporte.producto ? reporte.producto.nombre : 'N/A'}</td>
                  <td>{reporte.stock}</td>
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

export default Inventario;


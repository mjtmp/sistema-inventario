import React, { useEffect, useState } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import Sidebar from '../../components/Sidebar';
import Header from '../../layouts/Header';
import Footer from '../../layouts/Footer';
import styles from './styles/anadir-producto.module.css';

const AñadirProducto = () => {
  // Estados para almacenar los valores de los campos
  const [nombre, setNombre] = useState('');
  const [descripcion, setDescripcion] = useState('');
  const [precio, setPrecio] = useState('');
  const [tieneIva, setTieneIva] = useState(false);
  const [stock, setStock] = useState('');
  const [proveedorId, setProveedorId] = useState('');
  const [codigoBarras, setCodigoBarras] = useState('');
  const [proveedores, setProveedores] = useState([]); // Inicializado como array vacío

  // Obtener proveedores al montar el componente
  useEffect(() => {
    const obtenerProveedores = async () => {
      try {
        const response = await axios.get('http://localhost:8000/proveedores');
        setProveedores(response.data.proveedores);
        console.log('Proveedores obtenidos:', response.data.proveedores);
      } catch (error) {
        console.error('Error al obtener los proveedores:', error);
        
        alert('No se pudieron cargar los proveedores. Intente nuevamente.');
      }
    };
    obtenerProveedores();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validación básica
    if (!nombre || !precio || !stock || !proveedorId) {
      alert('Por favor complete todos los campos requeridos');
      return;
    }

    try {
      // Envía los datos al backend
      await axios.post('http://localhost:8000/productos', {
        nombre,
        descripcion,
        precio: parseFloat(precio),
        tiene_iva: tieneIva,
        stock: parseInt(stock, 10),
        proveedor_id: parseInt(proveedorId, 10),
        codigo_barras: codigoBarras || null,
      });
      alert('Producto añadido exitosamente');
      // Limpiar el formulario después de añadir el producto
      setNombre('');
      setDescripcion('');
      setPrecio('');
      setTieneIva(false);
      setStock('');
      setProveedorId('');
      setCodigoBarras('');
    } catch (error) {
      console.error('Error al añadir el producto:', error);
      alert('Hubo un error al añadir el producto. Intente nuevamente.');
    }
  };

  return (
    <div className={styles.container}>
      <Sidebar />
      <div className={styles.mainContent}>
        <Header />
        <div className="container mt-5">
          <h2 className={styles.title}>Añadir Producto</h2>
          <form onSubmit={handleSubmit} className={styles.formContainer}>
            <div className="form-group">
              <label>Nombre del Producto</label>
              <input
                type="text"
                className="form-control"
                value={nombre}
                onChange={(e) => setNombre(e.target.value)}
                required
              />
            </div>
            <div className="form-group mt-3">
              <label>Descripción</label>
              <textarea
                className="form-control"
                value={descripcion}
                onChange={(e) => setDescripcion(e.target.value)}
              />
            </div>
            <div className="form-group mt-3">
              <label>Precio</label>
              <input
                type="number"
                className="form-control"
                value={precio}
                onChange={(e) => setPrecio(e.target.value)}
                required
              />
            </div>
            <div className="form-group mt-3">
              <label>¿Tiene IVA?</label>
              <input
                type="checkbox"
                className="form-check-input ml-2"
                checked={tieneIva}
                onChange={(e) => setTieneIva(e.target.checked)}
              />
            </div>
            <div className="form-group mt-3">
              <label>Stock</label>
              <input
                type="number"
                className="form-control"
                value={stock}
                onChange={(e) => setStock(e.target.value)}
                required
              />
            </div>
            <div className="form-group mt-3">
              <label>Proveedor</label>
              <select
                className="form-control"
                value={proveedorId}
                onChange={(e) => setProveedorId(e.target.value)}
                required
              >
                <option value="">Seleccionar Proveedor</option>
                {proveedores.map((proveedor) => (
                  <option key={proveedor.proveedor_id} value={proveedor.proveedor_id}>
                    {proveedor.nombre}
                  </option>
                ))}
              </select>
            </div>
            <div className="form-group mt-3">
              <label>Código de Barras (opcional)</label>
              <input
                type="text"
                className="form-control"
                value={codigoBarras}
                onChange={(e) => setCodigoBarras(e.target.value)}
              />
            </div>
            <button type="submit" className="btn btn-primary mt-4">
              Añadir Producto
            </button>
          </form>
        </div>
        <Footer />
      </div>
    </div>
  );
};

export default AñadirProducto;

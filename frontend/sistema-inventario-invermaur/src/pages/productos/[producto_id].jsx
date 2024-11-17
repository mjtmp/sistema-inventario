import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import Sidebar from '../../components/Sidebar';
import Header from '../../layouts/Header';
import Footer from '../../layouts/Footer';
import styles from './styles/editar-producto.module.css';
import { useRouter } from 'next/router';

const EditarProducto = () => {
  const router = useRouter();
  const { producto_id } = router.query;

  const [producto, setProducto] = useState({
    nombre: '',
    descripcion: '',
    precio: '',
    tiene_iva: false,
    stock: '',
    proveedor_id: '',
    codigo_barras: ''
  });
  

  useEffect(() => {
    if (producto_id) {
      axios.get(`http://localhost:8000/productos/${producto_id}`)
        .then(response => {
          const { nombre, descripcion, precio, tiene_iva, stock, proveedor_id, codigo_barras } = response.data;
          setProducto({
            nombre,
            descripcion,
            precio,
            tiene_iva,
            stock,
            proveedor_id,
            codigo_barras
          });
        })
        .catch(error => {
          console.error('Error al obtener el producto:', error);
        });
    }
  }, [producto_id]);  

  const handleSubmit = async (e) => {
    e.preventDefault();
  
    try {
      // Enviar los datos con nombres consistentes con el backend
      await axios.put(`http://localhost:8000/productos/${producto_id}`, {
        nombre: producto.nombre,
        descripcion: producto.descripcion,
        precio: parseFloat(producto.precio),
        tiene_iva: producto.tiene_iva,
        stock: parseInt(producto.stock),
        proveedor_id: parseInt(producto.proveedor_id),
        codigo_barras: producto.codigo_barras || null
      });
      alert('Producto actualizado con éxito');
      router.push('/productos/consultar-productos');
    } catch (error) {
      console.error('Error al actualizar el producto:', error.response?.data || error.message);
      alert('Hubo un error al actualizar el producto');
    }
  };
  
  return (
    <div className={styles.container}>
      <Sidebar />
      <div className={styles.mainContent}>
        <Header />
        <div className="container mt-5">
          <h2 className={styles.title}>Editar Producto</h2>
          <form onSubmit={handleSubmit} className={styles.formContainer}>
            <div className="form-group">
              <label>Nombre del Producto</label>
              <input
                type="text"
                className="form-control"
                value={producto.nombre}
                onChange={(e) => setProducto({ ...producto, nombre: e.target.value })}
                required
              />
            </div>
            <div className="form-group mt-3">
              <label>Descripción</label>
              <textarea
                className="form-control"
                value={producto.descripcion}
                onChange={(e) => setProducto({ ...producto, descripcion: e.target.value })}
              />
            </div>
            <div className="form-group mt-3">
              <label>Precio Bs</label>
              <input
                type="number"
                className="form-control"
                value={producto.precio}
                onChange={(e) => setProducto({ ...producto, precio: e.target.value })}
                required
              />
            </div>
            <div className="form-group mt-3">
              <label>Stock</label>
              <input
                type="number"
                className="form-control"
                value={producto.stock}
                onChange={(e) => setProducto({ ...producto, stock: e.target.value })}
                required
              />
            </div>
            <div className="form-group mt-3">
              <label>ID del Proveedor</label>
              <input
                type="number"
                className="form-control"
                value={producto.proveedorId}
                onChange={(e) => setProducto({ ...producto, proveedorId: e.target.value })}
                required
              />
            </div>
            <div className="form-group mt-3">
              <label>Código de Barras</label>
              <input
                type="text"
                className="form-control"
                value={producto.codigoBarras}
                onChange={(e) => setProducto({ ...producto, codigoBarras: e.target.value })}
              />
            </div>
            <button type="submit" className="btn btn-primary mt-4">Actualizar Producto</button>
          </form>
        </div>
        <Footer />
      </div>
    </div>
  );
};

export default EditarProducto;


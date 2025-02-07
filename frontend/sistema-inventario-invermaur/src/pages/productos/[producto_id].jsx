import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import Sidebar from '../../components/Sidebar';
import Header from '../../layouts/Header';
import Footer from '../../layouts/Footer';
import styles from './styles/editar-producto.module.css';
import { useRouter } from 'next/router';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBarcode, faBox, faListAlt, faMoneyBill, faEdit, faTags, faWarehouse } from '@fortawesome/free-solid-svg-icons';

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
    categoria_id: '', 
    codigo: '',
    codigo_barras: '',
    ubicacion: '',
    cantidad_minima: '',
    cantidad_maxima: ''
  });
  const [proveedores, setProveedores] = useState([]);
  const [categorias, setCategorias] = useState([]);
  const [usuarioId, setUsuarioId] = useState(null);  // Nuevo estado para el usuario_id

  useEffect(() => {
    const userId = localStorage.getItem('usuario_id'); // Obtener el usuario_id del almacenamiento local
    setUsuarioId(userId);

    if (producto_id) {
      axios.get(`http://localhost:8000/productos/${producto_id}`)
        .then(response => {
          const { nombre, descripcion, precio, tiene_iva, stock, proveedor_id, categoria_id, codigo, codigo_barras, ubicacion, cantidad_minima, cantidad_maxima } = response.data;
          setProducto({
            nombre,
            descripcion,
            precio,
            tiene_iva,
            stock,
            proveedor_id,
            categoria_id,
            codigo,
            codigo_barras,
            ubicacion,
            cantidad_minima,
            cantidad_maxima
          });
        })
        .catch(error => {
          console.error('Error al obtener el producto:', error);
        });
    }
  }, [producto_id]);

  useEffect(() => {
    const obtenerProveedores = async () => {
      try {
        const response = await axios.get('http://localhost:8000/proveedores');
        setProveedores(response.data.proveedores);
      } catch (error) {
        console.error('Error al obtener los proveedores:', error);
        alert('No se pudieron cargar los proveedores. Intente nuevamente.');
      }
    };

    const obtenerCategorias = async () => {
      try {
        const response = await axios.get('http://localhost:8000/categorias');
        setCategorias(response.data);
      } catch (error) {
        console.error('Error al obtener las categorías:', error);
        alert('No se pudieron cargar las categorías. Intente nuevamente.');
      }
    };

    obtenerProveedores();
    obtenerCategorias();
  }, []);

  const handleCodigoChange = (e) => {
    const value = e.target.value;
    if (value.length <= 8) {
      setProducto({ ...producto, codigo: value });
    } else {
      alert('El código del producto no puede exceder los 8 caracteres');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (producto.cantidad_minima && producto.stock < producto.cantidad_minima) {
      alert('El stock debe ser mayor o igual a la cantidad mínima');
      return;
    }

    if (producto.cantidad_maxima && producto.stock > producto.cantidad_maxima) {
      alert('El stock debe ser menor o igual a la cantidad máxima');
      return;
    }

    if (!usuarioId) {
      alert('No se pudo obtener el ID del usuario. Por favor, inicia sesión de nuevo.');
      return;
    }

    try {
      // Verificar si el código ya existe
      const response = await axios.get(`http://localhost:8000/productos/search?codigo=${producto.codigo}`);
      if (response.data.length > 0 && response.data[0].producto_id !== producto_id) {
        alert('El código del producto ya existe. Por favor, elige un código diferente.');
        return;
      }

      await axios.put(`http://localhost:8000/productos/${producto_id}`, {
        nombre: producto.nombre,
        descripcion: producto.descripcion,
        precio: parseFloat(producto.precio),
        tiene_iva: producto.tiene_iva,
        stock: parseInt(producto.stock, 10),
        proveedor_id: parseInt(producto.proveedor_id, 10),
        categoria_id: parseInt(producto.categoria_id, 10),
        codigo: producto.codigo,
        codigo_barras: producto.codigo_barras || null,
        ubicacion: producto.ubicacion,
        cantidad_minima: parseInt(producto.cantidad_minima, 10) || null,
        cantidad_maxima: parseInt(producto.cantidad_maxima, 10) || null,
        usuario_id: usuarioId  // Incluyendo el usuario_id en la solicitud
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
        <h2 className={styles.title}>
            <FontAwesomeIcon icon={faEdit} className={styles.titleIcon} />
            Editar Producto
          </h2>
          <form onSubmit={handleSubmit} className={styles.formContainer}>
            <div className="row">
              <div className="col-md-6 form-group mt-3">
                <label className={styles.boldLabel}>
                  <FontAwesomeIcon icon={faBox} className={styles.icon} /> Nombre del Producto
                </label>
                <input
                  type="text"
                  className="form-control"
                  value={producto.nombre}
                  onChange={(e) => setProducto({ ...producto, nombre: e.target.value })}
                  required
                />
              </div>
              <div className="col-md-6 form-group mt-3">
                <label className={styles.boldLabel}>
                  <FontAwesomeIcon icon={faWarehouse} className={styles.icon} /> Stock
                </label>
                <input
                  type="number"
                  className="form-control"
                  value={producto.stock}
                  onChange={(e) => setProducto({ ...producto, stock: e.target.value })}
                  required
                />
              </div>
            </div>
            <div className="form-group mt-3">
              <label className={styles.boldLabel}>
                <FontAwesomeIcon icon={faListAlt} className={styles.icon} /> Descripción
              </label>
              <textarea
                className="form-control"
                value={producto.descripcion}
                onChange={(e) => setProducto({ ...producto, descripcion: e.target.value })}
              />
            </div>
            <div className="row">
              <div className="col-md-6 form-group mt-3">
                <label className={styles.boldLabel}>
                  <FontAwesomeIcon icon={faMoneyBill} className={styles.icon} /> Precio Bs
                </label>
                <input
                  type="number"
                  className="form-control"
                  value={producto.precio}
                  onChange={(e) => setProducto({ ...producto, precio: e.target.value })}
                  required
                />
              </div>
              <div className="col-md-6 form-group mt-3">
                <label className={styles.boldLabel}>
                  <FontAwesomeIcon icon={faTags} className={styles.icon} /> ¿Tiene IVA?
                </label>
                <input
                  type="checkbox"
                  className="form-check-input ml-2"
                  checked={producto.tiene_iva}
                  onChange={(e) => setProducto({ ...producto, tiene_iva: e.target.checked })}
                />
              </div>
            </div>
            <div className="row">
              <div className="col-md-6 form-group mt-3">
                <label className={styles.boldLabel}>
                  <FontAwesomeIcon icon={faTags} className={styles.icon} /> Proveedor
                </label>
                <select
                  className="form-control"
                  value={producto.proveedor_id}
                  onChange={(e) => setProducto({ ...producto, proveedor_id: e.target.value })}
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
              <div className="col-md-6 form-group mt-3">
                <label className={styles.boldLabel}>
                  <FontAwesomeIcon icon={faListAlt} className={styles.icon} /> Categoría
                </label>
                <select
                  className="form-control"
                  value={producto.categoria_id}
                  onChange={(e) => setProducto({ ...producto, categoria_id: e.target.value })}
                  required
                >
                  <option value="">Seleccionar Categoría</option>
                  {categorias.map((categoria) => (
                    <option key={categoria.categoria_id} value={categoria.categoria_id}>
                      {categoria.nombre}
                    </option>
                  ))}
                </select>
              </div>
            </div>
            <div className="row">
              <div className="col-md-6 form-group mt-3">
                <label className={styles.boldLabel}>
                  <FontAwesomeIcon icon={faBarcode} className={styles.icon} /> Código del Producto
                </label>
                <input
                  type="text"
                  className="form-control"
                  value={producto.codigo}
                  onChange={handleCodigoChange}
                  maxLength={8}
                  required
                />
              </div>
              <div className="col-md-6 form-group mt-3">
                <label className={styles.boldLabel}>
                  <FontAwesomeIcon icon={faBarcode} className={styles.icon} /> Código de Barras (opcional)
                </label>
                <input
                  type="text"
                  className="form-control"
                  value={producto.codigo_barras}
                  onChange={(e) => setProducto({ ...producto, codigo_barras: e.target.value })}
                />
              </div>
            </div>
            <div className="row">
              <div className="col-md-6 form-group mt-3">
                <label className={styles.boldLabel}>
                  <FontAwesomeIcon icon={faWarehouse} className={styles.icon} /> Ubicación
                </label>
                <input
                  type="text"
                  className="form-control"
                  value={producto.ubicacion}
                  onChange={(e) => setProducto({ ...producto, ubicacion: e.target.value })}
                  placeholder="Ej. A-1-1"
                />
                <small className="form-text text-muted">
                  Formato de ubicación: Pasillo-Estante-Nivel (Ej. A-1-1)
                </small>
              </div>
              <div className="col-md-6 form-group mt-3">
                <label className={styles.boldLabel}>
                  <FontAwesomeIcon icon={faWarehouse} className={styles.icon} /> Cantidad Mínima
                </label>
                <input
                  type="number"
                  className="form-control"
                  value={producto.cantidad_minima}
                  onChange={(e) => setProducto({ ...producto, cantidad_minima: e.target.value })}
                />
              </div>
            </div>
            <div className="row">
              <div className="col-md-6 form-group mt-3">
                <label className={styles.boldLabel}>
                  <FontAwesomeIcon icon={faWarehouse} className={styles.icon} /> Cantidad Máxima
                </label>
                <input
                  type="number"
                  className="form-control"
                  value={producto.cantidad_maxima}
                  onChange={(e) => setProducto({ ...producto, cantidad_maxima: e.target.value })}
                />
              </div>
            </div>
            <button type="submit" className={`${styles.btnPrimary} btn mt-4`}>Actualizar Producto</button>
          </form>
        </div>
        <Footer />
      </div>
    </div>
  );
};

export default EditarProducto;

  

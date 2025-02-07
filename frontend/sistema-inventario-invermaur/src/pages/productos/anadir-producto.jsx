import React, { useEffect, useState } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import Sidebar from '../../components/Sidebar';
import Header from '../../layouts/Header';
import Footer from '../../layouts/Footer';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBarcode, faBox, faListAlt, faMoneyBill, faPlusCircle, faTags, faWarehouse } from '@fortawesome/free-solid-svg-icons';
import styles from './styles/anadir-producto.module.css';

const AnadirProducto = () => {
  const [nombre, setNombre] = useState('');
  const [descripcion, setDescripcion] = useState('');
  const [precio, setPrecio] = useState('');
  const [tieneIva, setTieneIva] = useState(false);
  const [stock, setStock] = useState('');
  const [proveedorId, setProveedorId] = useState('');
  const [categoriaId, setCategoriaId] = useState('');
  const [codigo, setCodigo] = useState('');
  const [codigoBarras, setCodigoBarras] = useState('');
  const [ubicacion, setUbicacion] = useState('');
  const [cantidadMinima, setCantidadMinima] = useState('');
  const [cantidadMaxima, setCantidadMaxima] = useState('');
  const [proveedores, setProveedores] = useState([]); 
  const [categorias, setCategorias] = useState([]); 
  const [usuarioId, setUsuarioId] = useState(null);  // Nuevo estado para el usuario_id

  useEffect(() => {
    const userId = localStorage.getItem('usuario_id'); // Obtener el usuario_id del almacenamiento local
    setUsuarioId(userId);

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
        setCategorias(response.data.categorias);
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
      setCodigo(value);
    } else {
      alert('El código del producto no puede exceder los 8 caracteres');
    }
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!nombre || !precio || !stock || !proveedorId || !categoriaId || !codigo) {
      alert('Por favor complete todos los campos requeridos');
      return;
    }

    if (cantidadMinima && stock < cantidadMinima) {
      alert('El stock debe ser mayor o igual a la cantidad mínima');
      return;
    }

    if (cantidadMaxima && stock > cantidadMaxima) {
      alert('El stock debe ser menor o igual a la cantidad máxima');
      return;
    }

    if (!usuarioId) {
      alert('No se pudo obtener el ID del usuario. Por favor, inicia sesión de nuevo.');
      return;
    }

    try {
      // Verificar si el código ya existe
      const response = await axios.get(`http://localhost:8000/productos/search?codigo=${codigo}`);
      if (response.data.length > 0) {
        alert('El código del producto ya existe. Por favor, elige un código diferente.');
        return;
      }

      await axios.post('http://localhost:8000/productos', {
        nombre,
        descripcion,
        precio: parseFloat(precio),
        tiene_iva: tieneIva,
        stock: parseInt(stock, 10),
        proveedor_id: parseInt(proveedorId, 10),
        categoria_id: parseInt(categoriaId, 10),
        codigo,
        codigo_barras: codigoBarras || null,
        ubicacion,
        cantidad_minima: parseInt(cantidadMinima, 10) || null,
        cantidad_maxima: parseInt(cantidadMaxima, 10) || null,
        usuario_id: usuarioId  // Incluyendo el usuario_id en la solicitud
      });
      alert('Producto añadido exitosamente');
      setNombre('');
      setDescripcion('');
      setPrecio('');
      setTieneIva(false);
      setStock('');
      setProveedorId('');
      setCategoriaId('');
      setCodigo('');
      setCodigoBarras('');
      setUbicacion('');
      setCantidadMinima('');
      setCantidadMaxima('');
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
          <h2 className={styles.title}>
            <FontAwesomeIcon icon={faPlusCircle} className={styles.titleIcon} />
            Añadir Producto
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
                  value={nombre}
                  onChange={(e) => setNombre(e.target.value)}
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
                  value={stock}
                  onChange={(e) => setStock(e.target.value)}
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
                value={descripcion}
                onChange={(e) => setDescripcion(e.target.value)}
              />
            </div>
            <div className="row">
              <div className="col-md-6 form-group mt-3">
                <label className={styles.boldLabel}>
                  <FontAwesomeIcon icon={faMoneyBill} className={styles.icon} /> Precio
                </label>
                <input
                  type="number"
                  className="form-control"
                  value={precio}
                  onChange={(e) => setPrecio(e.target.value)}
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
                  checked={tieneIva}
                  onChange={(e) => setTieneIva(e.target.checked)}
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
              <div className="col-md-6 form-group mt-3">
                <label className={styles.boldLabel}>
                  <FontAwesomeIcon icon={faListAlt} className={styles.icon} /> Categoría
                </label>
                <select
                  className="form-control"
                  value={categoriaId}
                  onChange={(e) => setCategoriaId(e.target.value)}
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
                  value={codigo}
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
                  value={codigoBarras}
                  onChange={(e) => setCodigoBarras(e.target.value)}
                  maxLength={13}
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
                  value={ubicacion}
                  onChange={(e) => setUbicacion(e.target.value)}
                  placeholder="Ej. A-1-1"
                />
                <smal className="form-text text-muted">
                  Formato de ubicación: Pasillo - Estante - Nivel (Ej. A-1-1)
                </smal>
              </div>
              <div className="col-md-6 form-group mt-3">
                <label className={styles.boldLabel}>
                  <FontAwesomeIcon icon={faWarehouse} className={styles.icon} /> Cantidad Mínima
                </label>
                <input
                  type="number"
                  className="form-control"
                  value={cantidadMinima}
                  onChange={(e) => setCantidadMinima(e.target.value)}
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
                  value={cantidadMaxima}
                  onChange={(e) => setCantidadMaxima(e.target.value)}
                />
              </div>
            </div>
            <button type="submit" className={`${styles.btnPrimary} btn mt-4`}>
              Añadir Producto
            </button>
          </form>
        </div>
        <Footer />
      </div>
    </div>
  );
};

export default AnadirProducto;


import React, { useState, useEffect } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import Sidebar from "../../components/Sidebar";
import Header from "../../layouts/Header";
import Footer from "../../layouts/Footer";
import styles from "./styles/consultar-productos.module.css";
import Link from "next/link";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch, faEdit, faTrashAlt } from '@fortawesome/free-solid-svg-icons';
import Swal from 'sweetalert2';
import withReactContent from 'sweetalert2-react-content';

const MySwal = withReactContent(Swal);

const ConsultarProductos = () => {
  const [productos, setProductos] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [page, setPage] = useState(1);
  const [limit, setLimit] = useState(10);
  const [totalProductos, setTotalProductos] = useState(0);

  useEffect(() => {
    const fetchProductos = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/productos?skip=${(page - 1) * limit}&limit=${limit}`);
        setProductos(response.data.productos);
        setTotalProductos(response.data.total);
      } catch (error) {
        console.error("Error al cargar los productos:", error);
      }
    };
    fetchProductos();
  }, [page, limit]);

  // Filtro por nombre o categoría
  /*const filteredProductos = productos.filter(
    (producto) =>
      producto.nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (producto.categoria && producto.categoria.nombre.toLowerCase().includes(searchTerm.toLowerCase()))
  );*/
  
  // Filtro por nombre, categoría o código
  const filteredProductos = productos.filter(
    (producto) =>
      producto.nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (producto.categoria && producto.categoria.nombre.toLowerCase().includes(searchTerm.toLowerCase())) ||
      (producto.codigo && producto.codigo.toLowerCase().includes(searchTerm.toLowerCase())) // Añadir búsqueda por código
  );

  const handleEditProduct = async (producto_id) => {
    const result = await MySwal.fire({
      title: '¿Estás seguro?',
      text: '¿Deseas editar este producto?',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Sí, editar',
      cancelButtonText: 'Cancelar',
      customClass: {
        popup: 'my-popup-class',
        title: 'my-title-class',
        icon: 'my-icon-class',
        confirmButton: 'my-confirm-button-class',
        cancelButton: 'my-cancel-button-class'
      }
    });

    if (result.isConfirmed) {
      window.location.href = `/productos/${producto_id}`;
    }
  };

  const handleDeleteProduct = async (producto_id) => {
    const result = await MySwal.fire({
      title: '¿Estás seguro?',
      text: '¿Deseas eliminar este producto?',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#d33',
      cancelButtonColor: '#3085d6',
      confirmButtonText: 'Sí, eliminar',
      cancelButtonText: 'Cancelar',
      customClass: {
        popup: 'my-popup-class',
        title: 'my-title-class',
        icon: 'my-icon-class',
        confirmButton: 'my-confirm-button-class',
                cancelButton: 'my-cancel-button-class'
      }
    });

    if (result.isConfirmed) {
      try {
        await axios.delete(`http://localhost:8000/productos/${producto_id}`);
        setProductos(productos.filter((producto) => producto.producto_id !== producto_id));
        MySwal.fire({
          title: 'Eliminado',
          text: 'El producto ha sido eliminado correctamente.',
          icon: 'success',
          confirmButtonColor: '#3085d6',
          customClass: {
            popup: 'my-popup-class',
            title: 'my-title-class',
            icon: 'my-icon-class',
            confirmButton: 'my-confirm-button-class'
          }
        });
      } catch (error) {
        console.error('Error al eliminar el producto:', error);
        MySwal.fire({
          icon: 'error',
          title: 'Error',
          text: 'Hubo un error al eliminar el producto.',
          confirmButtonColor: '#d33',
          customClass: {
            popup: 'my-popup-class',
            title: 'my-title-class',
            icon: 'my-icon-class',
            confirmButton: 'my-confirm-button-class'
          }
        });
      }
    }
  };


  const totalPages = Math.ceil(totalProductos / limit);

  const handleNextPage = () => {
    if (page < totalPages) {
      setPage(page + 1);
    }
  };

  const handlePreviousPage = () => {
    if (page > 1) {
      setPage(page - 1);
    }
  };

  return (
    <div className={styles.container}>
      <Sidebar />
      <div className={styles.mainContent}>
        <Header />
        <div className="container mt-5">
          <h2 className={`${styles.title} text-center`}>Consultar Productos</h2>

          {/* Barra de búsqueda */}
          <div className={`${styles.searchContainer} d-flex justify-content-center`}>
            <div className="input-group mb-4" style={{ maxWidth: '600px' }}>
              <span className="input-group-text bg-primary text-white">
                <FontAwesomeIcon icon={faSearch} />
              </span>
              <input
                type="text"
                className={`form-control ${styles.searchInput}`}
                placeholder="Buscar por nombre, categoría o código..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>

          {/* Tabla de productos */}
          <div className={styles.tableContainer}>
            <table className={`${styles.table} table`}>
              <thead>
                <tr>
                  <th className="text-center">Código</th>
                  <th className="text-center">Nombre</th>
                  <th className="text-center">Descripción</th>
                  <th className="text-center">Precio Bs</th>
                  <th className="text-center">Stock</th>
                  <th className="text-center">Categoría</th>
                  <th className="text-center">Acciones</th>
                </tr>
              </thead>
              <tbody>
                {filteredProductos.map((producto) => (
                  <tr key={producto.producto_id}>
                    <td className="text-center">{producto.codigo}</td>
                    <td className="text-center">{producto.nombre}</td>
                    <td className="text-center">{producto.descripcion}</td>
                    <td className="text-center">{producto.precio}</td>
                    <td className="text-center">{producto.stock}</td>
                    <td className="text-center">{producto.categoria?.nombre || "Sin Categoría"}</td>
                    <td className="text-center">
                      <div className="d-flex justify-content-center gap-2">
                          <button 
                            className="btn btn-warning btn-sm"
                            onClick={() => handleEditProduct(producto.producto_id)}
                          >
                            <FontAwesomeIcon icon={faEdit} className="me-1" /> Editar
                          </button>
                        <button
                          className="btn btn-danger btn-sm"
                          onClick={() => handleDeleteProduct(producto.producto_id)}
                        >
                          <FontAwesomeIcon icon={faTrashAlt} className="me-1" /> Eliminar
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Paginación */}
          <nav>
            <ul className="pagination justify-content-center">
              <li className={`page-item ${page === 1 ? "disabled" : ""}`}>
                <button className="page-link" onClick={handlePreviousPage}>
                  Anterior
                </button>
              </li>
              <li className="page-item">
                <span className="page-link">
                  Página {page} de {totalPages}
                </span>
              </li>
              <li className={`page-item ${page === totalPages ? "disabled" : ""}`}>
                <button className="page-link" onClick={handleNextPage}>
                  Siguiente
                </button>
              </li>
            </ul>
          </nav>
        </div>
        <Footer />
      </div>
    </div>
  );
};

export default ConsultarProductos;


import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import Sidebar from '../../components/Sidebar';
import Header from '../../layouts/Header';
import Footer from '../../layouts/Footer';
import styles from './styles/consultar-categorias.module.css';
import Link from 'next/link';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch, faEdit, faTrashAlt } from '@fortawesome/free-solid-svg-icons';
import Swal from 'sweetalert2';
import withReactContent from 'sweetalert2-react-content';

const MySwal = withReactContent(Swal);

const ConsultarCategorias = () => {
  const [categorias, setCategorias] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [page, setPage] = useState(1);
  const [limit, setLimit] = useState(10);
  const [totalCategorias, setTotalCategorias] = useState(0);

  useEffect(() => {
    const fetchCategorias = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/categorias?skip=${(page - 1) * limit}&limit=${limit}`);
        setCategorias(response.data.categorias);
        setTotalCategorias(response.data.total);
      } catch (error) {
        console.error('Error al cargar las categorías:', error);
      }
    };
    fetchCategorias();
  }, [page, limit]);

  const filteredCategorias = categorias.filter(categoria =>
    categoria.nombre.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleEditCategory = async (categoria_id) => {
    const result = await MySwal.fire({
      title: '¿Estás seguro?',
      text: '¿Deseas editar esta categoría?',
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
      window.location.href = `/categorias/${categoria_id}`;
    }
  };

  const handleDeleteCategory = async (categoria_id) => {
    const result = await MySwal.fire({
      title: '¿Estás seguro?',
      text: '¿Deseas eliminar esta categoría?',
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
        await axios.delete(`http://localhost:8000/categorias/${categoria_id}`);
        setCategorias(categorias.filter(categoria => categoria.categoria_id !== categoria_id));
        MySwal.fire({
          title: 'Eliminado',
          text: 'La categoría ha sido eliminada correctamente.',
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
        console.error('Error al eliminar la categoría:', error);
        MySwal.fire({
          icon: 'error',
          title: 'Error',
          text: 'Hubo un error al eliminar la categoría.',
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

  const totalPages = Math.ceil(totalCategorias / limit);

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
          <h2 className={`${styles.title} text-center`}>Consultar Categorías</h2>

          {/* Barra de búsqueda */}
          <div className={`${styles.searchContainer} d-flex justify-content-center`}>
            <div className="input-group mb-4" style={{ maxWidth: '600px' }}>
              <span className="input-group-text bg-primary text-white">
                <FontAwesomeIcon icon={faSearch} />
              </span>
              <input
                type="text"
                className={`form-control ${styles.searchInput}`}
                placeholder="Buscar categoría por nombre..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>

          {/* Tabla de categorías */}
          <div className={styles.tableContainer}>
            <table className={`${styles.table} table`}>
              <thead>
                <tr>
                  <th className="text-center">Nombre</th>
                  <th className="text-center">Acciones</th>
                </tr>
              </thead>
              <tbody>
                {filteredCategorias.map((categoria) => (
                  <tr key={categoria.categoria_id}>
                    <td className="text-center">{categoria.nombre}</td>
                    <td className="text-center">
                      <div className="d-flex justify-content-center gap-2">
                        <button className="btn btn-warning btn-sm" onClick={() => handleEditCategory(categoria.categoria_id)}>
                          <FontAwesomeIcon icon={faEdit} className="me-1" /> Editar
                        </button>
                        <button
                          className="btn btn-danger btn-sm"
                          onClick={() => handleDeleteCategory(categoria.categoria_id)}
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
              <li className={`page-item ${page === 1 ? 'disabled' : ''}`}>
                <button className="page-link" onClick={handlePreviousPage}>Anterior</button>
              </li>
              <li className="page-item">
                <span className="page-link">
                  Página {page} de {totalPages}
                </span>
              </li>
              <li className={`page-item ${page === totalPages ? 'disabled' : ''}`}>
                <button className="page-link" onClick={handleNextPage}>Siguiente</button>
              </li>
            </ul>
          </nav>
        </div>
        <Footer />
      </div>
    </div>
  );
};

export default ConsultarCategorias;


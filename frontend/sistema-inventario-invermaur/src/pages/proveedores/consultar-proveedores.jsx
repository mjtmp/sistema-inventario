import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import Sidebar from '../../components/Sidebar';
import Header from '../../layouts/Header';
import Footer from '../../layouts/Footer';
import styles from './styles/consultar-proveedores.module.css';
import Link from 'next/link';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch, faEdit, faTrashAlt } from '@fortawesome/free-solid-svg-icons';
import Swal from 'sweetalert2';
import withReactContent from 'sweetalert2-react-content';

const MySwal = withReactContent(Swal);

const ConsultarProveedores = () => {
  const [proveedores, setProveedores] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [page, setPage] = useState(1);
  const [limit, setLimit] = useState(10);
  const [totalProveedores, setTotalProveedores] = useState(0);

  useEffect(() => {
    const fetchProveedores = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/proveedores?page=${page}&limit=${limit}`);
        setProveedores(response.data.proveedores);
        setTotalProveedores(response.data.total);
      } catch (error) {
        console.error('Error al cargar los proveedores:', error);
      }
    };
    fetchProveedores();
  }, [page, limit]);

  const filteredProveedores = proveedores
    ? proveedores.filter(proveedor =>
        proveedor.nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
        proveedor.rif.toLowerCase().includes(searchTerm.toLowerCase())
      )
    : [];

  const handleEditProveedor = async (proveedor_id) => {
    const result = await MySwal.fire({
      title: '¿Estás seguro?',
      text: '¿Deseas editar este proveedor?',
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
      window.location.href = `/proveedores/${proveedor_id}`;
    }
  };

  const handleDeleteProveedor = async (proveedor_id) => {
    const result = await MySwal.fire({
      title: '¿Estás seguro?',
      text: '¿Deseas eliminar este proveedor?',
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
        await axios.delete(`http://localhost:8000/proveedores/${proveedor_id}`);
        setProveedores(proveedores.filter((proveedor) => proveedor.proveedor_id !== proveedor_id));
        MySwal.fire({
          title: 'Eliminado',
          text: 'El proveedor ha sido eliminado correctamente.',
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
        console.error('Error al eliminar el proveedor:', error);
        MySwal.fire({
          icon: 'error',
          title: 'Error',
          text: 'Hubo un error al eliminar el proveedor.',
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

  const totalPages = Math.ceil(totalProveedores / limit);

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
          <h2 className={`${styles.title} text-center`}>Consultar Proveedores</h2>

          {/* Barra de búsqueda */}
          <div className={`${styles.searchContainer} d-flex justify-content-center`}>
            <div className="input-group mb-4" style={{ maxWidth: '600px' }}>
              <span className="input-group-text bg-primary text-white">
                <FontAwesomeIcon icon={faSearch} />
              </span>
              <input
                type="text"
                className={`form-control ${styles.searchInput}`}
                placeholder="Buscar proveedor por nombre o RIF..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>

          <div className={styles.tableContainer}>
            <table className={`${styles.table} table`}>
              <thead>
                <tr>
                  <th className="text-center">Nombre</th>
                  <th className="text-center">Email</th>
                  <th className="text-center">Teléfono</th>
                  <th className="text-center">Dirección</th>
                  <th className="text-center">RIF</th>
                  <th className="text-center">Acciones</th>
                </tr>
              </thead>
              <tbody>
                {filteredProveedores.map((proveedor) => (
                  <tr key={proveedor.proveedor_id}>
                    <td className="text-center">{proveedor.nombre}</td>
                    <td className="text-center">{proveedor.email}</td>
                    <td className="text-center">{proveedor.telefono}</td>
                    <td className={`${styles.direccion} text-center`}>{proveedor.direccion}</td>
                    <td className="text-center">{proveedor.rif}</td>
                    <td className="text-center">
                      <div className="d-flex justify-content-center gap-2">
                        <button
                          className="btn btn-warning btn-sm"
                          onClick={() => handleEditProveedor(proveedor.proveedor_id)}
                        >
                          <FontAwesomeIcon icon={faEdit} className="me-1" /> Editar
                        </button>
                        <button
                          className="btn btn-danger btn-sm"
                          onClick={() => handleDeleteProveedor(proveedor.proveedor_id)}
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
          <nav className={styles.paginationNav}>
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

export default ConsultarProveedores;




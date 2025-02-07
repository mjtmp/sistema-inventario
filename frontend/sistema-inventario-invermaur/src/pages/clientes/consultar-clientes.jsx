import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import Sidebar from '../../components/Sidebar';
import Header from '../../layouts/Header';
import Footer from '../../layouts/Footer';
import styles from './styles/consultar-clientes.module.css';
import Link from 'next/link';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch, faEdit, faTrashAlt } from '@fortawesome/free-solid-svg-icons';
import Swal from 'sweetalert2';
import withReactContent from 'sweetalert2-react-content';

const MySwal = withReactContent(Swal);

const ConsultarClientes = () => {
  const [clientes, setClientes] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [page, setPage] = useState(1);
  const [limit, setLimit] = useState(10);
  const [totalClientes, setTotalClientes] = useState(0);

  useEffect(() => {
    const fetchClientes = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/clientes?page=${page}&limit=${limit}`);
        setClientes(response.data.clientes);
        setTotalClientes(response.data.total);
      } catch (error) {
        console.error('Error al cargar los clientes:', error);
      }
    };
    fetchClientes();
  }, [page, limit]);

  const filteredClientes = clientes
    ? clientes.filter(cliente =>
        cliente.nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
        cliente.numero_documento.toLowerCase().includes(searchTerm.toLowerCase())
      )
    : [];

  const handleEditClient = async (cliente_id) => {
    const result = await MySwal.fire({
      title: '¿Estás seguro?',
      text: '¿Deseas editar este cliente?',
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
      window.location.href = `/clientes/${cliente_id}`;
    }
  };

  const handleDeleteClient = async (cliente_id) => {
    const result = await MySwal.fire({
      title: '¿Estás seguro?',
      text: '¿Deseas eliminar este cliente?',
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
        await axios.delete(`http://localhost:8000/clientes/${cliente_id}`);
        setClientes(clientes.filter((cliente) => cliente.cliente_id !== cliente_id));
        MySwal.fire({
          title: 'Eliminado',
          text: 'El cliente ha sido eliminado correctamente.',
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
        console.error('Error al eliminar el cliente:', error);
        MySwal.fire({
          icon: 'error',
          title: 'Error',
          text: 'Hubo un error al eliminar el cliente.',
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

  const totalPages = Math.ceil(totalClientes / limit);

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
          <h2 className={`${styles.title} text-center`}>Consultar Clientes</h2>

          {/* Barra de búsqueda */}
          <div className={`${styles.searchContainer} d-flex justify-content-center`}>
            <div className="input-group mb-4" style={{ maxWidth: '600px' }}>
              <span className="input-group-text bg-primary text-white">
                <FontAwesomeIcon icon={faSearch} />
              </span>
              <input
                type="text"
                className={`form-control ${styles.searchInput}`}
                placeholder="Buscar cliente por nombre o número de documento..."
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
                  <th className="text-center">Documento</th>
                  <th className="text-center">Acciones</th>
                </tr>
              </thead>
              <tbody>
                {filteredClientes.map((cliente) => (
                  <tr key={cliente.cliente_id}>
                    <td className="text-center">{cliente.nombre}</td>
                    <td className="text-center">{cliente.email}</td>
                    <td className="text-center">{cliente.telefono}</td>
                    <td className={`${styles.direccion} text-center`}>{cliente.direccion}</td>
                    <td className="text-center">
                      {cliente.tipo_documento} - {cliente.numero_documento}
                    </td>
                    <td className="text-center">
                      <div className="d-flex justify-content-center gap-2">
                        <button
                          className="btn btn-warning btn-sm"
                          onClick={() => handleEditClient(cliente.cliente_id)}
                        >
                          <FontAwesomeIcon icon={faEdit} className="me-1" /> Editar
                        </button>
                        <button
                          className="btn btn-danger btn-sm"
                          onClick={() => handleDeleteClient(cliente.cliente_id)}
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

export default ConsultarClientes;

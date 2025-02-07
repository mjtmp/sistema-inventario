import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Sidebar from '../../components/Sidebar';
import Header from '../../layouts/Header';
import Footer from '../../layouts/Footer';
import 'bootstrap/dist/css/bootstrap.min.css';
import styles from './styles/listar-entradas.module.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch } from '@fortawesome/free-solid-svg-icons';

const ListarEntradas = () => {
  const [entradas, setEntradas] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [page, setPage] = useState(1);
  const [limit, setLimit] = useState(10);
  const [totalEntradas, setTotalEntradas] = useState(0);

  useEffect(() => {
    fetchEntradas();
  }, [page, limit]);

  const fetchEntradas = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/entradas_inventario?skip=${(page - 1) * limit}&limit=${limit}`);
      setEntradas(response.data.entradas);  // Accede a las entradas dentro de la respuesta
      setTotalEntradas(response.data.total);  // Accede al total de entradas
    } catch (error) {
      console.error('Error al obtener las entradas:', error);
    }
  };

  const filteredEntradas = entradas.filter(
    entrada =>
      (entrada.producto_nombre && entrada.producto_nombre.toLowerCase().includes(searchTerm.toLowerCase())) ||
      (entrada.proveedor_nombre && entrada.proveedor_nombre.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  const totalPages = Math.ceil(totalEntradas / limit);

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
          <h2 className={styles.title}>Listado de Entradas de Inventario</h2>

          <div className={`${styles.searchContainer} d-flex justify-content-center`}>
            <div className="input-group mb-4" style={{ maxWidth: '600px' }}>
              <span className="input-group-text bg-primary text-white">
                <FontAwesomeIcon icon={faSearch} />
              </span>
              <input
                type="text"
                className={`form-control ${styles.searchInput}`}
                placeholder="Buscar por producto o proveedor..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>

          <table className={`table table-striped table-hover mt-4 ${styles.table}`}>
            <thead className="thead-dark">
              <tr>
                <th>ID</th>
                <th>Producto</th>
                <th>Proveedor</th>
                <th>Cantidad</th>
                <th>Precio de Compra (Bs)</th>
                <th>Fecha</th>
              </tr>
            </thead>
            <tbody>
              {filteredEntradas.length > 0 ? (
                filteredEntradas.map((entrada) => (
                  <tr key={entrada.entrada_id}>
                    <td>{entrada.entrada_id}</td>
                    <td>{entrada.producto_nombre || 'No disponible'}</td>
                    <td>{entrada.proveedor_nombre || 'No disponible'}</td>
                    <td>{entrada.cantidad}</td>
                    <td>{entrada.precio_compra}</td>
                    <td>{new Date(entrada.fecha).toLocaleDateString()}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="6">No se encontraron resultados</td>
                </tr>
              )}
            </tbody>
          </table>

          <div className={styles.pagination}>
            <button
              className={`${styles.pageButton} btn btn-primary`}
              disabled={page === 1}
              onClick={handlePreviousPage}
            >
              Anterior
            </button>
            <span className={styles.pageInfo}>
              Página {page} de {totalPages}
            </span>
            <button
              className={`${styles.pageButton} btn btn-primary`}
              disabled={page === totalPages}
              onClick={handleNextPage}
            >
              Siguiente
            </button>
          </div>
        </div>
        <Footer />
      </div>
    </div>
  );
};

export default ListarEntradas;


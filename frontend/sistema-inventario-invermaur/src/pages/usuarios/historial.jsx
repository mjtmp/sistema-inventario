import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Sidebar from '../../components/Sidebar';
import Header from '../../layouts/Header';
import Footer from '../../layouts/Footer';
import 'bootstrap/dist/css/bootstrap.min.css';
import styles from './styles/historial.module.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch } from '@fortawesome/free-solid-svg-icons';

const Historial = () => {
    const [historial, setHistorial] = useState([]);
    const [usuarios, setUsuarios] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [page, setPage] = useState(1);  // Nuevo estado para la página actual
    const [limit, setLimit] = useState(10);  // Nuevo estado para el número de elementos por página
    const [totalHistorial, setTotalHistorial] = useState(0);  // Nuevo estado para el total de elementos

    useEffect(() => {
        fetchHistorial();
        fetchUsuarios();
    }, [page, limit]);

    const fetchHistorial = async () => {
        try {
            const response = await axios.get(`http://localhost:8000/historial?skip=${(page - 1) * limit}&limit=${limit}`);
            if (response.data) {
                const historialData = response.data.historial || [];
                const totalData = response.data.total || historialData.length;
                setHistorial(historialData);
                setTotalHistorial(totalData);
            } else {
                setHistorial([]);
                setTotalHistorial(0);
            }
        } catch (error) {
            console.error('Error al obtener el historial:', error);
            setHistorial([]);
            setTotalHistorial(0);
        }
    };

    const fetchUsuarios = async () => {
        try {
            const response = await axios.get('http://localhost:8000/usuarios');
            setUsuarios(response.data);
        } catch (error) {
            console.error('Error al obtener los usuarios:', error);
        }
    };

    const getUsuarioNombre = (usuario_id) => {
        const usuario = usuarios.find((user) => user.usuario_id === usuario_id);
        return usuario ? usuario.nombre : 'Desconocido';
    };

    const filteredHistorial = (historial || []).filter(
        (entrada) =>
            entrada.accion.toLowerCase().includes(searchTerm.toLowerCase()) ||
            entrada.detalles.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const totalPages = Math.ceil(totalHistorial / limit);

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
                    <h2 className={styles.title}>Historial de Acciones</h2>

                    {/* Barra de búsqueda */}
                    <div className={`${styles.searchContainer} d-flex justify-content-center`}>
                        <div className="input-group mb-4" style={{ maxWidth: '600px' }}>
                            <span className="input-group-text bg-primary text-white">
                                <FontAwesomeIcon icon={faSearch} />
                            </span>
                            <input
                                type="text"
                                className={`form-control ${styles.searchInput}`}
                                placeholder="Buscar en el historial..."
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                            />
                        </div>
                    </div>

                    <div className={styles.tableContainer}>
                        <table className={`${styles.table} table`}>
                            <thead>
                                <tr>
                                    <th>Fecha</th>
                                    <th>Usuario</th>
                                    <th>Acción</th>
                                    <th>Detalles</th>
                                </tr>
                            </thead>
                            <tbody>
                                {filteredHistorial.map((entrada) => (
                                    <tr key={entrada.historial_id}>
                                        <td>{new Date(entrada.fecha).toLocaleDateString()}</td> {/* Solo fecha */}
                                        <td>{getUsuarioNombre(entrada.usuario_id)}</td> {/* Nombre del usuario */}
                                        <td>{entrada.accion}</td>
                                        <td>{entrada.detalles}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>

                    {/* Paginación */}
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

export default Historial;

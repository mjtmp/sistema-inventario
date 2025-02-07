import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Sidebar from '../../components/Sidebar';
import Header from '../../layouts/Header';
import Footer from '../../layouts/Footer';
import "bootstrap/dist/css/bootstrap.min.css";
import styles from './styles/reporte-entrega.module.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch, faFilePdf } from '@fortawesome/free-solid-svg-icons';

const ReporteEntrega = () => {
    const [pedidos, setPedidos] = useState([]);
    const [searchTerm, setSearchTerm] = useState("");
    const [page, setPage] = useState(1);
    const [limit, setLimit] = useState(10);
    const [totalPedidos, setTotalPedidos] = useState(0);
    const [usuarioId, setUsuarioId] = useState(null);  // Nuevo estado para el usuario_id

    useEffect(() => {
        const fetchPedidos = async () => {
            try {
                const response = await axios.get(`http://localhost:8000/reportes_entrega/pedidos?skip=${(page - 1) * limit}&limit=${limit}`);
                if (response.data && response.data.pedidos) {
                    const pedidosConClientes = await Promise.all(response.data.pedidos.map(async (pedido) => {
                        const clienteResponse = await axios.get(`http://localhost:8000/clientes/${pedido.cliente_id}`);
                        return {
                            ...pedido,
                            cliente_nombre: clienteResponse.data.nombre
                        };
                    }));
                    setPedidos(pedidosConClientes);
                    setTotalPedidos(response.data.total || pedidosConClientes.length);
                } else {
                    console.error("Datos de pedidos no encontrados");
                }
            } catch (error) {
                console.error("Error al cargar los pedidos:", error);
            }
        };

        const userId = localStorage.getItem('usuario_id'); // Obtener el usuario_id del almacenamiento local
        setUsuarioId(userId);

        fetchPedidos();
    }, [page, limit]);

    const handleGenerateReport = async (pedidoId) => {
        if (!usuarioId) {
            alert('No se pudo obtener el ID del usuario. Por favor, inicia sesión de nuevo.');
            return;
        }

        try {
            const response = await axios.get(`http://localhost:8000/reportes_entrega/pedidos/${pedidoId}/generar-reporte`, {
                params: { usuario_id: usuarioId }, // Incluyendo el usuario_id en la solicitud
                responseType: 'blob'
            });
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `reporte_entrega_${pedidoId}.pdf`);
            document.body.appendChild(link);
            link.click();
            link.remove();
        } catch (error) {
            console.error('Error al generar el reporte:', error);
        }
    };

    const filteredPedidos = pedidos.filter(
        (pedido) =>
            (pedido.cliente_nombre && pedido.cliente_nombre.toLowerCase().includes(searchTerm.toLowerCase())) ||
            (pedido.estado && pedido.estado.toLowerCase().includes(searchTerm.toLowerCase()))
    );

    const totalPages = Math.ceil(totalPedidos / limit);

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
                    <h2 className={styles.title}>Reporte de Entrega</h2>

                    <div className={`${styles.searchContainer} d-flex justify-content-center`}>
                        <div className="input-group mb-4" style={{ maxWidth: '600px' }}>
                            <span className="input-group-text bg-primary text-white">
                                <FontAwesomeIcon icon={faSearch} />
                            </span>
                            <input
                                type="text"
                                className={`form-control ${styles.searchInput}`}
                                placeholder="Buscar por Cliente Nombre o Estado..."
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                            />
                        </div>
                    </div>

                    <div className={styles.tableContainer}>
                        <table className={`${styles.table} table table-striped`}>
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Fecha Pedido</th>
                                    <th>Cliente</th>
                                    <th>Estado</th>
                                    <th>Acciones</th>
                                </tr>
                            </thead>
                            <tbody>
                                {filteredPedidos.map((pedido) => (
                                    <tr key={pedido.pedido_id}>
                                        <td>{pedido.pedido_id}</td>
                                        <td>{pedido.fecha_pedido}</td>
                                        <td>{pedido.cliente_nombre}</td>
                                        <td>{pedido.estado}</td>
                                        <td>
                                            <button className="btn btn-danger btn-sm" onClick={() => handleGenerateReport(pedido.pedido_id)}>
                                                <FontAwesomeIcon icon={faFilePdf} /> Generar Reporte
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>

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

export default ReporteEntrega;


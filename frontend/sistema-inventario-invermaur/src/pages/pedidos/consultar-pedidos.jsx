import React, { useState, useEffect } from "react";
import axios from "axios";
import Sidebar from "../../components/Sidebar";
import Header from "../../layouts/Header";
import Footer from "../../layouts/Footer";
import styles from "./styles/consultar-pedidos.module.css";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch, faCheckCircle, faTimesCircle, faFilePdf } from '@fortawesome/free-solid-svg-icons';

const ConsultarPedidos = () => {
    const [pedidos, setPedidos] = useState([]);
    const [searchTerm, setSearchTerm] = useState("");
    const [page, setPage] = useState(1);
    const [limit, setLimit] = useState(10);
    const [totalPedidos, setTotalPedidos] = useState(0);
    const [usuarioId, setUsuarioId] = useState(null); // Nuevo estado para el usuario_id

    useEffect(() => {
        const userId = localStorage.getItem('usuario_id'); // Obtener el usuario_id del almacenamiento local
        setUsuarioId(userId);
    
        const fetchPedidos = async () => {
            try {
                const response = await axios.get(`http://localhost:8000/pedidos?skip=${(page - 1) * limit}&limit=${limit}`);
                if (response.data && response.data.pedidos) {
                    const pedidosConClientes = await Promise.all(response.data.pedidos.map(async (pedido) => {
                        const clienteResponse = await axios.get(`http://localhost:8000/clientes/${pedido.cliente_id}`);
                        return {
                            ...pedido,
                            cliente_nombre: clienteResponse.data.nombre,
                            numero_documento: clienteResponse.data.numero_documento // Incluir número de documento del cliente
                        };
                    }));
                    setPedidos(pedidosConClientes);
                    setTotalPedidos(response.data.total || pedidosConClientes.length);
                }
            } catch (error) {
                console.error("Error al cargar los pedidos:", error);
                alert("Error al cargar los pedidos");
            }
        };
        fetchPedidos();
    }, [page, limit]);
    

    const filteredPedidos = pedidos.filter(
        (pedido) =>
            (pedido.cliente_nombre && pedido.cliente_nombre.toLowerCase().includes(searchTerm.toLowerCase())) ||
            (pedido.estado && pedido.estado.toLowerCase().includes(searchTerm.toLowerCase())) ||
            (pedido.pedido_id && pedido.pedido_id.toString().includes(searchTerm)) ||  // Añadir búsqueda por ID de Pedido
            (pedido.numero_documento && pedido.numero_documento.toLowerCase().includes(searchTerm.toLowerCase())) // Añadir búsqueda por número de documento del cliente
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

    const handleCancelOrder = async (pedido_id) => {
        try {
            await axios.put(`http://localhost:8000/pedidos/${pedido_id}`, { estado: "cancelado", usuario_id: usuarioId });
            setPedidos(pedidos.map(pedido => pedido.pedido_id === pedido_id ? { ...pedido, estado: "cancelado" } : pedido));
            alert("Pedido cancelado exitosamente");
        } catch (error) {
            console.error("Error al cancelar el pedido:", error);
            alert("Error al cancelar el pedido");
        }
    };

    const handleCompleteOrder = async (pedido_id) => {
        try {
            await axios.put(`http://localhost:8000/pedidos/${pedido_id}`, { estado: "completado", usuario_id: usuarioId });
            setPedidos(pedidos.map(pedido => pedido.pedido_id === pedido_id ? { ...pedido, estado: "completado" } : pedido));
            alert("Pedido completado exitosamente");
        } catch (error) {
            console.error("Error al completar el pedido:", error.response ? error.response.data : error.message);
            alert("Error al completar el pedido");
        }
    };

    const handleGeneratePDF = async (pedido_id) => {
        try {
            const response = await axios.get(`http://localhost:8000/pedidos/${pedido_id}/generate_pdf`, { responseType: 'blob' });
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `pedido_${pedido_id}.pdf`);
            document.body.appendChild(link);
            link.click();
            link.parentNode.removeChild(link);
            alert("PDF generado exitosamente");
        } catch (error) {
            console.error("Error al generar el PDF:", error.response ? error.response.data : error.message);
            alert("Error al generar el PDF");
        }
    };

    return (
        <div className={styles.container}>
            <Sidebar />
            <div className={styles.mainContent}>
                <Header />
                <div className={styles.contentWrapper}>
                    <h2 className={styles.title}>Consultar Pedidos</h2>

                    <div className={`${styles.searchContainer} d-flex justify-content-center`}>
                        <div className="input-group mb-4" style={{ maxWidth: '600px' }}>
                            <span className="input-group-text bg-primary text-white">
                                <FontAwesomeIcon icon={faSearch} />
                            </span>
                            <input
                                type="text"
                                className={`form-control ${styles.searchInput}`}
                                placeholder="Buscar por Cliente, Estado o ID de Pedido..."
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                            />
                        </div>
                    </div>

                    <div className={styles.tableWrapper}>
                        <table className={`${styles.table} table`}>
                            <thead>
                                <tr>
                                    <th className="text-center">Pedido ID</th>
                                    <th className="text-center">Cliente</th>
                                    <th className="text-center">Fecha</th>
                                    <th className="text-center">Estado</th>
                                    <th className="text-center">Acciones</th>
                                </tr>
                            </thead>
                            <tbody>
                                {filteredPedidos.length > 0 ? (
                                    filteredPedidos.map((pedido) => (
                                        <tr key={pedido.pedido_id}>
                                            <td className="text-center">000{pedido.pedido_id}</td>
                                            <td className="text-center">{pedido.cliente_nombre}</td>
                                            <td className="text-center">{pedido.fecha_pedido}</td>
                                            <td className="text-center">{pedido.estado}</td>
                                            <td className="text-center">
                                                <div className="d-flex justify-content-center gap-2">
                                                    <button
                                                        className="btn btn-success btn-sm"
                                                        onClick={() => handleCompleteOrder(pedido.pedido_id)}
                                                        disabled={pedido.estado !== "pendiente"}
                                                    >
                                                        <FontAwesomeIcon icon={faCheckCircle} className="me-1" /> Completar
                                                    </button>
                                                    <button
                                                        className="btn btn-danger btn-sm"
                                                        onClick={() => handleCancelOrder(pedido.pedido_id)}
                                                        disabled={pedido.estado !== "pendiente"}
                                                    >
                                                        <FontAwesomeIcon icon={faTimesCircle} className="me-1" /> Cancelar
                                                    </button>
                                                    <button
                                                        className="btn btn-primary btn-sm"
                                                        onClick={() => handleGeneratePDF(pedido.pedido_id)}
                                                    >
                                                        <FontAwesomeIcon icon={faFilePdf} className="me-1" /> PDF
                                                    </button>
                                                </div>
                                            </td>
                                        </tr>
                                    ))
                                ) : (
                                    <tr>
                                        <td colSpan="5">No se encontraron resultados</td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>

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

export default ConsultarPedidos;


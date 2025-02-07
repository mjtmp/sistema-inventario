import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import Sidebar from '../../components/Sidebar';
import Header from '../../layouts/Header';
import Footer from '../../layouts/Footer';
import styles from './styles/consultar-ordenes-compra.module.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch, faFilePdf, faPlusCircle, faCheckCircle, faTimesCircle } from '@fortawesome/free-solid-svg-icons';
import { useRouter } from 'next/router';

const ConsultarOrdenesCompra = () => {
    const [ordenesCompra, setOrdenesCompra] = useState([]);
    const [proveedores, setProveedores] = useState({});
    const [searchTerm, setSearchTerm] = useState('');
    const [page, setPage] = useState(1);
    const [limit, setLimit] = useState(10);
    const [totalOrdenesCompra, setTotalOrdenesCompra] = useState(0);
    const [usuarioId, setUsuarioId] = useState(null); // Nuevo estado para el usuario_id
    const router = useRouter();

    useEffect(() => {
        const userId = localStorage.getItem('usuario_id'); // Obtener el usuario_id del almacenamiento local
        setUsuarioId(userId);

        const fetchOrdenesCompra = async () => {
            try {
                const response = await axios.get(`http://localhost:8000/ordenes_compra?skip=${(page - 1) * limit}&limit=${limit}`);
                setOrdenesCompra(response.data.ordenes_compra);
                setTotalOrdenesCompra(response.data.total);
            } catch (error) {
                console.error('Error al obtener órdenes de compra:', error);
            }
        };

        const fetchProveedores = async () => {
            try {
                const response = await axios.get('http://localhost:8000/proveedores');
                const proveedoresData = response.data.proveedores.reduce((acc, proveedor) => {
                    acc[proveedor.proveedor_id] = proveedor.nombre;
                    return acc;
                }, {});
                setProveedores(proveedoresData);
            } catch (error) {
                console.error('Error al obtener proveedores:', error);
            }
        };

        fetchOrdenesCompra();
        fetchProveedores();
    }, [page, limit]);

    const handleCancelOrder = async (ordenCompraId) => {
        try {
            await axios.put(`http://localhost:8000/ordenes_compra/${ordenCompraId}`, { estado: "cancelado", usuario_id: usuarioId });
            setOrdenesCompra(ordenesCompra.map(orden => orden.orden_compra_id === ordenCompraId ? { ...orden, estado: "cancelado" } : orden));
            alert("Orden de compra cancelada exitosamente");
        } catch (error) {
            console.error("Error al cancelar la orden de compra:", error);
            alert("Error al cancelar la orden de compra");
        }
    };
    
    const handleCompleteOrder = async (ordenCompraId) => {
        try {
            await axios.put(`http://localhost:8000/ordenes_compra/${ordenCompraId}`, { estado: "completado", usuario_id: usuarioId });
            setOrdenesCompra(ordenesCompra.map(orden => orden.orden_compra_id === ordenCompraId ? { ...orden, estado: "completado" } : orden));
            alert("Orden de compra completada exitosamente");
        } catch (error) {
            console.error("Error al completar la orden de compra:", error.response ? error.response.data : error.message);
            alert("Error al completar la orden de compra");
        }
    };
  
    /*const filteredOrdenesCompra = ordenesCompra
        ? ordenesCompra.filter(orden =>
            proveedores[orden.proveedor_id]?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            orden.estado.toLowerCase().includes(searchTerm.toLowerCase())
        )
        : [];
    */
    const filteredOrdenesCompra = ordenesCompra.filter(
        orden =>
            proveedores[orden.proveedor_id]?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            orden.estado.toLowerCase().includes(searchTerm.toLowerCase()) ||
            orden.orden_compra_id.toString().includes(searchTerm) // Añadir búsqueda por ID
    );
        

    const handleGenerarPDF = async (ordenCompraId) => {
        try {
            const response = await axios.get(`http://localhost:8000/ordenes_compra/generar-pdf/${ordenCompraId}`, { responseType: 'blob' });
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `orden_pedido_${ordenCompraId}.pdf`);
            document.body.appendChild(link);
            link.click();
        } catch (error) {
            console.error('Error al generar PDF:', error);
        }
    };

    const handleCrearOrdenCompra = () => {
        router.push('/existencias/crear-orden-compra'); 
    };

    const totalPages = Math.ceil(totalOrdenesCompra / limit);

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
                    <h2 className={`${styles.title} text-center`}>Consultar Órdenes de Solicitud de Pedido</h2>

                    {/* Barra de búsqueda */}
                    <div className={`${styles.searchContainer} d-flex justify-content-center`}>
                        <div className="input-group mb-4" style={{ maxWidth: '600px' }}>
                            <span className="input-group-text bg-primary text-white">
                                <FontAwesomeIcon icon={faSearch} />
                            </span>
                            <input
                                type="text"
                                className={`form-control ${styles.searchInput}`}
                                placeholder="Buscar por proveedor, estado o ID de pedido..."
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                            />
                            <button className={styles.btnPrimary} onClick={handleCrearOrdenCompra}>
                                <FontAwesomeIcon icon={faPlusCircle} /> Crear Orden
                            </button>
                        </div>
                    </div>

                    {/* Tabla de órdenes de compra */}
                    <div className={styles.tableContainer}>
                        <table className={`${styles.table} table`}>
                            <thead>
                                <tr>
                                    <th className="text-center">ID</th>
                                    <th className="text-center">Proveedor</th>
                                    <th className="text-center">Fecha</th>
                                    <th className="text-center">Estado</th>
                                    <th className="text-center">Acciones</th>
                                </tr>
                            </thead>
                            <tbody>
                                {filteredOrdenesCompra.map(orden => (
                                    <tr key={orden.orden_compra_id}>
                                        <td className="text-center">000{orden.orden_compra_id}</td>
                                        <td className="text-center">{proveedores[orden.proveedor_id]}</td>
                                        <td className="text-center">{new Date(orden.fecha_orden).toLocaleDateString()}</td>
                                        <td className="text-center">{orden.estado}</td>
                                        <td className="text-center">
                                            <div className="d-flex justify-content-center gap-2">
                                                <button
                                                    className="btn btn-success btn-sm"
                                                    onClick={() => handleCompleteOrder(orden.orden_compra_id)}
                                                    disabled={orden.estado !== "pendiente"}
                                                >
                                                    <FontAwesomeIcon icon={faCheckCircle} className="me-1" /> Completar
                                                </button>
                                                <button
                                                    className="btn btn-danger btn-sm"
                                                    onClick={() => handleCancelOrder(orden.orden_compra_id)}
                                                    disabled={orden.estado !== "pendiente"}
                                                >
                                                    <FontAwesomeIcon icon={faTimesCircle} className="me-1" /> Cancelar
                                                </button>
                                                <button
                                                    className="btn btn-primary btn-sm"
                                                    onClick={() => handleGenerarPDF(orden.orden_compra_id)}
                                                >
                                                    <FontAwesomeIcon icon={faFilePdf} className="me-1" /> Generar PDF
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

export default ConsultarOrdenesCompra;


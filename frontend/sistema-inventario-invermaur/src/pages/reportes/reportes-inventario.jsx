import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Sidebar from '../../components/Sidebar';
import Header from '../../layouts/Header';
import Footer from '../../layouts/Footer';
import styles from './styles/reportes-inventario.module.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch, faFilePdf, faCalendarAlt } from '@fortawesome/free-solid-svg-icons';

const ReporteInventario = () => {
    const [productos, setProductos] = useState([]);
    const [searchTerm, setSearchTerm] = useState("");
    const [page, setPage] = useState(1);
    const [limit, setLimit] = useState(10);
    const [totalProductos, setTotalProductos] = useState(0);
    const [fechaInicio, setFechaInicio] = useState("");
    const [fechaFin, setFechaFin] = useState("");

    useEffect(() => {
        const fetchProductos = async () => {
            try {
                const response = await axios.get(`http://localhost:8000/productos/filtrar`, {
                    params: { skip: (page - 1) * limit, limit, fecha_inicio: fechaInicio, fecha_fin: fechaFin }
                });
                const productos = response.data.productos;

                // Obtener el precio de compra para cada producto
                const productosConPrecioCompra = await Promise.all(
                    productos.map(async (producto) => {
                        const responsePrecioCompra = await axios.get(`http://localhost:8000/productos/precio_compra/${producto.producto_id}`);
                        producto.precio_compra = responsePrecioCompra.data || 0; // Asignar 0 si no se encuentra el precio de compra
                        return producto;
                    })
                );

                setProductos(productosConPrecioCompra);
                setTotalProductos(response.data.total);
            } catch (error) {
                console.error('Error al cargar los productos:', error);
            }
        };
        fetchProductos();
    }, [page, limit, fechaInicio, fechaFin]);

    const filteredProductos = productos.filter(
        (producto) => producto.nombre.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const handleGenerateReport = async () => {
        try {
            const response = await axios.get('http://localhost:8000/generar-reporte-inventario', {
                params: { fecha_inicio: fechaInicio, fecha_fin: fechaFin },
                responseType: 'blob'
            });
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'reporte_inventario.pdf');
            document.body.appendChild(link);
            link.click();
            link.remove();
        } catch (error) {
            console.error('Error al generar el reporte:', error);
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
                <div className={`${styles.reportContainer} container`}>
                    <h2 className={styles.title}>Reporte de Inventario</h2>
                    <div className={styles.filters}>
                        <div className="input-group mb-4" style={{ maxWidth: '200px' }}>
                            <span className="input-group-text bg-primary text-white">
                                <FontAwesomeIcon icon={faSearch} />
                            </span>
                            <input
                                type="text"
                                className={`form-control ${styles.searchInput}`}
                                placeholder="Buscar producto..."
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                            />
                        </div>
                        <div className={styles.dateFilters}>
                            <div className="input-group mb-4" style={{ maxWidth: '200px' }}>
                                <span className="input-group-text bg-primary text-white">
                                    <FontAwesomeIcon icon={faCalendarAlt} />
                                </span>
                                <input
                                    type="date"
                                    className="form-control"
                                    value={fechaInicio}
                                    onChange={(e) => setFechaInicio(e.target.value)}
                                />
                            </div>
                            <div className="input-group mb-4" style={{ maxWidth: '200px' }}>
                                <span className="input-group-text bg-primary text-white">
                                    <FontAwesomeIcon icon={faCalendarAlt} />
                                </span>
                                <input
                                    type="date"
                                    className="form-control"
                                    value={fechaFin}
                                    onChange={(e) => setFechaFin(e.target.value)}
                                />
                            </div>
                        </div>
                        <button className={`${styles.reportButton} btn btn-danger`} onClick={handleGenerateReport}>
                            <FontAwesomeIcon icon={faFilePdf} /> Generar Reporte
                        </button>
                    </div>
                    <table className={`${styles.table} table`}>
                        <thead>
                            <tr>
                                <th>Código</th>
                                <th>Nombre</th>
                                <th>Categoría</th>
                                <th>Stock</th>
                                <th>Stock Min</th>
                                <th>Stock Max</th>
                                <th>Ubicación</th>
                                <th>Precio Venta</th>
                                <th>Precio Compra</th>
                                <th>Valor Total</th>
                            </tr>
                        </thead>
                        <tbody>
                            {filteredProductos.map((producto) => (
                                <tr key={producto.producto_id}>
                                    <td>{producto.codigo}</td>
                                    <td>{producto.nombre}</td>
                                    <td>{producto.categoria ? producto.categoria.nombre : ''}</td>
                                    <td>{producto.stock}</td>
                                    <td>{producto.cantidad_minima}</td>
                                    <td>{producto.cantidad_maxima}</td>
                                    <td>{producto.ubicacion}</td>
                                    <td>{producto.precio.toFixed(2)}</td>
                                    <td>{typeof producto.precio_compra === 'number' ? producto.precio_compra.toFixed(2) : 'N/A'}</td> {/* Verifica el tipo antes de aplicar toFixed */}
                                    <td>{(producto.stock * producto.precio).toFixed(2)}</td> {/* Calcula el valor total usando el precio de venta */}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                    <div className={styles.pagination}>
                        <button
                            className={`btn ${page === 1 ? "btn-secondary" : "btn-primary"}`}
                            onClick={handlePreviousPage}
                            disabled={page === 1}
                        >
                            Anterior
                        </button>
                        <span>
                            Página {page} de {totalPages}
                        </span>
                        <button
                            className={`btn ${page === totalPages ? "btn-secondary" : "btn-primary"}`}
                            onClick={handleNextPage}
                            disabled={page === totalPages}
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

export default ReporteInventario;

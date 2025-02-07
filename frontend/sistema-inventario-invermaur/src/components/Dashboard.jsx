import React, { useState, useEffect } from 'react';
import MetricCard from '../components/MetricCard';
import ChartComponent from '../components/ChartComponent'; 
import Notification from '../components/Notification';
import QuickAccessButtons from '../components/QuickAccessButtons';
import DateTime from '../components/DateTime'; 
import axios from 'axios';
import styles from '../styles/dashboard.module.css';
import Link from 'next/link';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBox, faTruck, faUsers, faUserShield } from '@fortawesome/free-solid-svg-icons';

const Dashboard = () => {
    const [metrics, setMetrics] = useState({
        totalProveedores: 0,
        totalProductos: 0,
        pedidosPendientes: 0,
        pedidosEntregados: 0,
        clientesRegistrados: 0,
        facturasEmitidas: 0,
        usuariosSistema: 0,
        valorInventario: 0,
        entradas: { total: 0, value: 0 },
        salidas: { total: 0, value: 0 },
        categoriasTotales: 0,
        dolarRate: 0
    });

    const [barDataEntradasSalidas, setBarDataEntradasSalidas] = useState([]);
    const [barLabelsEntradasSalidas, setBarLabelsEntradasSalidas] = useState([]);
    const [barDataCategorias, setBarDataCategorias] = useState([]);
    const [barLabelsCategorias, setBarLabelsCategorias] = useState([]);
    const [productosInventarioBajo, setProductosInventarioBajo] = useState([]);

    useEffect(() => {
        const fetchMetrics = async () => {
            try {
                const [proveedoresRes, productosRes, pendientesRes, entregadosRes, clientesRes, facturasRes, usuariosRes, inventarioRes, entradasTotalRes, salidasTotalRes, categoriasTotalRes, entradasSalidasRes, categoriasRes, dolarRes, inventarioBajoRes] = await Promise.all([
                    axios.get('http://localhost:8000/proveedores/total'),
                    axios.get('http://localhost:8000/productos/total_stock'),
                    axios.get('http://localhost:8000/pedidos/pendientes/total'),
                    axios.get('http://localhost:8000/pedidos/entregados/total'),
                    axios.get('http://localhost:8000/clientes/total'),
                    axios.get('http://localhost:8000/ordenes_compra?estado=completada'),
                    axios.get('http://localhost:8000/usuarios/total'),
                    axios.get('http://localhost:8000/productos/valor_inventario'),
                    axios.get('http://localhost:8000/entradas_inventario/total'),
                    axios.get('http://localhost:8000/salidas_inventario/total'),
                    axios.get('http://localhost:8000/categorias/total'),
                    axios.get('http://localhost:8000/entrada_salida/entradas_salidas_por_producto'),
                    axios.get('http://localhost:8000/categorias/conteo_productos'),
                    axios.get('http://localhost:8000/dollar/dollar-rate'),
                    axios.get('http://localhost:8000/productos/inventario_bajo')
                ]);

                console.log('Entradas y Salidas por Producto:', entradasSalidasRes.data);
                console.log('Conteo de Productos por Categoría:', categoriasRes.data);
                console.log('Productos con Inventario Bajo:', inventarioBajoRes.data);

                setMetrics({
                    totalProveedores: proveedoresRes.data.total,
                    totalProductos: productosRes.data.total,
                    pedidosPendientes: pendientesRes.data.total,
                    pedidosEntregados: entregadosRes.data.total,
                    clientesRegistrados: clientesRes.data.total,
                    facturasEmitidas: facturasRes.data.total,
                    usuariosSistema: usuariosRes.data.total,
                    valorInventario: inventarioRes.data.valor_total,
                    entradas: { total: entradasTotalRes.data.total, value: entradasTotalRes.data.valor_compras },
                    salidas: { total: salidasTotalRes.data.total, value: salidasTotalRes.data.valor_ventas },
                    categoriasTotales: categoriasTotalRes.data.total,
                    dolarRate: dolarRes.data.dolar
                });

                const labelsData = entradasSalidasRes.data.map(item => item.producto);
                const entradasData = entradasSalidasRes.data.map(item => item.total_entradas);
                const salidasData = entradasSalidasRes.data.map(item => item.total_salidas);

                setBarLabelsEntradasSalidas(labelsData);
                setBarDataEntradasSalidas([
                    {
                        label: 'Entradas',
                        data: entradasData,
                        backgroundColor: 'rgba(75, 192, 192, 0.6)',
                    },
                    {
                        label: 'Salidas',
                        data: salidasData,
                        backgroundColor: 'rgba(255, 99, 132, 0.6)',
                    }
                ]);

                const categoriasLabels = categoriasRes.data.map(item => item.nombre);
                const categoriasData = categoriasRes.data.map(item => item.total_productos);

                setBarLabelsCategorias(categoriasLabels);
                setBarDataCategorias([
                    {
                        label: 'Productos por Categoría',
                        data: categoriasData,
                        backgroundColor: 'rgba(153, 102, 255, 0.6)',
                    }
                ]);

                setProductosInventarioBajo(inventarioBajoRes.data);

            } catch (error) {
                console.error('Error fetching metrics:', error);
            }
        };

        fetchMetrics();
    }, []);

    const handleReponerProducto = (producto_id, cantidad) => {
        setProductosInventarioBajo(prevProductos => {
            const updatedProductos = prevProductos.filter(prod => prod.producto_id !== producto_id);
            return updatedProductos;
        });
    };

    const handleBackupDownload = async () => {
        try {
            const response = await axios.get('http://localhost:8000/backup', {
                responseType: 'blob'
            });
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'backup_inventario_sistema.db');
            document.body.appendChild(link);
            link.click();
            link.remove();
        } catch (error) {
            console.error('Error al descargar el respaldo:', error);
        }
    };

    return (
        <div className={`${styles.dashboardContainer}`}>
            <div className="row">
                <div className="col-md-12 d-flex justify-content-end">
                    <DateTime />
                </div>
            </div>
            <h1 className={`${styles.dashboardHeader} mb-4`}>Dashboard del Administrador</h1>

            <div className={`row ${styles.metricsRow}`}>
                <div className="col-md-3">
                    <Link href="/productos/consultar-productos" legacyBehavior>
                        <a className={styles.metricCardLink}>
                            <MetricCard title="Productos en Stock" value={metrics.totalProductos}>
                                {/*<FontAwesomeIcon icon={faBox} size="lg" className="me-2" />*/}
                            </MetricCard>
                        </a>
                    </Link>
                </div>
                <div className="col-md-3">
                    <Link href="/proveedores/consultar-proveedores" legacyBehavior>
                        <a className={styles.metricCardLink}>
                            <MetricCard title="Total de Proveedores" value={metrics.totalProveedores}>
                                {/*<FontAwesomeIcon icon={faTruck} size="lg" className="me-2" />*/}
                            </MetricCard>
                        </a>
                    </Link>
                </div>
                <div className="col-md-3">
                    <Link href="/clientes/consultar-clientes" legacyBehavior>
                        <a className={styles.metricCardLink}>
                            <MetricCard title="Clientes Registrados" value={metrics.clientesRegistrados}>
                                {/*<FontAwesomeIcon icon={faUsers} size="lg" className="me-2" />*/}
                            </MetricCard>
                        </a>
                    </Link>
                </div>
                <div className="col-md-3">
                    <Link href="/usuarios/gestionar-usuarios" legacyBehavior>
                        <a className={styles.metricCardLink}>
                            <MetricCard title="Usuarios del Sistema">
                                <FontAwesomeIcon icon={faUserShield} size="lg" className="me-2" />
                            </MetricCard>
                        </a>
                    </Link>
                </div>
            </div>

            <div className={`row ${styles.metricsRow}`}>
                <div className="col-md-3">
                    <MetricCard title="Pedidos Pendientes" value={metrics.pedidosPendientes} />
                </div>
                <div className="col-md-3">
                    <MetricCard title="Pedidos Entregados" value={metrics.pedidosEntregados} />
                </div>
                <div className="col-md-3">
                    <MetricCard title="Ordenes Emitidas" value={metrics.facturasEmitidas} />
                </div>
                <div className="col-md-3">
                    <MetricCard title="Valor del Inventario" value={`${metrics.valorInventario.toFixed(2)} Bs`} />
                </div>
                <div className="col-md-3">
                    <MetricCard title="Entradas" value={`${metrics.entradas.total} items - ${metrics.entradas.value} Bs`} />
                </div>
                <div className="col-md-3">
                    <MetricCard title="Salidas" value={`${metrics.salidas.total} items - ${metrics.salidas.value} Bs`} />
                </div>
                <div className="col-md-3">
                    <MetricCard title="Total Categorías" value={metrics.categoriasTotales} />
                </div>
                <div className="col-md-3">
                    <MetricCard title="Precio del Dólar" value={`${metrics.dolarRate.toFixed(4)} Bs/USD`} />
                </div>
            </div>

            <div className="row mt-4">
                <div className="col-md-12 mb-4">
                    <ChartComponent type="bar" title="Entradas y Salidas de Productos" data={barDataEntradasSalidas} labels={barLabelsEntradasSalidas} />
                </div>
                <div className="col-md-12 mb-4">
                    <ChartComponent type="bar" title="Productos por Categoría" data={barDataCategorias} labels={barLabelsCategorias} />
                </div>
            </div>

            {productosInventarioBajo.length > 0 && (
                <Notification 
                    productos={productosInventarioBajo} 
                    onRestock={handleReponerProducto}
                />
            )}

            <div className="row mt-4">
                <div className="col-lg-12">
                    <button className="btn btn-primary" onClick={handleBackupDownload}>
                        Descargar Respaldo
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;




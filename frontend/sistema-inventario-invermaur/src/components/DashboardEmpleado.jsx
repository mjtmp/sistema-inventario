import React, { useState, useEffect } from 'react';
import MetricCard from '../components/MetricCard';
import DateTime from '../components/DateTime';
import DollarRate from '../components/DollarRate';
import axios from 'axios';
import styles from '../styles/dashboard.module.css';
import Link from 'next/link';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBox, faTruck, faUsers, faClipboard } from '@fortawesome/free-solid-svg-icons';

const EmployeeDashboard = () => {
    const [metrics, setMetrics] = useState({
        totalProveedores: 0,
        totalProductos: 0,
        pedidosPendientes: 0,
        clientesRegistrados: 0,
        dolarRate: 0
    });

    useEffect(() => {
        const fetchMetrics = async () => {
            try {
                const [proveedoresRes, productosRes, pendientesRes, clientesRes, dolarRes] = await Promise.all([
                    axios.get('http://localhost:8000/proveedores/total'),
                    axios.get('http://localhost:8000/productos/total_stock'),
                    axios.get('http://localhost:8000/pedidos/pendientes/total'),
                    axios.get('http://localhost:8000/clientes/total'),
                    axios.get('http://localhost:8000/dollar/dollar-rate')
                ]);

                setMetrics({
                    totalProveedores: proveedoresRes.data.total,
                    totalProductos: productosRes.data.total,
                    pedidosPendientes: pendientesRes.data.total,
                    clientesRegistrados: clientesRes.data.total,
                    dolarRate: dolarRes.data.dolar
                });
            } catch (error) {
                console.error('Error fetching metrics:', error);
            }
        };

        fetchMetrics();
    }, []);

    return (
        <div className={`${styles.dashboardContainer}`}>
            <div className="row">
                <div className="col-md-6 d-flex justify-content-start">
                    <DateTime />
                </div>
                <div className="col-md-6 d-flex justify-content-end">
                    <DollarRate />
                </div>
            </div>
            <h1 className={`${styles.dashboardHeader} mb-4`}>Dashboard del Empleado</h1>

            <div className={`row ${styles.metricsRow}`}>
                <div className="col-md-3">
                    <Link href="/productos/consultar-productos" legacyBehavior>
                        <a className={styles.metricCardLink}>
                            <MetricCard title="Productos en Stock" >
                                <FontAwesomeIcon icon={faBox} size="lg" className="me-2" />
                            </MetricCard>
                        </a>
                    </Link>
                </div>
                <div className="col-md-3">
                    <Link href="/proveedores/consultar-proveedores" legacyBehavior>
                        <a className={styles.metricCardLink}>
                            <MetricCard title="Total de Proveedores">
                                <FontAwesomeIcon icon={faTruck} size="lg" className="me-2" />
                            </MetricCard>
                        </a>
                    </Link>
                </div>
                <div className="col-md-3">
                    <Link href="/clientes/consultar-clientes" legacyBehavior>
                        <a className={styles.metricCardLink}>
                            <MetricCard title="Clientes Registrados" >
                                <FontAwesomeIcon icon={faUsers} size="lg" className="me-2" />
                            </MetricCard>
                        </a>
                    </Link>
                </div>
                <div className="col-md-3">
                    <Link href="/pedidos/consultar-pedidos" legacyBehavior>
                        <a className={styles.metricCardLink}>
                            <MetricCard title="Pedidos Pendientes" >
                                <FontAwesomeIcon icon={faClipboard} size="lg" className="me-2" />
                            </MetricCard>
                        </a>
                    </Link>
                </div>
            </div>
        </div>
    );
};

export default EmployeeDashboard;



import React from 'react';
import MetricCard from '../components/MetricCard'; // Importamos el componente para mostrar métricas
import ChartComponent from '../components/ChartComponent'; // Importamos el componente para mostrar gráficos
import Notification from '../components/Notification'; // Importamos el componente de notificaciones
import QuickAccessButtons from '../components/QuickAccessButtons'; // Importamos botones de acceso rápido
import styles from '../styles/dashboard.module.css'; // Importamos los estilos para el dashboard

const Dashboard = () => {
    // Métricas estáticas para el dashboard (pueden ser dinámicas en una implementación real)
    const metrics = [
        { title: "Total de Proveedores", value: 120 },
        { title: "Productos en Stock", value: 550 },
        { title: "Pedidos Pendientes", value: 32 },
        { title: "Pedidos Entregados", value: 180 },
        { title: "Facturación del Mes", value: "Bs 1,500,000" },
        { title: "Clientes Registrados", value: 200 },
        { title: "Facturas Emitidas", value: 95 },
        { title: "Productos Vendidos", value: 450 },
        { title: "Usuarios del Sistema", value: 15 },
        { title: "Ingresos Totales (Bs)", value: "Bs 2,800,000" }
    ];

    return (
        <div className={`${styles.dashboardContainer} container mt-4`}>
            <h1 className={`${styles.dashboardHeader} mb-4`}>Dashboard del Administrador</h1>

            {/* Reorganizamos las métricas en un grid de 4x4 */}
            <div className="row">
                {metrics.map((metric, index) => (
                    <div className="col-md-3 mb-4" key={index}>
                        <MetricCard title={metric.title} value={metric.value} /> {/* Mostramos cada tarjeta de métrica */}
                    </div>
                ))}
            </div>
            
            {/* Componente de notificación */}
            <Notification />

            {/* Botones de acceso rápido */}
            <QuickAccessButtons />

            {/* Sección de gráficos centrados */}
            <div className={`row mt-4 ${styles.chartRow}`}>
                <div className="col-md-6 mb-4 d-flex justify-content-center">
                    <ChartComponent type="bar" title="Tendencias de Stock" /> {/* Gráfico de barras */}
                </div>
                <div className="col-md-6 mb-4 d-flex justify-content-center">
                    <ChartComponent type="pie" title="Categorización de Productos en Stock" /> {/* Gráfico circular */}
                </div>
            </div>
        </div>
    );
};

export default Dashboard;





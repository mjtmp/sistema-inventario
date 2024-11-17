import React from 'react';
import styles from '../styles/metric-card.module.css'; // Importamos los estilos para el componente de tarjeta de métrica

// El componente MetricCard acepta "title" para el título de la métrica y "value" para el valor a mostrar
const MetricCard = ({ title, value }) => {
    return (
        <div className={`card shadow-sm ${styles.metricCard}`}>
            <div className={`card-body ${styles.metricBody}`}>
                <h5 className={`card-title ${styles.metricTitle}`}>{title}</h5> {/* Título de la métrica */}
                <p className={`card-text ${styles.metricValue}`}>{value}</p> {/* Valor de la métrica */}
            </div>
        </div>
    );
};

export default MetricCard;



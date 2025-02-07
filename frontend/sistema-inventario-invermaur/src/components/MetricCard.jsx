import React from 'react';
import styles from '../styles/metric-card.module.css';

// El componente MetricCard acepta "title" para el título de la métrica, "value" para el valor a mostrar y "children" para los íconos
const MetricCard = ({ title, value, children }) => {
    return (
        <div className={`card shadow-sm ${styles.metricCard}`}>
            <div className={`card-body ${styles.metricBody}`}>
                {children && <div className={styles.iconContainer}>{children}</div>}
                <h5 className={`card-title ${styles.metricTitle}`}>{title}</h5> {/* Título de la métrica */}
                <p className={`card-text ${styles.metricValue}`}>{value}</p> {/* Valor de la métrica */}
            </div>
        </div>
    );
};

export default MetricCard;


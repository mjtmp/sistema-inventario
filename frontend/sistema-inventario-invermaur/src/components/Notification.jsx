import React from 'react';
import styles from '../styles/notification.module.css';

const Notification = () => {
    return (
        // Este componente muestra una notificación de alerta con un mensaje
        <div className={`alert alert-warning mt-4 ${styles.notification}`} role="alert">
            🔔 Tienes productos con inventario bajo y otros cercanos a su fecha de vencimiento.
        </div>
    );
};

export default Notification;

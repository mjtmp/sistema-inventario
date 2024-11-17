import React from 'react';
import { useRouter } from 'next/router';
import styles from '../styles/quick-access-buttons.module.css';

const QuickAccessButtons = () => {
    const router = useRouter();

    // Array de botones con sus rutas asociadas
    const buttons = [
        { label: "Nuevo Producto", route: "/productos/nuevo" },
        { label: "Nuevo Proveedor", route: "/proveedores/nuevo" },
        { label: "Nuevo Cliente", route: "/clientes/nuevo" }
    ];

    return (
        // Contenedor de botones de acceso rápido
        <div className={`d-flex gap-3 mt-4 ${styles.quickAccessContainer}`}>
            {buttons.map((button, index) => (
                // Cada botón redirige a su ruta correspondiente usando `router.push`
                <button
                    key={index}
                    className={`btn btn-primary ${styles.quickAccessButton}`}
                    onClick={() => router.push(button.route)}
                >
                    {button.label}
                </button>
            ))}
        </div>
    );
};

export default QuickAccessButtons;


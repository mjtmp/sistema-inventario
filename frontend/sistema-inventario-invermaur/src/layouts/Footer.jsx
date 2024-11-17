import React from 'react';
import styles from '../styles/footer.module.css';  // Importa los estilos específicos para el footer
import 'bootstrap/dist/css/bootstrap.min.css';     // Importa Bootstrap para diseño responsivo

// Componente Footer que define el pie de página
const Footer = () => {
    return (
        <footer className={`bg-light text-center py-3 ${styles.footer}`}>
            {/* Texto del pie de página con los derechos reservados */}
            <p className="mb-0">&copy; 2024 Sistema de Inventario - Todos los derechos reservados - Realizado por Mauricio Mejias</p>
        </footer>
    );
}

export default Footer;



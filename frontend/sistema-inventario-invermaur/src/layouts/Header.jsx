"use client";
import React, { useEffect } from "react";
import { useRouter } from "next/router"; // Hook para navegar entre páginas
import styles from "../styles/header.module.css"; // Importa los estilos específicos para el header
import "bootstrap/dist/css/bootstrap.min.css"; // Importa Bootstrap para diseño responsivo
import { Dropdown } from "react-bootstrap"; // Importa el componente Dropdown de React-Bootstrap
import Link from "next/link"; // Importa Link de Next.js para navegar entre páginas

// Componente Header que define la barra de navegación
const Header = () => {
  const router = useRouter(); // Hook para manipular la navegación del router
  const [name, setName] = React.useState(""); // Estado para el nombre del usuario
  useEffect(() => {
    const name = localStorage.getItem("name"); // Obtiene el nombre del usuario desde localStorage
    if (name) {
      setName(name); // Actualiza el estado con el nombre del usuario
    }
  }, []);
  // Función para manejar el cierre de sesión
  const handleLogout = () => {
    localStorage.removeItem("token"); // Elimina el token de localStorage
    localStorage.removeItem("rol"); // Elimina el rol de localStorage
    localStorage.removeItem("name"); // Elimina el nombre del usuario de localStorage
    router.push("/login"); // Redirige al usuario a la página de login
  };

  return (
    <header
      className={`navbar navbar-expand-lg navbar-light bg-light ${styles.header}`}
    >
      <div className="container-fluid">
        {/* Contenedor con el logo y enlace a la página principal */}
        <div className={`${styles.logoContainer} navbar-brand`}>
          <img
            src="/invermaur.png"
            alt="Logo Empresa"
            className={styles["header-logo"]}
          />
          <Link href="/admin-dashboard">
            <h1 className="h4 mb-0 system-inventory-link">
              Sistema de Inventario
            </h1>
          </Link>
        </div>

        {/* Menú de opciones del usuario */}
        <nav className={styles.nav}>
          <ul className="navbar-nav ml-auto">
            {/* Menú desplegable de opciones de usuario */}
            <li className="nav-item">
              <Dropdown>
                <Dropdown.Toggle variant="link" className="nav-link text-dark">
                  <strong>{name}</strong> {/* Muestra el nombre del usuario */}
                </Dropdown.Toggle>
                <Dropdown.Menu align="end">
                  {/* Opciones del menú */}
                  <Dropdown.Item href="/configuracion">
                    Configuración de Perfil
                  </Dropdown.Item>
                  <Dropdown.Item onClick={handleLogout}>
                    Cerrar sesión
                  </Dropdown.Item>
                </Dropdown.Menu>
              </Dropdown>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;

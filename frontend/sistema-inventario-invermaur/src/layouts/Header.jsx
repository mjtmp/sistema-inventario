"use client";
import React, { useEffect, useState } from "react";
import { useRouter } from "next/router";
import styles from "../styles/header.module.css";
import "bootstrap/dist/css/bootstrap.min.css";
import { Dropdown } from "react-bootstrap";
import Link from "next/link";

const Header = () => {
  const router = useRouter();
  const [name, setName] = useState("");
  const [dashboardLink, setDashboardLink] = useState("/");
  const [isClient, setIsClient] = useState(false);  // Agregar estado para controlar el renderizado del cliente

  useEffect(() => {
    const name = localStorage.getItem("name");
    const role = localStorage.getItem("rol");

    if (name) {
      setName(name);
    }

    if (role === "admin") {
      setDashboardLink("/admin-dashboard");
    } else if (role === "employee") {
      setDashboardLink("/employee-dashboard");
    }
    
    setIsClient(true);  // Establecer el estado para indicar que estamos en el cliente
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("rol");
    localStorage.removeItem("name");
    router.push("/login");
  };

  const handleConfiguracion = () => {
    router.push("/configuracion");
  };

  return (
    <header className={`navbar navbar-expand-lg navbar-light bg-light ${styles.header}`}>
      <div className="container-fluid">
        <div className={`${styles.logoContainer} navbar-brand`}>
          <img
            src="/invermaur.png"
            alt="Logo Empresa"
            className={styles["header-logo"]}
          />
          {isClient && (  // Renderizar el link sólo si estamos en el cliente
            <Link href={dashboardLink} style={{ textDecoration: 'none' }}>
              <h1 className="h4 mb-0 system-inventory-link">
                Sistema de Inventario
              </h1>
            </Link>
          )}
        </div>

        <nav className={styles.nav}>
          <ul className="navbar-nav ml-auto">
            <li className="nav-item">
              {isClient && (  // Renderizar el dropdown sólo si estamos en el cliente
                <Dropdown>
                  <Dropdown.Toggle variant="link" className="nav-link text-dark">
                    <strong>{name}</strong>
                  </Dropdown.Toggle>
                  <Dropdown.Menu align="end">
                    <Dropdown.Item onClick={handleConfiguracion}>
                      Configuración de Perfil
                    </Dropdown.Item>
                    <Dropdown.Item onClick={handleLogout}>
                      Cerrar sesión
                    </Dropdown.Item>
                  </Dropdown.Menu>
                </Dropdown>
              )}
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;


import React, { useState } from 'react';
import styles from '../styles/sidebar.module.css';
import { Collapse } from 'react-bootstrap';
import Link from 'next/link';

const Sidebar = () => {
    const [activeOption, setActiveOption] = useState(null);
    const [activeSubOption, setActiveSubOption] = useState(null); // Para el submenú de "Entrada"

    // Función para alternar la visibilidad del menú principal
    const handleToggle = (option) => {
        setActiveOption(activeOption === option ? null : option);
        setActiveSubOption(null); // Resetea el submenú al cambiar de opción principal
    };

    // Función para alternar la visibilidad del submenú
    const handleSubToggle = (subOption) => {
        setActiveSubOption(activeSubOption === subOption ? null : subOption);
    };

    const options = [
        {
            title: "Productos",
            subOptions: [
                { name: "Añadir Producto", path: "/productos/anadir-producto" },
                { name: "Consultar Productos", path: "/productos/consultar-productos" },
                { name: "Inventario", path: "/productos/inventario" }
            ],
        },
        {
            title: "Proveedores",
            subOptions: [
                { name: "Añadir Proveedor", path: "/proveedores/anadir-proveedor" },
                { name: "Consultar Proveedores", path: "/proveedores/consultar-proveedores" }
            ],
        },
        {
            title: "Clientes",
            subOptions: [
                { name: "Añadir Cliente", path: "/clientes/anadir-cliente" },
                { name: "Consultar Clientes", path: "/clientes/consultar-clientes" }
            ],
        },
        {
            title: "Gestión de Existencias",
            subOptions: [
                {
                    name: "Entrada",
                    path: "/existencias/entrada",
                    hasSubOptions: true,
                    subOptions: [
                        { name: "Entrada de Inventario", path: "/existencias/entrada-inventario" },
                        { name: "Listado de Inventario", path: "/existencias/listar-entradas" }
                    ]
                },
                { name: "Salida", path: "/existencias/listar-salidas" }
            ],
        },
        {
            title: "Usuarios",
            subOptions: [
                { name: "Gestionar Usuarios", path: "/usuarios/gestionar-usuarios" },
                { name: "Roles y Permisos", path: "/usuarios/roles-permisos" }
            ],
        },
        {
            title: "Reportes",
            subOptions: [
                { name: "Reporte de Inventario", path: "/reportes/reportes-inventario" },
                { name: "Reporte de Entrega", path: "/reportes/reportes-entrega" },
                { name: "Reporte de Entradas y Salidas", path: "/reportes/entradas-salidas" }
            ],
        }
    ];

    return (
        // Sidebar que contiene los enlaces de navegación con menús colapsables
        <div className={`bg-dark text-white ${styles.sidebar}`}>
            <h2 className={`text-center my-4 ${styles.title}`}>Panel de Administración</h2>
            <div className="list-group">
                {options.map((option, index) => (
                    <div key={index} className="mb-2">
                        <button
                            className={`list-group-item list-group-item-action bg-dark text-white d-flex justify-content-between align-items-center ${styles.optionTitle}`}
                            onClick={() => handleToggle(option.title)}
                        >
                            {option.title}
                            <span className={activeOption === option.title ? styles.arrowDown : styles.arrowRight}>➔</span>
                        </button>
                        <Collapse in={activeOption === option.title}>
                            <div className={`list-group ${styles.subOptions}`}>
                                {option.subOptions.map((subOption, subIndex) => (
                                    <div key={subIndex}>
                                        {/* Verifica si tiene sub-opciones adicionales (Ej: Entrada) */}
                                        {subOption.hasSubOptions ? (
                                            <>
                                                <button
                                                    className={`list-group-item list-group-item-action bg-secondary text-light ${styles.subOption}`}
                                                    onClick={() => handleSubToggle(subOption.name)}
                                                >
                                                    {subOption.name}
                                                </button>
                                                <Collapse in={activeSubOption === subOption.name}>
                                                    <div className={`list-group ${styles.subOptions}`}>
                                                        {subOption.subOptions.map((nestedSubOption, nestedIndex) => (
                                                            <Link
                                                                key={nestedIndex}
                                                                href={nestedSubOption.path}
                                                                className={`list-group-item list-group-item-action bg-secondary text-light ${styles.subOption}`}
                                                            >
                                                                {nestedSubOption.name}
                                                            </Link>
                                                        ))}
                                                    </div>
                                                </Collapse>
                                            </>
                                        ) : (
                                            <Link
                                                href={subOption.path}
                                                className={`list-group-item list-group-item-action bg-secondary text-light ${styles.subOption}`}
                                            >
                                                {subOption.name}
                                            </Link>
                                        )}
                                    </div>
                                ))}
                            </div>
                        </Collapse>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Sidebar;



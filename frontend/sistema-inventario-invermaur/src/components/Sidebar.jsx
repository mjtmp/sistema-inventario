import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTags, faBox, faTruck, faUsers, faClipboard, faWarehouse, faUserShield, faFileAlt, faBook } from '@fortawesome/free-solid-svg-icons';
import styles from '../styles/sidebar.module.css';
import { Collapse } from 'react-bootstrap';
import Link from 'next/link';

const Sidebar = ({ children }) => {
    const [activeOption, setActiveOption] = useState(null);
    const [activeSubOption, setActiveSubOption] = useState(null); // Para el submenú de "Entrada"
    const [isClient, setIsClient] = useState(false); // Estado para controlar el renderizado del cliente

    useEffect(() => {
        setIsClient(true); // Establecer el estado para indicar que estamos en el cliente
    }, []);

    const handleToggle = (option) => {
        setActiveOption(activeOption === option ? null : option);
        setActiveSubOption(null); // Resetea el submenú al cambiar de opción principal
    };

    const handleSubToggle = (subOption) => {
        setActiveSubOption(activeSubOption === subOption ? null : subOption);
    };

    const userRole = isClient ? localStorage.getItem('rol') : null; // Obtener el rol del usuario solo en el cliente

    const adminOptions = [
        {
            title: "Categorías",
            icon: faTags,
            subOptions: [
                { name: "Añadir Categoría", path: "/categorias/anadir-categoria" },
                { name: "Consultar Categorías", path: "/categorias/consultar-categorias" }
            ],
        },
        {
            title: "Productos",
            icon: faBox,
            subOptions: [
                { name: "Añadir Producto", path: "/productos/anadir-producto" },
                { name: "Consultar Productos", path: "/productos/consultar-productos" },
                { name: "Inventario", path: "/productos/inventario" }
            ],
        },
        {
            title: "Proveedores",
            icon: faTruck,
            subOptions: [
                { name: "Añadir Proveedor", path: "/proveedores/anadir-proveedor" },
                { name: "Consultar Proveedores", path: "/proveedores/consultar-proveedores" }
            ],
        },
        {
            title: "Clientes",
            icon: faUsers,
            subOptions: [
                { name: "Añadir Cliente", path: "/clientes/anadir-cliente" },
                { name: "Consultar Clientes", path: "/clientes/consultar-clientes" }
            ],
        },
        {
            title: "Pedidos",
            icon: faClipboard,
            subOptions: [
                { name: "Crear Pedido", path: "/pedidos/crear-pedido" },
                { name: "Consultar Pedidos", path: "/pedidos/consultar-pedidos" }
            ],
        },
        {
            title: "Gestión de Existencias",
            icon: faWarehouse,
            subOptions: [
                {
                    name: "Entrada",
                    path: "/existencias/entrada",
                    hasSubOptions: true,
                    subOptions: [
                        { name: "Entrada de Inventario", path: "/existencias/entrada-inventario" },
                        { name: "Listado de Inventario", path: "/existencias/listar-entradas" },
                        { name: "Ordenes de Pedido", path: "/existencias/consultar-ordenes" }
                    ]
                },
                { name: "Salida", path: "/existencias/listar-salidas" }
            ],
        },
        {
            title: "Usuarios",
            icon: faUserShield,
            subOptions: [
                { name: "Gestionar Usuarios", path: "/usuarios/gestionar-usuarios" }
            ],
        },
        {
            title: "Reportes",
            icon: faFileAlt,
            subOptions: [
                { name: "Reporte de Inventario", path: "/reportes/reportes-inventario" },
                { name: "Reporte de Entrega", path: "/reportes/reportes-entrega" }
            ],
        },
        {
            title: "Manual de Usuario",
            icon: faBook,
            subOptions: [
                { name: "Ver Manual", path: "http://localhost:8000/manuals", external: true }
            ],
        }
    ];

    const employeeOptions = [
        {
            title: "Productos",
            icon: faBox,
            subOptions: [
                { name: "Consultar Productos", path: "/productos/consultar-productos" },
                { name: "Inventario", path: "/productos/inventario" }
            ],
        },
        {
            title: "Proveedores",
            icon: faTruck,
            subOptions: [
                { name: "Consultar Proveedores", path: "/proveedores/consultar-proveedores" }
            ],
        },
        {
            title: "Clientes",
            icon: faUsers,
            subOptions: [
                { name: "Añadir Cliente", path: "/clientes/anadir-cliente" },
                { name: "Consultar Clientes", path: "/clientes/consultar-clientes" }
            ],
        },
        {
            title: "Pedidos",
            icon: faClipboard,
            subOptions: [
                { name: "Crear Pedido", path: "/pedidos/crear-pedido" },
                { name: "Consultar Pedidos", path: "/pedidos/consultar-pedidos" }
            ],
        },
        {
            title: "Gestión de Existencias",
            icon: faWarehouse,
            subOptions: [
                { name: "Salida", path: "/existencias/listar-salidas" }
            ],
        },
        {
            title: "Reportes",
            icon: faFileAlt,
            subOptions: [
                { name: "Reporte de Inventario", path: "/reportes/reportes-inventario" },
                { name: "Reporte de Entrega", path: "/reportes/reportes-entrega" }
            ],
        },
        {
            title: "Manual de Usuario",
            icon: faBook,
            subOptions: [
                { name: "Ver Manual", path: "http://localhost:8000/manuals", external: true }
            ],
        }
    ];

    const options = isClient && userRole === 'admin' ? adminOptions : employeeOptions;

    return (
        <>
            <div className={styles.sidebar}>
                {isClient && (
                    <h2 className={`text-center my-4 ${styles.title}`}>
                        {userRole === 'admin' ? 'Panel de Administración' : 'Panel de Empleado'}
                    </h2>
                )}
                <div className="list-group">
                    {options.map((option, index) => (
                        <div key={index} className="mb-2">
                            <button
                                className={`list-group-item list-group-item-action d-flex justify-content-between align-items-center ${styles.optionTitle}`}
                                onClick={() => handleToggle(option.title)}
                            >
                                <FontAwesomeIcon icon={option.icon} className="me-2" />
                                {option.title}
                                <span className={activeOption === option.title ? styles.arrowDown : styles.arrowRight}>➔</span>
                            </button>
                            <Collapse in={activeOption === option.title}>
                                <div className={`list-group ${styles.subOptions}`}>
                                    {option.subOptions.map((subOption, subIndex) => (
                                        <div key={subIndex}>
                                            {subOption.hasSubOptions ? (
                                                <>
                                                    <button
                                                        className={`list-group-item list-group-item-action bg-transparent border-none ${styles.subOption}`}
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
                                                                    className={styles.subOption}
                                                                >
                                                                    {nestedSubOption.name}
                                                                </Link>
                                                            ))}
                                                        </div>
                                                    </Collapse>
                                                </>
                                            ) : subOption.external ? (
                                                <a
                                                    href={subOption.path}
                                                    target="_blank"
                                                    rel="noopener noreferrer"
                                                    className={styles.subOption}
                                                >
                                                    {subOption.name}
                                                </a>
                                            ) : (
                                                <Link
                                                    href={subOption.path}
                                                    className={styles.subOption}
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
            <div>{children}</div>
        </>
    );
};

export default Sidebar;



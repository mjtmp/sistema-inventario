import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useRouter } from 'next/router';
import Sidebar from '../../components/Sidebar';
import Header from '../../layouts/Header';
import Footer from '../../layouts/Footer';
import 'bootstrap/dist/css/bootstrap.min.css';
import styles from './styles/gestionar-usuarios.module.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch, faEdit, faTrashAlt, faHistory } from '@fortawesome/free-solid-svg-icons';
import Swal from 'sweetalert2';
import withReactContent from 'sweetalert2-react-content';

const MySwal = withReactContent(Swal);

const GestionarUsuarios = () => {
    const [usuarios, setUsuarios] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [roles, setRoles] = useState([]); // Estado para roles
    const router = useRouter();

    useEffect(() => {
        fetchUsuarios();
        fetchRoles(); // Llamar la función para obtener los roles
    }, []);

    const fetchUsuarios = async () => {
        try {
            const response = await axios.get('http://localhost:8000/usuarios');
            setUsuarios(response.data);
        } catch (error) {
            console.error('Error al obtener usuarios:', error);
        }
    };

    const fetchRoles = async () => {
        try {
            const response = await axios.get('http://localhost:8000/roles');
            setRoles(response.data);
        } catch (error) {
            console.error('Error al obtener roles:', error);
        }
    };

    const handleDeleteUsuario = async (usuario_id) => {
        const result = await MySwal.fire({
            title: '¿Estás seguro?',
            text: '¿Deseas eliminar este usuario?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#3085d6',
            confirmButtonText: 'Sí, eliminar',
            cancelButtonText: 'Cancelar',
            customClass: {
                popup: 'my-popup-class',
                title: 'my-title-class',
                icon: 'my-icon-class',
                confirmButton: 'my-confirm-button-class',
                cancelButton: 'my-cancel-button-class'
            }
        });

        if (result.isConfirmed) {
            try {
                await axios.delete(`http://localhost:8000/usuarios/${usuario_id}`);
                setUsuarios(usuarios.filter((usuario) => usuario.usuario_id !== usuario_id));
                MySwal.fire({
                    title: 'Eliminado',
                    text: 'El usuario ha sido eliminado correctamente.',
                    icon: 'success',
                    confirmButtonColor: '#3085d6',
                    customClass: {
                        popup: 'my-popup-class',
                        title: 'my-title-class',
                        icon: 'my-icon-class',
                        confirmButton: 'my-confirm-button-class'
                    }
                });
            } catch (error) {
                console.error('Error al eliminar el usuario:', error);
                MySwal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Hubo un error al eliminar el usuario.',
                    confirmButtonColor: '#d33',
                    customClass: {
                        popup: 'my-popup-class',
                        title: 'my-title-class',
                        icon: 'my-icon-class',
                        confirmButton: 'my-confirm-button-class'
                    }
                });
            }
        }
    };

    const handleEditUsuario = async (usuario_id) => {
        const result = await MySwal.fire({
            title: '¿Estás seguro?',
            text: '¿Deseas editar este usuario?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Sí, editar',
            cancelButtonText: 'Cancelar',
            customClass: {
                popup: 'my-popup-class',
                title: 'my-title-class',
                icon: 'my-icon-class',
                confirmButton: 'my-confirm-button-class',
                cancelButton: 'my-cancel-button-class'
            }
        });

        if (result.isConfirmed) {
            window.location.href = `/usuarios/${usuario_id}`;
        }
    };

    const handleHistorial = () => {
        router.push('/usuarios/historial');
    }

    const handleRoleChange = async (usuario_id, rol_id) => {
        try {
            const usuario = usuarios.find(u => u.usuario_id === usuario_id);
            if (!usuario) {
                throw new Error("Usuario no encontrado");
            }
            // Incluye todos los campos requeridos en la solicitud de actualización
            const response = await axios.put(`http://localhost:8000/usuarios/${usuario_id}`, {
                nombre: usuario.nombre,
                email: usuario.email,
                contraseña: usuario.contraseña,
                rol_id: rol_id
            });
            alert("Rol asignado exitosamente");
            setUsuarios(usuarios.map(u => (u.usuario_id === usuario_id ? { ...u, rol_id: parseInt(rol_id) } : u)));
        } catch (error) {
            console.error("Error al asignar el rol:", error);
            alert("Error al asignar el rol");
        }
    };
    

    const filteredUsuarios = usuarios.filter((usuario) =>
        usuario.nombre.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className={styles.container}>
            <Sidebar />
            <div className={styles.mainContent}>
                <Header />
                <div className="container mt-5">
                    <h2 className={styles.title}>Gestión de Usuarios</h2>

                    <div className={`${styles.searchContainer} d-flex justify-content-center`}>
                        <div className="input-group mb-4" style={{ maxWidth: '600px' }}>
                            <span className="input-group-text bg-primary text-white">
                                <FontAwesomeIcon icon={faSearch} />
                            </span>
                            <input
                                type="text"
                                className={`form-control ${styles.searchInput}`}
                                placeholder="Buscar usuario por nombre..."
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                            />
                        </div>
                    </div>

                    <div className={styles.tableContainer}>
                        <table className={`${styles.table} table`}>
                            <thead>
                                <tr>
                                    <th>Nombre Completo</th>
                                    <th>Correo Electrónico</th>
                                    <th>Rol</th>
                                    <th>Acciones</th>
                                </tr>
                            </thead>
                            <tbody>
                                {filteredUsuarios.map((usuario) => (
                                    <tr key={usuario.usuario_id}>
                                        <td>{usuario.nombre}</td>
                                        <td>{usuario.email}</td>
                                        <td>
                                            <div className={styles.selectWrapper}>
                                                <select className={`${styles.selectRole} form-control`} onChange={(e) => handleRoleChange(usuario.usuario_id, e.target.value)} value={usuario.rol_id}>
                                                    <option value="">Seleccione un rol</option>
                                                    <option value="1">Admin</option>
                                                    <option value="2">Empleado</option>
                                                </select>
                                            </div>
                                        </td>
                                        <td className="text-center">
                                            <div className="d-flex justify-content-center gap-2">
                                                <button
                                                    className="btn btn-warning btn-sm"
                                                    onClick={() => handleEditUsuario(usuario.usuario_id)}
                                                >
                                                    <FontAwesomeIcon icon={faEdit} className="me-1" /> Editar
                                                </button>
                                                <button
                                                    className="btn btn-danger btn-sm"
                                                    onClick={() => handleDeleteUsuario(usuario.usuario_id)}
                                                >
                                                    <FontAwesomeIcon icon={faTrashAlt} className="me-1" /> Eliminar
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>

                    <div className={styles.marginBottom}>
                        <button className={`btn btn-secondary ${styles.btnUsers}`} onClick={handleHistorial}>
                            <FontAwesomeIcon icon={faHistory} className="me-1" /> Historial
                        </button>
                    </div>
                </div>
                <Footer />
            </div>
        </div>
    );
};

export default GestionarUsuarios;
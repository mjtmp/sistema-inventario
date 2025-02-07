import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import styles from '../styles/profile-settings.module.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser, faEnvelope, faLock } from '@fortawesome/free-solid-svg-icons';

const ProfileSettings = () => {
    const [usuario, setUsuario] = useState({
        nombre: '',
        email: '',
        contraseña: '',
        rol_id: null // Asegurarse de que rol_id se maneje correctamente
    });

    useEffect(() => {
        const usuario_id = localStorage.getItem('usuario_id'); // Obtener el ID del usuario desde localStorage

        if (usuario_id) {
            axios.get(`http://localhost:8000/usuarios/${usuario_id}`)
                .then(response => {
                    const { nombre, email, rol_id } = response.data; // Asegurarse de obtener rol_id
                    setUsuario({
                        nombre,
                        email,
                        rol_id, // Asignar rol_id
                        contraseña: ''
                    });
                })
                .catch(error => {
                    console.error('Error al obtener los datos del perfil:', error);
                });
        }
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();

        const usuario_id = localStorage.getItem('usuario_id'); // Obtener el ID del usuario desde localStorage

        try {
            const dataToUpdate = {
                nombre: usuario.nombre,
                email: usuario.email,
                rol_id: usuario.rol_id // Mantener el rol_id
            };

            if (usuario.contraseña) {
                dataToUpdate.contraseña = usuario.contraseña;
            }

            // Agregar console.log para verificar los datos
            console.log("Datos enviados:", dataToUpdate);

            await axios.put(`http://localhost:8000/usuarios/${usuario_id}`, dataToUpdate);
            alert('Perfil actualizado con éxito');
        } catch (error) {
            console.error('Error al actualizar el perfil:', error.response?.data || error.message);
            alert('Hubo un error al actualizar el perfil');
        }
    };

    return (
        <div className={`${styles.profileSettingsContainer} container mt-1`}>
            <h2 className={`${styles.title} mb-4`}>Configuración de Perfil</h2>
            <form onSubmit={handleSubmit} className={styles.formContainer}>
                <div className="form-group">
                    <label className={styles.boldLabel}>
                        <FontAwesomeIcon icon={faUser} className={styles.icon} /> Nombre
                    </label>
                    <input
                        type="text"
                        className="form-control"
                        value={usuario.nombre}
                        onChange={(e) => setUsuario({ ...usuario, nombre: e.target.value })}
                        required
                    />
                </div>
                <div className="form-group mt-3">
                    <label className={styles.boldLabel}>
                        <FontAwesomeIcon icon={faEnvelope} className={styles.icon} /> Email
                    </label>
                    <input
                        type="email"
                        className="form-control"
                        value={usuario.email}
                        onChange={(e) => setUsuario({ ...usuario, email: e.target.value })}
                        required
                    />
                </div>
                <div className="form-group mt-3">
                    <label className={styles.boldLabel}>
                        <FontAwesomeIcon icon={faLock} className={styles.icon} /> Contraseña
                    </label>
                    <input
                        type="password"
                        className="form-control"
                        value={usuario.contraseña}
                        onChange={(e) => setUsuario({ ...usuario, contraseña: e.target.value })}
                        placeholder="Ingrese nueva contraseña (opcional)"
                    />
                </div>
                <button type="submit" className="btn btn-primary mt-4">Guardar Cambios</button>
            </form>
        </div>
    );
};

export default ProfileSettings;



import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import Sidebar from '../../components/Sidebar';
import Header from '../../layouts/Header';
import Footer from '../../layouts/Footer';
import styles from './styles/editar-usuario.module.css';
import { useRouter } from 'next/router';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser, faEnvelope, faPhone, faMapMarkedAlt, faLock, faUserTag, faEdit } from '@fortawesome/free-solid-svg-icons';

const EditarUsuario = () => {
  const router = useRouter();
  const { usuario_id } = router.query;

  const [usuario, setUsuario] = useState({
    nombre: '',
    email: '',
    telefono: '',
    direccion: '',
    rol_id: '', // Cambiado a rol_id
    contraseña: '' // Campo de contraseña
  });

  useEffect(() => {
    if (usuario_id) {
      axios.get(`http://localhost:8000/usuarios/${usuario_id}`)
        .then(response => {
          const { nombre, email, telefono, direccion, rol_id } = response.data;
          setUsuario({
            nombre,
            email,
            telefono,
            direccion,
            rol_id, // Cambiado a rol_id
            contraseña: '' // No cargar la contraseña por razones de seguridad
          });
        })
        .catch(error => {
          console.error('Error al obtener el usuario:', error);
        });
    }
  }, [usuario_id]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setUsuario({ ...usuario, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const dataToUpdate = {
        nombre: usuario.nombre,
        email: usuario.email,
        telefono: usuario.telefono,
        direccion: usuario.direccion,
        rol_id: parseInt(usuario.rol_id) // Asegurarse de que rol_id sea un número
      };

      // Si se ha ingresado una nueva contraseña, incluirla en la actualización
      if (usuario.contraseña) {
        dataToUpdate.contraseña = usuario.contraseña;
      }

      // Enviar los datos con nombres consistentes con el backend
      await axios.put(`http://localhost:8000/usuarios/${usuario_id}`, dataToUpdate);
      alert('Usuario actualizado con éxito');
      router.push('/usuarios/gestionar-usuarios');
    } catch (error) {
      console.error('Error al actualizar el usuario:', error.response?.data || error.message);
      alert('Hubo un error al actualizar el usuario');
    }
  };

  return (
    <div className={styles.container}>
      <Sidebar />
      <div className={styles.mainContent}>
        <Header />
        <div className="container mt-5">
          <h2 className={styles.title}>
            <FontAwesomeIcon icon={faEdit} className={styles.titleIcon} />Editar Usuario
          </h2>
          <form onSubmit={handleSubmit} className={styles.formContainer}>
            <div className="form-group">
              <label className={styles.boldLabel}>
                <FontAwesomeIcon icon={faUser} className={styles.icon} /> Nombre del Usuario
              </label>
              <input
                type="text"
                className="form-control"
                name="nombre"
                value={usuario.nombre}
                onChange={handleChange}
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
                name="email"
                value={usuario.email}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group mt-3">
              <label className={styles.boldLabel}>
                <FontAwesomeIcon icon={faPhone} className={styles.icon} /> Teléfono
              </label>
              <input
                type="text"
                className="form-control"
                name="telefono"
                value={usuario.telefono}
                onChange={handleChange}
              />
            </div>
            <div className="form-group mt-3">
              <label className={styles.boldLabel}>
                <FontAwesomeIcon icon={faMapMarkedAlt} className={styles.icon} /> Dirección
              </label>
              <textarea
                className="form-control"
                name="direccion"
                value={usuario.direccion}
                onChange={handleChange}
              />
            </div>
            <div className="form-group mt-3">
              <label className={styles.boldLabel}>
                <FontAwesomeIcon icon={faUserTag} className={styles.icon} /> Rol
              </label>
              <select
                className="form-control"
                name="rol_id"
                value={usuario.rol_id} // Cambiado a rol_id
                onChange={handleChange} // Cambiado a rol_id
              >
                <option value="">Seleccione un rol</option>
                <option value="1">Admin</option> {/* Cambiado a valores numéricos */}
                <option value="2">Empleado</option> {/* Cambiado a valores numéricos */}
              </select>
            </div>
            <div className="form-group mt-3">
              <label className={styles.boldLabel}>
                <FontAwesomeIcon icon={faLock} className={styles.icon} /> Contraseña
              </label>
              <input
                type="password"
                className="form-control"
                name="contraseña"
                value={usuario.contraseña}
                onChange={handleChange}
                placeholder="Ingrese nueva contraseña (opcional)"
              />
            </div>
            <button type="submit" className={`${styles.btnPrimary} btn mt-4`}>
              Actualizar Usuario
            </button>
          </form>
        </div>
        <Footer />
      </div>
    </div>
  );
};

export default EditarUsuario;

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import Sidebar from '../../components/Sidebar';
import Header from '../../layouts/Header';
import Footer from '../../layouts/Footer';
import styles from './styles/editar-usuario.module.css';
import { useRouter } from 'next/router';

const EditarUsuario = () => {
  const router = useRouter();
  const { usuario_id } = router.query;

  const [usuario, setUsuario] = useState({
    nombre: '',
    email: '',
    telefono: '',
    direccion: '',
    rol: '',
    contraseña: '' // Campo de contraseña
  });

  useEffect(() => {
    if (usuario_id) {
      axios.get(`http://localhost:8000/usuarios/${usuario_id}`)
        .then(response => {
          const { nombre, email, telefono, direccion, rol } = response.data;
          setUsuario({
            nombre,
            email,
            telefono,
            direccion,
            rol,
            contraseña: '' // No cargar la contraseña por razones de seguridad
          });
        })
        .catch(error => {
          console.error('Error al obtener el usuario:', error);
        });
    }
  }, [usuario_id]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const dataToUpdate = {
        nombre: usuario.nombre,
        email: usuario.email,
        telefono: usuario.telefono,
        direccion: usuario.direccion,
        rol: usuario.rol
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
          <h2 className={styles.title}>Editar Usuario</h2>
          <form onSubmit={handleSubmit} className={styles.formContainer}>
            <div className="form-group">
              <label>Nombre del Usuario</label>
              <input
                type="text"
                className="form-control"
                value={usuario.nombre}
                onChange={(e) => setUsuario({ ...usuario, nombre: e.target.value })}
                required
              />
            </div>
            <div className="form-group mt-3">
              <label>Email</label>
              <input
                type="email"
                className="form-control"
                value={usuario.email}
                onChange={(e) => setUsuario({ ...usuario, email: e.target.value })}
                required
              />
            </div>
            <div className="form-group mt-3">
              <label>Teléfono</label>
              <input
                type="text"
                className="form-control"
                value={usuario.telefono}
                onChange={(e) => setUsuario({ ...usuario, telefono: e.target.value })}
              />
            </div>
            <div className="form-group mt-3">
              <label>Dirección</label>
              <textarea
                className="form-control"
                value={usuario.direccion}
                onChange={(e) => setUsuario({ ...usuario, direccion: e.target.value })}
              />
            </div>
            <div className="form-group mt-3">
              <label>Rol</label>
              <select
                className="form-control"
                value={usuario.rol}
                onChange={(e) => setUsuario({ ...usuario, rol: e.target.value })}
              >
                <option value="admin">admin</option>
                <option value="empleado">empleado</option>
              </select>
            </div>
            <div className="form-group mt-3">
              <label>Contraseña</label>
              <input
                type="password"
                className="form-control"
                value={usuario.contraseña}
                onChange={(e) => setUsuario({ ...usuario, contraseña: e.target.value })}
                placeholder="Ingrese nueva contraseña (opcional)"
              />
            </div>
            <button type="submit" className="btn btn-primary mt-4">Actualizar Usuario</button>
          </form>
        </div>
        <Footer />
      </div>
    </div>
  );
};

export default EditarUsuario;


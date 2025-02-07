import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import Sidebar from '../../components/Sidebar';
import Header from '../../layouts/Header';
import Footer from '../../layouts/Footer';
import styles from './styles/editar-proveedor.module.css';
import { useRouter } from 'next/router';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser, faEnvelope, faPhone, faAddressCard, faIdCard, faEdit } from '@fortawesome/free-solid-svg-icons';

const EditarProveedor = () => {
  const router = useRouter();
  const { proveedor_id } = router.query;

  const [proveedor, setProveedor] = useState({
    nombre: '',
    email: '',
    telefono: '',
    direccion: '',
    rif: ''  // Nuevo estado para RIF
  });
  const [usuarioId, setUsuarioId] = useState(null);  // Nuevo estado para el usuario_id

  useEffect(() => {
    const userId = localStorage.getItem('usuario_id'); // Obtener el usuario_id del almacenamiento local
    setUsuarioId(userId);

    if (proveedor_id) {
      axios.get(`http://localhost:8000/proveedores/${proveedor_id}`)
        .then(response => {
          const { nombre, email, telefono, direccion, rif } = response.data;  // Incluir RIF en la respuesta
          setProveedor({
            nombre,
            email,
            telefono,
            direccion,
            rif  // Asignar RIF al estado
          });
        })
        .catch(error => {
          console.error('Error al obtener el proveedor:', error);
        });
    }
  }, [proveedor_id]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!usuarioId) {
      alert('No se pudo obtener el ID del usuario. Por favor, inicia sesión de nuevo.');
      return;
    }

    try {
      await axios.put(`http://localhost:8000/proveedores/${proveedor_id}`, {
        nombre: proveedor.nombre,
        email: proveedor.email,
        telefono: proveedor.telefono,
        direccion: proveedor.direccion,
        rif: proveedor.rif,  // Incluir RIF en la solicitud de actualización
        usuario_id: usuarioId  // Incluyendo el usuario_id en la solicitud
      });
      alert('Proveedor actualizado con éxito');
      router.push('/proveedores/consultar-proveedores');
    } catch (error) {
      console.error('Error al actualizar el proveedor:', error.response?.data || error.message);
      alert('Hubo un error al actualizar el proveedor');
    }
  };

  return (
    <div className={styles.container}>
      <Sidebar />
      <div className={styles.mainContent}>
        <Header />
        <div className="container mt-5">
          <h2 className={styles.title}>
            <FontAwesomeIcon icon={faEdit} className={styles.titleIcon} />
            Editar Proveedor
          </h2>
          <form onSubmit={handleSubmit} className={styles.formContainer}>
            <div className="form-group">
              <label className={styles.boldLabel}>
                <FontAwesomeIcon icon={faUser} className={styles.icon} /> Nombre del Proveedor
              </label>
              <input
                type="text"
                className="form-control"
                value={proveedor.nombre}
                onChange={(e) => setProveedor({ ...proveedor, nombre: e.target.value })}
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
                value={proveedor.email}
                onChange={(e) => setProveedor({ ...proveedor, email: e.target.value })}
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
                value={proveedor.telefono}
                onChange={(e) => setProveedor({ ...proveedor, telefono: e.target.value })}
                required
              />
            </div>
            <div className="form-group mt-3">
              <label className={styles.boldLabel}>
                <FontAwesomeIcon icon={faAddressCard} className={styles.icon} /> Dirección
              </label>
              <textarea
                className="form-control"
                value={proveedor.direccion}
                onChange={(e) => setProveedor({ ...proveedor, direccion: e.target.value })}
              />
            </div>
            <div className="form-group mt-3">
              <label className={styles.boldLabel}>
                <FontAwesomeIcon icon={faIdCard} className={styles.icon} /> RIF
              </label> {/* Nuevo campo para RIF */}
              <input
                type="text"
                className="form-control"
                value={proveedor.rif}
                onChange={(e) => setProveedor({ ...proveedor, rif: e.target.value })}  // Actualiza el RIF
                required
              />
            </div>
            <button type="submit" className={`${styles.btnPrimary} btn mt-4`}>Actualizar Proveedor</button>
          </form>
        </div>
        <Footer />
      </div>
    </div>
  );
};

export default EditarProveedor;


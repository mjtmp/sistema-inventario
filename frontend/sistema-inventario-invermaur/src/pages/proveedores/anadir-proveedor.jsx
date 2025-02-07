import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import Sidebar from '../../components/Sidebar';
import Header from '../../layouts/Header';
import Footer from '../../layouts/Footer';
import styles from './styles/anadir-proveedor.module.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser, faEnvelope, faPhone, faAddressCard, faIdCard, faPlusCircle } from '@fortawesome/free-solid-svg-icons';

const AnadirProveedor = () => {
  const [nombre, setNombre] = useState('');
  const [email, setEmail] = useState('');
  const [telefono, setTelefono] = useState('');
  const [direccion, setDireccion] = useState('');
  const [rif, setRif] = useState('');
  const [usuarioId, setUsuarioId] = useState(null);  // Nuevo estado para el usuario_id

  useEffect(() => {
    const userId = localStorage.getItem('usuario_id'); // Obtener el usuario_id del almacenamiento local
    setUsuarioId(userId);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!nombre || !email || !telefono || !rif) {
      alert('Por favor complete todos los campos requeridos');
      return;
    }

    if (!usuarioId) {
      alert('No se pudo obtener el ID del usuario. Por favor, inicia sesión de nuevo.');
      return;
    }

    try {
      // Verificar si el número de RIF ya existe
      const response = await axios.get(`http://localhost:8000/proveedores/buscar-por-rif?rif=${rif}`);
      if (response.data.length > 0) {
        alert('El número de RIF ya existe. Por favor, intenta con un número distinto.');
        return;
      }

      await axios.post('http://localhost:8000/proveedores', {
        nombre,
        email,
        telefono,
        direccion,
        rif,
        usuario_id: usuarioId  // Incluyendo el usuario_id en la solicitud
      });
      alert('Proveedor añadido exitosamente');
      setNombre('');
      setEmail('');
      setTelefono('');
      setDireccion('');
      setRif('');
    } catch (error) {
      console.error('Error al añadir el proveedor:', error);
      alert('Hubo un error al añadir el proveedor. Por favor, intenta nuevamente.');
    }
  };

  return (
    <div className={styles.container}>
      <Sidebar />
      <div className={styles.mainContent}>
        <Header />
        <div className="container mt-5">
          <h2 className={styles.title}>
            <FontAwesomeIcon icon={faPlusCircle} className={styles.titleIcon} />
            Añadir Proveedor
          </h2>
          <form onSubmit={handleSubmit} className={styles.formContainer}>
            <div className="form-group">
              <label className={styles.boldLabel}>
                <FontAwesomeIcon icon={faUser} className={styles.icon} /> Nombre del Proveedor
              </label>
              <input 
                type="text" 
                className="form-control" 
                value={nombre} 
                onChange={(e) => setNombre(e.target.value)} 
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
                value={email} 
                onChange={(e) => setEmail(e.target.value)} 
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
                value={telefono} 
                onChange={(e) => setTelefono(e.target.value)} 
                required 
              />
            </div>
            <div className="form-group mt-3">
              <label className={styles.boldLabel}>
                <FontAwesomeIcon icon={faAddressCard} className={styles.icon} /> Dirección
              </label>
              <textarea 
                className="form-control" 
                value={direccion} 
                onChange={(e) => setDireccion(e.target.value)} 
              />
            </div>
            <div className="form-group mt-3">
              <label className={styles.boldLabel}>
                <FontAwesomeIcon icon={faIdCard} className={styles.icon} /> RIF
              </label>
              <input 
                type="text" 
                className="form-control" 
                value={rif} 
                onChange={(e) => setRif(e.target.value)} 
                required 
              />
            </div>
            <button type="submit" className={`${styles.btnPrimary} btn mt-4`}>Añadir Proveedor</button>
          </form>
        </div>
        <Footer />
      </div>
    </div>
  );
};

export default AnadirProveedor;


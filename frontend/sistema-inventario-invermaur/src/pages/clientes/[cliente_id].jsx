import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import Sidebar from '../../components/Sidebar';
import Header from '../../layouts/Header';
import Footer from '../../layouts/Footer';
import styles from './styles/editar-cliente.module.css';
import { useRouter } from 'next/router';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser, faEnvelope, faPhone, faAddressCard, faIdCard, faEdit } from '@fortawesome/free-solid-svg-icons';

const EditarCliente = () => {
  const router = useRouter();
  const { cliente_id } = router.query;

  const [cliente, setCliente] = useState({
    nombre: '',
    email: '',
    telefono: '',
    direccion: '',
    tipo_documento: '',  // Nuevo estado para tipo de documento
    numero_documento: ''  // Nuevo estado para número de documento
  });
  const [usuarioId, setUsuarioId] = useState(null);

  useEffect(() => {
    const userId = localStorage.getItem('usuario_id'); // Obtener el usuario_id del almacenamiento local
    setUsuarioId(userId);

    if (cliente_id) {
      axios.get(`http://localhost:8000/clientes/${cliente_id}`)
        .then(response => {
          const { nombre, email, telefono, direccion, tipo_documento, numero_documento } = response.data;
          setCliente({
            nombre,
            email,
            telefono,
            direccion,
            tipo_documento,
            numero_documento
          });
        })
        .catch(error => {
          console.error('Error al obtener el cliente:', error);
        });
    }
  }, [cliente_id]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!usuarioId) {
      alert('No se pudo obtener el ID del usuario. Por favor, inicia sesión de nuevo.');
      return;
    }

    console.log('Usuario ID:', usuarioId); // Verificar usuario_id
    console.log('Datos a enviar:', {
      nombre: cliente.nombre,
      email: cliente.email,
      telefono: cliente.telefono,
      direccion: cliente.direccion,
      tipo_documento: cliente.tipo_documento,
      numero_documento: cliente.numero_documento,
      usuario_id: usuarioId
    }); // Verificar los datos que se enviarán

    try {
      await axios.put(`http://localhost:8000/clientes/${cliente_id}`, {
        nombre: cliente.nombre,
        email: cliente.email,
        telefono: cliente.telefono,
        direccion: cliente.direccion,
        tipo_documento: cliente.tipo_documento,
        numero_documento: cliente.numero_documento,
        usuario_id: usuarioId // Incluyendo el usuario_id en la solicitud
      });
      alert('Cliente actualizado con éxito');
      router.push('/clientes/consultar-clientes');
    } catch (error) {
      console.error('Error al actualizar el cliente:', error.response?.data || error.message);
      alert('Hubo un error al actualizar el cliente');
    }
  };

  return (
    <div className={styles.container}>
      <Sidebar />
      <div className={styles.mainContent}>
        <Header />
        <div className="container mt-5">
          <h2 className={styles.title}>
            <FontAwesomeIcon icon={faEdit} className={styles.titleIcon} />Editar Cliente
          </h2>
          <form onSubmit={handleSubmit} className={styles.formContainer}>
            <div className="form-group">
              <label className={styles.boldLabel}>
                <FontAwesomeIcon icon={faUser} className={styles.icon} />Nombre del Cliente
              </label>
              <input
                type="text"
                className="form-control"
                value={cliente.nombre}
                onChange={(e) => setCliente({ ...cliente, nombre: e.target.value })}
                required
              />
            </div>
            <div className="form-group mt-3">
              <label className={styles.boldLabel}>
                <FontAwesomeIcon icon={faEnvelope} className={styles.icon} />Email
              </label>
              <input
                type="email"
                className="form-control"
                value={cliente.email}
                onChange={(e) => setCliente({ ...cliente, email: e.target.value })}
                required
              />
            </div>
            <div className="form-group mt-3">
              <label className={styles.boldLabel}>
                <FontAwesomeIcon icon={faPhone} className={styles.icon} />Teléfono
              </label>
              <input
                type="text"
                className="form-control"
                value={cliente.telefono}
                onChange={(e) => setCliente({ ...cliente, telefono: e.target.value })}
                required
              />
            </div>
            <div className="form-group mt-3">
              <label className={styles.boldLabel}>
                <FontAwesomeIcon icon={faAddressCard} className={styles.icon} />Dirección
              </label>
              <textarea
                className="form-control"
                value={cliente.direccion}
                onChange={(e) => setCliente({ ...cliente, direccion: e.target.value })}
              />
            </div>
            <div className="form-group mt-3">
              <label className={styles.boldLabel}>
                <FontAwesomeIcon icon={faIdCard} className={styles.icon} />Tipo de Documento
              </label> {/* Nuevo campo tipo de documento */}
              <select
                className="form-control"
                value={cliente.tipo_documento}
                onChange={(e) => setCliente({ ...cliente, tipo_documento: e.target.value })}
                required
              >
                <option value="">Selecciona un tipo de documento</option>
                <option value="CV">Cédula Venezolana</option>
                <option value="CE">Cédula Extranjera</option>
                <option value="PAS">Pasaporte</option>
                <option value="RIF-N">RIF - Personal Natural</option>
                <option value="RIF-J">RIF - Persona Juridica</option>
                <option value="RIF-E">RIF - E</option>
              </select>
            </div>
            <div className="form-group mt-3">
              <label className={styles.boldLabel}>
                <FontAwesomeIcon icon={faIdCard} className={styles.icon} />Número de Documento
              </label> {/* Nuevo campo número de documento */}
              <input
                type="text"
                className="form-control"
                value={cliente.numero_documento}
                onChange={(e) => setCliente({ ...cliente, numero_documento: e.target.value })}
                required
              />
            </div>
            <button type="submit" className={`${styles.btnPrimary} btn mt-4`}>Actualizar Cliente</button>
          </form>
        </div>
        <Footer />
      </div>
    </div>
  );
};

export default EditarCliente;


import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import Sidebar from '../../components/Sidebar';
import Header from '../../layouts/Header';
import Footer from '../../layouts/Footer';
import styles from './styles/anadir-cliente.module.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser, faEnvelope, faPhone, faAddressCard, faIdCard, faPlusCircle } from '@fortawesome/free-solid-svg-icons';

const AnadirCliente = () => {
  const [nombre, setNombre] = useState('');
  const [email, setEmail] = useState('');
  const [telefono, setTelefono] = useState('');
  const [direccion, setDireccion] = useState('');
  const [tipoDocumento, setTipoDocumento] = useState('');
  const [numeroDocumento, setNumeroDocumento] = useState('');
  const [usuarioId, setUsuarioId] = useState(null);

  useEffect(() => {
    const userId = localStorage.getItem('usuario_id'); // Obtener el usuario_id del almacenamiento local
    setUsuarioId(userId);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!nombre || !email || !telefono || !tipoDocumento || !numeroDocumento) {
      alert('Por favor complete todos los campos requeridos');
      return;
    }

    if (!usuarioId) {
      alert('No se pudo obtener el ID del usuario. Por favor, inicia sesión de nuevo.');
      return;
    }

    const clienteData = {
      nombre,
      email,
      telefono,
      direccion,
      tipo_documento: tipoDocumento,
      numero_documento: numeroDocumento,
      usuario_id: usuarioId  // Incluyendo el usuario_id en la solicitud
    };

    console.log('Usuario ID:', usuarioId); // Verificar usuario_id
    console.log('Datos a enviar:', clienteData); // Verificar los datos que se enviarán

    try {
      // Verificar si el número de documento ya existe
      const response = await axios.get(`http://localhost:8000/clientes/buscar-por-documento?numero_documento=${numeroDocumento}`);
      if (response.data.length > 0) {
        alert('El número de documento ya existe. Por favor, intenta con un número distinto.');
        return;
      }

      await axios.post('http://localhost:8000/clientes', clienteData);
      alert('Cliente añadido exitosamente');
      setNombre('');
      setEmail('');
      setTelefono('');
      setDireccion('');
      setTipoDocumento('');
      setNumeroDocumento('');
    } catch (error) {
      console.error('Error al añadir el cliente:', error);
      alert('Hubo un error al añadir el cliente. Intente nuevamente.');
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
            Añadir Cliente
          </h2>
          <form onSubmit={handleSubmit} className={styles.formContainer}>
            <div className="form-group">
              <label className={styles.boldLabel}>
                <FontAwesomeIcon icon={faUser} className={styles.icon} /> Nombre del Cliente
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
                <FontAwesomeIcon icon={faIdCard} className={styles.icon} /> Tipo de Documento
              </label>
              <select 
                className="form-control"
                value={tipoDocumento}
                onChange={(e) => setTipoDocumento(e.target.value)}
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
                <FontAwesomeIcon icon={faIdCard} className={styles.icon} /> Número de Documento
              </label>
              <input 
                type="text" 
                className="form-control" 
                value={numeroDocumento} 
                onChange={(e) => setNumeroDocumento(e.target.value)} 
                required 
              />
            </div>
            <button type="submit" className={`${styles.btnPrimary} btn mt-4`}>Añadir Cliente</button>
          </form>
        </div>
        <Footer />
      </div>
    </div>
  );
};

export default AnadirCliente;







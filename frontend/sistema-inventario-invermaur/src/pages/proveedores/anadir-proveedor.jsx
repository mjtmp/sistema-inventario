import React, { useState } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import Sidebar from '../../components/Sidebar'; // Componente para la barra lateral
import Header from '../../layouts/Header'; // Componente para el encabezado
import Footer from '../../layouts/Footer'; // Componente para el pie de página
import styles from './styles/anadir-proveedor.module.css'; // Estilos locales del componente

const AñadirProveedor = () => {
  // Estados para manejar los campos del formulario
  const [nombre, setNombre] = useState('');
  const [email, setEmail] = useState('');
  const [telefono, setTelefono] = useState('');
  const [direccion, setDireccion] = useState('');

  // Función que se ejecuta cuando se envía el formulario
  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevenir el comportamiento por defecto del formulario

    // Validar que los campos obligatorios no estén vacíos
    if (!nombre || !email || !telefono) {
      alert('Por favor complete todos los campos requeridos');
      return;
    }

    try {
      // Enviamos los datos del nuevo proveedor a la API
      await axios.post('http://localhost:8000/proveedores', {
        nombre,
        email,
        telefono,
        direccion
      });
      alert('Proveedor añadido exitosamente'); // Mensaje de éxito
      // Limpiamos los campos después de añadir el proveedor
      setNombre('');
      setEmail('');
      setTelefono('');
      setDireccion('');
    } catch (error) {
      console.error('Error al añadir el proveedor:', error); // Manejo de errores
      alert('Hubo un error al añadir el proveedor'); // Mensaje de error
    }
  };

  return (
    <div className={styles.container}>
      <Sidebar /> {/* Barra lateral */}
      <div className={styles.mainContent}>
        <Header /> {/* Cabecera */}
        <div className="container mt-5">
          <h2 className={styles.title}>Añadir Proveedor</h2>
          {/* Formulario para añadir un nuevo proveedor */}
          <form onSubmit={handleSubmit} className={styles.formContainer}>
            <div className="form-group">
              <label>Nombre del Proveedor</label>
              <input 
                type="text" 
                className="form-control" 
                value={nombre} 
                onChange={(e) => setNombre(e.target.value)} // Actualiza el nombre
                required 
              />
            </div>
            <div className="form-group mt-3">
              <label>Email</label>
              <input 
                type="email" 
                className="form-control" 
                value={email} 
                onChange={(e) => setEmail(e.target.value)} // Actualiza el email
                required 
              />
            </div>
            <div className="form-group mt-3">
              <label>Teléfono</label>
              <input 
                type="text" 
                className="form-control" 
                value={telefono} 
                onChange={(e) => setTelefono(e.target.value)} // Actualiza el teléfono
                required 
              />
            </div>
            <div className="form-group mt-3">
              <label>Dirección</label>
              <textarea 
                className="form-control" 
                value={direccion} 
                onChange={(e) => setDireccion(e.target.value)} // Actualiza la dirección
              />
            </div>
            <button type="submit" className="btn btn-primary mt-4">Añadir Proveedor</button> {/* Botón de envío */}
          </form>
        </div>
        <Footer /> {/* Pie de página */}
      </div>
    </div>
  );
};

export default AñadirProveedor; // Exportamos el componente

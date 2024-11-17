// Importación de dependencias y componentes necesarios
import React, { useState } from 'react'; // useState es un hook de React para gestionar el estado
import axios from 'axios'; // Axios para realizar peticiones HTTP
import 'bootstrap/dist/css/bootstrap.min.css'; // Estilos de Bootstrap
import Sidebar from '../../components/Sidebar'; // Sidebar componente
import Header from '../../layouts/Header'; // Header del sitio
import Footer from '../../layouts/Footer'; // Footer del sitio
import styles from './styles/anadir-cliente.module.css'; // Estilos personalizados para este componente

const AñadirCliente = () => {
  // Estados para almacenar los datos del cliente a añadir
  const [nombre, setNombre] = useState('');
  const [email, setEmail] = useState('');
  const [telefono, setTelefono] = useState('');
  const [direccion, setDireccion] = useState('');

  // Función que se ejecuta cuando el formulario se envía
  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevenir comportamiento por defecto del formulario

    // Validación básica para asegurarse de que los campos obligatorios estén completos
    if (!nombre || !email || !telefono) {
      alert('Por favor complete todos los campos requeridos');
      return;
    }

    try {
      // Realiza una solicitud POST para añadir el nuevo cliente
      await axios.post('http://localhost:8000/clientes', {
        nombre,
        email,
        telefono,
        direccion
      });
      alert('Cliente añadido exitosamente'); // Mensaje de éxito
      setNombre(''); // Reinicia el campo nombre
      setEmail(''); // Reinicia el campo email
      setTelefono(''); // Reinicia el campo teléfono
      setDireccion(''); // Reinicia el campo dirección
    } catch (error) {
      console.error('Error al añadir el cliente:', error); // Manejo de errores
      alert('Hubo un error al añadir el cliente'); // Mensaje de error si algo falla
    }
  };

  return (
    <div className={styles.container}>
      <Sidebar /> {/* Componente del sidebar */}
      <div className={styles.mainContent}>
        <Header /> {/* Componente del header */}
        <div className="container mt-5">
          <h2 className={styles.title}>Añadir Cliente</h2>
          <form onSubmit={handleSubmit} className={styles.formContainer}>
            {/* Campos del formulario para añadir un nuevo cliente */}
            <div className="form-group">
              <label>Nombre del Cliente</label>
              <input 
                type="text" 
                className="form-control" 
                value={nombre} 
                onChange={(e) => setNombre(e.target.value)} 
                required 
              />
            </div>
            <div className="form-group mt-3">
              <label>Email</label>
              <input 
                type="email" 
                className="form-control" 
                value={email} 
                onChange={(e) => setEmail(e.target.value)} 
                required 
              />
            </div>
            <div className="form-group mt-3">
              <label>Teléfono</label>
              <input 
                type="text" 
                className="form-control" 
                value={telefono} 
                onChange={(e) => setTelefono(e.target.value)} 
                required 
              />
            </div>
            <div className="form-group mt-3">
              <label>Dirección</label>
              <textarea 
                className="form-control" 
                value={direccion} 
                onChange={(e) => setDireccion(e.target.value)} 
              />
            </div>
            <button type="submit" className="btn btn-primary mt-4">Añadir Cliente</button> {/* Botón para enviar el formulario */}
          </form>
        </div>
        <Footer /> {/* Componente del footer */}
      </div>
    </div>
  );
};

export default AñadirCliente; // Exporta el componente para su uso en otras partes de la aplicación


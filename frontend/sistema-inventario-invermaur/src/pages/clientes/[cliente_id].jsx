// Importación de dependencias y componentes necesarios
import React, { useState, useEffect } from 'react'; // useState y useEffect son hooks de React
import axios from 'axios'; // Axios para realizar peticiones HTTP
import 'bootstrap/dist/css/bootstrap.min.css'; // Estilos de Bootstrap para el diseño
import Sidebar from '../../components/Sidebar'; // Sidebar componente
import Header from '../../layouts/Header'; // Header del sitio
import Footer from '../../layouts/Footer'; // Footer del sitio
import styles from './styles/editar-cliente.module.css'; // Estilos personalizados para este componente
import { useRouter } from 'next/router'; // useRouter para manejar rutas de Next.js

const EditarCliente = () => {
  // Obtiene el parametro cliente_id desde la URL
  const router = useRouter();
  const { cliente_id } = router.query;

  // Estado para almacenar la información del cliente
  const [cliente, setCliente] = useState({
    nombre: '',
    email: '',
    telefono: '',
    direccion: ''
  });

  // Hook de efecto para obtener la información del cliente desde el backend
  useEffect(() => {
    if (cliente_id) {
      axios.get(`http://localhost:8000/clientes/${cliente_id}`) // Se hace una solicitud GET al backend
        .then(response => {
          // Al recibir la respuesta, se establece el estado del cliente con los datos obtenidos
          const { nombre, email, telefono, direccion } = response.data;
          setCliente({
            nombre,
            email,
            telefono,
            direccion
          });
        })
        .catch(error => {
          console.error('Error al obtener el cliente:', error); // Manejo de errores
        });
    }
  }, [cliente_id]); // Este efecto solo se ejecuta cuando el cliente_id cambia

  // Función para manejar el formulario de edición
  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevenir comportamiento por defecto del formulario

    try {
      // Se realiza una solicitud PUT para actualizar el cliente en el backend
      await axios.put(`http://localhost:8000/clientes/${cliente_id}`, {
        nombre: cliente.nombre,
        email: cliente.email,
        telefono: cliente.telefono,
        direccion: cliente.direccion
      });
      alert('Cliente actualizado con éxito'); // Mensaje de éxito
      router.push('/clientes/consultar-clientes'); // Redirige a la página de clientes después de la actualización
    } catch (error) {
      console.error('Error al actualizar el cliente:', error.response?.data || error.message);
      alert('Hubo un error al actualizar el cliente'); // Mensaje de error si algo falla
    }
  };

  return (
    <div className={styles.container}>
      <Sidebar /> {/* Componente del sidebar */}
      <div className={styles.mainContent}>
        <Header /> {/* Componente del header */}
        <div className="container mt-5">
          <h2 className={styles.title}>Editar Cliente</h2>
          <form onSubmit={handleSubmit} className={styles.formContainer}>
            {/* Campos del formulario para editar los datos del cliente */}
            <div className="form-group">
              <label>Nombre del Cliente</label>
              <input
                type="text"
                className="form-control"
                value={cliente.nombre}
                onChange={(e) => setCliente({ ...cliente, nombre: e.target.value })}
                required
              />
            </div>
            <div className="form-group mt-3">
              <label>Email</label>
              <input
                type="email"
                className="form-control"
                value={cliente.email}
                onChange={(e) => setCliente({ ...cliente, email: e.target.value })}
                required
              />
            </div>
            <div className="form-group mt-3">
              <label>Teléfono</label>
              <input
                type="text"
                className="form-control"
                value={cliente.telefono}
                onChange={(e) => setCliente({ ...cliente, telefono: e.target.value })}
                required
              />
            </div>
            <div className="form-group mt-3">
              <label>Dirección</label>
              <textarea
                className="form-control"
                value={cliente.direccion}
                onChange={(e) => setCliente({ ...cliente, direccion: e.target.value })}
              />
            </div>
            <button type="submit" className="btn btn-primary mt-4">Actualizar Cliente</button> {/* Botón de envío */}
          </form>
        </div>
        <Footer /> {/* Componente del footer */}
      </div>
    </div>
  );
};

export default EditarCliente; // Exporta el componente para su uso en otras partes de la aplicación


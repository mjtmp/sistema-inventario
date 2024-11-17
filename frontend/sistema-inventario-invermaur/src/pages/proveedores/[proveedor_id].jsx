import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import Sidebar from '../../components/Sidebar'; // Componente para la barra lateral
import Header from '../../layouts/Header'; // Componente para el encabezado
import Footer from '../../layouts/Footer'; // Componente para el pie de página
import styles from './styles/editar-proveedor.module.css'; // Estilos locales del componente
import { useRouter } from 'next/router'; // Hook para manejo de rutas en Next.js

const EditarProveedor = () => {
  const router = useRouter(); // Usamos el hook para obtener el id del proveedor en la URL
  const { proveedor_id } = router.query; // Extraemos el id del proveedor desde la URL

  // Estado para manejar los datos del proveedor
  const [proveedor, setProveedor] = useState({
    nombre: '',
    email: '',
    telefono: '',
    direccion: ''
  });

  // useEffect para cargar los datos del proveedor desde la API cuando se obtenga el id
  useEffect(() => {
    if (proveedor_id) {
      axios.get(`http://localhost:8000/proveedores/${proveedor_id}`) // Llamada a la API para obtener el proveedor
        .then(response => {
          const { nombre, email, telefono, direccion } = response.data; // Desestructuramos la respuesta
          setProveedor({
            nombre,
            email,
            telefono,
            direccion
          });
        })
        .catch(error => {
          console.error('Error al obtener el proveedor:', error); // Manejo de errores en la obtención
        });
    }
  }, [proveedor_id]); // Dependencia en proveedor_id, se ejecuta cuando cambia

  // Función que se ejecuta cuando se envía el formulario
  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevenir el comportamiento por defecto del formulario

    try {
      // Actualizamos el proveedor en la base de datos mediante una solicitud PUT
      await axios.put(`http://localhost:8000/proveedores/${proveedor_id}`, {
        nombre: proveedor.nombre,
        email: proveedor.email,
        telefono: proveedor.telefono,
        direccion: proveedor.direccion
      });
      alert('Proveedor actualizado con éxito'); // Mensaje de éxito
      router.push('/proveedores/consultar-proveedores'); // Redirigir a la lista de proveedores
    } catch (error) {
      console.error('Error al actualizar el proveedor:', error.response?.data || error.message); // Manejo de errores
      alert('Hubo un error al actualizar el proveedor'); // Mensaje de error
    }
  };

  return (
    <div className={styles.container}>
      <Sidebar /> {/* Barra lateral */}
      <div className={styles.mainContent}>
        <Header /> {/* Cabecera */}
        <div className="container mt-5">
          <h2 className={styles.title}>Editar Proveedor</h2>
          {/* Formulario para editar el proveedor */}
          <form onSubmit={handleSubmit} className={styles.formContainer}>
            <div className="form-group">
              <label>Nombre del Proveedor</label>
              <input
                type="text"
                className="form-control"
                value={proveedor.nombre}
                onChange={(e) => setProveedor({ ...proveedor, nombre: e.target.value })} // Actualiza el nombre
                required
              />
            </div>
            <div className="form-group mt-3">
              <label>Email</label>
              <input
                type="email"
                className="form-control"
                value={proveedor.email}
                onChange={(e) => setProveedor({ ...proveedor, email: e.target.value })} // Actualiza el email
                required
              />
            </div>
            <div className="form-group mt-3">
              <label>Teléfono</label>
              <input
                type="text"
                className="form-control"
                value={proveedor.telefono}
                onChange={(e) => setProveedor({ ...proveedor, telefono: e.target.value })} // Actualiza el teléfono
                required
              />
            </div>
            <div className="form-group mt-3">
              <label>Dirección</label>
              <textarea
                className="form-control"
                value={proveedor.direccion}
                onChange={(e) => setProveedor({ ...proveedor, direccion: e.target.value })} // Actualiza la dirección
              />
            </div>
            <button type="submit" className="btn btn-primary mt-4">Actualizar Proveedor</button> {/* Botón de envío */}
          </form>
        </div>
        <Footer /> {/* Pie de página */}
      </div>
    </div>
  );
};

export default EditarProveedor; // Exportamos el componente

  

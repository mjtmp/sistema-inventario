import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import Sidebar from '../../components/Sidebar';
import Header from '../../layouts/Header';
import Footer from '../../layouts/Footer';
import styles from './styles/anadir-categoria.module.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlusCircle } from '@fortawesome/free-solid-svg-icons';

const AñadirCategoria = () => {
  const [nombre, setNombre] = useState('');
  const [usuarioId, setUsuarioId] = useState(null);

  useEffect(() => {
    const userId = localStorage.getItem('usuario_id'); // Obtener el usuario_id del almacenamiento local
    setUsuarioId(userId);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!nombre || !usuarioId) {
      alert('Por favor complete todos los campos requeridos');
      return;
    }

    const categoriaData = {
      nombre,
      usuario_id: usuarioId  // Incluyendo el usuario_id en la solicitud
    };

    try {
      await axios.post('http://localhost:8000/categorias', categoriaData);
      alert('Categoría añadida exitosamente');
      setNombre('');
    } catch (error) {
      console.error('Error al añadir la categoría:', error);
      alert('Hubo un error al añadir la categoría. Intente nuevamente.');
    }
  };

  return (
    <div className={styles.container}>
      <Sidebar />
      <div className={styles.mainContent}>
        <Header />
        <div className="container mt-5">
          <h2 className={styles.title}>
            <FontAwesomeIcon icon={faPlusCircle} className={styles.icon} /> Añadir Categoría
          </h2>
          <form onSubmit={handleSubmit} className={styles.formContainer}>
            <div className="form-group">
              <label className={styles.boldLabel}>Nombre de la Categoría</label>
              <input
                type="text"
                className={`form-control ${styles.inputField}`}
                value={nombre}
                onChange={(e) => setNombre(e.target.value)}
                required
              />
            </div>
            <button type="submit" className={`btn btn-primary ${styles.submitButton}`}>
              Añadir Categoría
            </button>
          </form>
        </div>
        <Footer />
      </div>
    </div>
  );
};

export default AñadirCategoria;



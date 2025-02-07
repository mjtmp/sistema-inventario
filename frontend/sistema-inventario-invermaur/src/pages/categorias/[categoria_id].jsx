import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import Sidebar from '../../components/Sidebar';
import Header from '../../layouts/Header';
import Footer from '../../layouts/Footer';
import styles from './styles/editar-categoria.module.css';
import { useRouter } from 'next/router';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEdit } from '@fortawesome/free-solid-svg-icons';

const EditarCategoria = () => {
  const router = useRouter();
  const { categoria_id } = router.query;

  const [categoria, setCategoria] = useState({ nombre: '' });
  const [usuarioId, setUsuarioId] = useState(null);

  useEffect(() => {
    const userId = localStorage.getItem('usuario_id'); // Obtener el usuario_id del almacenamiento local
    setUsuarioId(userId);

    if (categoria_id) {
      axios.get(`http://localhost:8000/categorias/${categoria_id}`)
        .then(response => {
          setCategoria(response.data);
        })
        .catch(error => {
          console.error('Error al obtener la categoría:', error);
        });
    }
  }, [categoria_id]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!usuarioId) {
      alert('No se pudo obtener el ID del usuario. Por favor, inicia sesión de nuevo.');
      return;
    }

    console.log('Usuario ID:', usuarioId); // Verificar usuario_id
    console.log('Datos a enviar:', {
      nombre: categoria.nombre,
      usuario_id: usuarioId
    }); // Verificar los datos que se enviarán

    try {
      await axios.put(`http://localhost:8000/categorias/${categoria_id}`, {
        nombre: categoria.nombre,
        usuario_id: usuarioId // Incluyendo el usuario_id en la solicitud
      });
      alert('Categoría actualizada con éxito');
      router.push('/categorias/consultar-categorias');
    } catch (error) {
      console.error('Error al actualizar la categoría:', error.response?.data || error.message);
      alert('Hubo un error al actualizar la categoría');
    }
  };

  return (
    <div className={styles.container}>
      <Sidebar />
      <div className={styles.mainContent}>
        <Header />
        <div className="container mt-5">
          <h2 className={styles.title}>
            <FontAwesomeIcon icon={faEdit} className={styles.icon} /> Editar Categoría
          </h2>
          <form onSubmit={handleSubmit} className={styles.formContainer}>
            <div className="form-group">
              <label className={styles.boldLabel}>Nombre de la Categoría</label>
              <input
                type="text"
                className={`form-control ${styles.inputField}`}
                value={categoria.nombre}
                onChange={(e) => setCategoria({ ...categoria, nombre: e.target.value })}
                required
              />
            </div>
            <button type="submit" className={`btn btn-primary ${styles.submitButton}`}>
              Actualizar Categoría
            </button>
          </form>
        </div>
        <Footer />
      </div>
    </div>
  );
};

export default EditarCategoria;


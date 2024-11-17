import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import Sidebar from '../../components/Sidebar';
import Header from '../../layouts/Header';
import Footer from '../../layouts/Footer';
import styles from './styles/consultar-proveedores.module.css';
import Link from 'next/link';

// Componente para consultar proveedores
const ConsultarProveedores = () => {
  // Estado para almacenar los proveedores obtenidos desde la API
  const [proveedores, setProveedores] = useState([]);
  // Estado para almacenar el término de búsqueda
  const [searchTerm, setSearchTerm] = useState('');
  // Estado para la página actual de la paginación
  const [page, setPage] = useState(1);
  // Estado para definir cuántos proveedores mostrar por página
  const [limit, setLimit] = useState(10);
  // Estado para almacenar el total de proveedores
  const [totalProveedores, setTotalProveedores] = useState(0);

  // useEffect para cargar los proveedores cada vez que la página o límite cambian
  useEffect(() => {
    const fetchProveedores = async () => {
      try {
        // Realiza la petición GET a la API para obtener proveedores con paginación
        const response = await axios.get(`http://localhost:8000/proveedores?page=${page}&limit=${limit}`);
        setProveedores(response.data.proveedores); // Establece los proveedores obtenidos
        setTotalProveedores(response.data.total); // Establece el total de proveedores
      } catch (error) {
        // Manejo de errores si la API no responde correctamente
        console.error('Error al cargar los proveedores:', error);
      }
    };
    fetchProveedores(); // Llama la función para obtener proveedores
  }, [page, limit]); // Dependencias para recargar cuando cambia la página o el límite

  // Filtra los proveedores según el término de búsqueda (filtra por nombre)
  const filteredProveedores = proveedores
    ? proveedores.filter(proveedor =>
        proveedor.nombre.toLowerCase().includes(searchTerm.toLowerCase())
      )
    : [];

  // Función para eliminar un proveedor
  const handleDelete = async (proveedor_id) => {
    const confirmDelete = window.confirm('¿Estás seguro de que deseas eliminar este proveedor?');
    if (confirmDelete) {
      try {
        // Realiza la petición DELETE a la API para eliminar el proveedor
        await axios.delete(`http://localhost:8000/proveedores/${proveedor_id}`);
        setProveedores(proveedores.filter(proveedor => proveedor.proveedor_id !== proveedor_id)); // Actualiza la lista de proveedores
        alert('Proveedor eliminado exitosamente');
      } catch (error) {
        // Manejo de errores si no se puede eliminar el proveedor
        console.error('Error al eliminar el proveedor:', error);
        alert('Hubo un error al eliminar el proveedor');
      }
    }
  };

  // Calcula el total de páginas en base al número de proveedores y el límite
  const totalPages = Math.ceil(totalProveedores / limit);

  // Funciones para cambiar de página en la paginación
  const handleNextPage = () => {
    if (page < totalPages) {
      setPage(page + 1); // Avanza a la siguiente página si no es la última
    }
  };

  const handlePreviousPage = () => {
    if (page > 1) {
      setPage(page - 1); // Regresa a la página anterior si no es la primera
    }
  };

  return (
    <div className={styles.container}>
      <Sidebar /> {/* Componente de la barra lateral */}
      <div className={styles.mainContent}>
        <Header /> {/* Componente del encabezado */}
        <div className="container mt-5">
          <h2 className={styles.title}>Consultar Proveedores</h2>
          {/* Campo de búsqueda para filtrar proveedores por nombre */}
          <input
            type="text"
            className="form-control mb-4"
            placeholder="Buscar proveedor por nombre..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)} // Actualiza el término de búsqueda
          />

          {/* Tabla para mostrar los proveedores filtrados */}
          <table className="table table-striped">
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Email</th>
                <th>Teléfono</th>
                <th>Dirección</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {/* Mapea los proveedores filtrados y los muestra en la tabla */}
              {filteredProveedores.map((proveedor) => (
                <tr key={proveedor.proveedor_id}>
                  <td>{proveedor.nombre}</td>
                  <td>{proveedor.email}</td>
                  <td>{proveedor.telefono}</td>
                  <td>{proveedor.direccion}</td>
                  <td>
                    {/* Botón para editar proveedor, redirige a la página de edición */}
                    <button className="btn btn-warning btn-sm">
                      {proveedor.proveedor_id ? (
                        <Link href={`/proveedores/${proveedor.proveedor_id}`}>Editar</Link>
                      ) : (
                        <span>No ID disponible</span>
                      )}
                    </button>
                    {/* Botón para eliminar proveedor */}
                    <button
                      className="btn btn-danger btn-sm ml-2"
                      onClick={() => handleDelete(proveedor.proveedor_id)}
                    >
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* Paginación para navegar entre páginas de proveedores */}
          <nav>
            <ul className="pagination justify-content-center">
              <li className={`page-item ${page === 1 ? 'disabled' : ''}`}>
                <button className="page-link" onClick={handlePreviousPage}>Anterior</button>
              </li>
              <li className="page-item">
                <span className="page-link">
                  Página {page} de {totalPages}
                </span>
              </li>
              <li className={`page-item ${page === totalPages ? 'disabled' : ''}`}>
                <button className="page-link" onClick={handleNextPage}>Siguiente</button>
              </li>
            </ul>
          </nav>
        </div>
        <Footer /> {/* Componente del pie de página */}
      </div>
    </div>
  );
};

export default ConsultarProveedores;


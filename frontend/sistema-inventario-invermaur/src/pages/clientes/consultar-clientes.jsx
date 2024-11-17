import React, { useState, useEffect } from 'react'; // Importamos React y los hooks useState y useEffect
import axios from 'axios'; // Importamos axios para realizar peticiones HTTP
import 'bootstrap/dist/css/bootstrap.min.css'; // Importamos el CSS de Bootstrap para los estilos
import Sidebar from '../../components/Sidebar'; // Importamos el componente Sidebar
import Header from '../../layouts/Header'; // Importamos el componente Header
import Footer from '../../layouts/Footer'; // Importamos el componente Footer
import styles from './styles/consultar-clientes.module.css'; // Importamos los estilos personalizados
import Link from 'next/link'; // Importamos Link de Next.js para enlaces

// Componente principal de la página ConsultarClientes
const ConsultarClientes = () => {
  // Declaramos los estados necesarios para manejar los clientes, la búsqueda, la paginación y el total de clientes
  const [clientes, setClientes] = useState([]); // Estado para almacenar los clientes obtenidos
  const [searchTerm, setSearchTerm] = useState(''); // Estado para el término de búsqueda
  const [page, setPage] = useState(1); // Estado para la página actual (paginación)
  const [limit, setLimit] = useState(10); // Estado para el límite de clientes por página
  const [totalClientes, setTotalClientes] = useState(0); // Estado para el total de clientes disponibles

  // useEffect para obtener los clientes de la API cada vez que cambian 'page' o 'limit'
  useEffect(() => {
    const fetchClientes = async () => {
      try {
        // Realizamos una solicitud GET para obtener los clientes según la página y límite actuales
        const response = await axios.get(`http://localhost:8000/clientes?page=${page}&limit=${limit}`);
        // Actualizamos el estado con los clientes y el total de clientes
        setClientes(response.data.clientes);
        setTotalClientes(response.data.total);
      } catch (error) {
        console.error('Error al cargar los clientes:', error); // Mostramos un error si la solicitud falla
      }
    };
    fetchClientes(); // Llamamos a la función para obtener los clientes
  }, [page, limit]); // El useEffect se ejecutará cada vez que cambien 'page' o 'limit'

  // Filtramos los clientes según el término de búsqueda ingresado
  const filteredClientes = clientes
    ? clientes.filter(cliente =>
        cliente.nombre.toLowerCase().includes(searchTerm.toLowerCase())
      )
    : [];

  // Función para manejar la eliminación de un cliente
  const handleDelete = async (cliente_id) => {
    // Confirmación antes de eliminar un cliente
    const confirmDelete = window.confirm('¿Estás seguro de que deseas eliminar este cliente?');
    if (confirmDelete) {
      try {
        // Realizamos una solicitud DELETE para eliminar al cliente
        await axios.delete(`http://localhost:8000/clientes/${cliente_id}`);
        // Actualizamos la lista de clientes después de eliminar uno
        setClientes(clientes.filter(cliente => cliente.cliente_id !== cliente_id));
        alert('Cliente eliminado exitosamente'); // Mensaje de éxito
      } catch (error) {
        console.error('Error al eliminar el cliente:', error); // Manejamos el error si la eliminación falla
        alert('Hubo un error al eliminar el cliente');
      }
    }
  };

  // Calculamos el número total de páginas para la paginación
  const totalPages = Math.ceil(totalClientes / limit);

  // Función para ir a la siguiente página
  const handleNextPage = () => {
    if (page < totalPages) {
      setPage(page + 1); // Aumentamos el número de página si no estamos en la última página
    }
  };

  // Función para ir a la página anterior
  const handlePreviousPage = () => {
    if (page > 1) {
      setPage(page - 1); // Reducimos el número de página si no estamos en la primera
    }
  };

  // Estructura del componente que se renderiza en el navegador
  return (
    <div className={styles.container}> {/* Contenedor principal con estilos personalizados */}
      <Sidebar /> {/* Componente de barra lateral */}
      <div className={styles.mainContent}> {/* Contenedor principal del contenido */}
        <Header /> {/* Componente de encabezado */}
        <div className="container mt-5"> {/* Contenedor de Bootstrap con márgenes */}
          <h2 className={styles.title}>Consultar Clientes</h2> {/* Título de la página */}
          <input
            type="text"
            className="form-control mb-4"
            placeholder="Buscar cliente por nombre..."
            value={searchTerm} // Valor del término de búsqueda
            onChange={(e) => setSearchTerm(e.target.value)} // Actualiza el término de búsqueda al escribir
          />

          {/* Tabla para mostrar los clientes */}
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
              {filteredClientes.map((cliente) => (
                <tr key={cliente.cliente_id}>
                  <td>{cliente.nombre}</td>
                  <td>{cliente.email}</td>
                  <td>{cliente.telefono}</td>
                  <td>{cliente.direccion}</td>
                  <td>
                    <button className="btn btn-warning btn-sm">
                      <Link href={`/clientes/${cliente.cliente_id}`}>Editar</Link> {/* Enlace para editar el cliente */}
                    </button>
                    <button
                      className="btn btn-danger btn-sm ml-2"
                      onClick={() => handleDelete(cliente.cliente_id)} // Llamada a la función de eliminación
                    >
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* Paginación para navegar entre páginas */}
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
        <Footer /> {/* Componente de pie de página */}
      </div>
    </div>
  );
};

export default ConsultarClientes; // Exportamos el componente para su uso en otras partes de la aplicación


import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import Sidebar from '../../components/Sidebar';
import Header from '../../layouts/Header';
import Footer from '../../layouts/Footer';
import styles from './styles/consultar-productos.module.css';
import Link from 'next/link';

const ConsultarProductos = () => {
  // Estados para manejar productos, búsqueda y paginación
  const [productos, setProductos] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [page, setPage] = useState(1); // Página actual
  const [limit, setLimit] = useState(10); // Límites de productos por página
  const [totalProductos, setTotalProductos] = useState(0); // Total de productos para calcular la paginación

  // Cargar productos desde el backend con paginación
  useEffect(() => {
    const fetchProductos = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/productos?page=${page}&limit=${limit}`);
        setProductos(response.data.productos); // Asumimos que la respuesta tiene una propiedad `productos`
        setTotalProductos(response.data.total); // Asumimos que la respuesta tiene la propiedad `total`
      } catch (error) {
        console.error('Error al cargar los productos:', error);
      }
    };
    fetchProductos();
  }, [page, limit]); // Dependencias: se recargará cuando cambien `page` o `limit`

  // Filtrar productos por nombre
  const filteredProductos = productos.filter(producto =>
    producto.nombre.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Manejar eliminación de un producto
  const handleDelete = async (producto_id) => {
    const confirmDelete = window.confirm('¿Estás seguro de que deseas eliminar este producto?');
    if (confirmDelete) {
      try {
        await axios.delete(`http://localhost:8000/productos/${producto_id}`);
        setProductos(productos.filter(producto => producto.producto_id !== producto_id));
        alert('Producto eliminado exitosamente');
      } catch (error) {
        console.error('Error al eliminar el producto:', error);
        alert('Hubo un error al eliminar el producto');
      }
    }
  };

  // Calcular el número total de páginas
  const totalPages = Math.ceil(totalProductos / limit);

  // Funciones para cambiar de página
  const handleNextPage = () => {
    if (page < totalPages) {
      setPage(page + 1);
    }
  };

  const handlePreviousPage = () => {
    if (page > 1) {
      setPage(page - 1);
    }
  };

  return (
    <div className={styles.container}>
      <Sidebar />
      <div className={styles.mainContent}>
        <Header />
        <div className="container mt-5">
          <h2 className={styles.title}>Consultar Productos</h2>

          {/* Filtro de búsqueda */}
          <input
            type="text"
            className="form-control mb-4"
            placeholder="Buscar producto por nombre..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />

          {/* Tabla de productos */}
          <table className="table table-striped">
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Descripción</th>
                <th>Precio Bs</th>
                <th>Stock</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {filteredProductos.map((producto) => (
                <tr key={producto.producto_id}>
                  <td>{producto.nombre}</td>
                  <td>{producto.descripcion}</td>
                  <td>{producto.precio}</td>
                  <td>{producto.stock}</td>
                  <td>
                    {/* Botón para editar */}
                    <button className="btn btn-warning btn-sm">
                        {producto.producto_id ? (
                            <Link href={`/productos/${producto.producto_id}`}>Editar</Link>
                        ) : (
                            <span>No ID disponible</span>
                        )}
                    </button>
                    {/* Botón para eliminar */}
                    <button
                      className="btn btn-danger btn-sm ml-2"
                      onClick={() => handleDelete(producto.producto_id)}
                    >
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* Paginación */}
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
        <Footer />
      </div>
    </div>
  );
};

export default ConsultarProductos;

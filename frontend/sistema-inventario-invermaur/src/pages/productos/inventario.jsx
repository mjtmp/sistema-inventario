import React, { useState, useEffect } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import Sidebar from "../../components/Sidebar";
import Header from "../../layouts/Header";
import Footer from "../../layouts/Footer";
import styles from "./styles/inventario.module.css";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch, faTimesCircle, faInfoCircle } from '@fortawesome/free-solid-svg-icons';

const Inventario = () => {
  const [productos, setProductos] = useState([]);
  const [proveedores, setProveedores] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [page, setPage] = useState(1);
  const [limit, setLimit] = useState(10);
  const [totalProductos, setTotalProductos] = useState(0);
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedImage, setSelectedImage] = useState("");

  const openModal = (imageSrc) => {
    setSelectedImage(imageSrc);
    setModalOpen(true);
  };

  const closeModal = () => {
    setModalOpen(false);
    setSelectedImage("");
  };

  useEffect(() => {
    const fetchProductos = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/productos?skip=${(page - 1) * limit}&limit=${limit}`);
        setProductos(Array.isArray(response.data.productos) ? response.data.productos : []);
        setTotalProductos(response.data.total || 0);
      } catch (error) {
        console.error("Error al cargar los productos:", error);
      }
    };

    const fetchProveedores = async () => {
      try {
        const response = await axios.get("http://localhost:8000/proveedores");
        setProveedores(response.data.proveedores || []);
      } catch (error) {
        console.error("Error al cargar los proveedores:", error);
      }
    };

    fetchProductos();
    fetchProveedores();
  }, [page, limit]);

  const getProveedorNombre = (id) => {
    const proveedor = proveedores.find((p) => p.proveedor_id === id);
    return proveedor ? proveedor.nombre : 'N/A';
  };

  const filteredProductos = productos.filter(
    (producto) =>
      producto.nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (producto.categoria && producto.categoria.nombre.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  const totalPages = Math.ceil(totalProductos / limit);

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
          <h2 className={`${styles.title} text-center`}>Inventario</h2>

          {/* Barra de búsqueda */}
          <div className={`${styles.searchContainer} d-flex justify-content-center`}>
            <div className="input-group mb-4" style={{ maxWidth: '600px' }}>
              <span className="input-group-text bg-primary text-white">
                <FontAwesomeIcon icon={faSearch} />
              </span>
              <input
                type="text"
                className={`form-control ${styles.searchInput}`}
                placeholder="Buscar por nombre o categoría..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>

          {/* Leyenda de iniciales */}
          <div className={`${styles.legend} text-center mb-3`}>
            <FontAwesomeIcon icon={faInfoCircle} className="me-2" />
            <span><strong>F.C.:</strong> Fecha de Creación, <strong>F.A.:</strong> Fecha de Actualización</span>
          </div>

          <div className={styles.tableContainer}>
            <table className={`${styles.table} table`}>
              <thead>
                <tr>
                  <th className="text-center">Nombre</th>
                  <th className="text-center">Precio</th>
                  <th className="text-center">IVA</th>
                  <th className="text-center">Stock</th>
                  <th className="text-center">Proveedor</th>
                  <th className="text-center">Código de Barras</th>
                  <th className="text-center">F.C.</th>
                  <th className="text-center">F.A.</th>
                </tr>
              </thead>
              <tbody>
                {filteredProductos.map((producto) => (
                  <tr key={producto.producto_id}>
                    <td className="text-center">{producto.nombre}</td>
                    <td className="text-center">{producto.precio}</td>
                    <td className="text-center">{producto.tiene_iva ? "Sí" : "No"}</td>
                    <td className="text-center">{producto.stock}</td>
                    <td className="text-center">{getProveedorNombre(producto.proveedor_id)}</td>
                    <td className="text-center">
                      <img
                        className="img-fluid w-50 h-50"
                        src={`http://localhost:8000/${producto.codigo_barras}`}
                        alt={producto.codigo_barras}
                        onClick={() => openModal(`http://localhost:8000/${producto.codigo_barras}`)}
                        style={{ cursor: "pointer" }}
                      />
                    </td>
                    <td className="text-center">
                      {producto.fecha_creacion
                        ? new Date(producto.fecha_creacion).toLocaleDateString()
                        : "Sin Fecha"}
                    </td>
                    <td className="text-center">
                      {producto.fecha_actualizacion
                        ? new Date(producto.fecha_actualizacion).toLocaleDateString()
                        : "Sin Fecha"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Paginación */}
          <nav>
            <ul className="pagination justify-content-center">
              <li className={`page-item ${page === 1 ? "disabled" : ""}`}>
                <button className="page-link" onClick={handlePreviousPage}>
                  Anterior
                </button>
              </li>
              <li className="page-item">
                <span className="page-link">
                  Página {page} de {totalPages}
                </span>
              </li>
              <li className={`page-item ${page === totalPages ? "disabled" : ""}`}>
                <button className="page-link" onClick={handleNextPage}>
                  Siguiente
                </button>
              </li>
            </ul>
          </nav>

          {/* Modal para código de barras */}
          {modalOpen && (
            <div
              className="modal show d-block"
              tabIndex="-1"
              onClick={closeModal}
              style={{
                backgroundColor: "rgba(0, 0, 0, 0.8)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              <div className="modal-dialog modal-dialog-centered">
                <div className="modal-content">
                  <img
                    src={selectedImage}
                    alt="Código de Barras"
                    className="img-fluid"
                    style={{ borderRadius: "5px" }}
                  />
                  <button
                    className="btn btn-danger mt-2"
                    onClick={closeModal}
                    style={{ position: "absolute", top: "10px", right: "10px" }}
                  >
                    <FontAwesomeIcon icon={faTimesCircle} /> Cerrar
                  </button>
                </div>
              </div>
            </div>
          )}

          <Footer />
        </div>
      </div>
    </div>
  );
};

export default Inventario;



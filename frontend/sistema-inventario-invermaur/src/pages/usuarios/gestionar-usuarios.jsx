import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Sidebar from '../../components/Sidebar';
import Header from '../../layouts/Header';
import Footer from '../../layouts/Footer';
import 'bootstrap/dist/css/bootstrap.min.css';
import styles from './styles/gestionar-usuarios.module.css';
import Link from 'next/link';

const GestionarUsuarios = () => {
  const [usuarios, setUsuarios] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({
    nombre: '',
    email: '',
    contraseña: '',
    confirmarContraseña: '',
    rol_id: '',
  });

  // Obtener usuarios desde el backend
  useEffect(() => {
    fetchUsuarios();
  }, []);

  const fetchUsuarios = async () => {
    try {
      const response = await axios.get('http://localhost:8000/usuarios');
      setUsuarios(response.data);
    } catch (error) {
      console.error('Error al obtener usuarios:', error);
    }
  };

  // Manejar cambios en el formulario
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  // Crear un nuevo usuario
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (formData.contraseña !== formData.confirmarContraseña) {
      alert('Las contraseñas no coinciden');
      return;
    }
    try {
      await axios.post('http://localhost:8000/usuarios', {
        nombre: formData.nombre,
        email: formData.email,
        contraseña: formData.contraseña,
        rol_id: parseInt(formData.rol_id),
      });
      alert('Usuario creado con éxito');
      setShowModal(false);
      fetchUsuarios(); // Actualiza la lista de usuarios
    } catch (error) {
      console.error('Error al crear el usuario:', error);
      alert('No se pudo crear el usuario. Inténtalo de nuevo.');
    }
  };

  const handleDelete = async (usuario_id) => {
    if (confirm("¿Estás seguro de que deseas eliminar este usuario?")) {
      try {
        await axios.delete(`http://localhost:8000/usuarios/${usuario_id}`);
        alert("Usuario eliminado con éxito");
        fetchUsuarios(); // Actualiza la lista de usuarios
      } catch (error) {
        console.error("Error al eliminar usuario:", error);
        alert("No se pudo eliminar el usuario. Inténtalo de nuevo.");
      }
    }
  };

  // Filtrar usuarios por nombre
  const filteredUsuarios = usuarios.filter((usuario) =>
    usuario.nombre.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className={styles.container}>
      <Sidebar />
      <div className={styles.mainContent}>
        <Header />
        <div className="container mt-5">
          <h2 className={styles.title}>Gestión de Usuarios</h2>

          {/* Filtro de búsqueda */}
          <div className="mb-3">
            <input
              type="text"
              className="form-control"
              placeholder="Buscar usuario por nombre"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>

          {/* Tabla de usuarios */}
          <table className="table table-striped mt-4">
            <thead>
              <tr>
                <th>Nombre Completo</th>
                <th>Correo Electrónico</th>
                <th>Rol</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {filteredUsuarios.map((usuario) => (
                <tr key={usuario.usuario_id}>
                  <td>{usuario.nombre}</td>
                  <td>{usuario.email}</td>
                  <td>{usuario.rol_id === 1 ? 'Admin' : 'Empleado'}</td>
                  <td>
                    {/* Botón para editar */}
                    <button className="btn btn-warning btn-sm">
                        {usuario.usuario_id ? (
                            <Link href={`/usuarios/${usuario.usuario_id}`}>Editar</Link>
                        ) : (
                            <span>No ID disponible</span>
                        )}
                    </button>
                    <button className="btn btn-danger btn-sm" onClick={() => handleDelete(usuario.usuario_id)}>Eliminar</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* Botón para agregar usuario */}
          <div className="mt-4">
            <button
              className="btn btn-success"
              onClick={() => setShowModal(true)}
            >
              Usuario Nuevo
            </button>
          </div>
        </div>

        {/* Modal para crear un nuevo usuario */}
        {showModal && (
          <div className="modal show d-block" style={{ backgroundColor: 'rgba(0, 0, 0, 0.5)' }}>
            <div className="modal-dialog">
              <div className="modal-content">
                <div className="modal-header">
                  <h5 className="modal-title">Crear Nuevo Usuario</h5>
                  <button
                    type="button"
                    className="btn-close"
                    onClick={() => setShowModal(false)}
                  ></button>
                </div>
                <div className="modal-body">
                  <form onSubmit={handleSubmit}>
                    <div className="mb-3">
                      <label className="form-label">Nombre y Apellido</label>
                      <input
                        type="text"
                        name="nombre"
                        className="form-control"
                        value={formData.nombre}
                        onChange={handleChange}
                        required
                      />
                    </div>
                    <div className="mb-3">
                      <label className="form-label">Correo Electrónico</label>
                      <input
                        type="email"
                        name="email"
                        className="form-control"
                        value={formData.email}
                        onChange={handleChange}
                        required
                      />
                    </div>
                    <div className="mb-3">
                      <label className="form-label">Contraseña</label>
                      <input
                        type="password"
                        name="contraseña"
                        className="form-control"
                        value={formData.contraseña}
                        onChange={handleChange}
                        required
                      />
                    </div>
                    <div className="mb-3">
                      <label className="form-label">Confirmar Contraseña</label>
                      <input
                        type="password"
                        name="confirmarContraseña"
                        className="form-control"
                        value={formData.confirmarContraseña}
                        onChange={handleChange}
                        required
                      />
                    </div>
                    <div className="mb-3">
                      <label className="form-label">Rol</label>
                      <select
                        name="rol_id"
                        className="form-select"
                        value={formData.rol_id}
                        onChange={handleChange}
                        required
                      >
                        <option value="">Seleccione un rol</option>
                        <option value="1">Admin</option>
                        <option value="2">Empleado</option>
                      </select>
                    </div>
                    <button type="submit" className="btn btn-primary">
                      Crear
                    </button>
                  </form>
                </div>
              </div>
            </div>
          </div>
        )}

        <Footer />
      </div>
    </div>
  );
};

export default GestionarUsuarios;


/*import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Sidebar from '../../components/Sidebar';
import Header from '../../layouts/Header';
import Footer from '../../layouts/Footer';
import 'bootstrap/dist/css/bootstrap.min.css';
import styles from './styles/gestionar-usuarios.module.css';

const GestionarUsuarios = () => {
  const [usuarios, setUsuarios] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');

  // Obtener usuarios desde el backend
  useEffect(() => {
    axios
      .get('http://localhost:8000/usuarios')
      .then((response) => {
        setUsuarios(response.data);
      })
      .catch((error) => console.error('Error al obtener usuarios:', error));
  }, []);

  // Filtrar usuarios por nombre
  const filteredUsuarios = usuarios.filter((usuario) =>
    usuario.nombre.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className={styles.container}>
      <Sidebar />
      <div className={styles.mainContent}>
        <Header />
        <div className="container mt-5">
          <h2 className={styles.title}>Gestión de Usuarios</h2>

          {/* Filtro de búsqueda */ /*
          <div className="mb-3">
            <input
              type="text"
              className="form-control"
              placeholder="Buscar usuario por nombre"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>

          {/* Tabla de usuarios *//*
          <table className="table table-striped mt-4">
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Correo Electrónico</th>
                <th>Rol</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {filteredUsuarios.map((usuario) => (
                <tr key={usuario.id}>
                  <td>{usuario.nombre}</td>
                  <td>{usuario.email}</td>
                  <td>{usuario.rol.nombre}</td>
                  <td>
                    <button className="btn btn-primary btn-sm me-2">
                      Editar
                    </button>
                    <button className="btn btn-danger btn-sm">Eliminar</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* Botón para agregar usuario *//*
          <div className="mt-4">
            <button className="btn btn-success" onClick={() => {}}>
              Usuario Nuevo
            </button>
          </div>
        </div>
        <Footer />
      </div>
    </div>
  );
};

export default GestionarUsuarios;
*/
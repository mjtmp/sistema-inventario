import React, { useState, useEffect } from "react";
import axios from "axios";
import Sidebar from "../../components/Sidebar";
import Header from "../../layouts/Header";
import Footer from "../../layouts/Footer";
import "bootstrap/dist/css/bootstrap.min.css";
import styles from "./styles/roles-permisos.module.css";

const RolesPermisos = () => {
  const [roles, setRoles] = useState([]);
  const [permisos, setPermisos] = useState([]);
  const [rolesPermisos, setRolesPermisos] = useState([]);
  const [selectedRol, setSelectedRol] = useState("");
  const [selectedPermiso, setSelectedPermiso] = useState("");
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    fetchRoles();
    fetchPermisos();
    fetchRolesPermisos();
  }, []);

  const fetchRoles = async () => {
    try {
      const response = await axios.get("http://localhost:8000/roles/?skip=0&limit=10");
      console.log("Roles obtenidos:", response.data);
      setRoles(response.data);
    } catch (error) {
      console.error("Error al obtener roles:", error);
    }
  };

  const fetchPermisos = async () => {
    try {
      const response = await axios.get("http://localhost:8000/permisos/?skip=0&limit=10");
      console.log("Permisos obtenidos:", response.data);
      setPermisos(response.data);
    } catch (error) {
      console.error("Error al obtener permisos:", error);
    }
  };

  const fetchRolesPermisos = async () => {
    try {
      const response = await axios.get("http://localhost:8000/roles_permisos");
      console.log("Relaciones roles-permisos obtenidas:", response.data);
      setRolesPermisos(response.data);
    } catch (error) {
      console.error("Error al obtener relaciones roles-permisos:", error);
    }
  };

  const handleAddRolePermission = async () => {
    if (!selectedRol || !selectedPermiso) {
      alert("Por favor, selecciona un rol y un permiso.");
      return;
    }

    try {
      await axios.post("http://localhost:8000/roles_permisos", {
        rol_id: parseInt(selectedRol),
        permiso_id: parseInt(selectedPermiso),
      });
      alert("Rol y permiso asociados con éxito.");
      fetchRolesPermisos();
      setSelectedRol("");
      setSelectedPermiso("");
    } catch (error) {
      console.error("Error al asociar rol y permiso:", error);
      alert("No se pudo asociar el rol y el permiso. Inténtalo de nuevo.");
    }
  };

  const handleDeleteRolePermission = async (rol_id, permiso_id) => {
    if (confirm("¿Estás seguro de que deseas eliminar esta relación?")) {
      try {
        await axios.delete(`http://localhost:8000/roles_permisos/${rol_id}/${permiso_id}`);
        alert("Relación eliminada con éxito.");
        fetchRolesPermisos();
      } catch (error) {
        console.error("Error al eliminar la relación:", error);
        alert("No se pudo eliminar la relación. Inténtalo de nuevo.");
      }
    }
  };

  const filteredRolesPermisos = rolesPermisos.filter((relacion) =>
    roles
      .find((rol) => rol.rol_id === relacion.rol_id)?.nombre
      .toLowerCase()
      .includes(searchTerm.toLowerCase())
  );

  return (
    <div className={styles.container}>
      <Sidebar />
      <div className={styles.mainContent}>
        <Header />
        <div className="container mt-5">
          <h2 className={styles.title}>Gestión de Roles y Permisos</h2>

          {/* Filtro de búsqueda */}
          <div className="mb-3">
            <input
              type="text"
              className="form-control"
              placeholder="Buscar por nombre de rol"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>

          {/* Tabla de relaciones */}
          {filteredRolesPermisos.length > 0 ? (
            <table className="table table-striped mt-4">
              <thead>
                <tr>
                  <th>Rol</th>
                  <th>Permiso</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {filteredRolesPermisos.map((relacion) => (
                  <tr key={`${relacion.rol_id}-${relacion.permiso_id}`}>
                    <td>
                      {roles.find((rol) => rol.rol_id === relacion.rol_id)?.nombre || "Desconocido"}
                    </td>
                    <td>
                      {permisos.find((permiso) => permiso.permiso_id === relacion.permiso_id)?.nombre ||
                        "Desconocido"}
                    </td>
                    <td>
                      <button
                        className="btn btn-danger btn-sm"
                        onClick={() =>
                          handleDeleteRolePermission(relacion.rol_id, relacion.permiso_id)
                        }
                      >
                        Eliminar
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>No hay relaciones roles-permisos disponibles.</p>
          )}

          {/* Formulario para agregar relaciones */}
          <div className="mt-4">
            <h4>Agregar Rol-Permiso</h4>
            <div className="row">
              <div className="col-md-4">
                <select
                  className="form-select"
                  value={selectedRol}
                  onChange={(e) => setSelectedRol(e.target.value)}
                >
                  <option value="">Selecciona un rol</option>
                  {roles.map((rol) => (
                    <option key={rol.rol_id} value={rol.rol_id}>
                      {rol.nombre}
                    </option>
                  ))}
                </select>
              </div>
              <div className="col-md-4">
                <select
                  className="form-select"
                  value={selectedPermiso}
                  onChange={(e) => setSelectedPermiso(e.target.value)}
                >
                  <option value="">Selecciona un permiso</option>
                  {permisos.map((permiso) => (
                    <option key={permiso.permiso_id} value={permiso.permiso_id}>
                      {permiso.nombre}
                    </option>
                  ))}
                </select>
              </div>
              <div className="col-md-4">
                <button className="btn btn-success" onClick={handleAddRolePermission}>
                  Agregar
                </button>
              </div>
            </div>
          </div>
        </div>
        <Footer />
      </div>
    </div>
  );
};

export default RolesPermisos;



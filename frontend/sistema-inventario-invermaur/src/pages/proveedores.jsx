// src/pages/proveedores.jsx
import { useEffect, useState } from 'react';
import { fetchProveedores } from '../services/api';

const ProveedoresPage = () => {
  const [proveedores, setProveedores] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetchProveedores();
        setProveedores(response.data);
      } catch (err) {
        setError('Error al cargar los proveedores');
      }
    };
    fetchData();
  }, []);

  return (
    <div className="container mt-4">
      <h1>Lista de Proveedores</h1>
      {error ? (
        <p>{error}</p>
      ) : (
        <ul>
          {proveedores.map((proveedor) => (
            <li key={proveedor.id}>{proveedor.nombre}</li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default ProveedoresPage;

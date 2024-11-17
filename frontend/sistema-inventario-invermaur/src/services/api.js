import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000', // Cambia esto al URL del backend
});

export const fetchProveedores = () => api.get('/proveedores');
export const createProveedor = (data) => api.post('/proveedores', data);
<<<<<<< HEAD

// Función para obtener la lista de facturas
export const fetchFacturas = () => api.get('/facturas'); // Asegúrate de que el endpoint es correcto

// Función para obtener una factura específica
export const fetchFactura = (numeroFactura) => api.get(`/facturas/${numeroFactura}`, { responseType: 'blob' });

// Agrega más funciones según necesites
=======
// Agrega más funciones según necesites
// api.js (agregando una función para login)
export const login = (data) => api.post('/login', data);

>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39

export default api;

import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000', // Cambia esto al URL del backend
});

export const fetchProveedores = () => api.get('/proveedores');
export const createProveedor = (data) => api.post('/proveedores', data);

// Función para obtener la lista de facturas
export const fetchFacturas = () => api.get('/facturas'); // Asegúrate de que el endpoint es correcto

// Función para obtener una factura específica
export const fetchFactura = (numeroFactura) => api.get(`/facturas/${numeroFactura}`, { responseType: 'blob' });

// Agrega más funciones según necesites

export default api;

import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000', // Cambia esto al URL del backend
});

export const fetchProveedores = () => api.get('/proveedores');
export const createProveedor = (data) => api.post('/proveedores', data);
// Agrega más funciones según necesites
// api.js (agregando una función para login)
export const login = (data) => api.post('/login', data);


export default api;

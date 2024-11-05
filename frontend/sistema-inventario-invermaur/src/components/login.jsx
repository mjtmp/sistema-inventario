import React, { useState } from 'react';
import { useRouter } from 'next/router';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import '../styles/login.css';  // Importa el archivo CSS personalizado

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const router = useRouter();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/login', { username, password });

      if (response.status === 200) {
        const token = response.data.token; // Suponiendo que el token se envía como response.data.token
        localStorage.setItem('token', token); // Guarda el token en localStorage

        const userRole = response.data.role; // role devuelto por el backend
        if (userRole === 'admin') {
          router.push('/admin-dashboard'); // Ruta del dashboard de administrador
        } else {
          router.push('/employee-dashboard'); // Ruta del dashboard de empleado
        }
      }
    } catch (error) {
      alert('Credenciales incorrectas, por favor intenta de nuevo');
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="text-center">
          <img src="/logo.png" alt="Logo Empresa" className="login-logo" />
          <h5 className="login-title">Bienvenido al Sistema de Gestión de Inventario</h5>
          <form onSubmit={handleLogin}>
            <div className="form-group">
              <input
                type="text"
                className="form-control"
                placeholder="Usuario"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>
            <div className="form-group mt-3">
              <input
                type="password"
                className="form-control"
                placeholder="Contraseña"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            <button type="submit" className="login-button">
              Iniciar Sesión
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Login;




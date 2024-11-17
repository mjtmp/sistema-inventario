import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import styles from '../styles/login.module.css';

const Login = () => {
  const [email, setEmail] = useState('');
  const [contraseña, setContraseña] = useState('');
  const router = useRouter();

  // Verifica si el usuario ya está autenticado al cargar el componente
  useEffect(() => {
    const token = localStorage.getItem('token');
    const userRol = localStorage.getItem('rol');
  
    // Si hay un token, redirige según el rol solo si estamos iniciando sesión
    if (token && router.pathname === '/login') {
      if (userRol === 'admin') {
        router.push('/admin-dashboard');
      } else {
        router.push('/employee-dashboard');
      }
    }
  }, [router]);
  

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/login', { email, contraseña });

      if (response.status === 200) {
        const token = response.data.token;
        const userRol = response.data.rol;
        localStorage.setItem('token', token);
        localStorage.setItem('rol', userRol); // Guardar el rol del usuario

        if (userRol === 'admin') {
          router.push('/admin-dashboard');
        } else {
          router.push('/employee-dashboard');
        }
      }
    } catch (error) {
      alert('Credenciales incorrectas, por favor intenta de nuevo');
    }
  };

  return (
    <div className={styles['login-container']}>
      <div className={styles['login-card']}>
        <div className="text-center">
          <img src="/invermaur.png" alt="Logo Empresa" className={styles['login-logo']} />
          <h5 className={styles['login-title']}>Bienvenido al Sistema de Gestión de Inventario</h5>
          <form onSubmit={handleLogin}>
            <div className="form-group">
              <input
                type="text"
                className="form-control"
                placeholder="Correo Electrónico"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div className="form-group mt-3">
              <input
                type="password"
                className="form-control"
                placeholder="Contraseña"
                value={contraseña}
                onChange={(e) => setContraseña(e.target.value)}
              />
            </div>
            <button type="submit" className={styles['login-button']}>
              Iniciar Sesión
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Login;







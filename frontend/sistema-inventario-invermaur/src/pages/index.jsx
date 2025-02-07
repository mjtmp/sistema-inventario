// src/pages/index.jsx
import React, { useEffect } from 'react';
import { useRouter } from 'next/router';

const Index = () => {
  const router = useRouter();

  useEffect(() => {
    // Verifica si hay un token guardado en el almacenamiento local
    const token = localStorage.getItem('token');
    const userRol = localStorage.getItem('rol');

    if (!token) {
      // Si no hay token, redirige al login
      router.push('/login');
    } else {
      // Si hay token, redirige según el rol del usuario
      if (userRol === 'admin') {
        router.push('/admin-dashboard');
      } else {
        router.push('/employee-dashboard');
      }
    }
  }, [router]);

  return <div>Cargando...</div>; // Puede ser un indicador de carga o pantalla en blanco temporal
};

export default Index;


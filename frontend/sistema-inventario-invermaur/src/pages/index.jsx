<<<<<<< HEAD
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



/*import 'bootstrap/dist/css/bootstrap.min.css';
=======
import 'bootstrap/dist/css/bootstrap.min.css';
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39
import { useEffect } from 'react';
import { useRouter } from 'next/router';

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    // Verifica si el usuario está autenticado al verificar el token en localStorage
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/login'); // Redirige al login si no hay token
    }
  }, [router]);

  return (
    <div className="container">
      <h1 className="mt-5">¡Bienvenido al Sistema de Inventario de Invermaur!</h1>
      <p>Esta es la página principal de tu aplicación de inventario.</p>
    </div>
  );
<<<<<<< HEAD
}*/
=======
}
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39

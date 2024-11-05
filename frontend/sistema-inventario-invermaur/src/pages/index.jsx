import 'bootstrap/dist/css/bootstrap.min.css';
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
}

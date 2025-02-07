import React, { useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { useRouter } from 'next/router';
import DashboardEmpleado from '../components/DashboardEmpleado'; // Importamos el componente Dashboard
import Header from '../layouts/Header';       // Importa el Header
import Footer from '../layouts/Footer';       // Importa el Footer
import Sidebar from '../components/Sidebar';     // Importa el Sidebar de empleados
import styles from '../styles/admin-dashboard.module.css';

const EmployeeDashboard = () => {
    const router = useRouter();

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (!token) {
            router.push('/login'); // Si no hay token, redirige a login
        }
    }, [router]);

    return (
        <div className={`d-flex ${styles.adminDashboardContainer}`}>
            <Sidebar /> {/* Sidebar específico de empleados */}

            <div className={`${styles.mainContent} flex-grow-1`}>
                <Header /> {/* Header arriba del Dashboard */}
                
                <div className="container mt-4">
                    <DashboardEmpleado /> {/* Componente del Dashboard principal */}
                </div>

                <Footer /> {/* Footer en la parte inferior */}
            </div>
        </div>
    );
};

export default EmployeeDashboard;



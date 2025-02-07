import React from 'react';
import Sidebar from '../components/Sidebar';
import Header from '../layouts/Header';
import Footer from '../layouts/Footer';
import ProfileSettings from '../components/ProfileSettings';
import 'bootstrap/dist/css/bootstrap.min.css';
import styles from '../styles/configuracion.module.css';

const Configuracion = () => {
    return (
        <div className={styles.configuracionContainer}>
            <Sidebar />
            <div className={styles.mainContent}>
                <Header />
                <div className={`${styles.profileContainer} container mt-5`}>
                    <ProfileSettings />
                </div>
                <Footer />
            </div>
        </div>
    );
};

export default Configuracion;


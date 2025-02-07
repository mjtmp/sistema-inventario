import React, { useState } from "react";
import axios from "axios";
import { useRouter } from "next/router";
import 'bootstrap/dist/css/bootstrap.min.css';
import styles from '../styles/login.module.css';

const Registro = () => {
    const [nombre, setNombre] = useState("");
    const [email, setEmail] = useState("");
    const [contraseña, setContraseña] = useState("");
    const router = useRouter();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await axios.post("http://localhost:8000/usuarios", {
                nombre,
                email,
                contraseña,
                rol_id: 2  // Asignar un rol predeterminado, por ejemplo, 2 para "usuario"
            });
            alert("Registro exitoso. Por favor, inicie sesión.");
            router.push("/login");
        } catch (error) {
            console.error("Error al registrar el usuario:", error);
            alert("Error al registrar el usuario");
        }
    };

    return (
        <div className={styles['login-container']}>
            <div className={styles['login-card']}>
                <div className="text-center">
                    <img src="/invermaur.png" alt="Logo Empresa" className={styles['login-logo']} />
                    <h5 className={styles['login-title']}>Registro de Usuario</h5>
                    <form onSubmit={handleSubmit}>
                        <div className="form-group">
                            <input
                                type="text"
                                className="form-control"
                                placeholder="Nombre"
                                value={nombre}
                                onChange={(e) => setNombre(e.target.value)}
                                required
                            />
                        </div>
                        <div className="form-group mt-3">
                            <input
                                type="email"
                                className="form-control"
                                placeholder="Correo Electrónico"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                            />
                        </div>
                        <div className="form-group mt-3">
                            <input
                                type="password"
                                className="form-control"
                                placeholder="Contraseña"
                                value={contraseña}
                                onChange={(e) => setContraseña(e.target.value)}
                                required
                            />
                        </div>
                        <button type="submit" className={styles['login-button']}>
                            Registrarse
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default Registro;

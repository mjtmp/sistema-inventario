import React from 'react';
import { Bar, Pie } from 'react-chartjs-2'; // Importamos los gráficos de barras y pie
import { Chart as ChartJS, BarElement, CategoryScale, LinearScale, ArcElement, Tooltip, Legend } from 'chart.js'; // Importamos los componentes necesarios de chart.js
import styles from '../styles/chart-component.module.css'; // Importamos los estilos para el componente

// Registrar los elementos necesarios para Bar y Pie
ChartJS.register(BarElement, CategoryScale, LinearScale, ArcElement, Tooltip, Legend);

// El componente ChartComponent acepta "type" para determinar el tipo de gráfico (bar o pie) y "title" para el título del gráfico
const ChartComponent = ({ type, title }) => {
    // Datos estáticos para el gráfico (pueden ser dinámicos en una implementación real)
    const data = {
        labels: ["Producto A", "Producto B", "Producto C"], // Las etiquetas del eje X (productos)
        datasets: [
            {
                label: "Cantidad", // Etiqueta de la barra
                data: [12, 19, 3], // Datos asociados a cada etiqueta
                backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56"] // Colores para las barras o sectores
            }
        ]
    };

    return (
        <div className={`card shadow-sm ${styles.chartCard}`}>
            <div className={`card-body ${styles.chartBody}`}>
                <h5 className={`card-title ${styles.chartTitle}`}>{title}</h5> {/* Título del gráfico */}
                {/* Si el tipo es "bar", mostramos un gráfico de barras; de lo contrario, mostramos un gráfico circular */}
                {type === "bar" ? <Bar data={data} /> : <Pie data={data} />}
            </div>
        </div>
    );
};

export default ChartComponent;




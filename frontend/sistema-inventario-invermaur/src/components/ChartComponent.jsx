import React from 'react';
import { Bar, Pie } from 'react-chartjs-2'; 
import { Chart as ChartJS, BarElement, CategoryScale, LinearScale, ArcElement, Tooltip, Legend } from 'chart.js'; 
import styles from '../styles/chart-component.module.css'; 

ChartJS.register(BarElement, CategoryScale, LinearScale, ArcElement, Tooltip, Legend);

const ChartComponent = ({ type, title, data, labels }) => {
    const chartData = {
        labels: labels,
        datasets: data
    };

    const options = {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: title,
            },
        },
        scales: {
            x: {
                ticks: {
                    maxRotation: 25, // Rota las etiquetas a 45 grados
                    minRotation: 25, // Asegura que las etiquetas se roten
                    autoSkip: true, // Salta algunas etiquetas si hay demasiadas
                }
            },
            y: {
                beginAtZero: true
            }
        }
    };

    return (
        <div className={`card shadow-sm ${styles.chartCard}`}>
            <div className={`card-body ${styles.chartBody}`}>
                <h5 className={`card-title ${styles.chartTitle}`}>{title}</h5>
                {type === "bar" ? <Bar data={chartData} options={options} /> : <Pie data={chartData} />}
            </div>
        </div>
    );
};

export default ChartComponent;


import React, { useEffect, useState } from 'react';
import axios from 'axios';
import styles from '../styles/datetime.module.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faDollarSign } from '@fortawesome/free-solid-svg-icons';

const DollarRate = () => {
    const [dollarRate, setDollarRate] = useState(null);

    useEffect(() => {
        const fetchDollarRate = async () => {
            try {
                const response = await axios.get('http://localhost:8000/dollar/dollar-rate');
                setDollarRate(response.data.dolar);
            } catch (error) {
                console.error('Error fetching dollar rate:', error);
            }
        };

        fetchDollarRate();
    }, []);

    if (dollarRate === null) {
        return null; // No mostrar nada si no hay tasa de dólar disponible
    }

    return (
        <div className={styles.datetime}>
            <div className={styles.date}>
                <FontAwesomeIcon icon={faDollarSign} className={styles.icon} />
                Precio del Dólar: {dollarRate.toFixed(4)} Bs/USD
            </div>
        </div>
    );
};

export default DollarRate;

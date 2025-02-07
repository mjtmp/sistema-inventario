import React, { useState, useEffect } from 'react';
import styles from '../styles/datetime.module.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faClock, faCalendarAlt } from '@fortawesome/free-solid-svg-icons';

const DateTime = () => {
    const [dateTime, setDateTime] = useState(null);

    useEffect(() => {
        setDateTime(new Date());
        const timer = setInterval(() => {
            setDateTime(new Date());
        }, 1000);

        return () => clearInterval(timer);
    }, []);

    if (!dateTime) {
        return null;
    }

    return (
        <div className={styles.datetime}>
            <div className={styles.date}>
                <FontAwesomeIcon icon={faCalendarAlt} className={styles.icon} />
                {dateTime.toLocaleDateString()}
            </div>
            <div className={styles.time}>
                <FontAwesomeIcon icon={faClock} className={styles.icon} />
                {dateTime.toLocaleTimeString()}
            </div>
        </div>
    );
};

export default DateTime;


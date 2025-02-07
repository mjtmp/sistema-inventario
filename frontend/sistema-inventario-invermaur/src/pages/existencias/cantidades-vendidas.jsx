import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ChartComponent from '../../components/ChartComponent';

const CantidadesVendidas = () => {
    const [data, setData] = useState([]);
    const [labels, setLabels] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            const result = await axios.get('http://localhost:8000/salidas_inventario/cantidades_vendidas');
            const labels = result.data.map(item => item.fecha);
            const quantities = result.data.map(item => item.cantidad);

            setLabels(labels);
            setData([
                {
                    label: 'Cantidades Vendidas',
                    data: quantities,
                    backgroundColor: 'rgba(255, 99, 132, 0.6)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1,
                }
            ]);
        };

        fetchData();
    }, []);

    return <ChartComponent type="line" title="Cantidades Vendidas" data={data} labels={labels} />;
};

export default CantidadesVendidas;




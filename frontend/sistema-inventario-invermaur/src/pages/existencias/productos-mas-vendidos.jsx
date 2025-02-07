import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ChartComponent from '../../components/ChartComponent';

const ProductosMasVendidos = () => {
    const [data, setData] = useState([]);
    const [labels, setLabels] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            const result = await axios.get('http://localhost:8000/salidas_inventario/productos_mas_vendidos');
            const labels = result.data.map(item => item.producto);
            const quantities = result.data.map(item => item.total_salidas);

            setLabels(labels);
            setData([
                {
                    label: 'Productos Más Vendidos',
                    data: quantities,
                    backgroundColor: 'rgba(75, 192, 192, 0.6)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1,
                }
            ]);
        };

        fetchData();
    }, []);

    return <ChartComponent type="bar" title="Productos Más Vendidos" data={data} labels={labels} />;
};

export default ProductosMasVendidos;




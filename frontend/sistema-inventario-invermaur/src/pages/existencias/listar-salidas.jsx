import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Sidebar from '../../components/Sidebar';
import Header from '../../layouts/Header';
import Footer from '../../layouts/Footer';
import styles from './styles/listar-salidas.module.css';
import { Table } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch } from '@fortawesome/free-solid-svg-icons';
import { Bar, Line } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    LineElement,
    PointElement,
    Title,
    Tooltip,
    Legend,
    Filler  // Importar Filler para el fondo blanco
} from 'chart.js';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    LineElement,
    PointElement,
    Title,
    Tooltip,
    Legend,
    Filler  // Registrar Filler para el fondo blanco
);

const ListarSalidas = () => {
    const [pedidosCompletados, setPedidosCompletados] = useState([]);
    const [loading, setLoading] = useState(true);
    const [search, setSearch] = useState('');
    const [productosMasVendidos, setProductosMasVendidos] = useState({ labels: [], datasets: [] });
    const [cantidadesVendidas, setCantidadesVendidas] = useState({ labels: [], datasets: [] });

    const fetchPedidosCompletados = async () => {
        try {
            const response = await axios.get('http://localhost:8000/pedidos/completados');
            if (response.data && response.data.length > 0) {
                const pedidosConDetalles = await Promise.all(response.data.map(async (pedido) => {
                    const clienteResponse = await axios.get(`http://localhost:8000/clientes/${pedido.cliente_id}`);
                    const detalles = await Promise.all(pedido.detalles.map(async (detalle) => {
                        const productoResponse = await axios.get(`http://localhost:8000/productos/${detalle.producto_id}`);
                        return {
                            ...detalle,
                            producto_nombre: productoResponse.data.nombre || 'N/A'
                        };
                    }));
                    return {
                        ...pedido,
                        cliente_nombre: clienteResponse.data.nombre || 'N/A',
                        detalles: detalles
                    };
                }));
                setPedidosCompletados(pedidosConDetalles);
                setLoading(false);
                console.log(pedidosConDetalles); // Verifica en la consola del navegador si se obtienen correctamente
            }
        } catch (error) {
            console.error('Error al obtener pedidos completados:', error);
            setLoading(false);
        }
    };

    const fetchProductosMasVendidos = async () => {
        try {
            const result = await axios.get('http://localhost:8000/salidas_inventario/productos_mas_vendidos_desde_pedidos');
            const labels = result.data.map(item => item.producto);
            const quantities = result.data.map(item => item.total_vendidos);

            setProductosMasVendidos({
                labels,
                datasets: [
                    {
                        label: 'Productos Más Vendidos',
                        data: quantities,
                        backgroundColor: 'rgba(75, 192, 192, 0.6)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1,
                    }
                ]
            });
        } catch (error) {
            console.error('Error al obtener productos más vendidos:', error);
        }
    };

    const fetchCantidadesVendidas = async () => {
        try {
            const result = await axios.get('http://localhost:8000/salidas_inventario/cantidades_vendidas_desde_pedidos');
            const labels = result.data.map(item => item.fecha);
            const quantities = result.data.map(item => item.cantidad);

            setCantidadesVendidas({
                labels,
                datasets: [
                    {
                        label: 'Cantidades Vendidas',
                        data: quantities,
                        backgroundColor: 'rgba(255, 99, 132, 0.6)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1,
                    }
                ]
            });
        } catch (error) {
            console.error('Error al obtener cantidades vendidas:', error);
        }
    };

    useEffect(() => {
        fetchPedidosCompletados();
        fetchProductosMasVendidos();
        fetchCantidadesVendidas();
    }, []);

    const handleSearch = (e) => {
        setSearch(e.target.value);
    };

    const filteredPedidos = pedidosCompletados.filter(pedido => 
        pedido.cliente_nombre.toLowerCase().includes(search.toLowerCase()) ||
        pedido.pedido_id.toString().includes(search.toLowerCase())
    );

    const optionsBar = {
        responsive: true,
        plugins: {
            title: {
                display: true,
                text: 'Productos Más Vendidos',
                font: {
                    size: 20  // Títulos más grandes
                },
                color: '#000000',  // Título en color negro
                padding: {
                    top: 10,  // Reducir el espacio superior del título
                    bottom: 10  // Reducir el espacio inferior del título
                }
            },
            legend: {
                labels: {
                    font: {
                        size: 12  // Tamaño de las etiquetas de la leyenda
                    }
                }
            },
            tooltip: {
                backgroundColor: '#ffffff',  // Fondo blanco para los tooltips
                titleColor: '#000000',
                bodyColor: '#000000',
                borderColor: '#cccccc',
                borderWidth: 1
            }
        },
        layout: {
            padding: {
                top: 0,  // Reducir el padding superior
                bottom: 0  // Reducir el padding inferior
            }
        },
        scales: {
            x: {
                ticks: {
                    color: '#000000',
                    padding: 10  // Espacio entre los números y el borde
                },
                grid: {
                    display: false
                }
            },
            y: {
                ticks: {
                    color: '#000000',
                    padding: 10  // Espacio entre los números y el borde
                },
                grid: {
                    color: '#e0e0e0'
                }
            }
        }
    };

    const optionsLine = {
        responsive: true,
        plugins: {
            title: {
                display: true,
                text: 'Cantidades Vendidas',
                font: {
                    size: 20  // Títulos más grandes
                },
                color: '#000000',  // Título en color negro
                padding: {
                    top: 10,  // Reducir el espacio superior del título
                    bottom: 10  // Reducir el espacio inferior del título
                }
            },
            legend: {
                labels: {
                    font: {
                        size: 12  // Tamaño de las etiquetas de la leyenda
                    }
                }
            },
            tooltip: {
                backgroundColor: '#ffffff',  // Fondo blanco para los tooltips
                titleColor: '#000000',
                bodyColor: '#000000',
                borderColor: '#cccccc',
                borderWidth: 1
            }
        },
        layout: {
            padding: {
                top: 0,  // Reducir el padding superior
                bottom: 0  // Reducir el padding inferior
            }
        },
        scales: {
            x: {
                ticks: {
                    color: '#000000',
                    padding: 10  // Espacio entre los números y el borde
                },
                grid: {
                    display: false
                }
            },
            y: {
                ticks: {
                    color: '#000000',
                    padding: 10  // Espacio entre los números y el borde
                },
                grid: {
                    color: '#e0e0e0'
                }
            }
        }
    };

    return (
        <div className={styles.container}>
            <Sidebar />
            <div className={styles.mainContent}>
                <Header />
                <div className={`container ${styles.contentWrapper}`}>
                    <h2 className={styles.title}>Salidas de Inventario</h2>
                    <div className={`${styles.searchContainer} d-flex justify-content-center`}>
                        <div className="input-group mb-4" style={{ maxWidth: '600px' }}>
                            <span className="input-group-text bg-primary text-white">
                                <FontAwesomeIcon icon={faSearch} />
                            </span>
                            <input 
                                type="text" 
                                className={`form-control ${styles.searchInput}`} 
                                placeholder="Buscar por cliente o número de pedido" 
                                value={search}
                                onChange={handleSearch}
                            />
                        </div>
                    </div>
                    {loading ? (
                        <p className={styles.loadingText}>Cargando pedidos completados...</p>
                    ) : (
                        <Table striped bordered hover className={styles.customTable}>
                            <thead>
                                <tr>
                                    <th>Pedido ID</th>
                                    <th>Cliente</th>
                                    <th>Fecha</th>
                                    <th>Estado</th>
                                    <th>Producto</th>
                                    <th>Cantidad</th>
                                    <th>Precio de Venta</th>
                                </tr>
                            </thead>
                            <tbody>
                                {filteredPedidos.map(pedido => 
                                    pedido.detalles.map(detalle => (
                                        <tr key={`${pedido.pedido_id}-${detalle.detalle_id}`}>
                                            <td>{pedido.pedido_id}</td>
                                            <td>{pedido.cliente_nombre}</td>
                                            <td>{new Date(pedido.fecha_pedido).toLocaleDateString()}</td>
                                            <td>{pedido.estado}</td>
                                            <td>{detalle.producto_nombre || 'N/A'}</td>
                                            <td>{detalle.cantidad}</td>
                                            <td>{(detalle.cantidad * detalle.precio_unitario).toFixed(2)}</td>
                                        </tr>
                                    ))
                                )}
                            </tbody>
                        </Table>
                    )}
                    <div className={`${styles.graficasContainer}`}>
                        <div className={styles.grafica}>
                            <Bar id="bar-chart" data={productosMasVendidos} options={optionsBar} />
                        </div>
                        <div className={styles.grafica}>
                            <Line id="line-chart" data={cantidadesVendidas} options={optionsLine} />
                        </div>
                    </div>
                </div>
                <Footer />
            </div>
        </div>
    );
};

export default ListarSalidas;

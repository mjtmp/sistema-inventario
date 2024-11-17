import React, { useState, useEffect } from 'react'; // Importación de React y Hooks
import axios from 'axios'; // Librería para hacer peticiones HTTP
import { useRouter } from 'next/router'; // Hook para redirección
import Sidebar from '../../components/Sidebar'; // Componente de barra lateral
import Header from '../../layouts/Header'; // Componente de cabecera
import Footer from '../../layouts/Footer'; // Componente de pie de página
import 'bootstrap/dist/css/bootstrap.min.css'; // Bootstrap para estilos
import styles from './styles/listar-salidas.module.css'; // Estilos locales
import { Modal, Button, Table } from 'react-bootstrap'; // Componentes de Bootstrap para modales y tablas

// Componente principal ListarSalidas
const ListarSalidas = () => {
    // Estado para manejar las salidas, carga, búsqueda y datos de pagos
    const [salidas, setSalidas] = useState([]);
    const [loading, setLoading] = useState(true);
    const [search, setSearch] = useState('');
    const [showModalVerPago, setShowModalVerPago] = useState(false);
    const [pagos, setPagos] = useState([]);
    const [facturaActual, setFacturaActual] = useState(null);
    const router = useRouter(); // Inicialización del hook para navegación

    // useEffect para obtener las salidas de inventario al cargar el componente
    useEffect(() => {
        axios.get('http://localhost:8000/salidas_inventario')
            .then(response => {
                const data = response.data;
                // Consolidar salidas por factura_id
                const salidasConsolidadas = data.reduce((acc, salida) => {
                    if (!acc[salida.factura_id]) {
                        acc[salida.factura_id] = {
                            ...salida,
                            cantidad_total: salida.cantidad,
                            monto_total: salida.cantidad * salida.precio_venta
                        };
                    } else {
                        acc[salida.factura_id].cantidad_total += salida.cantidad;
                        acc[salida.factura_id].monto_total += salida.cantidad * salida.precio_venta;
                    }
                    return acc;
                }, {});

                // Convertir el objeto en array para renderizado
                setSalidas(Object.values(salidasConsolidadas));
                setLoading(false); // Cambiar estado de carga
            })
            .catch(error => {
                console.error('Error al obtener salidas:', error); // Manejo de errores
                setLoading(false); // Cambiar estado de carga
            });
    }, []); // Este efecto se ejecuta solo una vez al montar el componente

    // Función para mostrar el modal de ver pago
    const handleShowVerPago = (factura) => {
        setFacturaActual(factura); // Establecer la factura actual
        axios.get(`http://localhost:8000/facturas/${factura.factura_id}/pagos`)
            .then(response => {
                setPagos(response.data); // Establecer los pagos para la factura
                setShowModalVerPago(true); // Mostrar el modal
            })
            .catch(error => {
                console.error('Error al obtener los pagos de la factura:', error); // Manejo de errores
            });
    };

    // Función para cerrar el modal de ver pago
    const handleCloseVerPago = () => {
        setShowModalVerPago(false); // Ocultar el modal
        setPagos([]); // Limpiar pagos
        setFacturaActual(null); // Limpiar factura actual
    };

    // Función para manejar el input de búsqueda
    const handleSearch = (e) => {
        setSearch(e.target.value); // Establecer el valor de búsqueda
    };

    // Función para redirigir a la página de nueva factura
    const handleNuevaFactura = () => {
        router.push('/existencias/nueva-factura-form'); // Redirigir a nueva factura
    };

    // Filtrar las salidas por número de factura
    const filteredSalidas = salidas.filter(salida => 
        (salida.factura ? salida.factura.numero_factura.toLowerCase() : '').includes(search.toLowerCase())
    );

    return (
        <div className={styles.container}>
            <Sidebar /> {/* Barra lateral */}
            <div className={styles.mainContent}>
                <Header /> {/* Cabecera */}
                <div className="container mt-5">
                    <div className="d-flex justify-content-between align-items-center mb-4">
                        <h2 className={styles.title}>Listado de Salidas de Inventario</h2>
                        <button className="btn btn-primary" onClick={handleNuevaFactura}>Nueva Factura</button> {/* Botón para nueva factura */}
                    </div>
                    <input
                        type="text"
                        placeholder="Buscar por número de factura"
                        value={search}
                        onChange={handleSearch} // Llamada a función de búsqueda
                        className="form-control mb-3" // Estilo de bootstrap
                    />
                    {loading ? (
                        <p>Cargando...</p> // Mensaje mientras se cargan los datos
                    ) : (
                        <table className="table table-striped mt-4">
                            <thead>
                                <tr>
                                    <th>Facturación</th>
                                    <th>Fecha</th>
                                    <th>Cliente</th>
                                    <th>Monto Total</th>
                                    <th>Pagado</th>
                                    <th>Debido</th>
                                    <th>Vendido Por</th>
                                    <th>Opciones</th>
                                </tr>
                            </thead>
                            <tbody>
                                {filteredSalidas.map((salida, index) => (
                                    <tr key={index}>
                                        <td>{salida.factura ? salida.factura.numero_factura : 'No disponible'}</td>
                                        <td>{new Date(salida.fecha).toLocaleDateString()}</td>
                                        <td>{salida.cliente ? salida.cliente.nombre : 'No disponible'}</td>
                                        <td>{salida.monto_total.toFixed(2)}</td>
                                        <td>{salida.factura ? salida.factura.pagado : 'No disponible'}</td>
                                        <td>{salida.factura ? salida.factura.debido : 'No disponible'}</td>
                                        <td>{salida.vendedor ? salida.vendedor.nombre : 'No disponible'}</td>
                                        <td>
                                            {/* Botones para ver pago, abonar, editar, eliminar, imprimir */}
                                            <button className="btn btn-sm btn-info mr-2" onClick={() => handleShowVerPago(salida.factura)}>Ver Pago</button>
                                            <button className="btn btn-sm btn-warning mr-2">Abonar</button>
                                            <button className="btn btn-sm btn-success mr-2">Editar</button>
                                            <button className="btn btn-sm btn-danger mr-2">Eliminar</button>
                                            <button className="btn btn-sm btn-secondary" onClick={() => handlePrint(salida.factura.factura_id, salida.factura.numero_factura)}>Imprimir</button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    )}
                </div>
                <Footer /> {/* Pie de página */}
            </div>
            {/* Modal de Ver Pago */}
            <Modal show={showModalVerPago} onHide={handleCloseVerPago}>
                <Modal.Header closeButton>
                    <Modal.Title>Pago de factura Nº: {facturaActual?.numero_factura}</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <p>Cliente: {facturaActual?.cliente?.nombre}</p>
                    <Table striped bordered hover>
                        <thead>
                            <tr>
                                <th>Fecha</th>
                                <th>Importe</th>
                                <th>Método de Pago</th>
                                <th>Recibido por</th>
                                <th>Eliminar</th>
                            </tr>
                        </thead>
                        <tbody>
                            {pagos.map((pago) => (
                                <tr key={pago.pago_id}>
                                    <td>{new Date(pago.fecha).toLocaleDateString()}</td>
                                    <td>{pago.monto}</td>
                                    <td>{pago.metodo_pago}</td>
                                    <td>Recibido por [Nombre del Usuario] {/* Reemplazar con el nombre del usuario que recibió el pago */}</td>
                                    <td><Button variant="danger" size="sm">Eliminar</Button></td>
                                </tr>
                            ))}
                        </tbody>
                    </Table>
                    <div>
                        <p>Total a pagar: {facturaActual?.monto_total}</p>
                        <p>Total pagado: [Valor Calculado] {/* Calcular y mostrar el total pagado */}</p>
                        <p>Importe total a pagar: [Valor Calculado] {/* Calcular y mostrar la diferencia entre el total a pagar y el total pagado */}</p>
                    </div>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={handleCloseVerPago}>Cerrar</Button>
                </Modal.Footer>
            </Modal>
        </div>
    );
};

export default ListarSalidas; // Exportar el componente



import React, { useState } from 'react';
import axios from 'axios';
import Select from 'react-select';
import { useRouter } from 'next/router';
import Sidebar from '../../components/Sidebar';
import Header from '../../layouts/Header';
import Footer from '../../layouts/Footer';
import 'bootstrap/dist/css/bootstrap.min.css';
import styles from './styles/nueva-factura-form.module.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser, faCalendarAlt, faBox, faPlusCircle, faTrashAlt, faUserTie } from '@fortawesome/free-solid-svg-icons';

const NuevaFactura = ({ onClose, onFacturaCreada }) => {
    const [clienteId, setClienteId] = useState('');
    const [fechaEmision, setFechaEmision] = useState('');
    const [productos, setProductos] = useState([{ producto: null, cantidad: '', precio: '' }]);
    const [vendedorId, setVendedorId] = useState('');
    const [clientesOptions, setClientesOptions] = useState([]);
    const [vendedoresOptions, setVendedoresOptions] = useState([]);
    const [productosOptions, setProductosOptions] = useState([]);
    const router = useRouter();

    const buscarClientes = (inputValue) => {
        if (inputValue.length < 2) return;

        axios.get(`http://localhost:8000/clientes/search?nombre=${inputValue}`)
            .then(response => {
                const options = response.data.map(cliente => ({
                    value: cliente.cliente_id,
                    label: cliente.nombre
                }));
                setClientesOptions(options);
            })
            .catch(error => {
                console.error('Error al buscar clientes:', error);
            });
    };

    const buscarVendedores = (inputValue) => {
        if (inputValue.length < 2) return;

        axios.get(`http://localhost:8000/usuarios/search?nombre=${inputValue}`)
            .then(response => {
                const options = response.data.map(usuario => ({
                    value: usuario.usuario_id,
                    label: usuario.nombre
                }));
                setVendedoresOptions(options);
            })
            .catch(error => {
                console.error('Error al buscar vendedores:', error);
            });
    };

    const buscarProductos = (inputValue) => {
        if (inputValue.length < 2) return;

        axios.get(`http://localhost:8000/productos/search?nombre=${inputValue}`)
            .then(response => {
                const options = response.data.map(producto => ({
                    value: producto.producto_id,
                    label: producto.nombre,
                    price: producto.precio
                }));
                setProductosOptions(options);
            })
            .catch(error => {
                console.error('Error al buscar productos:', error);
            });
    };

    const handleProductoChange = (index, selectedOption) => {
        const values = [...productos];
        values[index].producto = selectedOption;
        values[index].precio = selectedOption ? selectedOption.price : '';
        setProductos(values);
    };

    const handleCantidadChange = (index, event) => {
        const values = [...productos];
        values[index][event.target.name] = event.target.value;
        setProductos(values);
    };

    const handleAddProducto = () => {
        setProductos([...productos, { producto: null, cantidad: '', precio: '' }]);
    };

    const handleRemoveProducto = (index) => {
        const values = [...productos];
        values.splice(index, 1);
        setProductos(values);
    };

    const crearPedido = (clienteId) => {
        const fecha_pedido = new Date().toISOString().split('T')[0];
        const estado = 'pendiente';
    
        const detalles = productos.map((producto) => ({
            producto_id: producto.producto ? producto.producto.value : '',
            cantidad: producto.cantidad,
            precio_unitario: producto.precio,
            pedido_id: 0,
            detalle_id: 0
        }));
    
        return axios.post('http://localhost:8000/pedidos', { cliente_id: clienteId, fecha_pedido, estado, detalles })
            .then(response => response.data)
            .catch(error => {
                console.error('Error al crear pedido:', error.response ? error.response.data : error.message);
                throw error;
            });
    };
    
    const handleSubmit = (event) => {
        event.preventDefault();
        crearPedido(clienteId)
            .then(nuevoPedido => {
                const nuevaFactura = {
                    cliente_id: clienteId,
                    usuario_id: vendedorId,
                    pedido_id: nuevoPedido.pedido_id,
                    productos: productos.map((producto) => ({
                        producto_id: producto.producto ? producto.producto.value : '',
                        cantidad: producto.cantidad,
                        precio_unitario: producto.precio,
                    })),
                };
                console.log("Datos enviados para crear una nueva factura:", nuevaFactura);
    
                return axios.post('http://localhost:8000/facturas', nuevaFactura);
            })
            .then((response) => {
                if (onFacturaCreada) {
                    onFacturaCreada(response.data);
                }
                if (onClose) {
                    onClose();
                }
                router.push('./listar-salidas');
            })
            .catch((error) => {
                console.error('Error al crear factura:', error);
            });
    };

    return (
        <div className={styles.container}>
            <Sidebar />
            <div className={styles.mainContent}>
                <Header />
                <div className={`${styles.card} mt-5`}>
                    <h2 className={styles.title}>
                        <FontAwesomeIcon icon={faPlusCircle} className={styles.titleIcon} /> Crear Nueva Factura
                    </h2>
                    <form onSubmit={handleSubmit} className={styles.form}>
                        <div className={styles.formGroup}>
                            <label htmlFor="clienteId" className={styles.label}>
                                <FontAwesomeIcon icon={faUser} className={styles.icon} /> Cliente
                            </label>
                            <Select
                                value={clientesOptions.find(option => option.value === clienteId)}
                                onInputChange={buscarClientes}
                                onChange={(selectedOption) => setClienteId(selectedOption.value)}
                                options={clientesOptions}
                                placeholder="Seleccionar Cliente"
                                isSearchable
                                required
                                className={styles.customSelect}
                            />
                        </div>

                        <div className={styles.formGroup}>
                            <label htmlFor="fechaEmision" className={styles.label}>
                                <FontAwesomeIcon icon={faCalendarAlt} className={styles.icon} /> Fecha de Emisión
                            </label>
                            <input
                                type="date"
                                className={styles.input}
                                id="fechaEmision"
                                name="fechaEmision"
                                value={fechaEmision}
                                onChange={(e) => setFechaEmision(e.target.value)}
                                required
                            />
                        </div>

                        {productos.map((producto, index) => (
                            <div key={index} className={styles.productGroup}>
                                <label htmlFor="fechaEmision" className={styles.label}>
                                    <FontAwesomeIcon icon={faBox} className={styles.titleIcon} /> Productos
                                </label>
                                
                                <Select
                                    value={producto.producto}
                                    onInputChange={buscarProductos}
                                    onChange={(selectedOption) => handleProductoChange(index, selectedOption)}
                                    options={productosOptions}
                                    placeholder="Producto"
                                    isSearchable
                                    className={styles.productSelect}
                                    required
                                />
                                <input
                                    type="number"
                                    placeholder="Cantidad"
                                    name="cantidad"
                                    value={producto.cantidad}
                                    onChange={(event) => handleCantidadChange(index, event)}
                                    className={styles.inputSmall}
                                    required
                                />
                                <input
                                    type="number"
                                    placeholder="Precio"
                                    name="precio"
                                    value={producto.precio}
                                    className={styles.inputSmall}
                                    readOnly
                                />
                                <button
                                    type="button"
                                    className={styles.btnRemove}
                                    onClick={() => handleRemoveProducto(index)}
                                >
                                    <FontAwesomeIcon icon={faTrashAlt} />
                                </button>
                            </div>
                        ))}
                        <button
                            type="button"
                            className={styles.btnAdd}
                            onClick={handleAddProducto}
                        >
                            <FontAwesomeIcon icon={faPlusCircle} /> Añadir Producto
                        </button>

                        <div className={styles.formGroup}>
                            <label htmlFor="vendedorId" className={styles.label}>
                                <FontAwesomeIcon icon={faUserTie} className={styles.icon} /> Vendedor
                            </label>
                            <Select
                                value={vendedoresOptions.find(option => option.value === vendedorId)}
                                onInputChange={buscarVendedores}
                                onChange={(selectedOption) => setVendedorId(selectedOption.value)}
                                options={vendedoresOptions}
                                placeholder="Seleccionar Vendedor"
                                className={styles.customSelect}
                                isSearchable
                                required
                            />
                        </div>

                        <div className={styles.buttonGroup}>
                            <button type="submit" className={styles.btnPrimary}>Crear Factura</button>
                            {onClose && (
                                <button type="button" className={styles.btnSecondary} onClick={onClose}>
                                    Cancelar
                                </button>
                            )}
                        </div>
                    </form>
                </div>
                <Footer />
            </div>
        </div>
    );
};

export default NuevaFactura;


import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Select from 'react-select';
import Sidebar from '../../components/Sidebar';
import Header from '../../layouts/Header';
import Footer from '../../layouts/Footer';
import styles from './styles/crear-orden-compra.module.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlusCircle, faTrashAlt, faBox, faClipboardList, faBarcode } from '@fortawesome/free-solid-svg-icons';

const CrearOrdenCompra = () => {
    const [proveedores, setProveedores] = useState([]);
    const [productosOptions, setProductosOptions] = useState([]);
    const [selectedProveedor, setSelectedProveedor] = useState(null);
    const [fechaOrden, setFechaOrden] = useState('');
    const [estado, setEstado] = useState('pendiente');
    const [detalles, setDetalles] = useState([{ orden_compra_id: 0, producto: null, cantidad: '', precio_unitario: '', codigo: '', nombre: '' }]);
    const [mensajeExito, setMensajeExito] = useState('');
    const [usuarioId, setUsuarioId] = useState(null);

    useEffect(() => {
        const userId = localStorage.getItem('usuario_id');
        setUsuarioId(userId);

        axios.get('http://localhost:8000/productos')
            .then(response => {
                const options = response.data.productos.map(producto => ({
                    value: producto.producto_id,
                    label: `${producto.nombre} (SKU: ${producto.codigo})`
                }));
                setProductosOptions(options);
            })
            .catch(error => {
                console.error('Error al obtener productos:', error);
            });

        axios.get('http://localhost:8000/proveedores')
            .then(response => {
                const options = response.data.proveedores.map(proveedor => ({
                    value: proveedor.proveedor_id,
                    label: proveedor.nombre
                }));
                setProveedores(options);
            })
            .catch(error => {
                console.error('Error al obtener proveedores:', error);
            });
    }, []);

    const buscarProductosPorCodigo = (index, codigo) => {
        if (!codigo) return;
        axios.get(`http://localhost:8000/productos/search?codigo=${codigo}`)
            .then(response => {
                const options = response.data.map(producto => ({
                    value: producto.producto_id,
                    label: `${producto.nombre} (SKU: ${producto.codigo})`
                }));
                if (options.length > 0) {
                    handleProductoChange(index, options[0]);
                }
            })
            .catch(error => {
                console.error('Error al buscar productos por código:', error);
            });
    };

    const buscarProductos = (inputValue) => {
        if (inputValue.length < 2) return;
        axios.get(`http://localhost:8000/productos/search?nombre=${inputValue}`)
            .then(response => {
                const options = response.data.map(producto => ({
                    value: producto.producto_id,
                    label: `${producto.nombre} (SKU: ${producto.codigo})`
                }));
                setProductosOptions(options);
            })
            .catch(error => {
                console.error('Error al buscar productos:', error);
            });
    };

    const handleProductoChange = (index, selectedOption) => {
        const updatedDetalles = [...detalles];
        updatedDetalles[index] = {
            ...updatedDetalles[index],
            producto: selectedOption,
            codigo: selectedOption ? selectedOption.label.split('SKU: ')[1].replace(')', '') : '',
            nombre: selectedOption ? selectedOption.label.split(' (SKU: ')[0] : ''
        };
        setDetalles(updatedDetalles);
    };

    const handleCodigoChange = (index, event) => {
        const updatedDetalles = [...detalles];
        updatedDetalles[index] = {
            ...updatedDetalles[index],
            codigo: event.target.value
        };
        setDetalles(updatedDetalles);
        buscarProductosPorCodigo(index, event.target.value);
    };

    const handleNombreChange = (index, inputValue) => {
        const updatedDetalles = [...detalles];
        updatedDetalles[index] = {
            ...updatedDetalles[index],
            nombre: inputValue
        };
        setDetalles(updatedDetalles);
        buscarProductos(inputValue);
    };

    const agregarDetalle = () => {
        setDetalles([...detalles, { orden_compra_id: 0, producto: null, cantidad: '', precio_unitario: '', codigo: '', nombre: '' }]);
    };

    const eliminarDetalle = (index) => {
        setDetalles(detalles.filter((_, i) => i !== index));
    };

    const handleDetalleChange = (index, field, value) => {
        const nuevosDetalles = [...detalles];
        nuevosDetalles[index][field] = value;
        setDetalles(nuevosDetalles);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!usuarioId) {
            alert('No se pudo obtener el ID del usuario. Por favor, inicia sesión de nuevo.');
            return;
        }

        const ordenCompraData = {
            proveedor_id: selectedProveedor?.value || '',
            fecha_orden: fechaOrden,
            estado,
            detalles: detalles.map(detalle => ({
                orden_compra_id: detalle.orden_compra_id,
                producto_id: detalle.producto.value,
                cantidad: detalle.cantidad,
                precio_unitario: detalle.precio_unitario
            })),
            usuario_id: usuarioId
        };

        try {
            await axios.post('http://localhost:8000/ordenes_compra', ordenCompraData);
            setMensajeExito('Orden de compra creada exitosamente');
            setTimeout(() => setMensajeExito(''), 3000);
            setSelectedProveedor(null);
            setFechaOrden('');
            setEstado('pendiente');
            setDetalles([{ orden_compra_id: 0, producto: null, cantidad: '', precio_unitario: '', codigo: '', nombre: '' }]);
        } catch (error) {
            console.error('Error al crear la orden de compra:', error);
        }
    };

    return (
        <div className={styles.container}>
            <Sidebar />
            <div className={styles.mainContent}>
                <Header />
                <div className={`container mt-5 ${styles.card}`}>
                    <h2 className={styles.title}>
                        <FontAwesomeIcon icon={faClipboardList} className={styles.titleIcon} /> Crear Orden
                    </h2>
                    <form onSubmit={handleSubmit} className={styles.formContainer}>
                        <div className={styles.formGroup}>
                            <label htmlFor="proveedor" className={styles.boldLabel}>
                                <FontAwesomeIcon icon={faBox} className={styles.icon} /> Proveedor
                            </label>
                            <Select
                                id="proveedor"
                                options={proveedores}
                                onChange={setSelectedProveedor}
                                value={selectedProveedor}
                                placeholder="Seleccione un proveedor"
                                className={styles.inputField}
                            />
                        </div>

                        <div className={styles.formGroup}>
                            <label htmlFor="fechaOrden" className={styles.boldLabel}>
                                <FontAwesomeIcon icon={faClipboardList} className={styles.icon} /> Fecha de Orden
                            </label>
                            <input
                                type="date"
                                id="fechaOrden"
                                value={fechaOrden}
                                onChange={(e) => setFechaOrden(e.target.value)}
                                required
                                className={styles.inputField}
                            />
                        </div>

                        <div className={styles.formGroup}>
                            <label htmlFor="estado" className={styles.boldLabel}>
                                <FontAwesomeIcon icon={faClipboardList} className={styles.icon} /> Estado
                            </label>
                            <select
                                id="estado"
                                value={estado}
                                onChange={(e) => setEstado(e.target.value)}
                                required
                                className={styles.inputField}
                            >
                                <option value="pendiente">Pendiente</option>
                                <option value="completada">Completado</option>
                            </select>
                        </div>

                        <div className={styles.formGroup}>
                            <label className={styles.boldLabel}>
                                <FontAwesomeIcon icon={faBox} className={styles.icon} /> Detalles de Producto
                            </label>
                            {detalles.map((detalle, index) => (
                                <div key={index} className={styles.detalleRow}>
                                    <input
                                        type="text"
                                        placeholder="Código"
                                        value={detalle.codigo}
                                        onChange={(e) => handleCodigoChange(index, e)}
                                        className={styles.inputField}
                                    />
                                    <Select
                                        options={productosOptions}
                                        onInputChange={(inputValue) => handleNombreChange(index, inputValue)}
                                        onChange={option => handleProductoChange(index, option)}
                                        value={detalle.producto}
                                        placeholder="Producto"
                                        className={styles.inputField}
                                    />
                                    <input
                                        type="number"
                                        placeholder="Cantidad"
                                        value={detalle.cantidad}
                                        onChange={(e) => handleDetalleChange(index, 'cantidad', e.target.value)}
                                        required
                                        className={styles.inputField}
                                    />
                                    <input
                                        type="number"
                                        placeholder="Precio Unitario"
                                        value={detalle.precio_unitario}
                                        onChange={(e) => handleDetalleChange(index, 'precio_unitario', e.target.value)}
                                        required
                                        className={styles.inputField}
                                    />
                                    <button type="button" className={`btn btn-danger ${styles.btnDangerSmall}`} onClick={() => eliminarDetalle(index)}>
                                        <FontAwesomeIcon icon={faTrashAlt} /> Eliminar
                                    </button>
                                </div>
                            ))}
                            <button type="button" className={`btn btn-primary ${styles.btnPrimario}`} onClick={agregarDetalle}>
                                <FontAwesomeIcon icon={faPlusCircle} /> Añadir Producto
                            </button>
                        </div>

                        <button type="submit" className={`btn btn-success ${styles.btnPrimary}`}>
                            Crear Orden de Pedido
                        </button>

                        {mensajeExito && <p className={styles.successMessage}>{mensajeExito}</p>}
                    </form>
                </div>
                <Footer />
            </div>
        </div>
    );
};

export default CrearOrdenCompra;


import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useRouter } from 'next/router';
import Select from 'react-select';
import Sidebar from '../../components/Sidebar';
import Header from '../../layouts/Header';
import Footer from '../../layouts/Footer';
import 'bootstrap/dist/css/bootstrap.min.css';
import styles from './styles/editar-factura.module.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser, faCalendarAlt, faBox, faEdit, faPlusCircle, faTrashAlt, faUserTie } from '@fortawesome/free-solid-svg-icons';

const EditarFacturaForm = () => {
    const router = useRouter();
    const { factura_id } = router.query;

    const [clienteId, setClienteId] = useState('');
    const [fechaEmision, setFechaEmision] = useState('');
    const [productos, setProductos] = useState([{ producto: null, cantidad: '', precio: '' }]);
    const [vendedorId, setVendedorId] = useState('');
    const [clientesOptions, setClientesOptions] = useState([]);
    const [vendedoresOptions, setVendedoresOptions] = useState([]);
    const [productosOptions, setProductosOptions] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (factura_id) {
            axios.get(`http://localhost:8000/facturas/${factura_id}`)
                .then(response => {
                    const factura = response.data[0];
                    if (factura) {
                        const productos = factura.productos || [];
                        setClienteId(factura.cliente_id);
                        setFechaEmision(factura.fecha_emision);
                        setVendedorId(factura.usuario_id);
                        setProductos(productos.map(prod => ({
                            producto: { 
                                value: prod.producto_id, 
                                label: prod.nombre,
                                price: prod.precio_unitario
                            },
                            cantidad: prod.cantidad,
                            precio: prod.precio_unitario
                        })));
                        setLoading(false);
                    } else {
                        console.error('Factura no encontrada');
                        setLoading(false);
                    }
                })
                .catch(error => {
                    console.error('Error al obtener la factura:', error);
                    setLoading(false);
                });
        }
    }, [factura_id]);

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
        values[index].producto = selectedOption ? selectedOption : null;
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

    const handleSubmit = (event) => {
        event.preventDefault();
    
        const facturaEditada = {
            cliente_id: clienteId,
            usuario_id: vendedorId,
            fecha_emision: fechaEmision,
            productos: productos.map((producto) => ({
                producto_id: producto.producto ? producto.producto.value : null,
                cantidad: producto.cantidad,
                precio_unitario: producto.precio,
            })),
        };
    
        // Verificar que todos los campos requeridos están completos y válidos
        if (!clienteId || !vendedorId || !fechaEmision || productos.length === 0) {
            alert('Por favor, completa todos los campos requeridos y agrega al menos un producto.');
            return;
        }
    
        // Validar que todos los productos tengan producto_id
        const productosValidos = facturaEditada.productos.every(prod => prod.producto_id !== null);
        if (!productosValidos) {
            alert('Por favor, selecciona productos válidos.');
            return;
        }
    
        console.log("Datos enviados para editar la factura:", facturaEditada); // Agregar console.log aquí
    
        axios.put(`http://localhost:8000/facturas/editar/${factura_id}`, facturaEditada)
            .then((response) => {
                console.log('Factura actualizada:', response.data);
                // Redirigir a la lista de salidas después de la actualización exitosa
                router.push('/existencias/listar-salidas');
            })
            .catch((error) => {
                console.error('Error al actualizar la factura:', error);
                alert('Hubo un error al actualizar la factura. Por favor, intenta de nuevo.');
            });
    };
    
    if (loading) {
        return <p>Cargando...</p>;
    }

    return (
        <div className={styles.container}>
            <Sidebar />
            <div className={styles.mainContent}>
                <Header />
                <div className={`${styles.card} mt-5`}>
                    <h2 className={styles.title}>
                        <FontAwesomeIcon icon={faEdit} className={styles.titleIcon} />Editar Factura
                    </h2>
                    <form onSubmit={handleSubmit} className={styles.form}>
                        <div className={styles.formGroup}>
                            <label htmlFor="clienteId" className={styles.label}>
                                <FontAwesomeIcon icon={faUser} className={styles.icon} />Cliente
                            </label>
                            <Select
                                className={styles.customSelect}
                                value={clientesOptions.find(option => option.value === clienteId)}
                                onInputChange={buscarClientes}
                                onChange={(selectedOption) => setClienteId(selectedOption.value)}
                                options={clientesOptions}
                                placeholder="Seleccionar Cliente"
                                isSearchable
                                required
                            />
                        </div>
                        <div className={styles.formGroup}>
                            <label htmlFor="fechaEmision" className={styles.label}>
                                <FontAwesomeIcon icon={faCalendarAlt} className={styles.icon} />Fecha de Emisión
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
                                    className={styles.productSelect}
                                    isSearchable
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
                                <FontAwesomeIcon icon={faUserTie} className={styles.icon} />Vendedor
                            </label>
                            <Select
                                className={styles.customSelect}
                                value={vendedoresOptions.find(option => option.value === vendedorId)}
                                onInputChange={buscarVendedores}
                                onChange={(selectedOption) => setVendedorId(selectedOption.value)}
                                options={vendedoresOptions}
                                placeholder="Seleccionar Vendedor"
                                isSearchable
                                required
                            />
                        </div>

                        <div className={styles.buttonGroup}>
                            <button type="submit" className={styles.btnPrimary}>Guardar Cambios</button>
                            <button type="button" className={styles.btnSecondary} onClick={() => router.push('/existencias/listar-salidas')}>
                                Cancelar
                            </button>
                        </div>
                        

                    </form>
                </div>
                <Footer />
            </div>
        </div>
    );
};
    
export default EditarFacturaForm;
    



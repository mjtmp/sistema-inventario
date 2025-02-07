import React, { useState, useEffect } from "react";
import axios from "axios";
import { useRouter } from 'next/router';
import Select from 'react-select';
import "bootstrap/dist/css/bootstrap.min.css";
import Sidebar from "../../components/Sidebar";
import Header from "../../layouts/Header";
import Footer from "../../layouts/Footer";
import styles from "./styles/crear-pedido.module.css";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser, faBox, faPlusCircle, faTrashAlt, faBarcode } from '@fortawesome/free-solid-svg-icons';

const CrearPedido = () => {
    const [clienteId, setClienteId] = useState(null);
    const [productos, setProductos] = useState([{ producto: null, cantidad: '', precio_unitario: '', codigo: '', nombre: '' }]);
    const [clientesOptions, setClientesOptions] = useState([]);
    const [productosOptions, setProductosOptions] = useState([]);
    const [estado, setEstado] = useState("pendiente");
    const router = useRouter();
    const [usuarioId, setUsuarioId] = useState(null); // Nuevo estado para el usuario_id

    useEffect(() => {
        const userId = localStorage.getItem('usuario_id'); // Obtener el usuario_id del almacenamiento local
        setUsuarioId(userId);

        const fetchClientes = async () => {
            const response = await axios.get('http://localhost:8000/clientes');
            if (response.data && response.data.clientes && Array.isArray(response.data.clientes)) {
                const options = response.data.clientes.map(cliente => ({
                    value: cliente.cliente_id,
                    label: cliente.nombre
                }));
                setClientesOptions(options);
            } else {
                console.error("Los datos de clientes no son un array:", response.data);
            }
        };

        const fetchProductos = async () => {
            const response = await axios.get('http://localhost:8000/productos');
            if (response.data && response.data.productos && Array.isArray(response.data.productos)) {
                const options = response.data.productos.map(producto => ({
                    value: producto.producto_id,
                    label: `${producto.nombre} (SKU: ${producto.codigo})`,
                    price: producto.precio
                }));
                setProductosOptions(options);
            } else {
                console.error("Los datos de productos no son un array:", response.data);
            }
        };

        fetchClientes();
        fetchProductos();
    }, []);

    const buscarClientes = (inputValue) => {
        if (inputValue.length < 2) return;
        axios.get(`http://localhost:8000/clientes/search?nombre=${inputValue}`)
            .then(response => {
                if (response.data && response.data.clientes && Array.isArray(response.data.clientes)) {
                    const options = response.data.clientes.map(cliente => ({
                        value: cliente.cliente_id,
                        label: cliente.nombre
                    }));
                    setClientesOptions(options);
                } else {
                    console.error("Los datos de clientes no son un array:", response.data);
                }
            })
            .catch(error => {
                console.error('Error al buscar clientes:', error);
            });
    };

    const buscarProductos = (inputValue) => {
        if (inputValue.length < 2) return;
        axios.get(`http://localhost:8000/productos/search?nombre=${inputValue}`)
            .then(response => {
                if (response.data && Array.isArray(response.data)) { // No necesariamente productos
                    const options = response.data.map(producto => ({
                        value: producto.producto_id,
                        label: `${producto.nombre} (SKU: ${producto.codigo})`,
                        price: producto.precio
                    }));
                    setProductosOptions(options);
                } else {
                    console.error("Los datos de productos no son un array:", response.data);
                }
            })
            .catch(error => {
                console.error('Error al buscar productos:', error);
            });
    };

    const buscarProductosPorCodigo = (index, codigo) => {
        if (!codigo) return;
        axios.get(`http://localhost:8000/productos/search?codigo=${codigo}`)
            .then(response => {
                const options = response.data.map(producto => ({
                    value: producto.producto_id,
                    label: `${producto.nombre} (SKU: ${producto.codigo})`,
                    price: producto.precio
                }));
                if (options.length > 0) {
                    handleProductoChange(index, options[0]); // Asignar el primer producto encontrado
                }
            })
            .catch(error => {
                console.error('Error al buscar productos por código:', error);
            });
    };

    const handleProductoChange = (index, selectedOption) => {
        const updatedProductos = [...productos];
        updatedProductos[index] = {
            ...updatedProductos[index],
            producto: selectedOption,
            precio_unitario: selectedOption ? selectedOption.price : '',
            codigo: selectedOption ? selectedOption.label.split('SKU: ')[1].replace(')', '') : ''
        };
        setProductos(updatedProductos);
    };

    const handleCantidadChange = (index, event) => {
        const updatedProductos = [...productos];
        updatedProductos[index] = {
            ...updatedProductos[index],
            cantidad: event.target.value
        };
        setProductos(updatedProductos);
    };

    const handleCodigoChange = (index, event) => {
        const updatedProductos = [...productos];
        updatedProductos[index] = {
            ...updatedProductos[index],
            codigo: event.target.value
        };
        setProductos(updatedProductos);
        buscarProductosPorCodigo(index, event.target.value);
    };

    const handleNombreChange = (index, inputValue) => {
        const updatedProductos = [...productos];
        updatedProductos[index] = {
            ...updatedProductos[index],
            nombre: inputValue
        };
        setProductos(updatedProductos);
        buscarProductos(inputValue);
    };

    const addProducto = () => {
        setProductos([...productos, { producto: null, cantidad: '', precio_unitario: '', codigo: '', nombre: '' }]);
    };

    const removeProducto = (index) => {
        const updatedProductos = [...productos];
        updatedProductos.splice(index, 1);
        setProductos(updatedProductos);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!clienteId || productos.some(p => !p.producto || !p.cantidad)) {
            alert("Por favor completa todos los campos");
            return;
        }

        if (!usuarioId) {
            alert('No se pudo obtener el ID del usuario. Por favor, inicia sesión de nuevo.');
            return;
        }

        try {
            const detalles = productos.map(p => ({
                pedido_id: 0,
                producto_id: p.producto.value,
                cantidad: p.cantidad,
                precio_unitario: p.precio_unitario,
                detalle_id: 0
            }));

            const pedidoData = {
                cliente_id: clienteId.value,
                fecha_pedido: new Date().toISOString().split('T')[0],
                estado: estado,
                detalles: detalles,
                usuario_id: usuarioId  // Incluyendo el usuario_id en la solicitud
            };

            console.log("Pedido data being sent:", pedidoData);

            const response = await axios.post("http://localhost:8000/pedidos", pedidoData);
            console.log("Pedido creado:", response.data);
            router.push("/pedidos/consultar-pedidos");
        } catch (error) {
            console.error("Error al crear pedido:", error.response ? error.response.data : error.message);
            alert(error.response?.data?.detail || "Hubo un error al crear el pedido");
        }
    };

    return (
        <div className={`${styles.container} d-flex`}>
            <Sidebar />
            <div className={styles.mainContent}>
                <Header />
                <div className={`${styles.formContainer} container`}>
                    <h1 className={`${styles.title} text-center mb-4`}>
                        <FontAwesomeIcon icon={faPlusCircle} className={styles.titleIcon} /> Crear Pedido
                    </h1>
                    <form onSubmit={handleSubmit}>
                        <div className="mb-3">
                            <label htmlFor="cliente" className={`${styles.boldLabel} form-label`}>
                                <FontAwesomeIcon icon={faUser} className={styles.icon} /> Cliente
                            </label>
                            <Select
                                id="cliente"
                                options={clientesOptions}
                                onInputChange={buscarClientes}
                                onChange={setClienteId}
                                value={clienteId}
                                placeholder="Escribe el nombre del cliente"
                            />
                        </div>
                        {productos.map((producto, index) => (
                            <div key={index} className={`${styles.productContainer} mb-4 p-3 border rounded`}>
                                <div className="row mb-3">
                                    <div className="col-md-4">
                                        <label htmlFor={`codigo${index}`} className={`${styles.boldLabel} form-label`}>
                                            <FontAwesomeIcon icon={faBarcode} className={styles.icon} /> Código
                                        </label>
                                        <input
                                            type="text"
                                            className="form-control"
                                            id={`codigo${index}`}
                                            value={producto.codigo}
                                            onChange={(e) => handleCodigoChange(index, e)}
                                            placeholder="Código del Producto"
                                        />
                                    </div>
                                    <div className="col-md-8">
                                        <label htmlFor={`producto${index}`} className={`${styles.boldLabel} form-label`}>
                                            <FontAwesomeIcon icon={faBox} className={styles.icon} /> Producto
                                        </label>
                                        <Select
                                            id={`producto${index}`}
                                            options={productosOptions}
                                            onInputChange={(inputValue) => handleNombreChange(index, inputValue)}
                                            onChange={option => handleProductoChange(index, option)}
                                            value={producto.producto}
                                            placeholder="Escribe el nombre del producto"
                                        />
                                    </div>
                                </div>
                                <div className="row">
                                    <div className="col-md-6 mb-3">
                                        <label htmlFor={`cantidad${index}`} className={`${styles.boldLabel} form-label`}>Cantidad</label>
                                        <input
                                            type="number"
                                            className="form-control"
                                            id={`cantidad${index}`}
                                            value={producto.cantidad}
                                            onChange={(e) => handleCantidadChange(index, e)}
                                            required
                                        />
                                    </div>
                                    <div className="col-md-6 mb-3">
                                        <label htmlFor={`precio${index}`} className={`${styles.boldLabel} form-label`}>Precio Unitario</label>
                                        <input
                                            type="number"
                                            className="form-control"
                                            id={`precio${index}`}
                                            value={producto.precio_unitario}
                                            readOnly
                                        />
                                    </div>
                                </div>
                                {index > 0 && (
                                    <button
                                        type="button"
                                        className="btn btn-danger w-100"
                                        onClick={() => removeProducto(index)}
                                    >
                                        <FontAwesomeIcon icon={faTrashAlt} className="me-1" /> Eliminar Producto
                                    </button>
                                )}
                            </div>
                        ))}
                        <button type="button" className={`${styles.btnSecondary} btn mb-3 w-100`} onClick={addProducto}>
                            <FontAwesomeIcon icon={faPlusCircle} className="me-1" /> Añadir Producto
                        </button>
                        <button type="submit" className={`${styles.btnPrimary} btn w-100`}>
                            Crear Pedido
                        </button>
                    </form>
                </div>
                <Footer />
            </div>
        </div>
    );
};

export default CrearPedido;

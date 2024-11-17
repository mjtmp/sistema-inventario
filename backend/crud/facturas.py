from sqlalchemy.orm import Session
from models.models import Factura, FacturaProducto, Producto, Cliente, Usuario, Pago, SalidasInventario
from utils.generar_factura import generar_factura, obtener_numero_factura
from schemas.facturas import FacturaCreate, FacturaResponse, FacturaProductoResponse
import datetime

# Función para crear una nueva factura
def crear_factura(db: Session, factura_data: FacturaCreate):
    # Obtener cliente desde la base de datos por su ID
    cliente = db.query(Cliente).filter(Cliente.cliente_id == factura_data.cliente_id).first()
    # Obtener usuario desde la base de datos por su ID
    usuario = db.query(Usuario).filter(Usuario.usuario_id == factura_data.usuario_id).first()

    # Verificación de existencia del cliente y usuario
    if cliente is None:
        raise ValueError("Cliente no encontrado.")
    if usuario is None:
        raise ValueError("Usuario no encontrado.")

    # Cálculo del total de la factura
    total = sum(item.cantidad * item.precio_unitario for item in factura_data.productos)
    # Obtener el siguiente número de factura
    numero_factura = obtener_numero_factura(db)

    # Crear el objeto de factura y añadirlo a la base de datos
    factura = Factura(
        cliente_id=factura_data.cliente_id,
        usuario_id=factura_data.usuario_id,
        pedido_id=factura_data.pedido_id,
        numero_factura=numero_factura,
        fecha_emision=datetime.date.today(),
        monto_total=total,
        estado='pendiente'
    )
    db.add(factura)
    db.commit()
    db.refresh(factura)

    # Diccionario para consolidar los productos en la factura
    productos_consolidados = {}
    for item in factura_data.productos:
        # Obtener el producto de la base de datos
        producto = db.query(Producto).filter(Producto.producto_id == item.producto_id).first()
        if producto is None:
            raise ValueError(f"Producto con ID {item.producto_id} no encontrado.")

        # Crear un registro de producto asociado a la factura
        factura_producto = FacturaProducto(
            factura_id=factura.factura_id,
            producto_id=producto.producto_id,
            cantidad=item.cantidad,
            precio_unitario=producto.precio
        )
        db.add(factura_producto)

        # Consolidación de información del producto para la factura
        if item.producto_id not in productos_consolidados:
            productos_consolidados[item.producto_id] = {
                "producto_id": producto.producto_id,
                "cantidad": item.cantidad,
                "precio_unitario": producto.precio,
                "descripcion": producto.nombre,
                "tiene_iva": producto.tiene_iva,
                "monto_total": item.cantidad * producto.precio
            }
        else:
            productos_consolidados[item.producto_id]["cantidad"] += item.cantidad
            productos_consolidados[item.producto_id]["monto_total"] += item.cantidad * producto.precio

        # Crear una salida de inventario por cada producto
        salida_inventario = SalidasInventario(
            producto_id=producto.producto_id,
            cliente_id=factura.cliente_id,
            factura_id=factura.factura_id,
            cantidad=item.cantidad,
            precio_venta=producto.precio,
            vendedor_id=factura.usuario_id
        )
        db.add(salida_inventario)

    db.commit()

    # Generar la respuesta detallada de productos en la factura
    productos_detalles = [FacturaProductoResponse(**prod) for prod in productos_consolidados.values()]

    # Información del cliente
    cliente_info = {
        'nombre': cliente.nombre,
        'telefono': cliente.telefono,
        'email': cliente.email,
        'direccion': cliente.direccion
    }
    productos_detalles_dict = [prod.dict() for prod in productos_detalles]
    # Generar PDF de la factura
    pdf_path = generar_factura(cliente=cliente_info, factura_info={'numero': numero_factura, 'fecha': factura.fecha_emision}, productos=productos_detalles_dict)

    # Retornar la respuesta de la factura creada
    return FacturaResponse(
        factura_id=factura.factura_id,
        cliente_id=factura.cliente_id,
        usuario_id=factura.usuario_id,
        numero_factura=factura.numero_factura,
        total=factura.monto_total,
        productos=productos_detalles
    )

# Función para obtener una factura por su ID
def obtener_factura(db: Session, factura_id: int):
    return db.query(Factura).filter(Factura.factura_id == factura_id).first()

# Función para obtener los pagos asociados a una factura
def obtener_pagos_por_factura(db: Session, factura_id: int):
    factura = db.query(Factura).filter(Factura.factura_id == factura_id).first()
    if not factura:
        raise ValueError("Factura no encontrada.")

    # Obtener los pagos asociados al pedido de la factura
    pagos = db.query(Pago).filter(Pago.pedido_id == factura.pedido_id).all()
    return [
        {
            'pago_id': pago.pago_id,
            'fecha': pago.fecha,
            'monto': pago.monto,
            'metodo_pago': pago.metodo_pago,
            'pedido_id': pago.pedido_id
        }
        for pago in pagos
    ]

# Función para generar el PDF de la factura
def generar_pdf_factura(db: Session, factura_id: int):
    factura = db.query(Factura).filter(Factura.factura_id == factura_id).first()
    if not factura:
        raise ValueError("Factura no encontrada.")

    # Información del cliente
    cliente = {
        'nombre': factura.cliente.nombre,
        'telefono': factura.cliente.telefono,
        'email': factura.cliente.email,
        'direccion': factura.cliente.direccion
    }

    # Productos asociados a la factura
    productos = [{'cantidad': fp.cantidad,
                  'descripcion': fp.producto.nombre,
                  'precio_unitario': fp.precio_unitario,
                  'tiene_iva': fp.producto.tiene_iva,
                  'monto_total': fp.cantidad * fp.precio_unitario}
                 for fp in factura.productos]

    # Información de la factura (número y fecha)
    factura_info = {'numero': factura.numero_factura, 'fecha': factura.fecha_emision}
    # Generar y retornar el PDF de la factura
    return generar_factura(cliente, factura_info, productos)

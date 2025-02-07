from sqlalchemy.orm import Session
from sqlalchemy import text
from models.models import Factura, FacturaProducto, Producto, Cliente, Usuario, Pago, SalidasInventario
from utils.generar_factura import generar_factura, obtener_numero_factura
from schemas.facturas import FacturaCreate, FacturaResponse, FacturaProductoResponse, AbonoCreate, FacturaUpdate
from datetime import date, datetime
import datetime as dt


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
        fecha_emision=date.today(),
        #fecha_emision=datetime.date.today(),
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

from sqlalchemy import text

def obtenerProductosPorFactura(db: Session, factura_id: int):
    queryFactura = ''' 
    SELECT 
        Pedidos.pedido_id,
        Usuarios.usuario_id,
        Facturas.numero_factura,
        Facturas.monto_total,
        Facturas.debido,
        Facturas.factura_id,
        Clientes.cliente_id,
        Facturas.fecha_emision,
        Facturas.pagado,
        Facturas.estado
    FROM 
        Pedidos
    INNER JOIN Facturas ON Pedidos.pedido_id = Facturas.pedido_id
    INNER JOIN Usuarios ON Facturas.usuario_id = Usuarios.usuario_id
    INNER JOIN Clientes ON Pedidos.cliente_id = Clientes.cliente_id
    WHERE 
        Facturas.factura_id = :factura_id
    '''
    
    QueryProductos = """
    SELECT 
        FacturaProductos.id,
        FacturaProductos.cantidad,
        FacturaProductos.monto_total,
        FacturaProductos.precio_unitario,
        Productos.nombre,
        Productos.precio,
        Productos.descripcion,
        Facturas.factura_id
    FROM 
        FacturaProductos
    INNER JOIN 
        Facturas on FacturaProductos.factura_id = Facturas.factura_id
    INNER JOIN 
        Productos ON FacturaProductos.producto_id = Productos.producto_id
    WHERE 
        Facturas.factura_id = :factura_id
    """

    # Ejecutar las consultas
    result = db.execute(text(queryFactura), {"factura_id": factura_id})
    resultProductos = db.execute(text(QueryProductos), {"factura_id": factura_id})

    # Convertir los resultados en diccionarios
    factura = [dict(row) for row in result.mappings()]
    productos = [dict(row) for row in resultProductos.mappings()]

    # Asignar los productos al campo 'productos' en la factura
    if factura:
        factura[0]['productos'] = productos

    return factura

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
            'pedido_id': pago.pedido_id,
            "factura_id": factura.factura_id,
            "cliente": factura.cliente.nombre,  # Accede al nombre del cliente
            "usuario": factura.usuario.nombre  # Accede al nombre del usuario
        }
        for pago in pagos
    ]

# Función para agregar un abono a una factura
def agregar_abono_a_factura(db: Session, factura_id: int, abono_data: AbonoCreate):
    factura = db.query(Factura).filter(Factura.factura_id == factura_id).first()
    if not factura:
        raise ValueError("Factura no encontrada.")

    # Convertir la cadena de fecha a un objeto date
    fecha_abono = datetime.strptime(abono_data.fecha, "%Y-%m-%d").date()

    abono = Pago(
        pedido_id=factura.pedido_id,
        fecha=fecha_abono,  # Usar el objeto date
        monto=abono_data.monto,
        metodo_pago=abono_data.metodo_pago
    )
    db.add(abono)
    db.commit()
    db.refresh(abono)
    
    # Actualizar los montos pagados y debidos de la factura
    factura.pagado += abono_data.monto
    factura.debido = factura.monto_total - factura.pagado
    db.commit()
    db.refresh(factura)

    return abono

def editar_factura(db: Session, factura_id: int, factura_data: FacturaUpdate):
    # Buscar la factura existente por su ID
    factura = db.query(Factura).filter(Factura.factura_id == factura_id).first()
    if not factura:
        raise ValueError("Factura no encontrada.")

    # Verificación de existencia del cliente y usuario
    cliente = db.query(Cliente).filter(Cliente.cliente_id == factura_data.cliente_id).first()
    usuario = db.query(Usuario).filter(Usuario.usuario_id == factura_data.usuario_id).first()
    if cliente is None:
        raise ValueError("Cliente no encontrado.")
    if usuario is None:
        raise ValueError("Usuario no encontrado.")

    # Cálculo del total de la factura
    total = sum(item.cantidad * item.precio_unitario for item in factura_data.productos)

    # Convertir fecha_emision a objeto date si es una cadena
    if isinstance(factura_data.fecha_emision, str):
        try:
            factura_data.fecha_emision = datetime.strptime(factura_data.fecha_emision, "%Y-%m-%d").date()
        except ValueError as e:
            raise ValueError("Formato de fecha incorrecto. Use YYYY-MM-DD.")
    else:
        factura_data.fecha_emision = dt.date.today()

    # Actualizar los campos de la factura
    factura.cliente_id = factura_data.cliente_id
    factura.usuario_id = factura_data.usuario_id
    factura.fecha_emision = factura_data.fecha_emision
    factura.monto_total = total
    
    # Eliminar los productos antiguos
    db.query(FacturaProducto).filter(FacturaProducto.factura_id == factura_id).delete()

    # Eliminar las salidas de inventario antiguas
    db.query(SalidasInventario).filter(SalidasInventario.factura_id == factura_id).delete()

    # Diccionario para consolidar los productos en la factura
    productos_consolidados = {}
    for item in factura_data.productos:
        # Obtener el producto de la base de datos
        producto = db.query(Producto).filter(Producto.producto_id == item.producto_id).first()
        if producto is None:
            raise ValueError(f"Producto con ID {item.producto_id} no encontrado.")

        # Crear un registro de producto asociado a la factura
        nuevo_producto = FacturaProducto(
            factura_id=factura_id,
            producto_id=item.producto_id,
            cantidad=item.cantidad,
            precio_unitario=item.precio_unitario
        )
        db.add(nuevo_producto)

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
        nueva_salida = SalidasInventario(
            producto_id=producto.producto_id,
            cliente_id=factura.cliente_id,
            factura_id=factura.factura_id,
            cantidad=item.cantidad,
            precio_venta=producto.precio,
            vendedor_id=factura.usuario_id
        )
        db.add(nueva_salida)

    db.commit()

    # Generar la respuesta detallada de productos en la factura
    productos_detalles = [FacturaProductoResponse(**prod) for prod in productos_consolidados.values()]

    # Información del cliente
    cliente_info = {
        'nombre': factura.cliente.nombre,
        'telefono': factura.cliente.telefono,
        'email': factura.cliente.email,
        'direccion': factura.cliente.direccion
    }
    productos_detalles_dict = [prod.dict() for prod in productos_detalles]

    # Generar PDF de la factura actualizada
    pdf_path = generar_factura(cliente=cliente_info, factura_info={'numero': factura.numero_factura, 'fecha': factura.fecha_emision}, productos=productos_detalles_dict)

    db.refresh(factura)
    
    return {
        "factura_id": factura.factura_id,
        "cliente_id": factura.cliente_id,
        "usuario_id": factura.usuario_id,
        "numero_factura": factura.numero_factura,
        "total": factura.monto_total,
        "productos": productos_detalles
    }

# Función para eliminar una factura
def eliminar_factura(db: Session, factura_id: int):
    # Eliminar los productos asociados a la factura
    productos = db.query(FacturaProducto).filter(FacturaProducto.factura_id == factura_id).all()
    for producto in productos:
        db.delete(producto)
    
    # Eliminar las salidas de inventario asociadas a la factura
    salidas = db.query(SalidasInventario).filter(SalidasInventario.factura_id == factura_id).all()
    for salida in salidas:
        db.delete(salida)
    
    # Ahora, eliminar la factura
    factura = db.query(Factura).filter(Factura.factura_id == factura_id).first()
    if not factura:
        raise ValueError("Factura no encontrada.")
    db.delete(factura)
    db.commit()
    return {"message": "Factura eliminada correctamente"}

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

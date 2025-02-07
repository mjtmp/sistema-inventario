from sqlalchemy.orm import Session
from models.models import PedidosSalidasInventario, Producto, Pedido, DetallePedido
import logging
from schemas.salidas_inventario import SalidaInventarioCreate, SalidaInventarioUpdate
from datetime import datetime
from sqlalchemy import func
from crud.historial import registrar_accion  # Importar la función para registrar acciones

logging.basicConfig(level=logging.INFO)

def get_salida_inventario(db: Session, salida_id: int):
    return db.query(PedidosSalidasInventario).filter(PedidosSalidasInventario.salida_id == salida_id).first()

def get_salidas_inventario(db: Session, skip: int = 0, limit: int = 10):
    salidas = db.query(PedidosSalidasInventario).offset(skip).limit(limit).all()
    total = db.query(PedidosSalidasInventario).count()
    return salidas, total

def create_salida_inventario(db: Session, salida: SalidaInventarioCreate, usuario_id: int):
    producto = db.query(Producto).filter(Producto.producto_id == salida.producto_id).first()
    if producto.stock < salida.cantidad:
        raise ValueError(f"Stock insuficiente para el producto: {producto.nombre}")
    producto.stock -= salida.cantidad
    db_salida = PedidosSalidasInventario(**salida.dict(), vendedor_id=usuario_id)
    db.add(db_salida)
    db.commit()
    db.refresh(db_salida)
    registrar_accion(db, usuario_id, "Creación de salida de inventario", f"Salida de inventario ID {db_salida.salida_id} creada.")
    return db_salida

def update_salida_inventario(db: Session, salida_id: int, salida: SalidaInventarioUpdate, usuario_id: int):
    db_salida = get_salida_inventario(db, salida_id)
    if db_salida:
        for key, value in salida.dict(exclude_unset=True).items():
            setattr(db_salida, key, value)
        db.commit()
        db.refresh(db_salida)
        registrar_accion(db, usuario_id, "Actualización de salida de inventario", f"Salida de inventario ID {db_salida.salida_id} actualizada.")
    return db_salida

def delete_salida_inventario(db: Session, salida_id: int, usuario_id: int):
    db_salida = get_salida_inventario(db, salida_id)
    if db_salida:
        db.delete(db_salida)
        db.commit()
        registrar_accion(db, usuario_id, "Eliminación de salida de inventario", f"Salida de inventario ID {db_salida.salida_id} eliminada.")
    return db_salida

def get_total_salidas_inventario(db: Session):
    total_salidas = db.query(func.sum(PedidosSalidasInventario.cantidad)).scalar()
    total_valor_ventas = db.query(func.sum(PedidosSalidasInventario.precio_venta)).scalar()
    if total_salidas is None:
        total_salidas = 0
    if total_valor_ventas is None:
        total_valor_ventas = 0.0
    return total_salidas, total_valor_ventas

def get_productos_mas_vendidos(db: Session):
    query = db.query(
        Producto.nombre.label("producto"),
        func.sum(PedidosSalidasInventario.cantidad).label("total_salidas")
    ).join(Producto, PedidosSalidasInventario.producto_id == Producto.producto_id)\
     .group_by(Producto.nombre)\
     .order_by(func.sum(PedidosSalidasInventario.cantidad).desc()).all()
    
    return [{"producto": row.producto, "total_salidas": row.total_salidas} for row in query]

def get_productos_mas_vendidos_desde_pedidos(db: Session):
    query = db.query(
        Producto.nombre.label("producto"),
        func.sum(DetallePedido.cantidad).label("total_vendidos")
    ).join(DetallePedido, Producto.producto_id == DetallePedido.producto_id)\
     .join(Pedido, DetallePedido.pedido_id == Pedido.pedido_id)\
     .filter(Pedido.estado == 'completado')\
     .group_by(Producto.nombre)\
     .order_by(func.sum(DetallePedido.cantidad).desc())\
     .limit(5)\
     .all()
    
    return [{"producto": row.producto, "total_vendidos": row.total_vendidos} for row in query]

def get_cantidades_vendidas(db: Session):
    query = db.query(
        func.date(PedidosSalidasInventario.fecha).label("fecha"),
        func.sum(PedidosSalidasInventario.cantidad).label("cantidad")
    ).group_by(func.date(PedidosSalidasInventario.fecha))\
     .order_by(func.date(PedidosSalidasInventario.fecha)).all()
    
    return [{"fecha": row.fecha, "cantidad": row.cantidad} for row in query]

def get_cantidades_vendidas_desde_pedidos(db: Session):
    query = db.query(
        func.date(Pedido.fecha_pedido).label("fecha"),
        func.sum(DetallePedido.cantidad).label("cantidad")
    ).join(DetallePedido, Pedido.pedido_id == DetallePedido.pedido_id)\
     .filter(Pedido.estado == 'completado')\
     .group_by(func.date(Pedido.fecha_pedido))\
     .order_by(func.date(Pedido.fecha_pedido))\
     .all()
    
    return [{"fecha": row.fecha, "cantidad": row.cantidad} for row in query]

def get_salidas_inventario_por_pedido(db: Session, skip: int = 0, limit: int = 100):
    salidas = db.query(PedidosSalidasInventario).join(Pedido).filter(Pedido.estado == 'completado').offset(skip).limit(limit).all()
    total = db.query(PedidosSalidasInventario).join(Pedido).filter(Pedido.estado == 'completado').count()
    return salidas, total

def registrar_salidas_automaticamente(db: Session, usuario_id: int):
    pedidos_completados = db.query(Pedido).filter(Pedido.estado == 'completado').all()
    for pedido in pedidos_completados:
        for detalle in pedido.detalles:
            # Verificar si la salida ya existe
            salida_existente = db.query(PedidosSalidasInventario).filter_by(pedido_id=pedido.pedido_id, producto_id=detalle.producto_id).first()
            if salida_existente:
                continue  # Si ya existe, pasar al siguiente detalle
            
            db_salida = PedidosSalidasInventario(
                producto_id=detalle.producto_id,
                cliente_id=pedido.cliente_id,
                pedido_id=pedido.pedido_id,
                cantidad=detalle.cantidad,
                precio_venta=detalle.precio_unitario * detalle.cantidad,
                fecha=pedido.fecha_pedido,
                vendedor_id=usuario_id
            )
            db.add(db_salida)

    db.commit()
    logging.info("Salidas registradas automáticamente para los pedidos completados")
    return {"mensaje": "Salidas registradas automáticamente para los pedidos completados"}






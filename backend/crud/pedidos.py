from sqlalchemy.orm import Session
from models.models import Pedido, DetallePedido, Producto
from schemas.pedidos import PedidoCreate, PedidoUpdate
from crud.historial import registrar_accion  # Importar la función para registrar acciones
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_pedido(db: Session, pedido_id: int):
    return db.query(Pedido).filter(Pedido.pedido_id == pedido_id).first()

def get_pedidos(db: Session, skip: int = 0, limit: int = 10):
    pedidos = db.query(Pedido).offset(skip).limit(limit).all()
    total = db.query(Pedido).count()
    return pedidos, total

def create_pedido(db: Session, pedido: PedidoCreate, usuario_id: int):
    try:
        for detalle in pedido.detalles:
            producto = db.query(Producto).filter(Producto.producto_id == detalle.producto_id).first()
            if producto.stock < detalle.cantidad:
                raise ValueError(f"Stock insuficiente para el producto: {producto.nombre}")
            producto.stock -= detalle.cantidad
            db.add(producto)

        db_pedido = Pedido(
            cliente_id=pedido.cliente_id,
            fecha_pedido=pedido.fecha_pedido,
            estado=pedido.estado
        )
        db.add(db_pedido)
        db.commit()
        db.refresh(db_pedido)
        
        for detalle in pedido.detalles:
            db_detalle = DetallePedido(
                pedido_id=db_pedido.pedido_id,
                producto_id=detalle.producto_id,
                cantidad=detalle.cantidad,
                precio_unitario=detalle.precio_unitario
            )
            db.add(db_detalle)
        
        db.commit()
        registrar_accion(db, usuario_id, "Creación de pedido", f"Pedido ID {db_pedido.pedido_id} creado.")
        logger.debug("Pedido y detalles creados exitosamente: %s", db_pedido)
        return db_pedido
    except Exception as e:
        logger.error(f"Error al crear pedido: {str(e)}")
        raise

def update_pedido(db: Session, pedido_id: int, pedido: PedidoUpdate, usuario_id: int):
    db_pedido = get_pedido(db, pedido_id)
    if db_pedido:
        for key, value in pedido.dict(exclude_unset=True).items():
            setattr(db_pedido, key, value)

        if pedido.estado and pedido.estado == 'cancelado':
            # Reponer inventario
            for detalle in db_pedido.detalles:
                producto = db.query(Producto).filter(Producto.producto_id == detalle.producto_id).first()
                producto.stock += detalle.cantidad
                db.add(producto)

        db.commit()
        db.refresh(db_pedido)
        registrar_accion(db, usuario_id, "Actualización de pedido", f"Pedido ID {db_pedido.pedido_id} actualizado.")
    return db_pedido

def delete_pedido(db: Session, pedido_id: int, usuario_id: int):
    db_pedido = get_pedido(db, pedido_id)
    if db_pedido:
        # Reponer inventario
        for detalle in db_pedido.detalles:
            producto = db.query(Producto).filter(Producto.producto_id == detalle.producto_id).first()
            producto.stock += detalle.cantidad
            db.add(producto)
        
        db.delete(db_pedido)
        db.commit()
        registrar_accion(db, usuario_id, "Eliminación de pedido", f"Pedido ID {db_pedido.pedido_id} eliminado.")
    return db_pedido

def get_pedidos_completados(db: Session):
    return db.query(Pedido).filter(Pedido.estado == 'completado').all()



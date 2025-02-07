from sqlalchemy.orm import Session, joinedload
from models.models import OrdenCompra, DetalleOrdenCompra
from schemas.ordenes_compra import OrdenCompraCreate, OrdenCompraUpdate
from crud.historial import registrar_accion
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_orden_compra(db: Session, orden_compra_id: int):
    return db.query(OrdenCompra).filter(OrdenCompra.orden_compra_id == orden_compra_id).options(joinedload(OrdenCompra.detalles)).first()

def get_ordenes_compra(db: Session, skip: int = 0, limit: int = 10):
    ordenes_compra = db.query(OrdenCompra).options(joinedload(OrdenCompra.detalles)).offset(skip).limit(limit).all()
    total = db.query(OrdenCompra).count()
    return ordenes_compra, total

def create_orden_compra(db: Session, orden_compra: OrdenCompraCreate, usuario_id: int):
    try:
        db_orden_compra = OrdenCompra(
            proveedor_id=orden_compra.proveedor_id,
            fecha_orden=orden_compra.fecha_orden,
            estado=orden_compra.estado
        )
        db.add(db_orden_compra)
        db.commit()
        db.refresh(db_orden_compra)
        
        for detalle in orden_compra.detalles:
            db_detalle = DetalleOrdenCompra(
                orden_compra_id=db_orden_compra.orden_compra_id,
                producto_id=detalle.producto_id,
                cantidad=detalle.cantidad,
                precio_unitario=detalle.precio_unitario
            )
            db.add(db_detalle)
        
        db.commit()
        registrar_accion(db, usuario_id, "Creación de orden de compra", f"Orden de compra ID {db_orden_compra.orden_compra_id} creada.")
        logger.debug("Orden de compra y detalles creados exitosamente: %s", db_orden_compra)
        return db_orden_compra
    except Exception as e:
        logger.error(f"Error al crear orden de compra: {str(e)}")
        raise

def update_orden_compra(db: Session, orden_compra_id: int, orden_compra: OrdenCompraUpdate, usuario_id: int):
    db_orden_compra = get_orden_compra(db, orden_compra_id)
    if db_orden_compra:
        for key, value in orden_compra.dict(exclude_unset=True).items():
            setattr(db_orden_compra, key, value)
        db.commit()
        db.refresh(db_orden_compra)
        registrar_accion(db, usuario_id, "Actualización de orden de compra", f"Orden de compra ID {db_orden_compra.orden_compra_id} actualizada.")
    return db_orden_compra

def delete_orden_compra(db: Session, orden_compra_id: int, usuario_id: int):
    db_orden_compra = get_orden_compra(db, orden_compra_id)
    if db_orden_compra:
        db.delete(db_orden_compra)
        db.commit()
        registrar_accion(db, usuario_id, "Eliminación de orden de compra", f"Orden de compra ID {db_orden_compra.orden_compra_id} eliminada.")
    return db_orden_compra




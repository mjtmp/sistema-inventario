from sqlalchemy.orm import Session
from models.models import DetalleOrdenCompra
from schemas.detalle_orden_compra import DetalleOrdenCompraCreate, DetalleOrdenCompraUpdate

def get_detalle_orden_compra(db: Session, detalle_id: int):
    return db.query(DetalleOrdenCompra).filter(DetalleOrdenCompra.detalle_id == detalle_id).first()

def get_detalles_orden_compra(db: Session, orden_compra_id: int, skip: int = 0, limit: int = 10):
    return db.query(DetalleOrdenCompra).filter(DetalleOrdenCompra.orden_compra_id == orden_compra_id).offset(skip).limit(limit).all()

def create_detalle_orden_compra(db: Session, detalle: DetalleOrdenCompraCreate):
    db_detalle = DetalleOrdenCompra(
        orden_compra_id=detalle.orden_compra_id,
        producto_id=detalle.producto_id,
        cantidad=detalle.cantidad,
        precio_unitario=detalle.precio_unitario
    )
    db.add(db_detalle)
    db.commit()
    db.refresh(db_detalle)
    return db_detalle

def update_detalle_orden_compra(db: Session, detalle_id: int, detalle: DetalleOrdenCompraUpdate):
    db_detalle = get_detalle_orden_compra(db, detalle_id)
    if db_detalle:
        for key, value in detalle.dict(exclude_unset=True).items():
            setattr(db_detalle, key, value)
        db.commit()
        db.refresh(db_detalle)
    return db_detalle

def delete_detalle_orden_compra(db: Session, detalle_id: int):
    db_detalle = get_detalle_orden_compra(db, detalle_id)
    if db_detalle:
        db.delete(db_detalle)
        db.commit()
    return db_detalle

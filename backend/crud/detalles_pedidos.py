from sqlalchemy.orm import Session
from ..models.models import DetallePedido
from ..schemas.detalles_pedidos import DetallePedidoCreate, DetallePedidoUpdate

def get_detalle_pedido(db: Session, detalle_id: int):
    return db.query(DetallePedido).filter(DetallePedido.detalle_id == detalle_id).first()

def get_detalles_pedidos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(DetallePedido).offset(skip).limit(limit).all()

def create_detalle_pedido(db: Session, detalle_pedido: DetallePedidoCreate):
    db_detalle_pedido = DetallePedido(**detalle_pedido.dict())
    db.add(db_detalle_pedido)
    db.commit()
    db.refresh(db_detalle_pedido)
    return db_detalle_pedido

def update_detalle_pedido(db: Session, detalle_id: int, detalle_pedido: DetallePedidoUpdate):
    db_detalle_pedido = get_detalle_pedido(db, detalle_id)
    if db_detalle_pedido:
        for key, value in detalle_pedido.dict().items():
            setattr(db_detalle_pedido, key, value)
        db.commit()
        db.refresh(db_detalle_pedido)
    return db_detalle_pedido

def delete_detalle_pedido(db: Session, detalle_id: int):
    db_detalle_pedido = get_detalle_pedido(db, detalle_id)
    if db_detalle_pedido:
        db.delete(db_detalle_pedido)
        db.commit()
    return db_detalle_pedido

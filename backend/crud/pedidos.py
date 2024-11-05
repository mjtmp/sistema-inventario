from sqlalchemy.orm import Session
from ..models.models import Pedido
from ..schemas.pedidos import PedidoCreate, PedidoUpdate

def get_pedido(db: Session, pedido_id: int):
    return db.query(Pedido).filter(Pedido.pedido_id == pedido_id).first()

def get_pedidos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Pedido).offset(skip).limit(limit).all()

def create_pedido(db: Session, pedido: PedidoCreate):
    # Crear una instancia de Pedido con todos los datos
    db_pedido = Pedido(**pedido.dict())
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

def update_pedido(db: Session, pedido_id: int, pedido: PedidoUpdate):
    # Obtener el pedido actual para modificarlo
    db_pedido = get_pedido(db, pedido_id)
    if db_pedido:
        # Actualizar cada campo del pedido
        for key, value in pedido.dict().items():
            setattr(db_pedido, key, value)
        db.commit()
        db.refresh(db_pedido)
    return db_pedido

def delete_pedido(db: Session, pedido_id: int):
    db_pedido = get_pedido(db, pedido_id)
    if db_pedido:
        db.delete(db_pedido)
        db.commit()
    return db_pedido

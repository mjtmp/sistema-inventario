from sqlalchemy.orm import Session
from ..models.models import Proveedor
from ..schemas.proveedores import ProveedorCreate, ProveedorUpdate

def get_proveedor(db: Session, proveedor_id: int):
    return db.query(Proveedor).filter(Proveedor.proveedor_id == proveedor_id).first()

def get_proveedores(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Proveedor).offset(skip).limit(limit).all()

def create_proveedor(db: Session, proveedor: ProveedorCreate):
    db_proveedor = Proveedor(**proveedor.dict())
    db.add(db_proveedor)
    db.commit()
    db.refresh(db_proveedor)
    return db_proveedor

def update_proveedor(db: Session, proveedor_id: int, proveedor: ProveedorUpdate):
    db_proveedor = get_proveedor(db, proveedor_id)
    if db_proveedor:
        for key, value in proveedor.dict().items():
            setattr(db_proveedor, key, value)
        db.commit()
        db.refresh(db_proveedor)
    return db_proveedor

def delete_proveedor(db: Session, proveedor_id: int):
    db_proveedor = get_proveedor(db, proveedor_id)
    if db_proveedor:
        db.delete(db_proveedor)
        db.commit()
    return db_proveedor

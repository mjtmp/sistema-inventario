from sqlalchemy.orm import Session
from ..models.models import Rol
from ..schemas.rol import RolCreate, RolUpdate

def get_rol(db: Session, rol_id: int):
    return db.query(Rol).filter(Rol.rol_id == rol_id).first()

def get_roles(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Rol).offset(skip).limit(limit).all()

def create_rol(db: Session, rol: RolCreate):
    db_rol = Rol(**rol.dict())
    db.add(db_rol)
    db.commit()
    db.refresh(db_rol)
    return db_rol

def update_rol(db: Session, rol_id: int, rol: RolUpdate):
    db_rol = get_rol(db, rol_id)
    if db_rol:
        for key, value in rol.dict().items():
            setattr(db_rol, key, value)
        db.commit()
        db.refresh(db_rol)
    return db_rol

def delete_rol(db: Session, rol_id: int):
    db_rol = get_rol(db, rol_id)
    if db_rol:
        db.delete(db_rol)
        db.commit()
    return db_rol

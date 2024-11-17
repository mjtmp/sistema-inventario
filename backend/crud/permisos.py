from sqlalchemy.orm import Session
from models.models import Permiso  # Importa el modelo Permiso definido en models.
from schemas.permisos import PermisoCreate  # Importa el esquema Pydantic para validación de datos.
from sqlalchemy.exc import IntegrityError  # Manejo de errores específicos de integridad en la base de datos.

# Obtiene un permiso específico por su ID.
def get_permiso(db: Session, permiso_id: int):
    return db.query(Permiso).filter(Permiso.permiso_id == permiso_id).first()

# Recupera una lista de permisos con paginación (offset y limit).
def get_permisos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Permiso).offset(skip).limit(limit).all()

# Crea un nuevo permiso en la base de datos.
def create_permiso(db: Session, permiso: PermisoCreate):
    # Convierte el esquema Pydantic a un objeto del modelo Permiso.
    db_permiso = Permiso(**permiso.dict())
    try:
        db.add(db_permiso)  # Agrega el nuevo permiso a la sesión.
        db.commit()  # Confirma los cambios.
        db.refresh(db_permiso)  # Actualiza el objeto con los datos del permiso almacenado.
    except IntegrityError:  # Maneja errores de violación de restricciones únicas.
        db.rollback()  # Revierte la transacción si hay un error.
        return None
    return db_permiso

# Elimina un permiso por su ID.
def delete_permiso(db: Session, permiso_id: int):
    db_permiso = get_permiso(db, permiso_id)  # Busca el permiso.
    if db_permiso:  # Si el permiso existe:
        db.delete(db_permiso)  # Elimina el permiso de la sesión.
        db.commit()  # Confirma la eliminación.
    return db_permiso


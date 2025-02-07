from sqlalchemy.orm import Session
from models.models import Rol
from schemas.rol import RolCreate, RolUpdate

# Obtiene un rol por su ID.
def get_rol(db: Session, rol_id: int):
    return db.query(Rol).filter(Rol.rol_id == rol_id).first()

# Obtiene una lista de roles con paginación opcional (skip y limit).
def get_roles(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Rol).offset(skip).limit(limit).all()

# Crea un nuevo rol en la base de datos.
def create_rol(db: Session, rol: RolCreate):
    # Se construye una instancia del modelo Rol con los datos proporcionados.
    db_rol = Rol(**rol.dict())
    db.add(db_rol)  # Añade el objeto a la sesión.
    db.commit()  # Confirma los cambios en la base de datos.
    db.refresh(db_rol)  # Refresca el objeto para obtener el ID generado por la base de datos.
    return db_rol

# Actualiza un rol existente por su ID.
def update_rol(db: Session, rol_id: int, rol: RolUpdate):
    # Obtiene el rol por su ID.
    db_rol = get_rol(db, rol_id)
    if db_rol:
        # Actualiza los campos proporcionados en `rol`.
        for key, value in rol.dict().items():
            setattr(db_rol, key, value)
        db.commit()  # Guarda los cambios.
        db.refresh(db_rol)  # Refresca el objeto para asegurarse de que está actualizado.
    return db_rol

# Elimina un rol por su ID.
def delete_rol(db: Session, rol_id: int):
    # Obtiene el rol por su ID.
    db_rol = get_rol(db, rol_id)
    if db_rol:
        db.delete(db_rol)  # Marca el objeto para eliminación.
        db.commit()  # Confirma los cambios.
    return db_rol


from sqlalchemy.orm import Session  # Permite manejar sesiones para realizar operaciones en la base de datos.
from models.models import RolesPermisos  # Modelo ORM que representa la tabla "RolesPermisos".
from schemas.roles_permisos import RolesPermisosCreate  # Esquema para la creación de relaciones entre roles y permisos.
from sqlalchemy.exc import IntegrityError  # Manejo de errores de integridad, como violaciones de restricciones únicas.

# Obtener una relación específica entre rol y permiso.
def get_roles_permisos(db: Session, rol_id: int, permiso_id: int):
    return db.query(RolesPermisos).filter(
        RolesPermisos.rol_id == rol_id, RolesPermisos.permiso_id == permiso_id
    ).first()

# Listar relaciones entre roles y permisos con paginación (saltando y limitando registros).
def get_roles_permisos_list(db: Session, skip: int = 0, limit: int = 10):
    return db.query(RolesPermisos).offset(skip).limit(limit).all()

# Crear una nueva relación entre un rol y un permiso.
def create_roles_permisos(db: Session, roles_permisos: RolesPermisosCreate):
    db_roles_permisos = RolesPermisos(**roles_permisos.dict())  # Convierte el esquema en un objeto del modelo.
    try:
        db.add(db_roles_permisos)  # Agrega el nuevo registro a la sesión.
        db.commit()  # Confirma los cambios en la base de datos.
        db.refresh(db_roles_permisos)  # Refresca el objeto para incluir el ID generado por la BD.
    except IntegrityError:  # Si ya existe una relación igual, captura la excepción.
        db.rollback()  # Revierte la transacción para evitar inconsistencias.
        return None
    return db_roles_permisos

# Eliminar una relación entre rol y permiso si existe.
def delete_roles_permisos(db: Session, rol_id: int, permiso_id: int):
    db_roles_permisos = get_roles_permisos(db, rol_id, permiso_id)  # Busca la relación.
    if db_roles_permisos:
        db.delete(db_roles_permisos)  # Elimina el registro.
        db.commit()  # Confirma los cambios.
    return db_roles_permisos


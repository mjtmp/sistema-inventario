from fastapi import APIRouter, Depends, HTTPException  # Dependencias y manejo de excepciones para la API.
from sqlalchemy.orm import Session  # Manejo de sesiones.
from crud.roles_permisos import (
    get_roles_permisos,
    get_roles_permisos_list,
    create_roles_permisos,
    delete_roles_permisos,
)  # CRUD para roles y permisos.
from schemas.roles_permisos import RolesPermisos, RolesPermisosCreate  # Esquemas utilizados por la API.
from database import SessionLocal  # Conexión a la base de datos.

router = APIRouter()  # Crea un enrutador para gestionar las rutas relacionadas.

# Dependencia para obtener una sesión de la base de datos.
def get_db():
    db = SessionLocal()
    try:
        yield db  # Proporciona la sesión activa.
    finally:
        db.close()  # Cierra la sesión al terminar.

# Crear una nueva relación rol-permiso.
@router.post("/", response_model=RolesPermisos)
def crear_roles_permisos(roles_permisos: RolesPermisosCreate, db: Session = Depends(get_db)):
    db_roles_permisos = create_roles_permisos(db=db, roles_permisos=roles_permisos)
    if db_roles_permisos is None:  # Si ya existe la relación, lanza una excepción.
        raise HTTPException(status_code=400, detail="El rol y el permiso ya están asignados.")
    return db_roles_permisos

# Listar todas las relaciones rol-permiso con paginación.
@router.get("/", response_model=list[RolesPermisos])
def listar_roles_permisos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_roles_permisos_list(db=db, skip=skip, limit=limit)

# Eliminar una relación específica rol-permiso.
@router.delete("/{rol_id}/{permiso_id}", response_model=RolesPermisos)
def eliminar_roles_permisos(rol_id: int, permiso_id: int, db: Session = Depends(get_db)):
    db_roles_permisos = delete_roles_permisos(db=db, rol_id=rol_id, permiso_id=permiso_id)
    if db_roles_permisos is None:  # Si no existe la relación, lanza una excepción.
        raise HTTPException(status_code=404, detail="Relación rol-permiso no encontrada")
    return db_roles_permisos


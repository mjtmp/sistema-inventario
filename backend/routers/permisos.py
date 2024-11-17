from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud.permisos import get_permiso, get_permisos, create_permiso, delete_permiso
from schemas.permisos import Permiso, PermisoCreate
from database import SessionLocal  # Configuración de la base de datos.

router = APIRouter()  # Crea un enrutador para gestionar los endpoints de permisos.

# Dependencia que proporciona la sesión de la base de datos.
def get_db():
    db = SessionLocal()  # Crea una nueva sesión.
    try:
        yield db  # La devuelve para ser utilizada en las rutas.
    finally:
        db.close()  # Cierra la sesión al finalizar.

# Endpoint para crear un nuevo permiso.
@router.post("/", response_model=Permiso)
def crear_permiso(permiso: PermisoCreate, db: Session = Depends(get_db)):
    db_permiso = create_permiso(db=db, permiso=permiso)
    if db_permiso is None:  # Si el permiso ya existe:
        raise HTTPException(status_code=400, detail="El permiso ya existe.")
    return db_permiso

# Endpoint para listar permisos con paginación.
@router.get("/", response_model=list[Permiso])
def listar_permisos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_permisos(db=db, skip=skip, limit=limit)

# Endpoint para obtener un permiso específico por su ID.
@router.get("/{permiso_id}", response_model=Permiso)
def obtener_permiso(permiso_id: int, db: Session = Depends(get_db)):
    db_permiso = get_permiso(db=db, permiso_id=permiso_id)
    if db_permiso is None:  # Si no se encuentra el permiso:
        raise HTTPException(status_code=404, detail="Permiso no encontrado")
    return db_permiso

# Endpoint para eliminar un permiso por su ID.
@router.delete("/{permiso_id}", response_model=Permiso)
def eliminar_permiso(permiso_id: int, db: Session = Depends(get_db)):
    db_permiso = delete_permiso(db=db, permiso_id=permiso_id)
    if db_permiso is None:  # Si no se encuentra el permiso:
        raise HTTPException(status_code=404, detail="Permiso no encontrado")
    return db_permiso


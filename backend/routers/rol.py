from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
<<<<<<< HEAD
from crud.rol import get_rol, get_roles, create_rol, update_rol, delete_rol
from schemas.rol import Rol, RolCreate, RolUpdate
from database import SessionLocal

router = APIRouter()

# Dependencia para obtener una sesión de la base de datos.
def get_db():
    db = SessionLocal()
    try:
        yield db  # Retorna la sesión activa.
    finally:
        db.close()  # Cierra la sesión al finalizar.

# Crea un nuevo rol.
=======
from ..crud.rol import get_rol, get_roles, create_rol, update_rol, delete_rol
from ..schemas.rol import Rol, RolCreate, RolUpdate
from backend.database import SessionLocal

router = APIRouter()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39
@router.post("/", response_model=Rol)
def crear_rol(rol: RolCreate, db: Session = Depends(get_db)):
    return create_rol(db=db, rol=rol)

<<<<<<< HEAD
# Lista todos los roles con paginación.
=======
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39
@router.get("/", response_model=list[Rol])
def listar_roles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_roles(db=db, skip=skip, limit=limit)

<<<<<<< HEAD
# Obtiene un rol por su ID.
=======
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39
@router.get("/{rol_id}", response_model=Rol)
def obtener_rol(rol_id: int, db: Session = Depends(get_db)):
    db_rol = get_rol(db=db, rol_id=rol_id)
    if db_rol is None:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return db_rol

<<<<<<< HEAD
# Actualiza un rol por su ID.
=======
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39
@router.put("/{rol_id}", response_model=Rol)
def actualizar_rol(rol_id: int, rol: RolUpdate, db: Session = Depends(get_db)):
    db_rol = update_rol(db=db, rol_id=rol_id, rol=rol)
    if db_rol is None:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return db_rol

<<<<<<< HEAD
# Elimina un rol por su ID.
=======
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39
@router.delete("/{rol_id}", response_model=Rol)
def eliminar_rol(rol_id: int, db: Session = Depends(get_db)):
    db_rol = delete_rol(db=db, rol_id=rol_id)
    if db_rol is None:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return db_rol
<<<<<<< HEAD

=======
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39

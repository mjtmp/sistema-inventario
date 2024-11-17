from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
<<<<<<< HEAD
from crud.proveedores import get_proveedor, get_proveedores, create_proveedor, update_proveedor, delete_proveedor
from schemas.proveedores import Proveedor, ProveedorCreate, ProveedorUpdate
from database import SessionLocal

router = APIRouter()  # Crea un router para manejar las rutas relacionadas con proveedores

# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db  # Proporciona la sesión para ser usada en las rutas
    finally:
        db.close()  # Cierra la sesión después de su uso

# Ruta para crear un proveedor
=======
from ..crud.proveedores import get_proveedor, get_proveedores, create_proveedor, update_proveedor, delete_proveedor
from ..schemas.proveedores import Proveedor, ProveedorCreate, ProveedorUpdate
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
@router.post("/", response_model=Proveedor)
def crear_proveedor(proveedor: ProveedorCreate, db: Session = Depends(get_db)):
    return create_proveedor(db=db, proveedor=proveedor)

<<<<<<< HEAD
# Ruta para listar proveedores con paginación
@router.get("/", response_model=dict)
def listar_proveedores(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    proveedores, total = get_proveedores(db=db, skip=skip, limit=limit)
    # Convierte los objetos de base de datos en esquemas Pydantic y devuelve el total
    return {"proveedores": [Proveedor(**proveedor.to_dict()) for proveedor in proveedores], "total": total}

# Ruta para obtener un proveedor por ID
=======
@router.get("/", response_model=list[Proveedor])
def listar_proveedores(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_proveedores(db=db, skip=skip, limit=limit)

>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39
@router.get("/{proveedor_id}", response_model=Proveedor)
def obtener_proveedor(proveedor_id: int, db: Session = Depends(get_db)):
    db_proveedor = get_proveedor(db=db, proveedor_id=proveedor_id)
    if db_proveedor is None:
<<<<<<< HEAD
        # Lanza un error si no se encuentra el proveedor
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return db_proveedor

# Ruta para actualizar un proveedor
=======
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return db_proveedor

>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39
@router.put("/{proveedor_id}", response_model=Proveedor)
def actualizar_proveedor(proveedor_id: int, proveedor: ProveedorUpdate, db: Session = Depends(get_db)):
    db_proveedor = update_proveedor(db=db, proveedor_id=proveedor_id, proveedor=proveedor)
    if db_proveedor is None:
<<<<<<< HEAD
        # Lanza un error si no se encuentra el proveedor
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return db_proveedor

# Ruta para eliminar un proveedor
=======
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return db_proveedor

>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39
@router.delete("/{proveedor_id}", response_model=Proveedor)
def eliminar_proveedor(proveedor_id: int, db: Session = Depends(get_db)):
    db_proveedor = delete_proveedor(db=db, proveedor_id=proveedor_id)
    if db_proveedor is None:
<<<<<<< HEAD
        # Lanza un error si no se encuentra el proveedor
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return db_proveedor

=======
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return db_proveedor
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39

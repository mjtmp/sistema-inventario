from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
<<<<<<< HEAD
# Importa las funciones CRUD para interactuar con la base de datos.
from crud.reportes_inventario import (
    get_reporte_inventario, get_reportes_inventario, create_reporte_inventario, 
    update_reporte_inventario, delete_reporte_inventario
)
# Importa los esquemas para validar y estructurar los datos de entrada/salida.
from schemas.reportes_inventario import ReporteInventario, ReporteInventarioCreate, ReporteInventarioUpdate
from database import SessionLocal  # Módulo para manejar sesiones de base de datos.

router = APIRouter()

# Dependencia para obtener una sesión de la base de datos.
def get_db():
    db = SessionLocal()  # Crea una sesión de base de datos.
    try:
        yield db  # Retorna la sesión activa.
    finally:
        db.close()  # Cierra la sesión al finalizar.

# Crear un nuevo reporte de inventario.
=======
from ..crud.reportes_inventario import (
    get_reporte_inventario, get_reportes_inventario, create_reporte_inventario, 
    update_reporte_inventario, delete_reporte_inventario
)
from ..schemas.reportes_inventario import ReporteInventario, ReporteInventarioCreate, ReporteInventarioUpdate
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
@router.post("/", response_model=ReporteInventario)
def crear_reporte_inventario(reporte_inventario: ReporteInventarioCreate, db: Session = Depends(get_db)):
    return create_reporte_inventario(db=db, reporte_inventario=reporte_inventario)

<<<<<<< HEAD
# Listar reportes de inventario con soporte para paginación.
=======
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39
@router.get("/", response_model=list[ReporteInventario])
def listar_reportes_inventario(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_reportes_inventario(db=db, skip=skip, limit=limit)

<<<<<<< HEAD
# Obtener un reporte de inventario por su ID.
=======
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39
@router.get("/{reporte_id}", response_model=ReporteInventario)
def obtener_reporte_inventario(reporte_id: int, db: Session = Depends(get_db)):
    db_reporte_inventario = get_reporte_inventario(db=db, reporte_id=reporte_id)
    if db_reporte_inventario is None:
        raise HTTPException(status_code=404, detail="Reporte de inventario no encontrado")
    return db_reporte_inventario

<<<<<<< HEAD
# Actualizar un reporte de inventario existente.
=======
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39
@router.put("/{reporte_id}", response_model=ReporteInventario)
def actualizar_reporte_inventario(reporte_id: int, reporte_inventario: ReporteInventarioUpdate, db: Session = Depends(get_db)):
    db_reporte_inventario = update_reporte_inventario(db=db, reporte_id=reporte_id, reporte_inventario=reporte_inventario)
    if db_reporte_inventario is None:
        raise HTTPException(status_code=404, detail="Reporte de inventario no encontrado")
    return db_reporte_inventario

<<<<<<< HEAD
# Eliminar un reporte de inventario.
=======
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39
@router.delete("/{reporte_id}", response_model=ReporteInventario)
def eliminar_reporte_inventario(reporte_id: int, db: Session = Depends(get_db)):
    db_reporte_inventario = delete_reporte_inventario(db=db, reporte_id=reporte_id)
    if db_reporte_inventario is None:
        raise HTTPException(status_code=404, detail="Reporte de inventario no encontrado")
    return db_reporte_inventario
<<<<<<< HEAD

=======
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39

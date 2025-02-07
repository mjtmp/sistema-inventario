from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from schemas.productos import Producto
# Importa las funciones CRUD para interactuar con la base de datos.
from crud.reportes_inventario import (
    get_reporte_inventario, get_reportes_inventario, create_reporte_inventario, 
    update_reporte_inventario, delete_reporte_inventario, obtener_reporte_inventario
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
@router.post("/", response_model=ReporteInventario)
def crear_reporte_inventario(reporte_inventario: ReporteInventarioCreate, db: Session = Depends(get_db)):
    return create_reporte_inventario(db=db, reporte_inventario=reporte_inventario)

# Listar reportes de inventario con soporte para paginación.
@router.get("/", response_model=list[ReporteInventario])
def listar_reportes_inventario(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_reportes_inventario(db=db, skip=skip, limit=limit)

# Obtener un reporte de inventario por su ID.
@router.get("/{reporte_id}", response_model=ReporteInventario)
def obtener_reporte_inventario(reporte_id: int, db: Session = Depends(get_db)):
    db_reporte_inventario = get_reporte_inventario(db=db, reporte_id=reporte_id)
    if db_reporte_inventario is None:
        raise HTTPException(status_code=404, detail="Reporte de inventario no encontrado")
    return db_reporte_inventario

# Actualizar un reporte de inventario existente.
@router.put("/{reporte_id}", response_model=ReporteInventario)
def actualizar_reporte_inventario(reporte_id: int, reporte_inventario: ReporteInventarioUpdate, db: Session = Depends(get_db)):
    db_reporte_inventario = update_reporte_inventario(db=db, reporte_id=reporte_id, reporte_inventario=reporte_inventario)
    if db_reporte_inventario is None:
        raise HTTPException(status_code=404, detail="Reporte de inventario no encontrado")
    return db_reporte_inventario

# Eliminar un reporte de inventario.
@router.delete("/{reporte_id}", response_model=ReporteInventario)
def eliminar_reporte_inventario(reporte_id: int, db: Session = Depends(get_db)):
    db_reporte_inventario = delete_reporte_inventario(db=db, reporte_id=reporte_id)
    if db_reporte_inventario is None:
        raise HTTPException(status_code=404, detail="Reporte de inventario no encontrado")
    return db_reporte_inventario

from utils.generar_reporte_inventario import generar_reporte_inventario
from fastapi.responses import FileResponse 

@router.get("/generar-reporte-inventario")
def generar_reporte(fecha_inicio: Optional[str] = Query(None), fecha_fin: Optional[str] = Query(None), db: Session = Depends(get_db)):
    try:
        reporte_path = generar_reporte_inventario(fecha_inicio, fecha_fin)
        return FileResponse(reporte_path, media_type='application/pdf', filename="reporte_inventario.pdf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





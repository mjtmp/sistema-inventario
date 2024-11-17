from fastapi import APIRouter, Depends, HTTPException  # Herramientas para rutas y manejo de errores
from sqlalchemy.orm import Session  # Manejo de sesiones de base de datos
from crud.reportes_entrega import (  # Funciones CRUD importadas
    get_reporte_entrega, get_reportes_entrega, create_reporte_entrega, 
    update_reporte_entrega, delete_reporte_entrega
)
from schemas.reportes_entrega import ReporteEntrega, ReporteEntregaCreate, ReporteEntregaUpdate  # Esquemas de validación
from database import SessionLocal  # Sesión de la base de datos

# Crear un enrutador para las rutas relacionadas con reportes de entrega
router = APIRouter()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()  # Crear una nueva sesión
    try:
        yield db
    finally:
        db.close()  # Cerrar la sesión después de usarla

# Crear un nuevo reporte de entrega
@router.post("/", response_model=ReporteEntrega)
def crear_reporte_entrega(reporte_entrega: ReporteEntregaCreate, db: Session = Depends(get_db)):
    return create_reporte_entrega(db=db, reporte_entrega=reporte_entrega)

# Listar todos los reportes de entrega con soporte para paginación
@router.get("/", response_model=list[ReporteEntrega])
def listar_reportes_entrega(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_reportes_entrega(db=db, skip=skip, limit=limit)

# Obtener un reporte de entrega específico por su ID
@router.get("/{entrega_id}", response_model=ReporteEntrega)
def obtener_reporte_entrega(entrega_id: int, db: Session = Depends(get_db)):
    db_reporte_entrega = get_reporte_entrega(db=db, entrega_id=entrega_id)
    if db_reporte_entrega is None:
        # Manejar el caso donde el ID no existe en la base de datos
        raise HTTPException(status_code=404, detail="Reporte de entrega no encontrado")
    return db_reporte_entrega

# Actualizar un reporte de entrega existente
@router.put("/{entrega_id}", response_model=ReporteEntrega)
def actualizar_reporte_entrega(entrega_id: int, reporte_entrega: ReporteEntregaUpdate, db: Session = Depends(get_db)):
    db_reporte_entrega = update_reporte_entrega(db=db, entrega_id=entrega_id, reporte_entrega=reporte_entrega)
    if db_reporte_entrega is None:
        raise HTTPException(status_code=404, detail="Reporte de entrega no encontrado")
    return db_reporte_entrega

# Eliminar un reporte de entrega existente
@router.delete("/{entrega_id}", response_model=ReporteEntrega)
def eliminar_reporte_entrega(entrega_id: int, db: Session = Depends(get_db)):
    db_reporte_entrega = delete_reporte_entrega(db=db, entrega_id=entrega_id)
    if db_reporte_entrega is None:
        raise HTTPException(status_code=404, detail="Reporte de entrega no encontrado")
    return db_reporte_entrega


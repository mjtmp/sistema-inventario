from typing import List  # Para especificar listas en las respuestas
from fastapi import APIRouter, Depends, HTTPException  # FastAPI y manejo de dependencias
from sqlalchemy.orm import Session, joinedload  # Sesión y carga de relaciones
from crud.salidas_inventario import (
    get_salida_inventario, get_salidas_inventario, create_salida_inventario,
    update_salida_inventario, delete_salida_inventario
)
from schemas.salidas_inventario import SalidaInventario, SalidaInventarioCreate, SalidaInventarioUpdate
from database import SessionLocal
from models.models import SalidasInventario

router = APIRouter()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para crear una nueva salida de inventario
@router.post("/", response_model=SalidaInventario)
def crear_salida_inventario(salida: SalidaInventarioCreate, db: Session = Depends(get_db)):
    return create_salida_inventario(db=db, salida=salida)

# Endpoint para listar salidas de inventario con paginación
@router.get("/", response_model=List[SalidaInventario])
def listar_salidas_inventario(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    # Usa `joinedload` para cargar relaciones
    salidas = db.query(SalidasInventario).options(
        joinedload(SalidasInventario.cliente),  # Relación con cliente
        joinedload(SalidasInventario.vendedor),  # Relación con vendedor
        joinedload(SalidasInventario.factura)  # Relación con factura
    ).offset(skip).limit(limit).all()
    return salidas

# Endpoint para obtener una salida de inventario por ID
@router.get("/{salida_id}", response_model=SalidaInventario)
def obtener_salida_inventario(salida_id: int, db: Session = Depends(get_db)):
    db_salida = get_salida_inventario(db=db, salida_id=salida_id)
    if db_salida is None:
        raise HTTPException(status_code=404, detail="Salida no encontrada")
    return db_salida

# Endpoint para actualizar una salida de inventario
@router.put("/{salida_id}", response_model=SalidaInventario)
def actualizar_salida_inventario(salida_id: int, salida: SalidaInventarioUpdate, db: Session = Depends(get_db)):
    db_salida = update_salida_inventario(db=db, salida_id=salida_id, salida=salida)
    if db_salida is None:
        raise HTTPException(status_code=404, detail="Salida no encontrada")
    return db_salida

# Endpoint para eliminar una salida de inventario
@router.delete("/{salida_id}", response_model=SalidaInventario)
def eliminar_salida_inventario(salida_id: int, db: Session = Depends(get_db)):
    db_salida = delete_salida_inventario(db=db, salida_id=salida_id)
    if db_salida is None:
        raise HTTPException(status_code=404, detail="Salida no encontrada")
    return db_salida



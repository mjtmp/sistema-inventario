from typing import List  # Para manejar listas en los esquemas de respuesta
from fastapi import APIRouter, Depends, HTTPException  # Componentes de FastAPI para crear rutas y manejar dependencias
from sqlalchemy.orm import Session  # Sesión de SQLAlchemy
from crud.pagos import get_pago, get_pagos, create_pago, update_pago, delete_pago  # Operaciones CRUD para pagos
from schemas.pagos import Pago, PagoCreate, PagoUpdate  # Esquemas para validar datos de entrada y salida
from database import SessionLocal  # Objeto de sesión local para conectar con la base de datos

# Crea un enrutador para las rutas relacionadas con pagos
router = APIRouter()

# Dependencia que proporciona la sesión de base de datos para las operaciones
def get_db():
    db = SessionLocal()
    try:
        yield db  # Entrega la sesión para su uso
    finally:
        db.close()  # Cierra la conexión cuando ya no se necesita

# Ruta POST para crear un nuevo pago
@router.post("/", response_model=Pago)
def crear_pago(pago: PagoCreate, db: Session = Depends(get_db)):
    return create_pago(db=db, pago=pago)

# Ruta GET para listar todos los pagos con paginación
@router.get("/", response_model=List[Pago])
def listar_pagos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_pagos(db=db, skip=skip, limit=limit)

# Ruta GET para obtener un pago específico por ID
@router.get("/{pago_id}", response_model=Pago)
def obtener_pago(pago_id: int, db: Session = Depends(get_db)):
    db_pago = get_pago(db=db, pago_id=pago_id)
    if db_pago is None:  # Maneja el caso en que no se encuentra el pago
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return db_pago

# Ruta PUT para actualizar un pago por ID
@router.put("/{pago_id}", response_model=Pago)
def actualizar_pago(pago_id: int, pago: PagoUpdate, db: Session = Depends(get_db)):
    db_pago = update_pago(db=db, pago_id=pago_id, pago=pago)
    if db_pago is None:  # Maneja el caso en que no se encuentra el pago
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return db_pago

# Ruta DELETE para eliminar un pago por ID
@router.delete("/{pago_id}", response_model=Pago)
def eliminar_pago(pago_id: int, db: Session = Depends(get_db)):
    db_pago = delete_pago(db=db, pago_id=pago_id)
    if db_pago is None:  # Maneja el caso en que no se encuentra el pago
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return db_pago


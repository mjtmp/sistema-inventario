from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..crud.productos import get_producto, get_productos, create_producto, update_producto, delete_producto
from ..schemas.productos import Producto, ProductoCreate, ProductoUpdate
from backend.database import SessionLocal

router = APIRouter()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=Producto)
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    return create_producto(db=db, producto=producto)

@router.get("/", response_model=list[Producto])
def listar_productos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_productos(db=db, skip=skip, limit=limit)

@router.get("/{producto_id}", response_model=Producto)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = get_producto(db=db, producto_id=producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

@router.put("/{producto_id}", response_model=Producto)
def actualizar_producto(producto_id: int, producto: ProductoUpdate, db: Session = Depends(get_db)):
    db_producto = update_producto(db=db, producto_id=producto_id, producto=producto)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

@router.delete("/{producto_id}", response_model=Producto)
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = delete_producto(db=db, producto_id=producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

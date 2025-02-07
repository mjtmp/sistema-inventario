from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.models import Proveedor  # Asegúrate de importar el modelo Proveedor de SQLAlchemy
from crud.proveedores import get_proveedor, get_proveedores, create_proveedor, update_proveedor, delete_proveedor
from schemas.proveedores import Proveedor as ProveedorSchema, ProveedorCreate, ProveedorUpdate
from database import SessionLocal
from sqlalchemy import func  # Importa func para funciones de agregación
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ProveedorSchema)
def crear_proveedor(proveedor: ProveedorCreate, db: Session = Depends(get_db)):
    try:
        return create_proveedor(db=db, proveedor=proveedor, usuario_id=proveedor.usuario_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=dict)
def listar_proveedores(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    proveedores, total = get_proveedores(db=db, skip=skip, limit=limit)
    return {"proveedores": [ProveedorSchema(**proveedor.to_dict()) for proveedor in proveedores], "total": total}

@router.get("/total", response_model=dict)
def total_proveedores(db: Session = Depends(get_db)):
    total = db.query(func.count(Proveedor.proveedor_id)).scalar()
    return {"total": total}

@router.get("/buscar-por-rif", response_model=List[ProveedorSchema])
def buscar_proveedor_por_rif(rif: str, db: Session = Depends(get_db)):
    if rif:
        proveedores = db.query(Proveedor).filter(Proveedor.rif == rif).all()
        for proveedor in proveedores:
            proveedor.fecha_creacion = proveedor.fecha_creacion.isoformat() if proveedor.fecha_creacion else None
            proveedor.fecha_actualizacion = proveedor.fecha_actualizacion.isoformat() if proveedor.fecha_actualizacion else None
            for producto in proveedor.productos:
                producto.fecha_creacion = producto.fecha_creacion.isoformat() if producto.fecha_creacion else None
                producto.fecha_actualizacion = producto.fecha_actualizacion.isoformat() if producto.fecha_actualizacion else None
        return proveedores
    return []

@router.get("/{proveedor_id}", response_model=ProveedorSchema)
def obtener_proveedor(proveedor_id: int, db: Session = Depends(get_db)):
    db_proveedor = get_proveedor(db=db, proveedor_id=proveedor_id)
    if db_proveedor is None:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return db_proveedor

@router.put("/{proveedor_id}", response_model=ProveedorSchema)
def actualizar_proveedor(proveedor_id: int, proveedor: ProveedorUpdate, db: Session = Depends(get_db)):
    try:
        db_proveedor = update_proveedor(db=db, proveedor_id=proveedor_id, proveedor=proveedor, usuario_id=proveedor.usuario_id)
        if db_proveedor is None:
            raise HTTPException(status_code=404, detail="Proveedor no encontrado")
        return db_proveedor
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{proveedor_id}", response_model=ProveedorSchema)
def eliminar_proveedor(proveedor_id: int, usuario_id: int, db: Session = Depends(get_db)):
    db_proveedor = delete_proveedor(db=db, proveedor_id=proveedor_id, usuario_id=usuario_id)
    if db_proveedor is None:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return db_proveedor



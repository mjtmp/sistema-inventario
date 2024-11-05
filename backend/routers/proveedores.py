from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
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

@router.post("/", response_model=Proveedor)
def crear_proveedor(proveedor: ProveedorCreate, db: Session = Depends(get_db)):
    return create_proveedor(db=db, proveedor=proveedor)

@router.get("/", response_model=list[Proveedor])
def listar_proveedores(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_proveedores(db=db, skip=skip, limit=limit)

@router.get("/{proveedor_id}", response_model=Proveedor)
def obtener_proveedor(proveedor_id: int, db: Session = Depends(get_db)):
    db_proveedor = get_proveedor(db=db, proveedor_id=proveedor_id)
    if db_proveedor is None:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return db_proveedor

@router.put("/{proveedor_id}", response_model=Proveedor)
def actualizar_proveedor(proveedor_id: int, proveedor: ProveedorUpdate, db: Session = Depends(get_db)):
    db_proveedor = update_proveedor(db=db, proveedor_id=proveedor_id, proveedor=proveedor)
    if db_proveedor is None:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return db_proveedor

@router.delete("/{proveedor_id}", response_model=Proveedor)
def eliminar_proveedor(proveedor_id: int, db: Session = Depends(get_db)):
    db_proveedor = delete_proveedor(db=db, proveedor_id=proveedor_id)
    if db_proveedor is None:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return db_proveedor

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.models import Cliente
from crud.clientes import get_cliente, get_clientes, create_cliente, update_cliente, delete_cliente, numero_documento_existe
from schemas.clientes import Cliente as ClienteSchema, ClienteCreate, ClienteUpdate
from database import SessionLocal
from typing import List
from sqlalchemy import func

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ClienteSchema)
def crear_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    try:
        return create_cliente(db=db, cliente=cliente, usuario_id=cliente.usuario_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=dict)
def listar_clientes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    clientes, total = get_clientes(db=db, skip=skip, limit=limit)
    return {"clientes": [ClienteSchema(**cliente.to_dict()) for cliente in clientes], "total": total}

@router.get("/total", response_model=dict)
def total_clientes(db: Session = Depends(get_db)):
    total = db.query(func.count(Cliente.cliente_id)).scalar()
    return {"total": total}

@router.get("/search", response_model=List[ClienteSchema])
def listar_clientes_por_nombre(nombre: str = "", db: Session = Depends(get_db)):
    if nombre:
        return db.query(Cliente).filter(Cliente.nombre.ilike(f"%{nombre}%")).all()
    return db.query(Cliente).all()

@router.get("/buscar-por-documento", response_model=List[ClienteSchema])
def buscar_cliente_por_documento(numero_documento: str, db: Session = Depends(get_db)):
    if numero_documento:
        return db.query(Cliente).filter(Cliente.numero_documento == numero_documento).all()
    return []

@router.get("/{cliente_id}", response_model=ClienteSchema)
def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = get_cliente(db=db, cliente_id=cliente_id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return db_cliente

@router.put("/{cliente_id}", response_model=ClienteSchema)
def actualizar_cliente(cliente_id: int, cliente: ClienteUpdate, db: Session = Depends(get_db)):
    try:
        return update_cliente(db=db, cliente_id=cliente_id, cliente=cliente, usuario_id=cliente.usuario_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{cliente_id}", response_model=ClienteSchema)
def eliminar_cliente(cliente_id: int, usuario_id: int, db: Session = Depends(get_db)):
    db_cliente = delete_cliente(db=db, cliente_id=cliente_id, usuario_id=usuario_id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return db_cliente




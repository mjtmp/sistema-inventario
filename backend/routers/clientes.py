from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..crud.clientes import get_cliente, get_clientes, create_cliente, update_cliente, delete_cliente
from ..schemas.clientes import Cliente, ClienteCreate, ClienteUpdate
from backend.database import SessionLocal

router = APIRouter()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=Cliente)
def crear_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    return create_cliente(db=db, cliente=cliente)

@router.get("/", response_model=list[Cliente])
def listar_clientes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_clientes(db=db, skip=skip, limit=limit)

@router.get("/{cliente_id}", response_model=Cliente)
def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = get_cliente(db=db, cliente_id=cliente_id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return db_cliente

@router.put("/{cliente_id}", response_model=Cliente)
def actualizar_cliente(cliente_id: int, cliente: ClienteUpdate, db: Session = Depends(get_db)):
    db_cliente = update_cliente(db=db, cliente_id=cliente_id, cliente=cliente)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return db_cliente

@router.delete("/{cliente_id}", response_model=Cliente)
def eliminar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = delete_cliente(db=db, cliente_id=cliente_id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return db_cliente

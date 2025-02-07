from typing import List  # Importa para especificar listas en tipos de retorno
from fastapi import APIRouter, Depends, HTTPException  # Importaciones necesarias para rutas en FastAPI
from sqlalchemy.orm import Session  # Para manejar la sesión de la base de datos
from crud.pedidos import (  # Importa las funciones CRUD relacionadas con `Pedido`
    get_pedido, get_pedidos, create_pedido, update_pedido, delete_pedido
)
from schemas.pedidos import Pedido, PedidoCreate, PedidoUpdate  # Esquemas para los datos de entrada/salida
from database import SessionLocal  # Configuración de la conexión a la base de datos
import logging  # Para registrar eventos y errores

# Inicializa un enrutador para el módulo de pedidos
router = APIRouter()

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db  # Devuelve la sesión para cada solicitud
    finally:
        db.close()  # Asegura que la sesión se cierra después de usarla

# Configuración de logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Ruta para crear un pedido
@router.post("/", response_model=Pedido)
def crear_pedido(pedido: PedidoCreate, db: Session = Depends(get_db)):
    try:
        logger.debug("Datos recibidos para crear pedido: %s", pedido)  # Registro de datos de entrada
        return create_pedido(db=db, pedido=pedido)
    except Exception as e:
        logger.error(f"Error al crear pedido: {str(e)}")  # Registro de errores
        raise HTTPException(status_code=422, detail="Error al crear pedido")

# Ruta para listar pedidos con soporte de paginación
@router.get("/", response_model=List[Pedido])
def listar_pedidos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_pedidos(db=db, skip=skip, limit=limit)

# Ruta para obtener un pedido por su ID
@router.get("/{pedido_id}", response_model=Pedido)
def obtener_pedido(pedido_id: int, db: Session = Depends(get_db)):
    db_pedido = get_pedido(db=db, pedido_id=pedido_id)
    if db_pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")  # Error si no existe
    return db_pedido

# Ruta para actualizar un pedido existente
@router.put("/{pedido_id}", response_model=Pedido)
def actualizar_pedido(pedido_id: int, pedido: PedidoUpdate, db: Session = Depends(get_db)):
    db_pedido = update_pedido(db=db, pedido_id=pedido_id, pedido=pedido)
    if db_pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return db_pedido

# Ruta para eliminar un pedido por su ID
@router.delete("/{pedido_id}", response_model=Pedido)
def eliminar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    db_pedido = delete_pedido(db=db, pedido_id=pedido_id)
    if db_pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return db_pedido



'''from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud.pedidos import get_pedido, get_pedidos, create_pedido, update_pedido, delete_pedido
from schemas.pedidos import Pedido, PedidoCreate, PedidoUpdate
from database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=Pedido)
def crear_pedido(pedido: PedidoCreate, db: Session = Depends(get_db)):
    return create_pedido(db=db, pedido=pedido)

@router.get("/", response_model=List[Pedido])
def listar_pedidos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_pedidos(db=db, skip=skip, limit=limit)

@router.get("/{pedido_id}", response_model=Pedido)
def obtener_pedido(pedido_id: int, db: Session = Depends(get_db)):
    db_pedido = get_pedido(db=db, pedido_id=pedido_id)
    if db_pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return db_pedido

@router.put("/{pedido_id}", response_model=Pedido)
def actualizar_pedido(pedido_id: int, pedido: PedidoUpdate, db: Session = Depends(get_db)):
    db_pedido = update_pedido(db=db, pedido_id=pedido_id, pedido=pedido)
    if db_pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return db_pedido

@router.delete("/{pedido_id}", response_model=Pedido)
def eliminar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    db_pedido = delete_pedido(db=db, pedido_id=pedido_id)
    if db_pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return db_pedido'''


'''from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud.pedidos import get_pedido, get_pedidos, create_pedido, update_pedido, delete_pedido, crear_pedido
from schemas.pedidos import Pedido, PedidoCreate, PedidoUpdate
from database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=Pedido)
def crear_pedido(pedido: PedidoCreate, db: Session = Depends(get_db)):
    return create_pedido(db=db, pedido=pedido)

@router.post("/nuevo", response_model=Pedido)
def crear_pedido_nuevo(cliente_id: int, db: Session = Depends(get_db)):
    return crear_pedido(db, cliente_id)

@router.get("/", response_model=List[Pedido])
def listar_pedidos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_pedidos(db=db, skip=skip, limit=limit)

@router.get("/{pedido_id}", response_model=Pedido)
def obtener_pedido(pedido_id: int, db: Session = Depends(get_db)):
    db_pedido = get_pedido(db=db, pedido_id=pedido_id)
    if db_pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return db_pedido

@router.put("/{pedido_id}", response_model=Pedido)
def actualizar_pedido(pedido_id: int, pedido: PedidoUpdate, db: Session = Depends(get_db)):
    db_pedido = update_pedido(db=db, pedido_id=pedido_id, pedido=pedido)
    if db_pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return db_pedido

@router.delete("/{pedido_id}", response_model=Pedido)
def eliminar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    db_pedido = delete_pedido(db=db, pedido_id=pedido_id)
    if db_pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return db_pedido
'''

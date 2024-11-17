<<<<<<< HEAD
from fastapi import APIRouter, Depends, HTTPException  # Importamos las dependencias de FastAPI.
from sqlalchemy.orm import Session  # Importamos Session para acceder a la base de datos.
from models.models import Cliente  # Importamos el modelo Cliente.
from crud.clientes import get_cliente, get_clientes, create_cliente, update_cliente, delete_cliente  # Importamos las funciones del CRUD.
from schemas.clientes import Cliente as ClienteSchema, ClienteCreate, ClienteUpdate  # Importamos los esquemas de datos.
from database import SessionLocal  # Importamos la sesión de base de datos local.
from typing import List  # Importamos List para especificar que devolveremos una lista.

router = APIRouter()  # Creamos el enrutador de FastAPI.

# Función para obtener la base de datos.
def get_db():
    db = SessionLocal()  # Creamos una nueva sesión para interactuar con la base de datos.
    try:
        yield db  # Retornamos la sesión para usarla en las rutas.
    finally:
        db.close()  # Cerramos la sesión al finalizar.

# Ruta para crear un nuevo cliente.
@router.post("/", response_model=ClienteSchema)
def crear_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    return create_cliente(db=db, cliente=cliente)  # Llamamos a la función de CRUD para crear el cliente.

# Ruta para listar los clientes con paginación.
@router.get("/", response_model=dict)
def listar_clientes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    clientes, total = get_clientes(db=db, skip=skip, limit=limit)  # Obtenemos los clientes con la función CRUD.
    return {"clientes": [ClienteSchema(**cliente.to_dict()) for cliente in clientes], "total": total}  # Retornamos los clientes y el total.

# Ruta para listar los clientes que coincidan con un nombre.
@router.get("/search", response_model=List[ClienteSchema])
def listar_clientes_por_nombre(nombre: str = "", db: Session = Depends(get_db)):
    if nombre:  # Si se pasa un nombre, filtramos los clientes.
        return db.query(Cliente).filter(Cliente.nombre.ilike(f"%{nombre}%")).all()  # Realizamos la consulta en la base de datos.
    return db.query(Cliente).all()  # Si no se pasa nombre, retornamos todos los clientes.

# Ruta para obtener un cliente específico por su ID.
@router.get("/{cliente_id}", response_model=ClienteSchema)
def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = get_cliente(db=db, cliente_id=cliente_id)  # Buscamos el cliente por ID.
    if db_cliente is None:  # Si no se encuentra el cliente.
        raise HTTPException(status_code=404, detail="Cliente no encontrado")  # Lanzamos una excepción 404.
    return db_cliente  # Retornamos el cliente encontrado.

# Ruta para actualizar un cliente específico por su ID.
@router.put("/{cliente_id}", response_model=ClienteSchema)
def actualizar_cliente(cliente_id: int, cliente: ClienteUpdate, db: Session = Depends(get_db)):
    db_cliente = update_cliente(db=db, cliente_id=cliente_id, cliente=cliente)  # Llamamos a la función CRUD para actualizar.
    if db_cliente is None:  # Si no se encuentra el cliente.
        raise HTTPException(status_code=404, detail="Cliente no encontrado")  # Lanzamos una excepción 404.
    return db_cliente  # Retornamos el cliente actualizado.

# Ruta para eliminar un cliente específico por su ID.
@router.delete("/{cliente_id}", response_model=ClienteSchema)
def eliminar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = delete_cliente(db=db, cliente_id=cliente_id)  # Llamamos a la función CRUD para eliminar.
    if db_cliente is None:  # Si no se encuentra el cliente.
        raise HTTPException(status_code=404, detail="Cliente no encontrado")  # Lanzamos una excepción 404.
    return db_cliente  # Retornamos el cliente eliminado.

=======
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
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39

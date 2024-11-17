<<<<<<< HEAD
from fastapi import APIRouter, Depends, HTTPException  # Para manejar rutas, dependencias y excepciones.
from sqlalchemy.orm import Session  # Manejo de sesiones de la base de datos.
from models.models import Producto  # Modelo de SQLAlchemy.
from crud.productos import (  # Funciones CRUD para productos.
    get_producto, get_productos, create_producto, update_producto, delete_producto
)
from schemas.productos import Producto as ProductoSchema, ProductoCreate, ProductoUpdate  # Esquemas Pydantic.
from database import SessionLocal  # Gestión de conexión a la base de datos.
from typing import List  # Tipado para listas.

router = APIRouter()  # Crea un enrutador para gestionar las rutas relacionadas con productos.

# Dependencia para obtener una sesión de la base de datos.
def get_db():
    db = SessionLocal()
    try:
        yield db  # Retorna la sesión para uso temporal.
    finally:
        db.close()  # Cierra la conexión después de usarla.

# Ruta para crear un producto.
@router.post("/", response_model=ProductoSchema)
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    return create_producto(db=db, producto=producto)

# Ruta para listar productos con paginación y contar el total.
@router.get("/", response_model=dict)
def listar_productos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    productos, total = get_productos(db=db, skip=skip, limit=limit)
    # Convierte cada producto al esquema definido y devuelve un diccionario con productos y total.
    return {"productos": [ProductoSchema(**producto.to_dict()) for producto in productos], "total": total}

# Ruta para buscar productos por nombre (búsqueda parcial).
@router.get("/search", response_model=List[ProductoSchema])
def listar_productos_por_nombre(nombre: str = "", db: Session = Depends(get_db)):
    if nombre:
        # Busca productos cuyo nombre contenga el término buscado (case insensitive).
        return db.query(Producto).filter(Producto.nombre.ilike(f"%{nombre}%")).all()
    return db.query(Producto).all()  # Devuelve todos los productos si no se especifica un nombre.

# Ruta para obtener un producto específico por su ID.
@router.get("/{producto_id}", response_model=ProductoSchema)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = get_producto(db=db, producto_id=producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")  # Maneja error de no encontrado.
    return db_producto

# Ruta para actualizar un producto.
@router.put("/{producto_id}", response_model=ProductoSchema)
def actualizar_producto(producto_id: int, producto: ProductoUpdate, db: Session = Depends(get_db)):
    db_producto = update_producto(db=db, producto_id=producto_id, producto=producto)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

# Ruta para eliminar un producto.
@router.delete("/{producto_id}", response_model=ProductoSchema)
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = delete_producto(db=db, producto_id=producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto





'''from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud.productos import get_producto, get_productos, create_producto, update_producto, delete_producto
from schemas.productos import Producto, ProductoCreate, ProductoUpdate
from database import SessionLocal
from typing import List
=======
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..crud.productos import get_producto, get_productos, create_producto, update_producto, delete_producto
from ..schemas.productos import Producto, ProductoCreate, ProductoUpdate
from backend.database import SessionLocal
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39

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

<<<<<<< HEAD
@router.get("/", response_model=dict)
def listar_productos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    productos, total = get_productos(db=db, skip=skip, limit=limit)
    return {"productos": [Producto(**producto.to_dict()) for producto in productos], "total": total}
=======
@router.get("/", response_model=list[Producto])
def listar_productos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_productos(db=db, skip=skip, limit=limit)
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39

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
<<<<<<< HEAD
'''
=======
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39

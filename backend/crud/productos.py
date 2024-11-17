<<<<<<< HEAD
from sqlalchemy.orm import Session  # Para manejar la sesión de base de datos.
from datetime import datetime  # Para gestionar las fechas de creación y actualización.
from models.models import Producto  # Modelo de SQLAlchemy para la tabla de productos.
from schemas.productos import ProductoCreate, ProductoUpdate  # Esquemas Pydantic para validación de datos.

# Obtener un producto específico por su ID.
def get_producto(db: Session, producto_id: int):
    return db.query(Producto).filter(Producto.producto_id == producto_id).first()

# Obtener todos los productos con paginación y contar el total.
def get_productos(db: Session, skip: int = 0, limit: int = 10):
    productos = db.query(Producto).offset(skip).limit(limit).all()  # Obtiene una lista paginada.
    total = db.query(Producto).count()  # Cuenta el total de productos en la base de datos.
    return productos, total  # Devuelve los productos y el total.

# Crear un nuevo producto en la base de datos.
def create_producto(db: Session, producto: ProductoCreate):
    # Crea un objeto de producto con las fechas de creación y actualización.
    db_producto = Producto(**producto.dict(), fecha_creacion=datetime.now(), fecha_actualizacion=datetime.now())
    db.add(db_producto)  # Añade el producto a la sesión.
    db.commit()  # Guarda los cambios en la base de datos.
    db.refresh(db_producto)  # Actualiza la instancia con los datos generados (e.g., IDs).
    return db_producto

# Actualizar un producto existente por su ID.
def update_producto(db: Session, producto_id: int, producto: ProductoUpdate):
    db_producto = get_producto(db, producto_id)  # Busca el producto.
    if db_producto:
        for key, value in producto.dict().items():
            setattr(db_producto, key, value)  # Actualiza los campos con los valores proporcionados.
        db_producto.fecha_actualizacion = datetime.now()  # Actualiza la fecha de modificación.
        db.commit()  # Guarda los cambios.
        db.refresh(db_producto)  # Actualiza los datos del objeto.
    return db_producto

# Eliminar un producto por su ID.
def delete_producto(db: Session, producto_id: int):
    db_producto = get_producto(db, producto_id)  # Busca el producto.
    if db_producto:
        db.delete(db_producto)  # Elimina el producto.
        db.commit()  # Guarda los cambios.
    return db_producto

=======
from sqlalchemy.orm import Session
from ..models.models import Producto
from ..schemas.productos import ProductoCreate, ProductoUpdate

def get_producto(db: Session, producto_id: int):
    return db.query(Producto).filter(Producto.producto_id == producto_id).first()

def get_productos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Producto).offset(skip).limit(limit).all()

def create_producto(db: Session, producto: ProductoCreate):
    # Crear una instancia de Producto con todos los datos, incluido 'proveedor_id'
    db_producto = Producto(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

def update_producto(db: Session, producto_id: int, producto: ProductoUpdate):
    # Obtener el producto actual para modificarlo
    db_producto = get_producto(db, producto_id)
    if db_producto:
        # Actualizar cada campo de producto, incluido 'proveedor_id' si es necesario
        for key, value in producto.dict().items():
            setattr(db_producto, key, value)
        db.commit()
        db.refresh(db_producto)
    return db_producto

def delete_producto(db: Session, producto_id: int):
    db_producto = get_producto(db, producto_id)
    if db_producto:
        db.delete(db_producto)
        db.commit()
    return db_producto
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39

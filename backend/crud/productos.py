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

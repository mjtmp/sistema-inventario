from sqlalchemy.orm import Session
from models.models import Categoria, Producto
from schemas.categorias import CategoriaCreate, CategoriaUpdate
from sqlalchemy import func
from crud.historial import registrar_accion  # Importar la función para registrar acciones

def get_categoria(db: Session, categoria_id: int):
    return db.query(Categoria).filter(Categoria.categoria_id == categoria_id).first()

def get_categorias_con_conteo_productos(db: Session):
    query = db.query(
        Categoria.nombre,
        func.count(Producto.producto_id).label("total_productos")
    ).join(Producto, Producto.categoria_id == Categoria.categoria_id)\
     .group_by(Categoria.nombre).all()

    return [{"nombre": row.nombre, "total_productos": row.total_productos} for row in query]

def get_categorias(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Categoria).offset(skip).limit(limit).all()

    
def create_categoria(db: Session, categoria: CategoriaCreate):
    db_categoria = Categoria(**categoria.dict())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

    
def update_categoria(db: Session, categoria_id: int, categoria: CategoriaUpdate, usuario_id: int):
    db_categoria = db.query(Categoria).filter(Categoria.categoria_id == categoria_id).first()
    if db_categoria:
        for key, value in categoria.dict().items():
            setattr(db_categoria, key, value)
        db.commit()
        db.refresh(db_categoria)
        registrar_accion(db, usuario_id, "Actualización de categoría", f"Categoría {db_categoria.nombre} actualizada.")
        return db_categoria
    return None

def delete_categoria(db: Session, categoria_id: int, usuario_id: int):
    db_categoria = db.query(Categoria).filter(Categoria.categoria_id == categoria_id).first()
    if db_categoria:
        db.delete(db_categoria)
        db.commit()
        registrar_accion(db, usuario_id, "Eliminación de categoría", f"Categoría {db_categoria.nombre} eliminada.")
        return db_categoria
    return None

def get_total_categorias(db: Session):
    return db.query(func.count(Categoria.categoria_id)).scalar()



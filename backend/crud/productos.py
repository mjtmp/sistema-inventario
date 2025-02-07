from sqlalchemy.orm import Session
from datetime import datetime, date
from models.models import Producto, Categoria, EntradaInventario
from schemas.productos import ProductoCreate, ProductoUpdate
from utils.generar_codeBar import BarcodeGenerator
from sqlalchemy import func
from crud.historial import registrar_accion  # Importar la función para registrar acciones

def codigo_existe(db: Session, codigo: str) -> bool:
    return db.query(Producto).filter(Producto.codigo == codigo).first() is not None

def get_producto(db: Session, producto_id: int):
    producto = db.query(Producto).filter(Producto.producto_id == producto_id).first()
    return producto

def get_productos(db: Session, skip: int = 0, limit: int = 100):
    productos = db.query(Producto).offset(skip).limit(limit).all()
    total = db.query(Producto).count()
    return productos, total

def create_producto(db: Session, producto: ProductoCreate, usuario_id: int):
    if codigo_existe(db, producto.codigo):
        raise ValueError("El código del producto ya existe. Por favor, elige un código distinto.")
    
    if producto.cantidad_minima is not None and producto.stock < producto.cantidad_minima:
        raise ValueError("El stock debe ser mayor o igual a la cantidad mínima.")
    
    if producto.cantidad_maxima is not None and producto.stock > producto.cantidad_maxima:
        raise ValueError("El stock debe ser menor o igual a la cantidad máxima.")
    
    generador = BarcodeGenerator()
    producto.codigo_barras = generador.generate(ean=producto.codigo_barras)

    if not producto.categoria_id:
        raise ValueError("El ID de la categoría no puede ser nulo.")
    categoria = db.query(Categoria).filter(Categoria.categoria_id == producto.categoria_id).first()
    if not categoria:
        raise ValueError("La categoría especificada no existe.")

    producto_data = producto.dict()
    producto_data.pop('usuario_id', None)  # Eliminar el campo usuario_id del diccionario
    db_producto = Producto(**producto_data, fecha_creacion=date.today(), fecha_actualizacion=date.today())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    
    registrar_accion(db, usuario_id, "Creación de producto", f"Producto {db_producto.nombre} creado.")
    
    # Convertir las fechas a cadenas antes de devolver la respuesta
    db_producto.fecha_creacion = db_producto.fecha_creacion.isoformat() if db_producto.fecha_creacion else None
    db_producto.fecha_actualizacion = db_producto.fecha_actualizacion.isoformat() if db_producto.fecha_actualizacion else None
    return db_producto

def update_producto(db: Session, producto_id: int, producto: ProductoUpdate, usuario_id: int):
    db_producto = get_producto(db, producto_id)
    if db_producto:
        if producto.codigo and producto.codigo != db_producto.codigo:
            if codigo_existe(db, producto.codigo):
                raise ValueError("El código del producto ya existe. Por favor, elige un código distinto.")
        
        if producto.categoria_id:
            categoria = db.query(Categoria).filter(Categoria.categoria_id == producto.categoria_id).first()
            if not categoria:
                raise ValueError("La categoría especificada no existe.")
        
        if producto.cantidad_minima is not None and producto.stock < producto.cantidad_minima:
            raise ValueError("El stock debe ser mayor o igual a la cantidad mínima.")
        
        if producto.cantidad_maxima is not None and producto.stock > producto.cantidad_maxima:
            raise ValueError("El stock debe ser menor o igual a la cantidad máxima.")

        for key, value in producto.dict(exclude_unset=True).items():
            setattr(db_producto, key, value)
        db_producto.fecha_actualizacion = date.today()
        db.commit()
        db.refresh(db_producto)
        
        registrar_accion(db, usuario_id, "Actualización de producto", f"Producto {db_producto.nombre} actualizado.")
        
        # Convertir las fechas a cadenas antes de devolver la respuesta
        db_producto.fecha_creacion = db_producto.fecha_creacion.isoformat() if db_producto.fecha_creacion else None
        db_producto.fecha_actualizacion = db_producto.fecha_actualizacion.isoformat() if db_producto.fecha_actualizacion else None
    return db_producto

def delete_producto(db: Session, producto_id: int, usuario_id: int):
    db_producto = get_producto(db, producto_id)
    if db_producto:
        db.delete(db_producto)
        db.commit()
        registrar_accion(db, usuario_id, "Eliminación de producto", f"Producto {db_producto.nombre} eliminado.")
    return db_producto

def get_productos_por_fecha(db: Session, fecha_inicio=None, fecha_fin=None, skip=0, limit=100):
    query = db.query(Producto)
    if fecha_inicio and fecha_fin:
        query = query.filter(Producto.fecha_actualizacion.between(fecha_inicio, fecha_fin))
    total = query.count()
    productos = query.offset(skip).limit(limit).all()
    return productos, total

def get_total_productos_stock(db: Session):
    total = db.query(func.sum(Producto.stock)).scalar() 
    return total

def get_valor_inventario(db: Session):
    valor_total = db.query(func.sum(Producto.precio * Producto.stock)).scalar()
    if valor_total is None:
        valor_total = 0.0
    return valor_total

def check_product_levels(db: Session, producto_id: int):
    producto = get_producto(db, producto_id)
    if producto.stock < producto.cantidad_minima:
        return f"Stock bajo de {producto.nombre} (Código: {producto.codigo}). Stock actual: {producto.stock} unidades. Ubicación: {producto.ubicacion}. Reabastecer."
    if producto.stock > producto.cantidad_maxima:
        return f"Stock excedido de {producto.nombre} (Código: {producto.codigo}). Stock actual: {producto.stock} unidades. Ubicación: {producto.ubicacion}. Reducir stock."
    return None

def parse_date(date_str):
    if isinstance(date_str, str):
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    elif isinstance(date_str, datetime):
        return date_str.date()
    return date_str

def get_productos_inventario_bajo(db: Session):
    productos_bajos = db.query(Producto).filter(Producto.stock < Producto.cantidad_minima).all()
    alertas = []
    for producto in productos_bajos:
        producto.fecha_creacion = parse_date(producto.fecha_creacion)
        producto.fecha_actualizacion = parse_date(producto.fecha_actualizacion)
        alerta = {
            "producto_id": producto.producto_id,
            "nombre": producto.nombre,
            "codigo": producto.codigo,
            "stock": producto.stock,
            "ubicacion": producto.ubicacion,
            "cantidad_minima": producto.cantidad_minima,
            "cantidad_maxima": producto.cantidad_maxima,
            "fecha_creacion": producto.fecha_creacion.isoformat() if producto.fecha_creacion else None,
            "fecha_actualizacion": producto.fecha_actualizacion.isoformat() if producto.fecha_actualizacion else None
        }
        alertas.append(alerta)
    return alertas

def get_precio_costo_unitario(db: Session, producto_id: int):
    entrada_reciente = db.query(EntradaInventario).filter(EntradaInventario.producto_id == producto_id).order_by(EntradaInventario.fecha.desc()).first()
    return entrada_reciente.precio_compra if entrada_reciente else 0.0








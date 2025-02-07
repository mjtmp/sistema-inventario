from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from models.models import Producto
from crud.productos import (
    get_producto, get_productos, create_producto, update_producto, 
    delete_producto, get_productos_por_fecha, 
    get_total_productos_stock, get_valor_inventario, check_product_levels,
    get_productos_inventario_bajo, get_precio_costo_unitario
)
from schemas.productos import Producto as ProductoSchema, ProductoCreate, ProductoUpdate, ProductoResponse
from database import SessionLocal
from typing import List, Optional
from datetime import datetime, date

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Nueva ruta para obtener productos con inventario bajo.
@router.get("/inventario_bajo", response_model=List[dict])
def obtener_productos_inventario_bajo(db: Session = Depends(get_db)):
    alertas = get_productos_inventario_bajo(db)
    if not alertas:
        return []
    return alertas

# Nueva ruta para reponer directamente productos.
# Definición de la función parse_date
def parse_date(date_str):
    if isinstance(date_str, str):
        return datetime.fromisoformat(date_str).date()
    elif isinstance(date_str, datetime):
        return date_str.date()
    return date_str

@router.put("/reponer/{producto_id}", response_model=ProductoSchema)
def reponer_producto(producto_id: int, cantidad: int = Query(...), db: Session = Depends(get_db)):
    db_producto = get_producto(db=db, producto_id=producto_id)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    db_producto.stock += cantidad
    db_producto.fecha_actualizacion = datetime.now().date()

    # Asegurarse de que las fechas están en el formato adecuado para SQLite
    db_producto.fecha_creacion = parse_date(db_producto.fecha_creacion)
    db_producto.fecha_actualizacion = parse_date(db_producto.fecha_actualizacion)

    db.commit()
    db.refresh(db_producto)

    # Convertir las fechas a cadenas ISO para la respuesta
    db_producto.fecha_creacion = db_producto.fecha_creacion.isoformat() if db_producto.fecha_creacion else None
    db_producto.fecha_actualizacion = db_producto.fecha_actualizacion.isoformat() if db_producto.fecha_actualizacion else None

    return db_producto

@router.get("/total_stock", response_model=dict)
def total_productos_stock(db: Session = Depends(get_db)):
    total = get_total_productos_stock(db)
    return {"total": total}

@router.get("/valor_inventario", response_model=dict)
def valor_inventario(db: Session = Depends(get_db)):
    valor_total = get_valor_inventario(db)
    return {"valor_total": valor_total}

@router.post("/", response_model=ProductoSchema)
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    try:
        return create_producto(db=db, producto=producto, usuario_id=producto.usuario_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# Añadimos una ruta para obtener el precio de compra de un producto
@router.get("/precio_compra/{producto_id}", response_model=float)
def obtener_precio_compra(producto_id: int, db: Session = Depends(get_db)):
    try:
        precio_compra = get_precio_costo_unitario(db, producto_id)
        return precio_compra
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/filtrar", response_model=dict)
def filtrar_productos_por_fecha(skip: int = 0, limit: int = 10, fecha_inicio: Optional[str] = Query(None), fecha_fin: Optional[str] = Query(None), db: Session = Depends(get_db)):
    productos, total = get_productos_por_fecha(db=db, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, skip=skip, limit=limit)
    return {"productos": [ProductoSchema(**producto.to_dict()) for producto in productos], "total": total}

@router.get("/", response_model=dict)
def listar_productos(skip: int = 0, limit: int = 100, fecha_inicio: Optional[str] = Query(None), fecha_fin: Optional[str] = Query(None), db: Session = Depends(get_db)):
    if fecha_inicio and fecha_fin:
        productos, total = get_productos_por_fecha(db=db, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, skip=skip, limit=limit)
    else:
        productos, total = get_productos(db=db, skip=skip, limit=limit)
    return {"productos": [ProductoSchema(**producto.to_dict()) for producto in productos], "total": total}

@router.get("/search", response_model=List[ProductoSchema])
def listar_productos_por_nombre_o_codigo(nombre: Optional[str] = "", codigo: Optional[str] = "", db: Session = Depends(get_db)):
    if codigo:
        productos = db.query(Producto).filter(Producto.codigo.ilike(f"%{codigo}%")).all()
    else:
        productos = db.query(Producto).filter(Producto.nombre.ilike(f"%{nombre}%")).order_by(Producto.nombre.asc()).all()
    
    for producto in productos:
        producto.fecha_creacion = producto.fecha_creacion.isoformat() if producto.fecha_creacion else None
        producto.fecha_actualizacion = producto.fecha_actualizacion.isoformat() if producto.fecha_actualizacion else None
    return productos

@router.get("/{producto_id}", response_model=ProductoSchema)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = get_producto(db=db, producto_id=producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Convertir las fechas a cadenas antes de devolver la respuesta
    db_producto.fecha_creacion = db_producto.fecha_creacion.isoformat() if db_producto.fecha_creacion else None
    db_producto.fecha_actualizacion = db_producto.fecha_actualizacion.isoformat() if db_producto.fecha_actualizacion else None
    return db_producto

@router.put("/{producto_id}", response_model=ProductoSchema)
def actualizar_producto(producto_id: int, producto: ProductoUpdate, db: Session = Depends(get_db)):
    try:
        db_producto = update_producto(db=db, producto_id=producto_id, producto=producto, usuario_id=producto.usuario_id)
        if db_producto is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return db_producto
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{producto_id}", response_model=ProductoSchema)
def eliminar_producto(producto_id: int, usuario_id: int, db: Session = Depends(get_db)):
    db_producto = delete_producto(db=db, producto_id=producto_id, usuario_id=usuario_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

# Ruta para verificar los niveles de inventario de un producto.
@router.get("/check_levels/{producto_id}", response_model=dict)
def verificar_niveles_producto(producto_id: int, db: Session = Depends(get_db)):
    alerta = check_product_levels(db, producto_id)
    if alerta:
        return {"alerta": alerta}
    return {"mensaje": "Niveles de inventario normales"}


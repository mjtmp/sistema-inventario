from sqlalchemy.orm import Session  # Manejo de sesiones de la base de datos
from models.models import SalidasInventario, Producto  # Modelos de base de datos
from schemas.salidas_inventario import SalidaInventarioCreate, SalidaInventarioUpdate  # Esquemas Pydantic
from datetime import datetime  # Manejo de fechas

# Obtiene una salida de inventario específica por su ID
def get_salida_inventario(db: Session, salida_id: int):
    return db.query(SalidasInventario).filter(SalidasInventario.salida_id == salida_id).first()

# Obtiene una lista de salidas de inventario con paginación
def get_salidas_inventario(db: Session, skip: int = 0, limit: int = 10):
    return db.query(SalidasInventario).offset(skip).limit(limit).all()

# Crea una nueva salida de inventario
def create_salida_inventario(db: Session, salida: SalidaInventarioCreate):
    # Verifica si el producto asociado existe
    producto = db.query(Producto).filter(Producto.producto_id == salida.producto_id).first()
    if not producto:
        raise ValueError(f"Producto con ID {salida.producto_id} no encontrado.")
    
    iva_porcentaje = 0.16  # IVA del 16%
    monto_total = salida.cantidad * salida.precio_venta
    # Si el producto tiene IVA, agrega el impuesto
    if producto.tiene_iva:
        monto_total += monto_total * iva_porcentaje

    # Crea una instancia del modelo SalidasInventario
    db_salida = SalidasInventario(
        producto_id=salida.producto_id,
        cliente_id=salida.cliente_id,
        factura_id=salida.factura_id,
        cantidad=salida.cantidad,
        precio_venta=monto_total,
        fecha=datetime.now(),
        vendedor_id=salida.vendedor_id
    )
    db.add(db_salida)  # Añade la salida a la sesión
    db.commit()  # Guarda los cambios en la base de datos
    db.refresh(db_salida)  # Refresca la instancia con los datos guardados
    return db_salida

# Actualiza una salida de inventario existente
def update_salida_inventario(db: Session, salida_id: int, salida: SalidaInventarioUpdate):
    db_salida = get_salida_inventario(db, salida_id)
    if db_salida:
        # Verifica si el producto asociado existe
        producto = db.query(Producto).filter(Producto.producto_id == salida.producto_id).first()
        if not producto:
            raise ValueError(f"Producto con ID {salida.producto_id} no encontrado.")

        iva_porcentaje = 0.16  # IVA del 16%
        monto_total = salida.cantidad * salida.precio_venta
        if producto.tiene_iva:
            monto_total += monto_total * iva_porcentaje

        # Actualiza los campos de la salida
        db_salida.producto_id = salida.producto_id
        db_salida.cliente_id = salida.cliente_id
        db_salida.factura_id = salida.factura_id
        db_salida.cantidad = salida.cantidad
        db_salida.precio_venta = monto_total
        db_salida.vendedor_id = salida.vendedor_id
        db.commit()  # Guarda los cambios
        db.refresh(db_salida)  # Refresca la instancia
    return db_salida

# Elimina una salida de inventario por su ID
def delete_salida_inventario(db: Session, salida_id: int):
    db_salida = get_salida_inventario(db, salida_id)
    if db_salida:
        db.delete(db_salida)  # Marca la salida para eliminación
        db.commit()  # Aplica los cambios
    return db_salida



'''from sqlalchemy.orm import Session
from models.models import SalidasInventario
from schemas.salidas_inventario import SalidaInventarioCreate, SalidaInventarioUpdate
from datetime import datetime

def get_salida_inventario(db: Session, salida_id: int):
    return db.query(SalidasInventario).filter(SalidasInventario.salida_id == salida_id).first()

def get_salidas_inventario(db: Session, skip: int = 0, limit: int = 10):
    return db.query(SalidasInventario).offset(skip).limit(limit).all()

def create_salida_inventario(db: Session, salida: SalidaInventarioCreate):
    db_salida = SalidasInventario(
        producto_id=salida.producto_id,
        cliente_id=salida.cliente_id,
        factura_id=salida.factura_id,  # Incluimos factura_id
        cantidad=salida.cantidad,
        precio_venta=salida.precio_venta,
        fecha=datetime.now(),
        vendedor_id=salida.vendedor_id
    )
    db.add(db_salida)
    db.commit()
    db.refresh(db_salida)
    return db_salida

def update_salida_inventario(db: Session, salida_id: int, salida: SalidaInventarioUpdate):
    db_salida = get_salida_inventario(db, salida_id)
    if db_salida:
        db_salida.producto_id = salida.producto_id
        db_salida.cliente_id = salida.cliente_id
        db_salida.factura_id = salida.factura_id  # Incluimos factura_id
        db_salida.cantidad = salida.cantidad
        db_salida.precio_venta = salida.precio_venta
        db_salida.vendedor_id = salida.vendedor_id
        db.commit()
        db.refresh(db_salida)
    return db_salida

def delete_salida_inventario(db: Session, salida_id: int):
    db_salida = get_salida_inventario(db, salida_id)
    if db_salida:
        db.delete(db_salida)
        db.commit()
    return db_salida
'''

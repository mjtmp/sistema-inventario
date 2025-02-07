from sqlalchemy.orm import Session
from datetime import datetime
from models.models import Proveedor
from schemas.proveedores import ProveedorCreate, ProveedorUpdate
from crud.historial import registrar_accion  # Importar la función para registrar acciones

def rif_existe(db: Session, rif: str) -> bool:
    return db.query(Proveedor).filter(Proveedor.rif == rif).first() is not None

def get_proveedor(db: Session, proveedor_id: int):
    proveedor = db.query(Proveedor).filter(Proveedor.proveedor_id == proveedor_id).first()
    if proveedor:
        proveedor.fecha_creacion = proveedor.fecha_creacion.isoformat() if proveedor.fecha_creacion else None
        proveedor.fecha_actualizacion = proveedor.fecha_actualizacion.isoformat() if proveedor.fecha_actualizacion else None
        for producto in proveedor.productos:
            producto.fecha_creacion = producto.fecha_creacion.isoformat() if producto.fecha_creacion else None
            producto.fecha_actualizacion = producto.fecha_actualizacion.isoformat() if producto.fecha_actualizacion else None
    return proveedor

def get_proveedores(db: Session, skip: int = 0, limit: int = 10):
    proveedores = db.query(Proveedor).offset(skip).limit(limit).all()
    for proveedor in proveedores:
        proveedor.fecha_creacion = proveedor.fecha_creacion.isoformat() if proveedor.fecha_creacion else None
        proveedor.fecha_actualizacion = proveedor.fecha_actualizacion.isoformat() if proveedor.fecha_actualizacion else None
        for producto in proveedor.productos:
            producto.fecha_creacion = producto.fecha_creacion.isoformat() if producto.fecha_creacion else None
            producto.fecha_actualizacion = producto.fecha_actualizacion.isoformat() if producto.fecha_actualizacion else None
    total = db.query(Proveedor).count()
    return proveedores, total

def create_proveedor(db: Session, proveedor: ProveedorCreate, usuario_id: int):
    if rif_existe(db, proveedor.rif):
        raise ValueError("El RIF ya existe. Por favor, elige un RIF distinto.")
    proveedor_data = proveedor.dict()
    proveedor_data.pop('usuario_id', None)  # Eliminar el campo usuario_id del diccionario
    db_proveedor = Proveedor(**proveedor_data, fecha_creacion=datetime.now(), fecha_actualizacion=datetime.now())
    db.add(db_proveedor)
    db.commit()
    db.refresh(db_proveedor)
    registrar_accion(db, usuario_id, "Registro de proveedor", f"Proveedor {db_proveedor.nombre} registrado.")
    
    db_proveedor.fecha_creacion = db_proveedor.fecha_creacion.isoformat() if db_proveedor.fecha_creacion else None
    db_proveedor.fecha_actualizacion = db_proveedor.fecha_actualizacion.isoformat() if db_proveedor.fecha_actualizacion else None
    
    return db_proveedor

def update_proveedor(db: Session, proveedor_id: int, proveedor: ProveedorUpdate, usuario_id: int):
    db_proveedor = db.query(Proveedor).filter(Proveedor.proveedor_id == proveedor_id).first()
    if db_proveedor:
        if proveedor.rif and proveedor.rif != db_proveedor.rif:
            if rif_existe(db, proveedor.rif):
                raise ValueError("El RIF ya existe. Por favor, elige un RIF distinto.")
        for key, value in proveedor.dict(exclude_unset=True).items():
            setattr(db_proveedor, key, value)
        db_proveedor.fecha_actualizacion = datetime.now()

        # Convertir fechas a objetos date si son cadenas.
        if isinstance(db_proveedor.fecha_creacion, str):
            db_proveedor.fecha_creacion = datetime.fromisoformat(db_proveedor.fecha_creacion).date()
        if isinstance(db_proveedor.fecha_actualizacion, str):
            db_proveedor.fecha_actualizacion = datetime.fromisoformat(db_proveedor.fecha_actualizacion).date()
        
        db.commit()
        db.refresh(db_proveedor)
        registrar_accion(db, usuario_id, "Actualización de proveedor", f"Proveedor {db_proveedor.nombre} actualizado.")

        # Convertir fechas a cadenas para la respuesta
        db_proveedor.fecha_creacion = db_proveedor.fecha_creacion.isoformat() if db_proveedor.fecha_creacion else None
        db_proveedor.fecha_actualizacion = db_proveedor.fecha_actualizacion.isoformat() if db_proveedor.fecha_actualizacion else None

        # Convertir las fechas de los productos a cadenas para la respuesta
        for producto in db_proveedor.productos:
            producto.fecha_creacion = producto.fecha_creacion.isoformat() if producto.fecha_creacion else None
            producto.fecha_actualizacion = producto.fecha_actualizacion.isoformat() if producto.fecha_actualizacion else None

    return db_proveedor

def delete_proveedor(db: Session, proveedor_id: int, usuario_id: int):
    db_proveedor = get_proveedor(db, proveedor_id)
    if db_proveedor:
        db.delete(db_proveedor)
        db.commit()
        registrar_accion(db, usuario_id, "Eliminación de proveedor", f"Proveedor {db_proveedor.nombre} eliminado.")
    return db_proveedor


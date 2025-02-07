from sqlalchemy.orm import Session
from datetime import datetime
from models.models import Cliente
from schemas.clientes import ClienteCreate, ClienteUpdate
from crud.historial import registrar_accion  # Importar la función para registrar acciones

def numero_documento_existe(db: Session, numero_documento: str) -> bool:
    return db.query(Cliente).filter(Cliente.numero_documento == numero_documento).first() is not None

def get_cliente(db: Session, cliente_id: int):
    return db.query(Cliente).filter(Cliente.cliente_id == cliente_id).first()

def get_clientes(db: Session, skip: int = 0, limit: int = 10):
    clientes = db.query(Cliente).offset(skip).limit(limit).all()
    total = db.query(Cliente).count()
    return clientes, total

def create_cliente(db: Session, cliente: ClienteCreate, usuario_id: int):
    if numero_documento_existe(db, cliente.numero_documento):
        raise ValueError("El número de documento ya existe. Por favor, elige un número de documento distinto.")
    db_cliente = Cliente(**cliente.dict(exclude={"usuario_id"}), fecha_creacion=datetime.now(), fecha_actualizacion=datetime.now())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    registrar_accion(db, usuario_id, "Registro de cliente", f"Cliente {db_cliente.nombre} registrado.")
    return db_cliente

def update_cliente(db: Session, cliente_id: int, cliente: ClienteUpdate, usuario_id: int):
    db_cliente = get_cliente(db, cliente_id)
    if db_cliente:
        if cliente.numero_documento and cliente.numero_documento != db_cliente.numero_documento:
            if numero_documento_existe(db, cliente.numero_documento):
                raise ValueError("El número de documento ya existe. Por favor, elige un número de documento distinto.")
        for key, value in cliente.dict(exclude_unset=True).items():
            setattr(db_cliente, key, value)
        db_cliente.fecha_actualizacion = datetime.now()
        db.commit()
        db.refresh(db_cliente)
        registrar_accion(db, usuario_id, "Actualización de cliente", f"Cliente {db_cliente.nombre} actualizado.")
        return db_cliente
    return None

def delete_cliente(db: Session, cliente_id: int, usuario_id: int):
    db_cliente = get_cliente(db, cliente_id)
    if db_cliente:
        db.delete(db_cliente)
        db.commit()
        registrar_accion(db, usuario_id, "Eliminación de cliente", f"Cliente {db_cliente.nombre} eliminado.")
        return db_cliente
    return None



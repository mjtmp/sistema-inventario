from sqlalchemy.orm import Session  # Importa la sesión de SQLAlchemy para interactuar con la base de datos
from models.models import Pago  # Modelo de la tabla `Pago` en la base de datos
from schemas.pagos import PagoCreate, PagoUpdate  # Esquemas Pydantic para la creación y actualización de pagos
from datetime import datetime  # Para obtener la fecha y hora actual

# Obtiene un pago específico por su ID
def get_pago(db: Session, pago_id: int):
    return db.query(Pago).filter(Pago.pago_id == pago_id).first()

# Lista todos los pagos con opciones de paginación (saltando `skip` elementos y limitando a `limit` resultados)
def get_pagos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Pago).offset(skip).limit(limit).all()

# Crea un nuevo pago en la base de datos, asignándole la fecha actual
def create_pago(db: Session, pago: PagoCreate):
    db_pago = Pago(**pago.dict(), fecha=datetime.now())  # Crea una instancia del modelo `Pago`
    db.add(db_pago)  # Agrega el pago a la sesión
    db.commit()  # Confirma los cambios en la base de datos
    db.refresh(db_pago)  # Actualiza el objeto con los datos almacenados
    return db_pago  # Devuelve el objeto creado

# Actualiza los datos de un pago existente
def update_pago(db: Session, pago_id: int, pago: PagoUpdate):
    db_pago = get_pago(db, pago_id)  # Busca el pago por ID
    if db_pago:  # Si el pago existe, actualiza sus atributos
        for key, value in pago.dict().items():
            setattr(db_pago, key, value)  # Asigna los nuevos valores
        db.commit()  # Guarda los cambios
        db.refresh(db_pago)  # Actualiza el objeto con los datos actualizados
    return db_pago  # Devuelve el pago actualizado (o `None` si no se encontró)

# Elimina un pago de la base de datos
def delete_pago(db: Session, pago_id: int):
    db_pago = get_pago(db, pago_id)  # Busca el pago por ID
    if db_pago:  # Si el pago existe, lo elimina
        db.delete(db_pago)  # Marca el objeto para eliminación
        db.commit()  # Confirma los cambios en la base de datos
    return db_pago  # Devuelve el pago eliminado (o `None` si no se encontró)


<<<<<<< HEAD
from sqlalchemy.orm import Session  # Importamos Session para interactuar con la base de datos.
from datetime import datetime  # Para obtener la fecha y hora actual.
from models.models import Cliente  # Importamos el modelo Cliente para interactuar con la tabla correspondiente.
from schemas.clientes import ClienteCreate, ClienteUpdate  # Importamos los esquemas para la creación y actualización de clientes.

# Función para obtener un cliente por su ID.
def get_cliente(db: Session, cliente_id: int):
    return db.query(Cliente).filter(Cliente.cliente_id == cliente_id).first()  # Realiza la consulta en la base de datos.

# Función para obtener todos los clientes con paginación.
def get_clientes(db: Session, skip: int = 0, limit: int = 10):
    clientes = db.query(Cliente).offset(skip).limit(limit).all()  # Obtiene los clientes con paginación.
    total = db.query(Cliente).count()  # Cuenta el total de clientes en la base de datos.
    return clientes, total  # Devuelve los clientes y el total.

# Función para crear un nuevo cliente.
def create_cliente(db: Session, cliente: ClienteCreate):
    # Asignamos la fecha de creación y la fecha de actualización al crear un nuevo cliente.
    db_cliente = Cliente(**cliente.dict(), fecha_creacion=datetime.now(), fecha_actualizacion=datetime.now())
    db.add(db_cliente)  # Añadimos el cliente a la sesión de base de datos.
    db.commit()  # Confirmamos la transacción.
    db.refresh(db_cliente)  # Refrescamos el cliente con los datos actualizados (como el ID generado).
    return db_cliente  # Retornamos el cliente creado.

# Función para actualizar un cliente existente.
def update_cliente(db: Session, cliente_id: int, cliente: ClienteUpdate):
    db_cliente = get_cliente(db, cliente_id)  # Buscamos el cliente por su ID.
    if db_cliente:  # Si el cliente existe en la base de datos.
        # Actualizamos cada atributo que se haya enviado en la solicitud (sin modificar los no proporcionados).
        for key, value in cliente.dict(exclude_unset=True).items():
            setattr(db_cliente, key, value)
        db_cliente.fecha_actualizacion = datetime.now()  # Actualizamos la fecha de actualización.
        db.commit()  # Confirmamos los cambios.
        db.refresh(db_cliente)  # Refrescamos los datos del cliente actualizado.
        return db_cliente  # Retornamos el cliente actualizado.
    return None  # Si no se encuentra el cliente, retornamos None.

# Función para eliminar un cliente.
def delete_cliente(db: Session, cliente_id: int):
    db_cliente = get_cliente(db, cliente_id)  # Buscamos el cliente por su ID.
    if db_cliente:  # Si el cliente existe.
        db.delete(db_cliente)  # Eliminamos el cliente de la base de datos.
        db.commit()  # Confirmamos la transacción de eliminación.
        return db_cliente  # Retornamos el cliente eliminado.
    return None  # Si el cliente no se encuentra, retornamos None.

=======
from sqlalchemy.orm import Session
from ..models.models import Cliente
from ..schemas.clientes import ClienteCreate, ClienteUpdate

def get_cliente(db: Session, cliente_id: int):
    return db.query(Cliente).filter(Cliente.cliente_id == cliente_id).first()

def get_clientes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Cliente).offset(skip).limit(limit).all()

def create_cliente(db: Session, cliente: ClienteCreate):
    db_cliente = Cliente(**cliente.dict())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def update_cliente(db: Session, cliente_id: int, cliente: ClienteUpdate):
    db_cliente = get_cliente(db, cliente_id)
    if db_cliente:
        for key, value in cliente.dict(exclude_unset=True).items():
            setattr(db_cliente, key, value)
        db.commit()
        db.refresh(db_cliente)
        return db_cliente
    return None

def delete_cliente(db: Session, cliente_id: int):
    db_cliente = get_cliente(db, cliente_id)
    if db_cliente:
        db.delete(db_cliente)
        db.commit()
        return db_cliente
    return None
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39

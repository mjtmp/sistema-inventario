from sqlalchemy.orm import Session  # Importa la clase `Session` para interactuar con la base de datos
from models.models import Pedido  # Modelo ORM de la tabla `Pedido`
from schemas.pedidos import PedidoCreate, PedidoUpdate  # Esquemas para validación y manipulación de datos
import datetime  # Se importa para manejar fechas si es necesario
import logging  # Utilizado para registrar mensajes informativos y errores

# Configuración básica para logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)  # Configura un logger específico para este módulo

# Obtiene un pedido específico por su ID
def get_pedido(db: Session, pedido_id: int):
    return db.query(Pedido).filter(Pedido.pedido_id == pedido_id).first()

# Lista todos los pedidos con soporte de paginación (salto y límite)
def get_pedidos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Pedido).offset(skip).limit(limit).all()

# Crea un nuevo pedido en la base de datos
def create_pedido(db: Session, pedido: PedidoCreate):
    try:
        # Convierte el esquema recibido a una instancia del modelo
        db_pedido = Pedido(**pedido.dict())
        db.add(db_pedido)  # Añade el pedido a la sesión
        db.commit()  # Confirma los cambios
        db.refresh(db_pedido)  # Actualiza la instancia con los datos generados por la base de datos (como IDs)
        logger.debug("Pedido creado exitosamente: %s", db_pedido)  # Registro de éxito
        return db_pedido
    except Exception as e:
        logger.error(f"Error al crear pedido: {str(e)}")  # Registro de errores
        raise  # Propaga el error

# Actualiza un pedido existente
def update_pedido(db: Session, pedido_id: int, pedido: PedidoUpdate):
    db_pedido = get_pedido(db, pedido_id)
    if db_pedido:
        # Actualiza los atributos del pedido con los valores del esquema
        for key, value in pedido.dict().items():
            setattr(db_pedido, key, value)
        db.commit()  # Guarda los cambios en la base de datos
        db.refresh(db_pedido)  # Refresca la instancia para reflejar los cambios
    return db_pedido

# Elimina un pedido por su ID
def delete_pedido(db: Session, pedido_id: int):
    db_pedido = get_pedido(db, pedido_id)
    if db_pedido:
        db.delete(db_pedido)  # Marca el pedido para eliminación
        db.commit()  # Confirma los cambios
    return db_pedido



'''from sqlalchemy.orm import Session
from models.models import Pedido
from schemas.pedidos import PedidoCreate, PedidoUpdate
import datetime

def get_pedido(db: Session, pedido_id: int):
    return db.query(Pedido).filter(Pedido.pedido_id == pedido_id).first()

def get_pedidos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Pedido).offset(skip).limit(limit).all()

def create_pedido(db: Session, pedido: PedidoCreate):
    db_pedido = Pedido(**pedido.dict())
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

def update_pedido(db: Session, pedido_id: int, pedido: PedidoUpdate):
    db_pedido = get_pedido(db, pedido_id)
    if db_pedido:
        for key, value in pedido.dict().items():
            setattr(db_pedido, key, value)
        db.commit()
        db.refresh(db_pedido)
    return db_pedido

def delete_pedido(db: Session, pedido_id: int):
    db_pedido = get_pedido(db, pedido_id)
    if db_pedido:
        db.delete(db_pedido)
        db.commit()
    return db_pedido
'''
# Importar las dependencias necesarias
from sqlalchemy.orm import Session
from models.models import DetallePedido
from schemas.detalles_pedidos import DetallePedidoCreate, DetallePedidoUpdate

# Función para obtener un detalle de pedido por su ID
def get_detalle_pedido(db: Session, detalle_id: int):
    return db.query(DetallePedido).filter(DetallePedido.detalle_id == detalle_id).first()

# Función para obtener todos los detalles de pedidos con paginación
def get_detalles_pedidos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(DetallePedido).offset(skip).limit(limit).all()

# Función para crear un nuevo detalle de pedido
def create_detalle_pedido(db: Session, detalle_pedido: DetallePedidoCreate):
    # Crear una nueva instancia de DetallePedido usando los datos del esquema
    db_detalle_pedido = DetallePedido(**detalle_pedido.dict())
    db.add(db_detalle_pedido)  # Agregar el objeto a la sesión de la base de datos
    db.commit()  # Confirmar los cambios
    db.refresh(db_detalle_pedido)  # Refrescar el objeto con los datos más recientes de la base de datos
    return db_detalle_pedido  # Retornar el objeto recién creado

# Función para actualizar un detalle de pedido existente
def update_detalle_pedido(db: Session, detalle_id: int, detalle_pedido: DetallePedidoUpdate):
    db_detalle_pedido = get_detalle_pedido(db, detalle_id)  # Obtener el detalle de pedido por su ID
    if db_detalle_pedido:
        for key, value in detalle_pedido.dict().items():  # Iterar sobre los campos a actualizar
            setattr(db_detalle_pedido, key, value)  # Asignar los nuevos valores
        db.commit()  # Confirmar los cambios
        db.refresh(db_detalle_pedido)  # Refrescar el objeto con los datos actualizados
    return db_detalle_pedido  # Retornar el objeto actualizado

# Función para eliminar un detalle de pedido
def delete_detalle_pedido(db: Session, detalle_id: int):
    db_detalle_pedido = get_detalle_pedido(db, detalle_id)  # Obtener el detalle de pedido por su ID
    if db_detalle_pedido:
        db.delete(db_detalle_pedido)  # Eliminar el objeto de la base de datos
        db.commit()  # Confirmar los cambios
    return db_detalle_pedido  # Retornar el objeto eliminado


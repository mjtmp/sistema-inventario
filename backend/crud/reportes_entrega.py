from sqlalchemy.orm import Session 
from models.models import ReportesEntrega, Pedido, Cliente, DetallePedido  # Modelo ORM para la tabla 'ReportesEntrega'
from schemas.reportes_entrega import ReporteEntregaCreate, ReporteEntregaUpdate  
from crud.historial import registrar_accion  # Importar la función para registrar acciones

def get_reporte_entrega(db: Session, entrega_id: int):
    return db.query(ReportesEntrega).filter(ReportesEntrega.entrega_id == entrega_id).first()

# Obtener una lista de reportes de entrega con paginación
def get_reportes_entrega(db: Session, skip: int = 0, limit: int = 10):
    return db.query(ReportesEntrega).offset(skip).limit(limit).all()

# Crear un nuevo reporte de entrega
def create_reporte_entrega(db: Session, reporte_entrega: ReporteEntregaCreate, usuario_id: int):
    db_reporte_entrega = ReportesEntrega(**reporte_entrega.dict())
    db.add(db_reporte_entrega)  # Agregar el objeto a la sesión
    db.commit()  # Confirmar los cambios en la base de datos
    db.refresh(db_reporte_entrega)  # Refrescar la instancia con los datos de la BD
    registrar_accion(db, usuario_id, "Creación de reporte de entrega", f"Reporte de entrega ID {db_reporte_entrega.entrega_id} creado.")
    return db_reporte_entrega

# Actualizar un reporte de entrega existente
def update_reporte_entrega(db: Session, entrega_id: int, reporte_entrega: ReporteEntregaUpdate, usuario_id: int):
    db_reporte_entrega = get_reporte_entrega(db, entrega_id)  # Obtener el reporte existente
    if db_reporte_entrega:
        for key, value in reporte_entrega.dict(exclude_unset=True).items():
            setattr(db_reporte_entrega, key, value)
        db.commit()  # Guardar los cambios
        db.refresh(db_reporte_entrega)  # Refrescar la instancia actualizada
        registrar_accion(db, usuario_id, "Actualización de reporte de entrega", f"Reporte de entrega ID {db_reporte_entrega.entrega_id} actualizado.")
    return db_reporte_entrega

# Eliminar un reporte de entrega por su ID
def delete_reporte_entrega(db: Session, entrega_id: int, usuario_id: int):
    db_reporte_entrega = get_reporte_entrega(db, entrega_id)  # Obtener el reporte existente
    if db_reporte_entrega:
        db.delete(db_reporte_entrega)  # Eliminar el objeto de la sesión
        db.commit()  # Confirmar los cambios en la base de datos
        registrar_accion(db, usuario_id, "Eliminación de reporte de entrega", f"Reporte de entrega ID {db_reporte_entrega.entrega_id} eliminado.")
    return db_reporte_entrega

def obtener_pedidos(db: Session, skip: int = 0, limit: int = 10):
    total = db.query(Pedido).count()
    pedidos = db.query(Pedido).offset(skip).limit(limit).all()
    return pedidos, total

def obtener_pedido(db: Session, pedido_id: int):
    return db.query(Pedido).filter(Pedido.pedido_id == pedido_id).first()

def obtener_detalles_pedido(db: Session, pedido_id: int):
    return db.query(DetallePedido).filter(DetallePedido.pedido_id == pedido_id).all()



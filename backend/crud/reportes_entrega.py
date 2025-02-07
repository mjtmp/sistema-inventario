from sqlalchemy.orm import Session  # Manejo de la sesión con la base de datos
from models.models import ReportesEntrega  # Modelo ORM para la tabla 'ReportesEntrega'
from schemas.reportes_entrega import ReporteEntregaCreate, ReporteEntregaUpdate  # Esquemas de validación

# Obtener un reporte de entrega específico por su ID
def get_reporte_entrega(db: Session, entrega_id: int):
    return db.query(ReportesEntrega).filter(ReportesEntrega.entrega_id == entrega_id).first()

# Obtener una lista de reportes de entrega con paginación
def get_reportes_entrega(db: Session, skip: int = 0, limit: int = 10):
    return db.query(ReportesEntrega).offset(skip).limit(limit).all()

# Crear un nuevo reporte de entrega
def create_reporte_entrega(db: Session, reporte_entrega: ReporteEntregaCreate):
    # Se crea una instancia del modelo 'ReportesEntrega' usando los datos proporcionados
    db_reporte_entrega = ReportesEntrega(**reporte_entrega.dict())
    db.add(db_reporte_entrega)  # Agregar el objeto a la sesión
    db.commit()  # Confirmar los cambios en la base de datos
    db.refresh(db_reporte_entrega)  # Refrescar la instancia con los datos de la BD
    return db_reporte_entrega

# Actualizar un reporte de entrega existente
def update_reporte_entrega(db: Session, entrega_id: int, reporte_entrega: ReporteEntregaUpdate):
    db_reporte_entrega = get_reporte_entrega(db, entrega_id)  # Obtener el reporte existente
    if db_reporte_entrega:
        # Actualizar los campos del reporte con los datos proporcionados
        for key, value in reporte_entrega.dict().items():
            setattr(db_reporte_entrega, key, value)
        db.commit()  # Guardar los cambios
        db.refresh(db_reporte_entrega)  # Refrescar la instancia actualizada
    return db_reporte_entrega

# Eliminar un reporte de entrega por su ID
def delete_reporte_entrega(db: Session, entrega_id: int):
    db_reporte_entrega = get_reporte_entrega(db, entrega_id)  # Obtener el reporte existente
    if db_reporte_entrega:
        db.delete(db_reporte_entrega)  # Eliminar el objeto de la sesión
        db.commit()  # Confirmar los cambios en la base de datos
    return db_reporte_entrega

from sqlalchemy.orm import Session
from models.models import Producto, EntradaInventario, SalidasInventario, ReportesInventario  # Modelo ORM para la tabla de reportes de inventario.
from schemas.reportes_inventario import ReporteInventarioCreate, ReporteInventarioUpdate  # Esquemas para validación de entrada/salida.
from sqlalchemy import or_

# Obtener un reporte de inventario específico por su ID.
def get_reporte_inventario(db: Session, reporte_id: int):
    return db.query(ReportesInventario).filter(ReportesInventario.reporte_id == reporte_id).first()

# Obtener una lista de reportes de inventario con soporte para paginación.
def get_reportes_inventario(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ReportesInventario).offset(skip).limit(limit).all()

# Crear un nuevo reporte de inventario en la base de datos.
def create_reporte_inventario(db: Session, reporte_inventario: ReporteInventarioCreate):
    # Convierte los datos de entrada en una instancia del modelo.
    db_reporte_inventario = ReportesInventario(**reporte_inventario.dict())
    db.add(db_reporte_inventario)  # Añade el objeto a la sesión.
    db.commit()  # Confirma los cambios en la base de datos.
    db.refresh(db_reporte_inventario)  # Refresca el objeto para incluir los cambios confirmados.
    return db_reporte_inventario

# Actualizar un reporte de inventario existente por su ID.
def update_reporte_inventario(db: Session, reporte_id: int, reporte_inventario: ReporteInventarioUpdate):
    db_reporte_inventario = get_reporte_inventario(db, reporte_id)  # Obtiene el reporte existente.
    if db_reporte_inventario:
        # Itera sobre los campos actualizables y los modifica.
        for key, value in reporte_inventario.dict().items():
            setattr(db_reporte_inventario, key, value)
        db.commit()  # Confirma los cambios.
        db.refresh(db_reporte_inventario)  # Actualiza el objeto en la sesión.
    return db_reporte_inventario

# Eliminar un reporte de inventario por su ID.
def delete_reporte_inventario(db: Session, reporte_id: int):
    db_reporte_inventario = get_reporte_inventario(db, reporte_id)
    if db_reporte_inventario:
        db.delete(db_reporte_inventario)  # Marca el objeto para eliminación.
        db.commit()  # Confirma los cambios en la base de datos.
    return db_reporte_inventario

#Para probar
def obtener_reporte_inventario(db: Session, fecha_inicio=None, fecha_fin=None):
    query = db.query(Producto)
    if fecha_inicio and fecha_fin:
        query = query.filter(Producto.fecha_actualizacion.between(fecha_inicio, fecha_fin))
    return query.all()






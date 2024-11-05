from sqlalchemy.orm import Session
from ..models.models import ReportesInventario
from ..schemas.reportes_inventario import ReporteInventarioCreate, ReporteInventarioUpdate

def get_reporte_inventario(db: Session, reporte_id: int):
    return db.query(ReportesInventario).filter(ReportesInventario.reporte_id == reporte_id).first()

def get_reportes_inventario(db: Session, skip: int = 0, limit: int = 10):
    return db.query(ReportesInventario).offset(skip).limit(limit).all()

def create_reporte_inventario(db: Session, reporte_inventario: ReporteInventarioCreate):
    db_reporte_inventario = ReportesInventario(**reporte_inventario.dict())
    db.add(db_reporte_inventario)
    db.commit()
    db.refresh(db_reporte_inventario)
    return db_reporte_inventario

def update_reporte_inventario(db: Session, reporte_id: int, reporte_inventario: ReporteInventarioUpdate):
    db_reporte_inventario = get_reporte_inventario(db, reporte_id)
    if db_reporte_inventario:
        for key, value in reporte_inventario.dict().items():
            setattr(db_reporte_inventario, key, value)
        db.commit()
        db.refresh(db_reporte_inventario)
    return db_reporte_inventario

def delete_reporte_inventario(db: Session, reporte_id: int):
    db_reporte_inventario = get_reporte_inventario(db, reporte_id)
    if db_reporte_inventario:
        db.delete(db_reporte_inventario)
        db.commit()
    return db_reporte_inventario

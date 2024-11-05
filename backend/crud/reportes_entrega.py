from sqlalchemy.orm import Session
from ..models.models import ReportesEntrega
from ..schemas.reportes_entrega import ReporteEntregaCreate, ReporteEntregaUpdate

def get_reporte_entrega(db: Session, entrega_id: int):
    return db.query(ReportesEntrega).filter(ReportesEntrega.entrega_id == entrega_id).first()

def get_reportes_entrega(db: Session, skip: int = 0, limit: int = 10):
    return db.query(ReportesEntrega).offset(skip).limit(limit).all()

def create_reporte_entrega(db: Session, reporte_entrega: ReporteEntregaCreate):
    db_reporte_entrega = ReportesEntrega(**reporte_entrega.dict())
    db.add(db_reporte_entrega)
    db.commit()
    db.refresh(db_reporte_entrega)
    return db_reporte_entrega

def update_reporte_entrega(db: Session, entrega_id: int, reporte_entrega: ReporteEntregaUpdate):
    db_reporte_entrega = get_reporte_entrega(db, entrega_id)
    if db_reporte_entrega:
        for key, value in reporte_entrega.dict().items():
            setattr(db_reporte_entrega, key, value)
        db.commit()
        db.refresh(db_reporte_entrega)
    return db_reporte_entrega

def delete_reporte_entrega(db: Session, entrega_id: int):
    db_reporte_entrega = get_reporte_entrega(db, entrega_id)
    if db_reporte_entrega:
        db.delete(db_reporte_entrega)
        db.commit()
    return db_reporte_entrega

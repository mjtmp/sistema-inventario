from sqlalchemy.orm import Session
from models.models import Historial
from datetime import datetime
from typing import Optional

def registrar_accion(db: Session, usuario_id: int, accion: str, detalles: Optional[str] = None):
    entrada_historial = Historial(usuario_id=usuario_id, accion=accion, detalles=detalles)
    db.add(entrada_historial)
    db.commit()
    db.refresh(entrada_historial)
    return entrada_historial

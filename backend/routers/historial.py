from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.models import Historial
from database import get_db
from schemas.historial import Historial as HistorialSchema

router = APIRouter()

@router.get("/", response_model=dict)
def consultar_historial(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    historial = db.query(Historial).offset(skip).limit(limit).all()
    total = db.query(Historial).count()
    historial_serialized = [HistorialSchema.from_orm(item) for item in historial]
    return {"historial": historial_serialized, "total": total}


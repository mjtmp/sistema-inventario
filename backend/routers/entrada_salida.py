from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crud.entrada_salida import get_entradas_salidas_por_producto
from schemas.entrada_salida import ProductoEntradasSalidasResponse
from database import get_db
from typing import List

router = APIRouter()

@router.get("/entradas_salidas_por_producto", response_model=List[ProductoEntradasSalidasResponse])
def entradas_salidas_por_producto(db: Session = Depends(get_db)):
    return get_entradas_salidas_por_producto(db)

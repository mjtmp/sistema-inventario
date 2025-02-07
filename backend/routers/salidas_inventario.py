from typing import List, Dict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from crud.salidas_inventario import (
    get_salida_inventario, get_salidas_inventario, create_salida_inventario,
    update_salida_inventario, delete_salida_inventario, get_total_salidas_inventario, get_productos_mas_vendidos,
    get_cantidades_vendidas, get_salidas_inventario_por_pedido, get_productos_mas_vendidos_desde_pedidos,
    get_cantidades_vendidas_desde_pedidos
)
from schemas.salidas_inventario import SalidaInventario, SalidaInventarioCreate, SalidaInventarioUpdate, SalidaProductoResponse
from database import get_db, SessionLocal
from models.models import PedidosSalidasInventario

router = APIRouter()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/productos_mas_vendidos_desde_pedidos", response_model=List[Dict])
def productos_mas_vendidos_desde_pedidos(db: Session = Depends(get_db)):
    return get_productos_mas_vendidos_desde_pedidos(db)

@router.get("/cantidades_vendidas_desde_pedidos", response_model=List[Dict])
def cantidades_vendidas_desde_pedidos(db: Session = Depends(get_db)):
    return get_cantidades_vendidas_desde_pedidos(db)

@router.get("/por_pedido", response_model=dict)
def listar_salidas_por_pedido(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    salidas, total = get_salidas_inventario_por_pedido(db=db, skip=skip, limit=limit)
    return {"salidas": [SalidaInventario(**salida.to_dict()) for salida in salidas], "total": total}

@router.get("/total", response_model=dict)
def total_salidas(db: Session = Depends(get_db)):
    total_salidas, total_valor_ventas = get_total_salidas_inventario(db)
    return {"total": total_salidas, "valor_ventas": total_valor_ventas}

@router.get("/productos_mas_vendidos", response_model=List[Dict])
def productos_mas_vendidos(db: Session = Depends(get_db)):
    return get_productos_mas_vendidos(db)

@router.get("/cantidades_vendidas", response_model=List[Dict])
def cantidades_vendidas(db: Session = Depends(get_db)):
    return get_cantidades_vendidas(db)

# Endpoint para crear una nueva salida de inventario
@router.post("/", response_model=SalidaInventario)
def crear_salida_inventario(salida: SalidaInventarioCreate, db: Session = Depends(get_db)):
    return create_salida_inventario(db=db, salida=salida)

# Endpoint para listar salidas de inventario con paginación
@router.get("/", response_model=List[SalidaInventario])
def listar_salidas_inventario(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    salidas = db.query(PedidosSalidasInventario).options(
        joinedload(PedidosSalidasInventario.cliente),
        joinedload(PedidosSalidasInventario.vendedor),
        joinedload(PedidosSalidasInventario.pedido)
    ).offset(skip).limit(limit).all()
    return salidas

# Endpoint para obtener una salida de inventario por ID
@router.get("/{salida_id}", response_model=SalidaInventario)
def obtener_salida_inventario(salida_id: int, db: Session = Depends(get_db)):
    db_salida = get_salida_inventario(db=db, salida_id=salida_id)
    if db_salida is None:
        raise HTTPException(status_code=404, detail="Salida no encontrada")
    return db_salida

# Endpoint para actualizar una salida de inventario
@router.put("/{salida_id}", response_model=SalidaInventario)
def actualizar_salida_inventario(salida_id: int, salida: SalidaInventarioUpdate, db: Session = Depends(get_db)):
    db_salida = update_salida_inventario(db=db, salida_id=salida_id, salida=salida)
    if db_salida is None:
        raise HTTPException(status_code=404, detail="Salida no encontrada")
    return db_salida

# Endpoint para eliminar una salida de inventario
@router.delete("/{salida_id}", response_model=SalidaInventario)
def eliminar_salida_inventario(salida_id: int, db: Session = Depends(get_db)):
    db_salida = delete_salida_inventario(db=db, salida_id=salida_id)
    if db_salida is None:
        raise HTTPException(status_code=404, detail="Salida no encontrada")
    return db_salida




from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, SessionLocal
from schemas.entrada_inventario import EntradaInventario, EntradaInventarioCreate, EntradaInventarioUpdate, EntradaInventarioResponse, EntradaProductoResponse, EntradaPorProductoFechaResponse
from crud.entrada_inventario import (
    create_entrada_inventario,
    get_entrada_inventario,
    get_all_entradas_inventario,
    update_entrada_inventario,
    delete_entrada_inventario,
    get_total_entradas_inventario,
    get_total_entradas_por_producto,
    get_entradas_por_producto_y_fecha,
    get_precio_compra_reciente,
    get_productos_con_precio_compra,
    create_entradas_from_orden_compra
)
from models.models import EntradaInventario  # Asegúrate de importar el modelo de la base de datos
from typing import List

router = APIRouter()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para obtener el total de entradas de inventario y el valor total de compras
@router.get("/total", response_model=dict)
def total_entradas(db: Session = Depends(get_db)):
    total_entradas, total_valor_compras = get_total_entradas_inventario(db)
    return {"total": total_entradas, "valor_compras": total_valor_compras}

@router.get("/total_por_producto", response_model=List[EntradaProductoResponse])
def total_entradas_por_producto(db: Session = Depends(get_db)):
    return get_total_entradas_por_producto(db)

@router.get("/entradas_por_producto", response_model=List[EntradaPorProductoFechaResponse])
def entradas_por_producto_y_fecha(db: Session = Depends(get_db)):
    return get_entradas_por_producto_y_fecha(db)

@router.post("/from-orden-compra/{orden_compra_id}", response_model=dict)
def registrar_entrada_desde_orden_compra(orden_compra_id: int, usuario_id: int, db: Session = Depends(get_db)):
    try:
        return create_entradas_from_orden_compra(db, orden_compra_id, usuario_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/", response_model=EntradaInventarioResponse)
def create_entry(entrada_data: EntradaInventarioCreate, db: Session = Depends(get_db)):
    entrada = create_entrada_inventario(db, entrada_data, usuario_id=entrada_data.usuario_id)
    if not entrada:
        raise HTTPException(status_code=404, detail="Entrada de inventario no encontrada")
    # Asegúrate de incluir los nombres de los productos y proveedores en la respuesta
    return EntradaInventarioResponse(
        entrada_id=entrada.entrada_id,
        producto_id=entrada.producto_id,
        producto_nombre=entrada.producto.nombre,  # Añadir el nombre del producto
        proveedor_id=entrada.proveedor_id,
        proveedor_nombre=entrada.proveedor.nombre,  # Añadir el nombre del proveedor
        cantidad=entrada.cantidad,
        precio_compra=entrada.precio_compra,
        fecha=entrada.fecha
    )


# Endpoint para leer una entrada de inventario específica por su ID
@router.get("/{entrada_id}", response_model=EntradaInventarioResponse)
def read_entry(entrada_id: int, db: Session = Depends(get_db)):
    entrada = get_entrada_inventario(db, entrada_id)
    if not entrada:
        raise HTTPException(status_code=404, detail="Entrada de inventario no encontrada")
    return entrada

# Endpoint para leer todas las entradas de inventario
@router.get("/", response_model=dict)
def read_all_entries(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    entradas = get_all_entradas_inventario(db, skip=skip, limit=limit)
    total = db.query(EntradaInventario).count()  # Obtener el total de entradas
    return {"entradas": entradas, "total": total}

# Endpoint para actualizar una entrada de inventario por ID
@router.put("/{entrada_id}", response_model=EntradaInventarioResponse)
def update_entry(entrada_id: int, entrada_data: EntradaInventarioUpdate, db: Session = Depends(get_db)):
    entrada = update_entrada_inventario(db, entrada_id, entrada_data, usuario_id=entrada_data.usuario_id)
    if not entrada:
        raise HTTPException(status_code=404, detail="Entrada de inventario no encontrada")
    return entrada

# Endpoint para eliminar una entrada de inventario por ID
@router.delete("/{entrada_id}", response_model=dict)
def delete_entry(entrada_id: int, usuario_id: int, db: Session = Depends(get_db)):
    entrada = delete_entrada_inventario(db, entrada_id, usuario_id)
    if not entrada:
        raise HTTPException(status_code=404, detail="Entrada de inventario no encontrada")
    return {"detail": "Entrada de inventario eliminada exitosamente"}

# Endpoint para obtener el precio de compra más reciente de un producto
@router.get("/precio_compra_reciente/{producto_id}", response_model=float)
def obtener_precio_compra_reciente(producto_id: int, db: Session = Depends(get_db)):
    return get_precio_compra_reciente(db, producto_id)

# Endpoint para obtener productos que tienen un precio de compra
@router.get("/productos_con_precio_compra", response_model=List[EntradaInventarioResponse])
def productos_con_precio_compra(db: Session = Depends(get_db)):
    productos = get_productos_con_precio_compra(db)
    return productos




<<<<<<< HEAD
# Importar las dependencias necesarias
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud.detalles_pedidos import (
    get_detalle_pedido, get_detalles_pedidos, create_detalle_pedido, 
    update_detalle_pedido, delete_detalle_pedido
)
from schemas.detalles_pedidos import DetallePedido, DetallePedidoCreate, DetallePedidoUpdate
from database import SessionLocal

# Crear el router de FastAPI para manejar las solicitudes de detalles de pedidos
router = APIRouter()

=======
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..crud.detalles_pedidos import (
    get_detalle_pedido, get_detalles_pedidos, create_detalle_pedido, 
    update_detalle_pedido, delete_detalle_pedido
)
from ..schemas.detalles_pedidos import DetallePedido, DetallePedidoCreate, DetallePedidoUpdate
from backend.database import SessionLocal

router = APIRouter()
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39
# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
<<<<<<< HEAD
        yield db  # Devolver la sesión de base de datos
    finally:
        db.close()  # Cerrar la sesión cuando termine

# Ruta para crear un nuevo detalle de pedido
=======
        yield db
    finally:
        db.close()

>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39
@router.post("/", response_model=DetallePedido)
def crear_detalle_pedido(detalle_pedido: DetallePedidoCreate, db: Session = Depends(get_db)):
    return create_detalle_pedido(db=db, detalle_pedido=detalle_pedido)

<<<<<<< HEAD
# Ruta para obtener una lista de detalles de pedidos con paginación
=======
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39
@router.get("/", response_model=list[DetallePedido])
def listar_detalles_pedidos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_detalles_pedidos(db=db, skip=skip, limit=limit)

<<<<<<< HEAD
# Ruta para obtener un detalle de pedido por su ID
=======
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39
@router.get("/{detalle_id}", response_model=DetallePedido)
def obtener_detalle_pedido(detalle_id: int, db: Session = Depends(get_db)):
    db_detalle_pedido = get_detalle_pedido(db=db, detalle_id=detalle_id)
    if db_detalle_pedido is None:
        raise HTTPException(status_code=404, detail="Detalle de pedido no encontrado")
    return db_detalle_pedido

<<<<<<< HEAD
# Ruta para actualizar un detalle de pedido
=======
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39
@router.put("/{detalle_id}", response_model=DetallePedido)
def actualizar_detalle_pedido(detalle_id: int, detalle_pedido: DetallePedidoUpdate, db: Session = Depends(get_db)):
    db_detalle_pedido = update_detalle_pedido(db=db, detalle_id=detalle_id, detalle_pedido=detalle_pedido)
    if db_detalle_pedido is None:
        raise HTTPException(status_code=404, detail="Detalle de pedido no encontrado")
    return db_detalle_pedido

<<<<<<< HEAD
# Ruta para eliminar un detalle de pedido
=======
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39
@router.delete("/{detalle_id}", response_model=DetallePedido)
def eliminar_detalle_pedido(detalle_id: int, db: Session = Depends(get_db)):
    db_detalle_pedido = delete_detalle_pedido(db=db, detalle_id=detalle_id)
    if db_detalle_pedido is None:
        raise HTTPException(status_code=404, detail="Detalle de pedido no encontrado")
    return db_detalle_pedido
<<<<<<< HEAD

=======
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39

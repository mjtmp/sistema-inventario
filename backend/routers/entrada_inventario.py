from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db  # Importa la función para obtener la sesión de la base de datos
from schemas.entrada_inventario import EntradaInventario, EntradaInventarioCreate, EntradaInventarioUpdate, EntradaInventarioResponse
from crud.entrada_inventario import (
    create_entrada_inventario,
    get_entrada_inventario,
    get_all_entradas_inventario,
    update_entrada_inventario,
    delete_entrada_inventario
)

router = APIRouter()

# Endpoint para crear una nueva entrada de inventario
@router.post("/", response_model=EntradaInventario)
def create_entry(entrada_data: EntradaInventarioCreate, db: Session = Depends(get_db)):
    return create_entrada_inventario(db, entrada_data)

# Endpoint para leer una entrada de inventario específica por su ID
@router.get("/{entrada_id}", response_model=EntradaInventarioResponse)  # Responde con los detalles, no solo el objeto
def read_entry(entrada_id: int, db: Session = Depends(get_db)):
    entrada = get_entrada_inventario(db, entrada_id)
    if not entrada:
        raise HTTPException(status_code=404, detail="Entrada de inventario no encontrada")  # Manejo de error si no se encuentra la entrada
    return entrada  # Devuelve la entrada con los detalles (producto y proveedor)

# Endpoint para leer todas las entradas de inventario
@router.get("/", response_model=list[EntradaInventarioResponse])  # Responde con una lista de entradas detalladas
def read_all_entries(db: Session = Depends(get_db)):
    entradas = get_all_entradas_inventario(db)
    return entradas  # Devuelve todas las entradas formateadas

# Endpoint para actualizar una entrada de inventario por ID
@router.put("/{entrada_id}", response_model=EntradaInventario)
def update_entry(entrada_id: int, entrada_data: EntradaInventarioUpdate, db: Session = Depends(get_db)):
    entrada = update_entrada_inventario(db, entrada_id, entrada_data)
    if not entrada:
        raise HTTPException(status_code=404, detail="Entrada de inventario no encontrada")
    return entrada  # Devuelve la entrada actualizada

# Endpoint para eliminar una entrada de inventario por ID
@router.delete("/{entrada_id}")
def delete_entry(entrada_id: int, db: Session = Depends(get_db)):
    entrada = delete_entrada_inventario(db, entrada_id)
    if not entrada:
        raise HTTPException(status_code=404, detail="Entrada de inventario no encontrada")
    return {"detail": "Entrada de inventario eliminada exitosamente"}  # Mensaje de éxito


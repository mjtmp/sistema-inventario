from sqlalchemy.orm import Session, joinedload
from models.models import EntradaInventario
from schemas.entrada_inventario import EntradaInventarioCreate, EntradaInventarioUpdate, EntradaInventarioResponse

# Crea una nueva entrada de inventario en la base de datos
def create_entrada_inventario(db: Session, entrada_data: EntradaInventarioCreate):
    entrada = EntradaInventario(**entrada_data.dict())  # Se crea una instancia de EntradaInventario a partir de los datos recibidos
    db.add(entrada)  # Se añade la entrada a la sesión
    db.commit()  # Se confirma la transacción en la base de datos
    db.refresh(entrada)  # Se refresca el objeto para obtener los datos actualizados (como el ID generado)
    return entrada  # Retorna la entrada creada

# Obtiene una entrada de inventario específica por su ID
def get_entrada_inventario(db: Session, entrada_id: int):
    return db.query(EntradaInventario).filter(EntradaInventario.entrada_id == entrada_id).first()  # Consulta por ID

# Obtiene todas las entradas de inventario, incluyendo detalles del producto y proveedor relacionados
def get_all_entradas_inventario(db: Session):
    entradas = db.query(EntradaInventario).options(
        joinedload(EntradaInventario.producto),  # Realiza un JOIN con la tabla de Producto
        joinedload(EntradaInventario.proveedor)  # Realiza un JOIN con la tabla de Proveedor
    ).all()  # Obtiene todas las entradas

    result = []  # Lista para almacenar las respuestas formateadas
    for entrada in entradas:
        result.append(EntradaInventarioResponse(  # Formatea los datos en la respuesta
            entrada_id=entrada.entrada_id,
            producto_id=entrada.producto_id,
            producto_nombre=entrada.producto.nombre,  # Nombre del producto (de la relación JOIN)
            proveedor_id=entrada.proveedor_id,
            proveedor_nombre=entrada.proveedor.nombre,  # Nombre del proveedor (de la relación JOIN)
            cantidad=entrada.cantidad,
            precio_compra=entrada.precio_compra,
            fecha=entrada.fecha
        ))
    return result  # Devuelve la lista de respuestas formateadas

# Actualiza una entrada de inventario existente
def update_entrada_inventario(db: Session, entrada_id: int, entrada_data: EntradaInventarioUpdate):
    entrada = db.query(EntradaInventario).filter(EntradaInventario.entrada_id == entrada_id).first()  # Busca la entrada por ID
    if entrada:
        for key, value in entrada_data.dict(exclude_unset=True).items():  # Excluye los campos no establecidos
            setattr(entrada, key, value)  # Asigna los nuevos valores a la entrada
        db.commit()  # Confirma los cambios
        db.refresh(entrada)  # Refresca el objeto para obtener los datos actualizados
    return entrada  # Retorna la entrada actualizada

# Elimina una entrada de inventario
def delete_entrada_inventario(db: Session, entrada_id: int):
    entrada = db.query(EntradaInventario).filter(EntradaInventario.entrada_id == entrada_id).first()  # Busca la entrada por ID
    if entrada:
        db.delete(entrada)  # Elimina la entrada de la base de datos
        db.commit()  # Confirma la eliminación
    return entrada  # Retorna la entrada eliminada (si fue encontrada y eliminada)




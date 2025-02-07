from sqlalchemy.orm import Session, joinedload
import datetime
from sqlalchemy import text, func
from models.models import EntradaInventario, Producto, OrdenCompra
from schemas.entrada_inventario import EntradaInventarioCreate, EntradaInventarioUpdate, EntradaInventarioResponse
from crud.historial import registrar_accion  # Importar la función para registrar acciones

# Crea una nueva entrada de inventario en la base de datos
def create_entrada_inventario(db: Session, entrada_data: EntradaInventarioCreate, usuario_id: int):
    entrada_data_dict = entrada_data.dict()
    entrada_data_dict.pop('usuario_id', None)
    entrada = EntradaInventario(**entrada_data_dict)
    db.add(entrada)
    db.commit()
    db.refresh(entrada)
    registrar_accion(db, usuario_id, "Registro de entrada de inventario", f"Entrada de {entrada.cantidad} unidades de {entrada.producto.nombre} registrada.")
    return entrada

def create_entradas_from_orden_compra(db: Session, orden_compra_id: int, usuario_id: int):
    orden_compra = db.query(OrdenCompra).filter(OrdenCompra.orden_compra_id == orden_compra_id, OrdenCompra.estado == 'completado').first()
    if not orden_compra:
        raise ValueError("Orden de compra no encontrada o no está completada")

    for detalle in orden_compra.detalles:
        entrada_data = EntradaInventarioCreate(
            producto_id = detalle.producto_id,
            cantidad = detalle.cantidad,
            precio_compra = detalle.precio_unitario,
            fecha = datetime.date.today(),
            proveedor_id = orden_compra.proveedor_id
        )
        create_entrada_inventario(db, entrada_data, usuario_id)

    return {"message": "Entradas de inventario creadas a partir de la orden de compra completada"}

# Obtiene una entrada de inventario específica por su ID
def get_entrada_inventario(db: Session, entrada_id: int):
    return db.query(EntradaInventario).filter(EntradaInventario.entrada_id == entrada_id).first()

def get_total_entradas_por_producto(db: Session):
    query = db.query(
        Producto.nombre.label("producto"),
        func.sum(EntradaInventario.cantidad).label("total_entradas"),
        func.sum(EntradaInventario.cantidad * EntradaInventario.precio_compra).label("valor_entradas")
    ).join(Producto, EntradaInventario.producto_id == Producto.producto_id)\
     .group_by(Producto.nombre).all()

    return [{"producto": row.producto, "total_entradas": row.total_entradas, "valor_entradas": row.valor_entradas} for row in query]

def get_entradas_por_producto_y_fecha(db: Session):
    query = db.query(
        Producto.nombre.label("producto"),
        EntradaInventario.fecha.label("fecha"),
        func.sum(EntradaInventario.cantidad).label("cantidad")
    ).join(Producto, EntradaInventario.producto_id == Producto.producto_id)\
     .group_by(Producto.nombre, EntradaInventario.fecha)\
     .order_by(EntradaInventario.fecha).all()

    return [{"producto": row.producto, "fecha": row.fecha, "cantidad": row.cantidad} for row in query]

# Obtiene todas las entradas de inventario, incluyendo detalles del producto y proveedor relacionados
'''def get_all_entradas_inventario(db: Session):
    query = """
    SELECT 
        EntradasInventario.entrada_id, 
        EntradasInventario.producto_id, 
        Productos.nombre AS producto_nombre, 
        Productos.proveedor_id, 
        Proveedores.nombre AS proveedor_nombre, 
        EntradasInventario.cantidad, 
        EntradasInventario.precio_compra, 
        EntradasInventario.fecha
    FROM 
        EntradasInventario 
    INNER JOIN 
        Productos 
    ON 
        EntradasInventario.producto_id = Productos.producto_id 
    INNER JOIN 
        Proveedores 
    ON 
        Productos.proveedor_id = Proveedores.proveedor_id;
    """

    result = db.execute(text(query))
    entries = [dict(row) for row in result.mappings()]
    return entries'''
    
def get_all_entradas_inventario(db: Session, skip: int = 0, limit: int = 10):
    query = """
    SELECT 
        EntradasInventario.entrada_id, 
        EntradasInventario.producto_id, 
        Productos.nombre AS producto_nombre, 
        Productos.proveedor_id, 
        Proveedores.nombre AS proveedor_nombre, 
        EntradasInventario.cantidad, 
        EntradasInventario.precio_compra, 
        EntradasInventario.fecha
    FROM 
        EntradasInventario 
    INNER JOIN 
        Productos 
    ON 
        EntradasInventario.producto_id = Productos.producto_id 
    INNER JOIN 
        Proveedores 
    ON 
        Productos.proveedor_id = Proveedores.proveedor_id
    LIMIT :limit OFFSET :skip;
    """
    result = db.execute(text(query), {"limit": limit, "skip": skip})
    entries = [dict(row) for row in result.mappings()]
    return entries



# Obtiene el total de entradas de inventario y el valor total de compras
def get_total_entradas_inventario(db: Session):
    total_entradas = db.query(func.sum(EntradaInventario.cantidad)).scalar()
    total_valor_compras = db.query(func.sum(EntradaInventario.cantidad * EntradaInventario.precio_compra)).scalar()
    if total_entradas is None:
        total_entradas = 0
    if total_valor_compras is None:
        total_valor_compras = 0.0
    return total_entradas, total_valor_compras

# Obtiene productos que tienen un precio de compra
def get_productos_con_precio_compra(db: Session):
    query = db.query(
        Producto.producto_id,
        Producto.nombre,
        Producto.codigo,
        Producto.stock,
        Producto.cantidad_minima,
        Producto.cantidad_maxima,
        Producto.ubicacion,
        Producto.precio,
        EntradaInventario.precio_compra
    ).join(EntradaInventario, EntradaInventario.producto_id == Producto.producto_id).all()

    return query

def get_precio_compra_reciente(db: Session, producto_id: int):
    entrada = db.query(EntradaInventario).filter(EntradaInventario.producto_id == producto_id).order_by(EntradaInventario.fecha.desc()).first()
    return entrada.precio_compra if entrada else 0.0

# Actualiza una entrada de inventario existente
def update_entrada_inventario(db: Session, entrada_id: int, entrada_data: EntradaInventarioUpdate, usuario_id: int):
    entrada = db.query(EntradaInventario).filter(EntradaInventario.entrada_id == entrada_id).first()
    if entrada:
        for key, value in entrada_data.dict(exclude_unset=True).items():
            setattr(entrada, key, value)
        db.commit()
        db.refresh(entrada)
        registrar_accion(db, usuario_id, "Actualización de entrada de inventario", f"Entrada de {entrada.cantidad} unidades de {entrada.producto.nombre} actualizada.")
    return entrada

# Elimina una entrada de inventario
def delete_entrada_inventario(db: Session, entrada_id: int, usuario_id: int):
    entrada = db.query(EntradaInventario).filter(EntradaInventario.entrada_id == entrada_id).first()
    if entrada:
        db.delete(entrada)
        db.commit()
        registrar_accion(db, usuario_id, "Eliminación de entrada de inventario", f"Entrada de {entrada.cantidad} unidades de {entrada.producto.nombre} eliminada.")
    return entrada




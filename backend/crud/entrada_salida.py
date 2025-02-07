from sqlalchemy.orm import Session
from sqlalchemy import func
from models.models import EntradaInventario, SalidasInventario, Producto

def get_entradas_salidas_por_producto(db: Session):
    entradas_query = db.query(
        Producto.nombre.label("producto"),
        func.sum(EntradaInventario.cantidad).label("total_entradas"),
        func.sum(EntradaInventario.cantidad * EntradaInventario.precio_compra).label("valor_entradas")
    ).join(Producto, EntradaInventario.producto_id == Producto.producto_id)\
     .group_by(Producto.nombre).all()

    salidas_query = db.query(
        Producto.nombre.label("producto"),
        func.sum(SalidasInventario.cantidad).label("total_salidas"),
        func.sum(SalidasInventario.cantidad * SalidasInventario.precio_venta).label("valor_salidas")
    ).join(Producto, SalidasInventario.producto_id == Producto.producto_id)\
     .group_by(Producto.nombre).all()

    entradas_dict = {entry.producto: entry._asdict() for entry in entradas_query}
    salidas_dict = {entry.producto: entry._asdict() for entry in salidas_query}

    combined = []
    all_productos = set(entradas_dict.keys()).union(set(salidas_dict.keys()))

    for producto in all_productos:
        total_entradas = entradas_dict.get(producto, {}).get("total_entradas", 0)
        valor_entradas = entradas_dict.get(producto, {}).get("valor_entradas", 0.0)
        total_salidas = salidas_dict.get(producto, {}).get("total_salidas", 0)
        valor_salidas = salidas_dict.get(producto, {}).get("valor_salidas", 0.0)

        combined.append({
            "producto": producto,
            "total_entradas": total_entradas,
            "valor_entradas": valor_entradas,
            "total_salidas": total_salidas,
            "valor_salidas": valor_salidas
        })

    return combined


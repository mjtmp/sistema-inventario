from pydantic import BaseModel
from typing import List

# Esquema para la actualización de facturas
class FacturaUpdate(BaseModel):
    cliente_id: int
    usuario_id: int
    fecha_emision: str
    productos: List['FacturaProductoCreate']

# Esquema para la creación de facturas
class FacturaCreate(BaseModel):
    cliente_id: int
    usuario_id: int
    pedido_id: int
    productos: List['FacturaProductoCreate']

# Esquema para la respuesta de una factura
class FacturaResponse(BaseModel):
    factura_id: int
    cliente_id: int
    usuario_id: int
    numero_factura: str
    total: float
    productos: List['FacturaProductoResponse']

# Esquema para la creación de abonos
class AbonoCreate(BaseModel):
    fecha: str
    monto: float
    metodo_pago: str

# Esquema para los productos de una factura
class FacturaProductoCreate(BaseModel):
    producto_id: int
    cantidad: int
    precio_unitario: float

# Esquema para la respuesta de los productos de una factura
class FacturaProductoResponse(BaseModel):
    producto_id: int
    cantidad: int
    precio_unitario: float
    descripcion: str
    tiene_iva: bool
    monto_total: float

    class Config:
        from_attributes = True


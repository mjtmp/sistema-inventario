from pydantic import BaseModel  # Modelo base de Pydantic
from datetime import date  # Manejo de fechas
from typing import Optional  # Tipos opcionales

# Esquema para los datos de un cliente
class Cliente(BaseModel):
    cliente_id: int
    nombre: str

# Esquema para los datos de un usuario/vendedor
class Usuario(BaseModel):
    usuario_id: int
    nombre: str

# Esquema para los datos de una factura
class Factura(BaseModel):
    factura_id: int
    numero_factura: str
    monto_total: float
    pagado: float
    debido: float

# Base para las salidas de inventario
class SalidaInventarioBase(BaseModel):
    producto_id: int
    cliente_id: int
    factura_id: int
    cantidad: int
    precio_venta: float
    vendedor_id: int

# Esquema para crear una salida de inventario
class SalidaInventarioCreate(SalidaInventarioBase):
    pass

# Esquema para actualizar una salida de inventario
class SalidaInventarioUpdate(SalidaInventarioBase):
    pass

# Esquema para representar una salida de inventario con datos adicionales
class SalidaInventario(SalidaInventarioBase):
    salida_id: int
    fecha: date
    cliente: Optional[Cliente] = None  # Relación con cliente
    vendedor: Optional[Usuario] = None  # Relación con vendedor
    factura: Optional[Factura] = None  # Relación con factura

    class Config:
        from_attributes = True  # Permite que los atributos del modelo de SQLAlchemy se utilicen directamente

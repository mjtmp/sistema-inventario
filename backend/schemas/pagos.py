from pydantic import BaseModel  # Base para definir esquemas Pydantic
from datetime import date  # Tipo de datos para manejar fechas
from typing import Optional  # Para campos opcionales

# Clase base con los atributos comunes a todas las operaciones de pago
class PagoBase(BaseModel):
    pedido_id: int  # ID del pedido asociado al pago
    monto: float  # Monto del pago
    metodo_pago: Optional[str] = None  # Método de pago (opcional)

# Esquema para la creación de pagos (mismos campos que `PagoBase`)
class PagoCreate(PagoBase):
    pass

# Esquema para la actualización de pagos (mismos campos que `PagoBase`)
class PagoUpdate(PagoBase):
    pass

# Esquema para la respuesta de un pago, incluyendo el ID y la fecha
class Pago(PagoBase):
    pago_id: int  # ID único del pago
    fecha: date  # Fecha en que se realizó el pago

    class Config:
        from_attributes = True  # Permite convertir atributos del modelo SQLAlchemy a Pydantic

<<<<<<< HEAD
# Importar las dependencias necesarias
from pydantic import BaseModel
from typing import Optional

# Esquema base para los detalles de los pedidos
class DetallePedidoBase(BaseModel):
    pedido_id: int  # ID del pedido
    producto_id: int  # ID del producto asociado
    cantidad: int  # Cantidad del producto en el detalle
    precio_unitario: float  # Precio unitario del producto

# Esquema para crear un nuevo detalle de pedido (hereda de DetallePedidoBase)
class DetallePedidoCreate(DetallePedidoBase):
    pass

# Esquema para actualizar un detalle de pedido
class DetallePedidoUpdate(BaseModel):
    cantidad: Optional[int]  # Cantidad opcional
    precio_unitario: Optional[float]  # Precio unitario opcional

# Esquema final que incluye el ID del detalle de pedido
class DetallePedido(DetallePedidoBase):
    detalle_id: int  # ID del detalle de pedido

    class Config:
        from_attributes = True  # Permite la conversión de atributos del modelo a pydantic

=======
from pydantic import BaseModel
from typing import Optional

class DetallePedidoBase(BaseModel):
    pedido_id: int
    producto_id: int
    cantidad: int
    precio_unitario: float

class DetallePedidoCreate(DetallePedidoBase):
    pass

class DetallePedidoUpdate(BaseModel):
    cantidad: Optional[int]
    precio_unitario: Optional[float]

class DetallePedido(DetallePedidoBase):
    detalle_id: int

    class Config:
        from_attributes = True
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39

from pydantic import BaseModel  # Base para esquemas en FastAPI
from datetime import date  # Para manejar fechas
from typing import List, Optional  # Tipos opcionales y listas
from .detalles_pedidos import DetallePedido  # Relación con detalles del pedido

# Esquema base que contiene los campos comunes
class PedidoBase(BaseModel):
    cliente_id: int  # Relación con el cliente
    fecha_pedido: date  # Fecha del pedido

# Esquema para la creación de un pedido
class PedidoCreate(PedidoBase):
    pass  # Hereda los campos del esquema base

# Esquema para la actualización de un pedido
class PedidoUpdate(PedidoBase):
    pass  # Hereda los campos del esquema base

# Esquema para representar un pedido completo
class Pedido(PedidoBase):
    pedido_id: int  # Identificador único del pedido
    detalles: List[DetallePedido] = []  # Lista de detalles relacionados

    # Configuración adicional para usar atributos del modelo ORM
    class Config:
        from_attributes = True

from pydantic import BaseModel  # Importamos la clase BaseModel de Pydantic.
from typing import Optional  # Importamos Optional para indicar campos opcionales.

# Esquema base para el cliente.
class ClienteBase(BaseModel):
    nombre: str  # El nombre del cliente es obligatorio.
    email: Optional[str] = None  # El email es opcional.
    telefono: Optional[str] = None  # El teléfono es opcional.
    direccion: Optional[str] = None  # La dirección es opcional.

# Esquema para crear un nuevo cliente (hereda de ClienteBase).
class ClienteCreate(ClienteBase):
    pass  # No tiene atributos adicionales, solo hereda los del esquema base.

# Esquema para actualizar un cliente (hereda de ClienteBase).
class ClienteUpdate(ClienteBase):
    pass  # No tiene atributos adicionales, solo hereda los del esquema base.

# Esquema que se usa para representar al cliente con su ID.
class Cliente(ClienteBase):
    cliente_id: int  # El ID del cliente es obligatorio.

    # Configuración adicional para el modelo.
    class Config:
        from_attributes = True  # Permite la creación del cliente a partir de los atributos del modelo.


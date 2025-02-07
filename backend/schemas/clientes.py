from pydantic import BaseModel
from typing import Optional

class ClienteBase(BaseModel):
    nombre: str
    email: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    tipo_documento: Optional[str] = None  # Nuevo campo para tipo de documento
    numero_documento: Optional[str] = None  # Nuevo campo para número de documento

class ClienteCreate(ClienteBase):
    usuario_id: int  # Asegurar que usuario_id está incluido

class ClienteUpdate(ClienteBase):
    usuario_id: int

class Cliente(ClienteBase):
    cliente_id: int

    class Config:
        from_attributes = True


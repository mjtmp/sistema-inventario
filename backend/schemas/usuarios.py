from pydantic import BaseModel
from typing import Optional

class UsuarioBase(BaseModel):
    nombre: str
    email: str
    rol_id: int

class UsuarioCreate(UsuarioBase):
    contraseña: str

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    contraseña: Optional[str] = None
    rol_id: Optional[int] = None

class Usuario(UsuarioBase):
    usuario_id: int

    class Config:
        from_attributes = True

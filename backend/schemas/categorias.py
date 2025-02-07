from pydantic import BaseModel
from typing import Optional

class CategoriaBase(BaseModel):
    nombre: str

class CategoriaCreate(CategoriaBase):
    pass  # Asegurar que usuario_id está incluido

class CategoriaUpdate(CategoriaBase):
    usuario_id: int  # Incluir usuario_id

class Categoria(CategoriaBase):
    categoria_id: int

class CategoriaProductoResponse(BaseModel):
    nombre: str
    total_productos: int

    class Config:
        from_attributes = True


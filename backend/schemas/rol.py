from pydantic import BaseModel
from typing import Optional

# Clase base con atributos comunes a todas las operaciones.
class RolBase(BaseModel):
    nombre: str

# Esquema para la creación de roles.
class RolCreate(RolBase):
    pass  # Utiliza los atributos de RolBase sin cambios.

# Esquema para la actualización de roles. Los campos son opcionales.
class RolUpdate(BaseModel):
    nombre: Optional[str] = None

# Esquema para la representación completa de un rol.
class Rol(RolBase):
    rol_id: int  # ID del rol.

    class Config:
        # Configuración para mapear directamente desde los atributos del modelo SQLAlchemy.
        from_attributes = True


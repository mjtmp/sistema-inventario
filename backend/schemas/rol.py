from pydantic import BaseModel
from typing import Optional

<<<<<<< HEAD
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

=======
class RolBase(BaseModel):
    nombre: str

class RolCreate(RolBase):
    pass

class RolUpdate(BaseModel):
    nombre: Optional[str] = None

class Rol(RolBase):
    rol_id: int

    class Config:
        from_attributes = True
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39

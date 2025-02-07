from pydantic import BaseModel  # Importa BaseModel para la validación de los esquemas
from typing import Optional  # Importa Optional para valores opcionales en los esquemas
from datetime import datetime  # Importa datetime para manejar fechas y horas

# Esquema base para el usuario
class UsuarioBase(BaseModel):
    nombre: str  # Nombre del usuario
    email: str  # Email del usuario
    contraseña: str  # Contraseña del usuario
    rol_id: int  # ID del rol del usuario
    
class Rol(BaseModel):
    nombre: str  # Nombre del rol del usuario

# Esquema para la creación de un nuevo usuario
class UsuarioCreate(UsuarioBase):
    pass  # No se requiere ninguna modificación, hereda de UsuarioBase

# Esquema para la actualización de un usuario existente
class UsuarioUpdate(UsuarioBase):
    nombre: Optional[str] = None  # Nombre opcional para la actualización
    email: Optional[str] = None  # Email opcional para la actualización
    contraseña: Optional[str] = None  # Contraseña opcional para la actualización

# Esquema para representar al usuario en la base de datos (con id )
class Usuario(UsuarioBase):
    usuario_id: int  # ID del usuario
    rol: Optional[Rol]  # Rol asociado al usuario (relación opcional)
    
    class Config:
        from_attributes = True  # Asegura que SQLAlchemy pueda convertir el modelo en un diccionario



'''from pydantic import BaseModel
from typing import Optional

class UsuarioBase(BaseModel):
    nombre: str
    email: str
    rol_id: int
    contraseña: str
    
class Rol(BaseModel):
    nombre: str

class UsuarioCreate(UsuarioBase):
    contraseña: str

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    contraseña: Optional[str] = None
    rol_id: Optional[int] = None

class Usuario(UsuarioBase):
    usuario_id: int
    rol: Optional[Rol]  # Incluye el esquema del rol como relación

    class Config:
        from_attributes = True'''

from pydantic import BaseModel  # Base para definir esquemas de datos con validación.

# Clase base que define los atributos comunes de un permiso.
class PermisoBase(BaseModel):
    nombre: str  # Nombre del permiso.

# Esquema para la creación de permisos. Hereda de PermisoBase.
class PermisoCreate(PermisoBase):
    pass  # No agrega atributos adicionales.

# Esquema que incluye el ID del permiso y se utiliza para respuestas.
class Permiso(PermisoBase):
    permiso_id: int  # ID único del permiso.

    # Configuración para que los atributos se mapeen correctamente desde el modelo.
    class Config:
        from_attributes = True


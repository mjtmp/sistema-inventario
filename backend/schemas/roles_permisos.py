from pydantic import BaseModel  # Esquema base para validación y serialización.

# Esquema base que contiene los atributos compartidos entre creación y respuesta.
class RolesPermisosBase(BaseModel):
    rol_id: int  # ID del rol.
    permiso_id: int  # ID del permiso.

# Esquema para la creación de una relación rol-permiso.
class RolesPermisosCreate(RolesPermisosBase):
    pass  # Hereda directamente de RolesPermisosBase.

# Esquema de respuesta para roles-permisos (lo que la API devolverá).
class RolesPermisos(RolesPermisosBase):
    pass  # Igual al esquema base, pero se podrían agregar más configuraciones si fuera necesario.

    # Configuración para que los modelos de la base de datos se conviertan automáticamente en este esquema.
    class Config:
        from_attributes = True


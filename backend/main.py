from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import engine, SessionLocal
from backend.models import Base
from backend.routers import productos, proveedores, clientes, pedidos, detalles_pedidos, reportes_entrega, reportes_inventario, rol, usuarios
from fastapi.middleware.cors import CORSMiddleware
from backend.crud.usuarios import get_usuario_by_email, verify_password  # Importa las funciones para autenticación
from pydantic import BaseModel

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Cambia esto si el frontend está en otro puerto o dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluye los routers con prefijos para evitar conflictos de ruta
app.include_router(productos.router, prefix="/productos")
app.include_router(proveedores.router, prefix="/proveedores")
app.include_router(clientes.router, prefix="/clientes")
app.include_router(pedidos.router, prefix="/pedidos")
app.include_router(detalles_pedidos.router, prefix="/detalles_pedidos")
app.include_router(reportes_entrega.router, prefix="/reportes_entrega")
app.include_router(reportes_inventario.router, prefix="/reportes_inventario")
app.include_router(rol.router, prefix="/roles")
app.include_router(usuarios.router, prefix="/usuarios")

# Pydantic schema para recibir los datos de login
class LoginData(BaseModel):
    email: str
    contrasena: str  # Cambia a 'contrasena' si es necesario

# Ruta de login
@app.post("/login")
async def login(data: LoginData, db: Session = Depends(SessionLocal)):
    # Busca al usuario por email
    usuario = get_usuario_by_email(db, data.email)
    # Verifica si el usuario existe y la contraseña es correcta
    if not usuario or not verify_password(data.contrasena, usuario.contraseña):  # Asegúrate de que la columna coincida
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    # Si las credenciales son válidas, responde con un mensaje de éxito
    return {"message": "Inicio de sesión exitoso"}

@app.get("/")
def read_root():
    return {"message": "Bienvenido al sistema de gestión de inventario"}

@app.get("/example")
async def read_example():
    return {"message": "This is an example"}

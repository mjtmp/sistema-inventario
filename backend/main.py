from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal, get_db
from models.models import Base
from routers import productos, proveedores, clientes, pedidos, detalles_pedidos, reportes_entrega, reportes_inventario, rol, usuarios, entrada_inventario, salidas_inventario, roles_permisos, permisos, pagos, facturas
from fastapi.middleware.cors import CORSMiddleware
from crud.usuarios import get_usuario_by_email, verify_password  # Importa las funciones para autenticación
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer


# Configuración de la clave secreta y algoritmo
SECRET_KEY = "your_secret_key_here"  # Cambia esto a una clave secreta segura
ALGORITHM = "HS256"

# OAuth2PasswordBearer es necesario para el flujo de autenticación con JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

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
app.include_router(entrada_inventario.router, prefix="/entradas_inventario")
app.include_router(salidas_inventario.router, prefix="/salidas_inventario")
app.include_router(roles_permisos.router, prefix="/roles_permisos")
app.include_router(permisos.router, prefix="/permisos")
app.include_router(pagos.router, prefix="/pagos")  # Se añade la ruta para pagos
app.include_router(facturas.router, prefix="/facturas")  # Incluye el router de factura


# Pydantic schema para recibir los datos de login
class LoginData(BaseModel):
    email: str
    contraseña: str  # Cambia a 'contrasena' si es necesario

# Función para crear el JWT
def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Ruta de login
@app.post("/login")
async def login(data: LoginData, db: Session = Depends(get_db)):
    # Busca al usuario por email
    usuario = get_usuario_by_email(db, data.email)
    # Verifica si el usuario existe y la contraseña es correcta
    if not usuario or not verify_password(data.contraseña, usuario.contraseña):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    # Crear el token con la información del usuario (rol es parte de la carga útil del token)
    access_token = create_access_token(data={"sub": usuario.email, "rol": usuario.rol.nombre})

    # Devuelve el token y el rol del usuario
    return {"message": "Inicio de sesión exitoso", "token": access_token, "rol": usuario.rol.nombre}


@app.get("/")
def read_root():
    return {"message": "Bienvenido al sistema de gestión de inventario"}

@app.get("/example")
async def read_example():
    return {"message": "This is an example"}



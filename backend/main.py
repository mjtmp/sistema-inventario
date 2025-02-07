from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import engine, SessionLocal, get_db
from models.models import Base
from routers import productos, proveedores, clientes, pedidos, detalles_pedidos, reportes_entrega, reportes_inventario, rol, usuarios, entrada_inventario, salidas_inventario, roles_permisos, permisos, pagos, facturas, categorias, dollar, entrada_salida, ordenes_compra, historial, backup, manuals
from fastapi.middleware.cors import CORSMiddleware
from crud.usuarios import get_usuario_by_email, verify_password  # Importa las funciones para autenticación
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse 
from utils.generar_reporte_inventario import generar_reporte_inventario
import schedule  # Importar el archivo del scheduler

# Configuración de la clave secreta y algoritmo
SECRET_KEY = "your_secret_key_here"  # Cambia esto a una clave secreta segura
ALGORITHM = "HS256"

# OAuth2PasswordBearer es necesario para el flujo de autenticación con JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI()
app.mount("/media", StaticFiles(directory="media"), name="media")

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
app.include_router(categorias.router, prefix="/categorias")
app.include_router(dollar.router, prefix="/dollar")
app.include_router(entrada_salida.router, prefix="/entrada_salida")
app.include_router(ordenes_compra.router, prefix="/ordenes_compra")
app.include_router(historial.router, prefix="/historial")
app.include_router(backup.router, prefix="/backup")
app.include_router(manuals.router, prefix="/manuals")

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
    access_token = create_access_token(data={"sub": usuario.email, "rol": usuario.rol.nombre, "usuario_id": usuario.usuario_id})

    # Devuelve el token y el rol del usuario
    return {"message": "Inicio de sesión exitoso", "token": access_token, "rol": usuario.rol.nombre, "usuario_id": usuario.usuario_id, "usuarioName": usuario.nombre}


@app.get("/")
def read_root():
    return {"message": "Bienvenido al sistema de gestión de inventario"}

@app.get("/example")
async def read_example():
    return {"message": "This is an example"}

@app.get("/generar-reporte-inventario")
def generar_reporte(fecha_inicio: str = Query(None), fecha_fin: str = Query(None), db: Session = Depends(get_db)):
    try:
        reporte_path = generar_reporte_inventario(fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)  # Genera el reporte filtrado por fecha si están presentes, o completo si no
        return FileResponse(reporte_path, media_type='application/pdf', filename="reporte_inventario.pdf")
    except Exception as e:
        return {"error": str(e)}


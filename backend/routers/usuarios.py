<<<<<<< HEAD
from fastapi import APIRouter, Depends, HTTPException  # Importa las clases necesarias de FastAPI
from sqlalchemy.orm import Session  # Importa la clase Session de SQLAlchemy
from crud.usuarios import get_usuario, get_usuarios, get_usuario_by_email, create_usuario, update_usuario, delete_usuario  # Importa las funciones CRUD
from schemas.usuarios import Usuario as UsuarioSchema, UsuarioCreate, UsuarioUpdate  # Importa los esquemas
from models.models import Usuario  # Importa el modelo Usuario
from database import SessionLocal  # Importa la sesión de la base de datos
from typing import List  # Importa List para indicar que la respuesta es una lista

router = APIRouter()  # Crea una instancia del enrutador de FastAPI

# Dependencia para obtener la sesión de la base de datos
def get_db():
    # Establece una sesión local de la base de datos
    db = SessionLocal()
    try:
        yield db  # Devuelve la sesión de la base de datos a quien la requiera
    finally:
        db.close()  # Cierra la sesión al finalizar la petición

# Ruta para crear un nuevo usuario
@router.post("/", response_model=UsuarioSchema)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # Verifica si el email ya está registrado
    db_usuario = get_usuario_by_email(db, email=usuario.email)
    if db_usuario:
        raise HTTPException(status_code=400, detail="El email ya está registrado")  # Si el email ya existe, lanza un error
    return create_usuario(db=db, usuario=usuario)  # Llama a la función de creación del usuario

# Ruta para listar usuarios con paginación
@router.get("/", response_model=List[UsuarioSchema])
def listar_usuarios(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_usuarios(db=db, skip=skip, limit=limit)  # Llama a la función para obtener los usuarios

# Ruta para buscar usuarios por nombre
@router.get("/search", response_model=List[UsuarioSchema])
def listar_usuarios_por_nombre(nombre: str = "", db: Session = Depends(get_db)):
    # Si se proporciona un nombre, realiza la búsqueda con un filtro LIKE
    if nombre:
        return db.query(Usuario).filter(Usuario.nombre.ilike(f"%{nombre}%")).all()
    return db.query(Usuario).all()  # Devuelve todos los usuarios si no se proporciona un nombre

# Ruta para obtener un usuario específico por su ID
@router.get("/{usuario_id}", response_model=UsuarioSchema)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = get_usuario(db=db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")  # Si no se encuentra el usuario, lanza un error
    return db_usuario  # Devuelve el usuario encontrado

# Ruta para actualizar un usuario por su ID
@router.put("/{usuario_id}", response_model=UsuarioSchema)
def actualizar_usuario(usuario_id: int, usuario: UsuarioUpdate, db: Session = Depends(get_db)):
    db_usuario = update_usuario(db=db, usuario_id=usuario_id, usuario=usuario)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")  # Si no se encuentra el usuario, lanza un error
    return db_usuario  # Devuelve el usuario actualizado

# Ruta para eliminar un usuario por su ID
@router.delete("/{usuario_id}", response_model=UsuarioSchema)
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = delete_usuario(db=db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")  # Si no se encuentra el usuario, lanza un error
    return db_usuario  # Devuelve el usuario eliminado



'''from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud.usuarios import get_usuario, get_usuarios, get_usuario_by_email, create_usuario, update_usuario, delete_usuario
from schemas.usuarios import Usuario, UsuarioCreate, UsuarioUpdate
from database import SessionLocal
=======
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..crud.usuarios import get_usuario, get_usuarios, get_usuario_by_email, create_usuario, update_usuario, delete_usuario
from ..schemas.usuarios import Usuario, UsuarioCreate, UsuarioUpdate
from backend.database import SessionLocal
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39

router = APIRouter()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=Usuario)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = get_usuario_by_email(db, email=usuario.email)
    if db_usuario:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    return create_usuario(db=db, usuario=usuario)

@router.get("/", response_model=list[Usuario])
def listar_usuarios(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_usuarios(db=db, skip=skip, limit=limit)

@router.get("/{usuario_id}", response_model=Usuario)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = get_usuario(db=db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

@router.put("/{usuario_id}", response_model=Usuario)
def actualizar_usuario(usuario_id: int, usuario: UsuarioUpdate, db: Session = Depends(get_db)):
    db_usuario = update_usuario(db=db, usuario_id=usuario_id, usuario=usuario)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

@router.delete("/{usuario_id}", response_model=Usuario)
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = delete_usuario(db=db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario
<<<<<<< HEAD
'''
=======
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39

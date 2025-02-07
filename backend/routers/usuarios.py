from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud.usuarios import get_usuario, get_usuarios, get_usuario_by_email, create_usuario, update_usuario, delete_usuario, update_profile, change_password
from schemas.usuarios import Usuario as UsuarioSchema, UsuarioCreate, UsuarioUpdate, UsuarioProfileUpdate, ChangePassword
from models.models import Usuario
from database import SessionLocal
from typing import List
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Datos para el dashboard
@router.get("/total", response_model=int)
def total_usuarios(db: Session = Depends(get_db)):
    total = db.query(Usuario).count()
    return total

# Obtener usuario actual
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, "SECRET_KEY", algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_usuario(db, usuario_id=int(user_id))
    if user is None:
        raise credentials_exception
    return user

# Ruta para crear un nuevo usuario
@router.post("/", response_model=UsuarioSchema)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = get_usuario_by_email(db, email=usuario.email)
    if db_usuario:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    return create_usuario(db=db, usuario=usuario)

# Ruta para listar usuarios con paginación
@router.get("/", response_model=List[UsuarioSchema])
def listar_usuarios(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_usuarios(db=db, skip=skip, limit=limit)

# Ruta para buscar usuarios por nombre
@router.get("/search", response_model=List[UsuarioSchema])
def listar_usuarios_por_nombre(nombre: str = "", db: Session = Depends(get_db)):
    if nombre:
        return db.query(Usuario).filter(Usuario.nombre.ilike(f"%{nombre}%")).all()
    return db.query(Usuario).all()

# Ruta para obtener un usuario específico por su ID
@router.get("/{usuario_id}", response_model=UsuarioSchema)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = get_usuario(db=db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

# Ruta para actualizar un usuario por su ID
@router.put("/{usuario_id}", response_model=UsuarioSchema)
def actualizar_usuario(usuario_id: int, usuario: UsuarioUpdate, db: Session = Depends(get_db)):
    db_usuario = update_usuario(db=db, usuario_id=usuario_id, usuario=usuario)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

# Ruta para eliminar un usuario por su ID
@router.delete("/{usuario_id}", response_model=UsuarioSchema)
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = delete_usuario(db=db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

# Ruta para obtener el perfil del usuario actual
@router.get("/profile", response_model=UsuarioSchema)
def get_profile(current_user: UsuarioSchema = Depends(get_current_user)):
    return current_user

# Ruta para actualizar el perfil del usuario actual
@router.put("/profile", response_model=UsuarioSchema)
def update_profile_endpoint(profile_update: UsuarioProfileUpdate, db: Session = Depends(get_db), current_user: UsuarioSchema = Depends(get_current_user)):
    updated_user = update_profile(db, current_user.usuario_id, profile_update)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return updated_user

# Ruta para cambiar la contraseña del usuario actual
@router.put("/change-password", response_model=UsuarioSchema)
def change_password_endpoint(password_data: ChangePassword, db: Session = Depends(get_db), current_user: UsuarioSchema = Depends(get_current_user)):
    updated_user = change_password(db, current_user.usuario_id, password_data)
    if updated_user is None:
        raise HTTPException(status_code=400, detail="Contraseña actual incorrecta")
    return updated_user




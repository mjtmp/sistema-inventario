from sqlalchemy.orm import Session
from ..models.models import Usuario
from ..schemas.usuarios import UsuarioCreate, UsuarioUpdate

def get_usuario(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.usuario_id == usuario_id).first()

def get_usuarios(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Usuario).offset(skip).limit(limit).all()

def get_usuario_by_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()

def create_usuario(db: Session, usuario: UsuarioCreate):
    db_usuario = Usuario(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def update_usuario(db: Session, usuario_id: int, usuario: UsuarioUpdate):
    db_usuario = get_usuario(db, usuario_id)
    if db_usuario:
        for key, value in usuario.dict().items():
            setattr(db_usuario, key, value)
        db.commit()
        db.refresh(db_usuario)
    return db_usuario

def delete_usuario(db: Session, usuario_id: int):
    db_usuario = get_usuario(db, usuario_id)
    if db_usuario:
        db.delete(db_usuario)
        db.commit()
    return db_usuario

# Función de autenticación para verificar la contraseña
def verify_password(plain_password: str, stored_password: str) -> bool:
    return plain_password == stored_password  # Compara las contraseñas directamente

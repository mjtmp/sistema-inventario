from sqlalchemy.orm import Session
<<<<<<< HEAD
from datetime import datetime
from models.models import Usuario  # Importa el modelo Usuario de SQLAlchemy
from schemas.usuarios import UsuarioCreate, UsuarioUpdate  # Importa los esquemas para la creación y actualización de usuarios
from sqlalchemy.orm import joinedload  # Utilizado para cargar relaciones de manera eficiente

# Obtener un solo usuario por ID
def get_usuario(db: Session, usuario_id: int):
    # Realiza una consulta para obtener un usuario por su ID
    return db.query(Usuario).filter(Usuario.usuario_id == usuario_id).first()

# Obtener todos los usuarios, con opción de paginación
def get_usuarios(db: Session, skip: int = 0, limit: int = 10):
    # Consulta todos los usuarios y permite la paginación (offset y limit)
    return db.query(Usuario).options(joinedload(Usuario.rol)).offset(skip).limit(limit).all()

# Obtener un usuario por email
def get_usuario_by_email(db: Session, email: str):
    # Consulta para obtener un usuario a través de su email
    return db.query(Usuario).filter(Usuario.email == email).first()

# Crear un nuevo usuario
def create_usuario(db: Session, usuario: UsuarioCreate):
    # Crea una nueva instancia del modelo Usuario con los datos recibidos
    db_usuario = Usuario(**usuario.dict(), fecha_creacion=datetime.now(), fecha_actualizacion=datetime.now())
    db.add(db_usuario)  # Agrega el nuevo usuario a la sesión
    db.commit()  # Realiza la transacción en la base de datos
    db.refresh(db_usuario)  # Refresca el objeto con los datos actuales de la base de datos
    return db_usuario  # Devuelve el usuario creado

# Actualizar un usuario existente
def update_usuario(db: Session, usuario_id: int, usuario: UsuarioUpdate):
    # Busca el usuario por ID
    db_usuario = get_usuario(db, usuario_id)
    if db_usuario:
        # Si el usuario existe, actualiza sus atributos con los nuevos valores
        for key, value in usuario.dict().items():
            setattr(db_usuario, key, value)
        db.commit()  # Realiza la transacción en la base de datos
        db.refresh(db_usuario)  # Refresca el objeto actualizado
    return db_usuario  # Devuelve el usuario actualizado

# Eliminar un usuario
def delete_usuario(db: Session, usuario_id: int):
    # Busca el usuario por ID
    db_usuario = get_usuario(db, usuario_id)
    if db_usuario:
        db.delete(db_usuario)  # Elimina el usuario de la base de datos
        db.commit()  # Realiza la transacción en la base de datos
    return db_usuario  # Devuelve el usuario eliminado

# Función de autenticación para verificar la contraseña
def verify_password(plain_password: str, stored_password: str) -> bool:
    # Compara la contraseña proporcionada con la almacenada (sin cifrado en este caso)
    return plain_password == stored_password


'''from sqlalchemy.orm import Session
from datetime import datetime  # Para obtener la fecha y hora actual
from models.models import Usuario
from schemas.usuarios import UsuarioCreate, UsuarioUpdate

from sqlalchemy.orm import joinedload
=======
from ..models.models import Usuario
from ..schemas.usuarios import UsuarioCreate, UsuarioUpdate
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39

def get_usuario(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.usuario_id == usuario_id).first()

def get_usuarios(db: Session, skip: int = 0, limit: int = 10):
<<<<<<< HEAD
    return db.query(Usuario).options(joinedload(Usuario.rol)).offset(skip).limit(limit).all()

def get_usuarios(db: Session, skip: int = 0, limit: int = 10):
=======
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39
    return db.query(Usuario).offset(skip).limit(limit).all()

def get_usuario_by_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()

def create_usuario(db: Session, usuario: UsuarioCreate):
<<<<<<< HEAD
    db_usuario = Usuario(**usuario.dict(), fecha_creacion=datetime.now(), fecha_actualizacion=datetime.now())
=======
    db_usuario = Usuario(**usuario.dict())
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def update_usuario(db: Session, usuario_id: int, usuario: UsuarioUpdate):
    db_usuario = get_usuario(db, usuario_id)
    if db_usuario:
        for key, value in usuario.dict().items():
            setattr(db_usuario, key, value)
<<<<<<< HEAD
        db_usuario.fecha_actualizacion = datetime.now()
=======
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39
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
<<<<<<< HEAD
'''
=======
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39

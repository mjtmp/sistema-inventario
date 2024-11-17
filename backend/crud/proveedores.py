from sqlalchemy.orm import Session
<<<<<<< HEAD
from datetime import datetime
from models.models import Proveedor  # Importa el modelo de Proveedor definido en SQLAlchemy
from schemas.proveedores import ProveedorCreate, ProveedorUpdate  # Esquemas de Pydantic para validación

# Obtener un proveedor por su ID
def get_proveedor(db: Session, proveedor_id: int):
    # Busca un proveedor en la base de datos cuyo `proveedor_id` coincida
    return db.query(Proveedor).filter(Proveedor.proveedor_id == proveedor_id).first()

# Obtener una lista de proveedores con paginación
def get_proveedores(db: Session, skip: int = 0, limit: int = 10):
    # Recupera un subconjunto de proveedores, basado en los parámetros `skip` y `limit`
    proveedores = db.query(Proveedor).offset(skip).limit(limit).all()
    # Cuenta el número total de proveedores en la base de datos
    total = db.query(Proveedor).count()
    # Devuelve la lista de proveedores y el total
    return proveedores, total

# Crear un nuevo proveedor
def create_proveedor(db: Session, proveedor: ProveedorCreate):
    # Crea una instancia de `Proveedor` utilizando los datos del esquema y establece las fechas
    db_proveedor = Proveedor(**proveedor.dict(), fecha_creacion=datetime.now(), fecha_actualizacion=datetime.now())
    # Añade el nuevo proveedor a la sesión de la base de datos
    db.add(db_proveedor)
    # Guarda los cambios en la base de datos
    db.commit()
    # Refresca la instancia para incluir datos generados automáticamente (por ejemplo, `proveedor_id`)
    db.refresh(db_proveedor)
    return db_proveedor

# Actualizar un proveedor existente
def update_proveedor(db: Session, proveedor_id: int, proveedor: ProveedorUpdate):
    # Busca el proveedor existente por su ID
    db_proveedor = get_proveedor(db, proveedor_id)
    if db_proveedor:
        # Actualiza los atributos del proveedor con los nuevos valores proporcionados
        for key, value in proveedor.dict().items():
            setattr(db_proveedor, key, value)
        # Actualiza la fecha de modificación
        db_proveedor.fecha_actualizacion = datetime.now()
        # Guarda los cambios en la base de datos
        db.commit()
        # Refresca la instancia para obtener los datos actualizados
        db.refresh(db_proveedor)
    return db_proveedor

# Eliminar un proveedor
def delete_proveedor(db: Session, proveedor_id: int):
    # Busca el proveedor por su ID
    db_proveedor = get_proveedor(db, proveedor_id)
    if db_proveedor:
        # Elimina el proveedor de la base de datos
        db.delete(db_proveedor)
        # Guarda los cambios en la base de datos
        db.commit()
    return db_proveedor

=======
from ..models.models import Proveedor
from ..schemas.proveedores import ProveedorCreate, ProveedorUpdate

def get_proveedor(db: Session, proveedor_id: int):
    return db.query(Proveedor).filter(Proveedor.proveedor_id == proveedor_id).first()

def get_proveedores(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Proveedor).offset(skip).limit(limit).all()

def create_proveedor(db: Session, proveedor: ProveedorCreate):
    db_proveedor = Proveedor(**proveedor.dict())
    db.add(db_proveedor)
    db.commit()
    db.refresh(db_proveedor)
    return db_proveedor

def update_proveedor(db: Session, proveedor_id: int, proveedor: ProveedorUpdate):
    db_proveedor = get_proveedor(db, proveedor_id)
    if db_proveedor:
        for key, value in proveedor.dict().items():
            setattr(db_proveedor, key, value)
        db.commit()
        db.refresh(db_proveedor)
    return db_proveedor

def delete_proveedor(db: Session, proveedor_id: int):
    db_proveedor = get_proveedor(db, proveedor_id)
    if db_proveedor:
        db.delete(db_proveedor)
        db.commit()
    return db_proveedor
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39

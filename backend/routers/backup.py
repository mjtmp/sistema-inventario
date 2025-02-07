from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
import shutil
import os
from database import get_db

router = APIRouter()

@router.get("/", response_class=FileResponse)
def create_backup(db: Session = Depends(get_db)):
    db_file = "./database/inventario_sistema.db"
    backup_file = "./database/backup_inventario_sistema.db"

    # Crear una copia del archivo de base de datos
    shutil.copy(db_file, backup_file)

    return FileResponse(
        path=backup_file,
        media_type='application/octet-stream',
        filename='backup_inventario_sistema.db'
    )

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud.categorias import create_categoria, get_categorias, update_categoria, delete_categoria, get_categoria, get_total_categorias, get_categorias_con_conteo_productos
from schemas.categorias import Categoria, CategoriaCreate, CategoriaUpdate, CategoriaProductoResponse
from database import SessionLocal
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/total", response_model=dict)
def total_categorias(db: Session = Depends(get_db)):
    total = get_total_categorias(db)
    return {"total": total}

@router.get("/conteo_productos", response_model=List[CategoriaProductoResponse])
def categorias_con_conteo_productos(db: Session = Depends(get_db)):
    return get_categorias_con_conteo_productos(db)

@router.post("/", response_model=Categoria)
def crear_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    try:
        return create_categoria(db=db, categoria=categoria).to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/", response_model=dict)
def listar_categorias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categorias = get_categorias(db, skip, limit)
    total = get_total_categorias(db)
    return {"categorias": [categoria.to_dict() for categoria in categorias], "total": total}

@router.get("/{categoria_id}", response_model=Categoria)
def obtener_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = get_categoria(db, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    return categoria.to_dict()

@router.put("/{categoria_id}", response_model=Categoria)
def actualizar_categoria(categoria_id: int, categoria: CategoriaUpdate, db: Session = Depends(get_db)):
    try:
        return update_categoria(db=db, categoria_id=categoria_id, categoria=categoria, usuario_id=categoria.usuario_id).to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{categoria_id}", response_model=Categoria)
def eliminar_categoria(categoria_id: int, usuario_id: int, db: Session = Depends(get_db)):
    db_categoria = delete_categoria(db=db, categoria_id=categoria_id, usuario_id=usuario_id)
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    return db_categoria.to_dict()



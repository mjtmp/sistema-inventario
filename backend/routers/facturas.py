import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from models.models import Factura  # Importar el modelo Factura de SQLAlchemy
from crud.facturas import crear_factura, generar_pdf_factura, obtener_factura, obtener_pagos_por_factura, agregar_abono_a_factura, eliminar_factura, editar_factura, obtenerProductosPorFactura
from schemas.facturas import FacturaCreate, FacturaResponse, AbonoCreate, FacturaUpdate
from fastapi.responses import FileResponse
from database import get_db
from sqlalchemy import func  # Importa func para funciones de agregación
import traceback

# Configuración de logging para registrar errores
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

# Nueva ruta para obtener el total de facturas.
@router.get("/total", response_model=dict)
def total_facturas(db: Session = Depends(get_db)):
    total = db.query(func.count(Factura.factura_id)).scalar()
    return {"total": total}

# Endpoint para crear una factura
@router.post("/", response_model=FacturaResponse)
def crear_factura_endpoint(factura_data: FacturaCreate, db: Session = Depends(get_db)):
    try:
        # Llamada a la función para crear la factura
        return crear_factura(db, factura_data)
    except ValueError as e:
        # Manejo de errores cuando no se encuentra el cliente o el usuario
        logger.error(f"Error de valor: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # Captura de errores inesperados
        logger.error(f"Error inesperado al crear la factura: {str(e)}")
        logger.debug("Detalles del error: ", exc_info=True)
        raise HTTPException(status_code=400, detail="Error al crear la factura")

# Endpoint para descargar el PDF de una factura
@router.get("/{factura_id}/pdf")
def descargar_factura_pdf(factura_id: int, db: Session = Depends(get_db)):
    try:
        # Obtener la factura para conseguir el número de factura
        factura = obtener_factura(db, factura_id)
        if not factura:
            raise HTTPException(status_code=404, detail="Factura no encontrada")
        
        numero_factura = factura.numero_factura

        # Generar el PDF de la factura
        pdf_path = generar_pdf_factura(db, factura_id)
        # Retornar el PDF como respuesta
        return FileResponse(pdf_path, media_type='application/pdf', filename=f"Factura_{numero_factura}.pdf")
    except Exception as e:
        # Manejo de errores durante la generación del PDF
        logger.error(f"Error al generar el PDF para la factura {factura_id}: {str(e)}")
        logger.debug("Detalles del error: ", exc_info=True)
        raise HTTPException(status_code=400, detail="Error al generar el PDF")

# Endpoint para obtener los pagos asociados a una factura
@router.get("/{factura_id}/pagos")
def obtener_pagos(factura_id: int, db: Session = Depends(get_db)):
    try:
        # Llamada a la función para obtener los pagos
        pagos = obtener_pagos_por_factura(db, factura_id)
        return {"pagos": pagos}
    except ValueError as e:
        # Manejo de errores cuando no se encuentra la factura
        logger.error(f"Error de valor: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # Captura de errores inesperados
        logger.error(f"Error inesperado al obtener los pagos: {str(e)}")
        logger.debug("Detalles del error: ", exc_info=True)
        raise HTTPException(status_code=400, detail="Error al obtener los pagos")

@router.post("/{factura_id}/abonos")
def agregar_abono(factura_id: int, abono_data: AbonoCreate, db: Session = Depends(get_db)):
    try:
        return agregar_abono_a_factura(db, factura_id, abono_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error inesperado al agregar abono: {str(e)}")
        logger.debug("Detalles del error: ", exc_info=True)
        raise HTTPException(status_code=500, detail="Error al agregar abono")

@router.get("/{factura_id}")
def obtener_factura_endpoint(factura_id: int, db: Session = Depends(get_db)):
    try:
        return obtenerProductosPorFactura(db, factura_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# Endpoint para eliminar una factura
@router.delete("/{factura_id}")
def eliminar_factura_endpoint(factura_id: int, db: Session = Depends(get_db)):
    try:
        return eliminar_factura(db, factura_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error inesperado al eliminar la factura: {str(e)}")
        logger.debug("Detalles del error: ", exc_info=True)
        raise HTTPException(status_code=500, detail="Error al eliminar la factura")

# Endpoint para editar una factura usando PUT
@router.put("/editar/{factura_id}", response_model=FacturaResponse)
def editar_factura_endpoint(factura_id: int, factura_data: FacturaUpdate, db: Session = Depends(get_db)):
    try:
        return editar_factura(db, factura_id, factura_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error inesperado al editar la factura: {str(e)}")
        logger.debug("Detalles del error: ", exc_info=True)
        raise HTTPException(status_code=500, detail="Error al editar la factura")

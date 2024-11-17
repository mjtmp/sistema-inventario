import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud.facturas import crear_factura, generar_pdf_factura, obtener_factura, obtener_pagos_por_factura
from schemas.facturas import FacturaCreate, FacturaResponse
from fastapi.responses import FileResponse
from database import get_db
import traceback

# Configuración de logging para registrar errores
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

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


'''import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud.facturas import crear_factura, generar_pdf_factura, obtener_factura
from schemas.facturas import FacturaCreate, FacturaResponse
from fastapi.responses import FileResponse
from database import get_db
import traceback

# Configuración de logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=FacturaResponse)
def crear_factura_endpoint(factura_data: FacturaCreate, db: Session = Depends(get_db)):
    try:
        return crear_factura(db, factura_data)
    except ValueError as e:
        # Manejo de errores específicos con código 404
        logger.error(f"Error de valor: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # Capturamos excepciones genéricas y las logueamos
        logger.error(f"Error inesperado al crear la factura: {str(e)}")
        logger.debug("Detalles del error: ", exc_info=True)
        raise HTTPException(status_code=400, detail="Error al crear la factura")

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
        return FileResponse(pdf_path, media_type='application/pdf', filename=f"Factura_{numero_factura}.pdf")
    except Exception as e:
        # Capturamos cualquier excepción durante la generación del PDF
        logger.error(f"Error al generar el PDF para la factura {factura_id}: {str(e)}")
        logger.debug("Detalles del error: ", exc_info=True)
        raise HTTPException(status_code=400, detail="Error al generar el PDF")
'''
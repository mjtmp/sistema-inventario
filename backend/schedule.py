from apscheduler.schedulers.background import BackgroundScheduler
from database import SessionLocal
from crud.salidas_inventario import registrar_salidas_automaticamente
import logging

logging.basicConfig(level=logging.INFO)

def job():
    db = SessionLocal()
    try:
        usuario_id = 1  # Aquí debes obtener el ID del usuario actual
        registrar_salidas_automaticamente(db, usuario_id)
        logging.info("Salidas registradas automáticamente para los pedidos completados")
    finally:
        db.close()

scheduler = BackgroundScheduler()
scheduler.add_job(job, 'interval', minutes=60)  # Ejecutar cada 1 minuto para pruebas rápidas
scheduler.start()

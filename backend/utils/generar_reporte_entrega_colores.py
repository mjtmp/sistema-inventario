import os
import random
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from sqlalchemy.orm import Session
from crud.reportes_entrega import obtener_pedido, obtener_detalles_pedido
from database import SessionLocal

def generar_reporte_entrega_colores(pedido_id: int):
    db = SessionLocal()
    pedido = obtener_pedido(db, pedido_id)
    cliente = pedido.cliente
    detalles = obtener_detalles_pedido(db, pedido_id)
    
    numero_reporte = f"RE-{pedido_id:06d}"
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    transportista = "Juan Perez"
    numero_guia = ''.join([str(random.randint(0, 9)) for _ in range(12)])  # Generar número de guía aleatorio de 12 dígitos

    # Crear el PDF
    pdf_output = f"reportes/reporte_entrega_colores_{pedido_id}.pdf"
    c = canvas.Canvas(pdf_output, pagesize=letter)

    # Encabezado
    c.setFont("Helvetica-Bold", 12)
    c.drawString(30, 750, "Invermaur, C.A.")
    c.setFont("Helvetica", 10)
    c.drawString(30, 735, "Av. Juan de Urpin, Residencia Vittoria III, Piso PB, Local 6,")
    c.drawString(30, 720, "Barrio El Espejo, Barcelona - Edo. Anzoátegui")
    c.drawString(30, 705, "Teléfono: (0281) 274.07.27 / 276.98.35")
    c.setFillColor(colors.blue)
    c.rect(30, 700, 550, 2, fill=True, stroke=False)

    # Título y Fecha
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, 680, "REPORTE DE ENTREGA")
    c.setFont("Helvetica", 10)
    c.drawString(30, 665, f"Reporte No: {numero_reporte}")
    c.drawString(30, 650, f"Fecha: {fecha_actual}")
    c.drawString(30, 635, f"Pedido ID: {pedido_id}")

    # Datos del Cliente
    c.setFont("Helvetica-Bold", 12)
    c.drawString(30, 615, "Datos del Cliente")
    c.setFont("Helvetica", 10)
    c.drawString(30, 600, f"Nombre: {cliente.nombre}")
    c.drawString(30, 585, f"Dirección: {cliente.direccion}")
    c.drawString(30, 570, f"Teléfono: {cliente.telefono}")
    c.drawString(30, 555, f"{cliente.tipo_documento}: {cliente.numero_documento}")

    # Datos del Transportista
    c.setFont("Helvetica-Bold", 12)
    c.drawString(300, 615, "Datos del Transportista")
    c.setFont("Helvetica", 10)
    c.drawString(300, 600, f"Nombre: {transportista}")
    c.drawString(300, 585, f"Número de Guía: {numero_guia}")

    # Tabla de Productos
    c.setFont("Helvetica-Bold", 12)
    c.drawString(30, 540, "Productos Entregados")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(30, 525, "Código")
    c.drawString(110, 525, "Producto")
    c.drawString(250, 525, "Cantidad")
    c.drawString(310, 525, "Precio Unit.")
    c.drawString(380, 525, "Subtotal")

    c.setFont("Helvetica", 10)
    y = 510
    total_pedido = 0
    for detalle in detalles:
        codigo_producto = detalle.producto.codigo
        nombre_producto = detalle.producto.nombre
        cantidad = detalle.cantidad
        precio_unitario = detalle.precio_unitario
        subtotal = cantidad * precio_unitario
        total_pedido += subtotal

        c.drawString(30, y, codigo_producto)
        c.drawString(110, y, nombre_producto)
        c.drawString(250, y, str(cantidad))
        c.drawString(310, y, f'{precio_unitario:.2f}')
        c.drawString(380, y, f'{subtotal:.2f}')
        y -= 15

    c.setFont("Helvetica-Bold", 10)
    c.drawString(30, y-10, f"Total del Pedido: Bs. {total_pedido:,.2f}")

    # Observaciones
    observaciones = ("Todos los productos entregados cumplen con los estándares de calidad y están verificados antes del envío. "
                     "Para cualquier duda o incidencia, por favor contacte a nuestro servicio al cliente en un plazo de 24 horas. "
                     "Agradecemos su preferencia por Invermaur, C.A. y esperamos seguir brindándole nuestros servicios.")
    c.setFont("Helvetica", 10)
    c.drawString(30, y-30, "Observaciones:")
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(30, y-45, observaciones[:90])
    c.drawString(30, y-60, observaciones[90:180])
    c.drawString(30, y-75, observaciones[180:270])

    # Firma del Receptor
    c.setFont("Helvetica-Bold", 10)
    c.drawString(30, y-100, "Datos del Receptor")
    c.setFont("Helvetica", 10)
    c.drawString(30, y-115, "________________________")
    c.drawString(30, y-130, f"Nombre: {cliente.nombre}")
    c.drawString(30, y-145, f"Cédula: {cliente.numero_documento}")

    c.save()

    return pdf_output

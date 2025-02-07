import os
import random
from fpdf import FPDF
from datetime import datetime
from sqlalchemy.orm import Session
from crud.reportes_entrega import obtener_pedido, obtener_detalles_pedido
from database import SessionLocal

class PDF(FPDF):
    def __init__(self, db):
        super().__init__()
        self.db = db

    def header(self):
        self.image('utils/logo/invermaur.png', 10, 8, 33)
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Invermaur, C.A.', 0, 1, 'C')
        self.set_font('Arial', '', 10)
        self.cell(0, 5, 'Av. Juan de Urpin, Residencia Vittoria III, Piso PB, Local 6,', 0, 1, 'C')
        self.cell(0, 5, 'Barrio El Espejo, Barcelona - Edo. Anzoátegui', 0, 1, 'C')
        self.cell(0, 5, 'Teléfono: (0281) 274.07.27 / 276.98.35', 0, 1, 'C')
        self.ln(10)
        self.cell(0, 0, '_____________________________________________________________________________________________', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def titulo(self, numero_reporte, pedido_id, fecha_actual):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'REPORTE DE ENTREGA', 0, 1, 'C')
        self.set_font('Arial', '', 10)
        self.cell(100, 10, f'Reporte No: {numero_reporte}', 0, 0, 'L')
        transportista = "Juan Perez"
        numero_guia = ''.join([str(random.randint(0, 9)) for _ in range(12)])  # Generar número de guía aleatorio de 12 dígitos
        self.cell(0, 10, f'Transportista: {transportista}  |  Nro. Guía: {numero_guia}', 0, 1, 'R')
        self.cell(100, 10, f'Fecha: {fecha_actual}', 0, 0, 'L')
        self.cell(0, 10, f'Pedido ID: {pedido_id}', 0, 1, 'R')
        self.ln(10)

    def datos_cliente(self, cliente):
        self.set_font('Arial', 'B', 10)
        self.cell(0, 10, 'Datos del Cliente', 0, 1, 'L')
        self.set_font('Arial', '', 10)
        self.cell(0, 6, f'Nombre: {cliente.nombre}', 0, 1, 'L')
        self.cell(0, 6, f'Dirección: {cliente.direccion}', 0, 1, 'L')
        self.cell(0, 6, f'Teléfono: {cliente.telefono}', 0, 1, 'L')
        self.cell(0, 6, f'Número de documento: {cliente.tipo_documento}-{cliente.numero_documento}', 0, 1, 'L')
        self.ln(10)

    def tabla_productos(self, detalles):
        self.set_font('Arial', 'B', 10)
        self.set_x(25)  # Centramos la tabla
        self.cell(30, 6, 'Código', 1, 0, 'C')
        self.cell(60, 6, 'Producto', 1, 0, 'C')
        self.cell(20, 6, 'Cantidad', 1, 0, 'C')
        self.cell(20, 6, 'Precio Unit.', 1, 0, 'C')
        self.cell(30, 6, 'Subtotal', 1, 1, 'C')

        self.set_font('Arial', '', 10)
        total_pedido = 0
        for detalle in detalles:
            codigo_producto = detalle.producto.codigo
            nombre_producto = detalle.producto.nombre
            cantidad = detalle.cantidad
            precio_unitario = detalle.precio_unitario
            subtotal = cantidad * precio_unitario
            total_pedido += subtotal

            self.set_x(25)  # Centramos la tabla en cada fila
            self.cell(30, 6, codigo_producto, 1)
            self.cell(60, 6, nombre_producto, 1)
            self.cell(20, 6, str(cantidad), 1)
            self.cell(20, 6, f'{precio_unitario:.2f}', 1)
            self.cell(30, 6, f'{subtotal:.2f}', 1)
            self.ln()

        self.set_font('Arial', 'B', 10)
        self.set_x(25)  # Centramos la tabla
        self.cell(130, 6, 'Total del Pedido:', 1, 0, 'R')
        self.cell(30, 6, f'Bs. {total_pedido:,.2f}', 1, 1, 'C')
        self.ln(10)

    def datos_receptor(self, nombre_receptor, cedula_receptor):
        self.set_font('Arial', 'B', 10)
        self.cell(0, 10, 'Datos del Receptor', 0, 1, 'C')
        self.cell(0, 10, '________________________', 0, 1, 'C')  # Línea para firmar
        self.set_font('Arial', '', 10)
        self.cell(0, 6, f'Nombre: {nombre_receptor}', 0, 1, 'C')
        self.cell(0, 6, f'Cédula: {cedula_receptor}', 0, 1, 'C')
        self.ln(10)

    def observaciones(self, observaciones):
        self.set_font('Arial', 'B', 10)
        self.cell(0, 10, 'Observaciones', 0, 1, 'L')
        self.set_font('Arial', '', 9)
        self.multi_cell(0, 6, observaciones, 1, 'L')

def generar_reporte_entrega(pedido_id: int):
    db = SessionLocal()
    pedido = obtener_pedido(db, pedido_id)
    cliente = pedido.cliente
    detalles = obtener_detalles_pedido(db, pedido_id)

    # Generar un número de reporte único
    numero_reporte = f"RE-{pedido_id:06d}"

    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    pdf = PDF(db)
    pdf.add_page()
    pdf.titulo(numero_reporte, pedido_id, fecha_actual)
    pdf.datos_cliente(cliente)
    pdf.tabla_productos(detalles)

    observaciones = ("Todos los productos entregados cumplen con los estándares de calidad y están verificados antes del envío. "
                     "Para cualquier duda o incidencia, por favor contacte a nuestro servicio al cliente en un plazo de 24 horas. "
                     "Agradecemos su preferencia por Invermaur, C.A. y esperamos seguir brindándole nuestros servicios.")
    nombre_receptor = cliente.nombre
    cedula_receptor = cliente.numero_documento
    pdf.datos_receptor(nombre_receptor, cedula_receptor)
    pdf.observaciones(observaciones)

    os.makedirs("reportes", exist_ok=True)
    pdf_output = f"reportes/reporte_entrega_{pedido_id}.pdf"
    pdf.output(pdf_output)

    return pdf_output







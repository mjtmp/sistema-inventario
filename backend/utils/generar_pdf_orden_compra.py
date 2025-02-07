import os
from fpdf import FPDF
from datetime import datetime
from sqlalchemy.orm import Session
from models.models import OrdenCompra, DetalleOrdenCompra, Proveedor
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

    def titulo(self, numero_orden, fecha_actual):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'ORDEN DE PEDIDO', 0, 1, 'C')
        self.set_font('Arial', '', 10)
        self.cell(0, 10, f'Orden No: {numero_orden}', 0, 1, 'L')
        self.cell(0, 10, f'Fecha: {fecha_actual}', 0, 1, 'L')
        self.ln(10)

    def datos_proveedor(self, proveedor):
        self.set_font('Arial', 'B', 10)
        self.cell(0, 10, 'Datos del Proveedor', 0, 1, 'L')
        self.set_font('Arial', '', 10)
        self.cell(0, 6, f'Nombre: {proveedor.nombre}', 0, 1, 'L')
        self.cell(0, 6, f'Dirección: {proveedor.direccion}', 0, 1, 'L')
        self.cell(0, 6, f'Teléfono: {proveedor.telefono}', 0, 1, 'L')
        self.cell(0, 6, f'Número de Identificación Fiscal: {proveedor.rif}', 0, 1, 'L')
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
        total_compra = 0
        for detalle in detalles:
            codigo_producto = detalle.producto.codigo
            nombre_producto = detalle.producto.nombre
            cantidad = detalle.cantidad
            precio_unitario = detalle.precio_unitario
            subtotal = cantidad * precio_unitario
            total_compra += subtotal

            self.set_x(25)  # Centramos la tabla en cada fila
            self.cell(30, 6, codigo_producto, 1)
            self.cell(60, 6, nombre_producto, 1)
            self.cell(20, 6, str(cantidad), 1)
            self.cell(20, 6, f'{precio_unitario:.2f}', 1)
            self.cell(30, 6, f'{subtotal:.2f}', 1)
            self.ln()

        self.set_font('Arial', 'B', 10)
        self.set_x(25)  # Centramos la tabla
        self.cell(130, 6, 'Total de la Orden:', 1, 0, 'R')
        self.cell(30, 6, f'{total_compra:,.2f}', 1, 1, 'C')
        self.ln(10)

    def condiciones_pago(self, forma_pago, plazos_pago):
        self.set_font('Arial', 'B', 10)
        self.cell(0, 10, 'Condiciones de Pago', 0, 1, 'L')
        self.set_font('Arial', '', 10)
        self.cell(0, 6, f'Forma de Pago: {forma_pago}', 0, 1, 'L')
        self.cell(0, 6, f'Plazos de Pago: {plazos_pago}', 0, 1, 'L')
        self.ln(10)

    def condiciones_entrega(self, fecha_entrega, lugar_entrega):
        self.set_font('Arial', 'B', 10)
        self.cell(0, 10, 'Condiciones de Entrega', 0, 1, 'L')
        self.set_font('Arial', '', 10)
        self.cell(0, 6, f'Fecha de Entrega Estimada: {fecha_entrega}', 0, 1, 'L')
        self.cell(0, 6, f'Lugar de Entrega: {lugar_entrega}', 0, 1, 'L')
        self.ln(10)

    def observaciones(self, observaciones):
        self.set_font('Arial', 'B', 10)
        self.cell(0, 10, 'Observaciones', 0, 1, 'L')
        self.set_font('Arial', '', 9)
        self.multi_cell(0, 6, observaciones, 1, 'L')

def generar_pdf_orden_compra(orden_compra_id: int):
    db = SessionLocal()
    orden_compra = db.query(OrdenCompra).filter(OrdenCompra.orden_compra_id == orden_compra_id).first()
    proveedor = db.query(Proveedor).filter(Proveedor.proveedor_id == orden_compra.proveedor_id).first()
    detalles = db.query(DetalleOrdenCompra).filter(DetalleOrdenCompra.orden_compra_id == orden_compra_id).all()

    numero_orden = f"OC-{orden_compra_id:06d}"
    fecha_actual = datetime.now().strftime("%Y-%m-%d")

    pdf = PDF(db)
    pdf.add_page()
    pdf.titulo(numero_orden, fecha_actual)
    pdf.datos_proveedor(proveedor)
    pdf.tabla_productos(detalles)

    observaciones = "Todos los productos deben cumplir con los estándares de calidad y estar verificados antes del envío."
    forma_pago = "Transferencia bancaria"
    plazos_pago = "Pago al contado"
    fecha_entrega = "15 días después de la emisión"
    lugar_entrega = "Almacen principal"

    pdf.condiciones_pago(forma_pago, plazos_pago)
    pdf.condiciones_entrega(fecha_entrega, lugar_entrega)
    pdf.observaciones(observaciones)

    os.makedirs("ordenes_compra", exist_ok=True)
    pdf_output = f"ordenes_compra/orden_pedido_{orden_compra_id}.pdf"
    pdf.output(pdf_output)

    return pdf_output

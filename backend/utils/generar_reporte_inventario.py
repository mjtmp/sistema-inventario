import os
from fpdf import FPDF
from datetime import datetime
from sqlalchemy.orm import Session
from crud.productos import get_productos_por_fecha, get_precio_costo_unitario
from database import SessionLocal

class PDF(FPDF):
    def header(self):
        self.image('utils/logo/invermaur.png', 10, 8, 33)  # Logo de la empresa
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
        self.set_font('Arial', 'I', 6)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def titulo(self, fecha_actual, fecha_inicio, fecha_fin):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'REPORTE DE INVENTARIO', 0, 1, 'C')
        self.set_font('Arial', '', 8)
        self.cell(0, 10, f'Fecha: {fecha_actual}', 0, 1, 'C')
        if fecha_inicio and fecha_fin:
            self.cell(0, 10, f'De: {fecha_inicio} A: {fecha_fin}', 0, 1, 'C')
        self.ln(10)

    def tabla_productos(self, productos, db):
        self.set_font('Arial', 'B', 8)
        self.set_x(10)  # Asegurar que la tabla esté centrada en la hoja
        self.cell(20, 6, 'Código', 1)
        self.cell(30, 6, 'Nombre', 1)
        self.cell(30, 6, 'Categoría', 1)
        self.cell(10, 6, 'Stock', 1)
        self.cell(16, 6, 'Stock Min', 1)
        self.cell(16, 6, 'Stock Max', 1)
        self.cell(16, 6, 'Ubicación', 1)
        self.cell(16, 6, 'P. Compra', 1)  # Abreviación de "Precio Compra"
        self.cell(16, 6, 'P. Venta', 1)
        self.cell(16, 6, 'V. Total', 1)
        self.ln()

        self.set_font('Arial', '', 8)
        for producto in productos:
            precio_compra = get_precio_costo_unitario(db, producto.producto_id)
            valor_total = producto.stock * precio_compra
            self.cell(20, 6, str(producto.codigo), 1)
            self.cell(30, 6, producto.nombre, 1)
            self.cell(30, 6, producto.categoria.nombre if producto.categoria else '', 1)
            self.cell(10, 6, str(producto.stock), 1)
            self.cell(16, 6, str(producto.cantidad_minima), 1)
            self.cell(16, 6, str(producto.cantidad_maxima), 1)
            self.cell(16, 6, producto.ubicacion if producto.ubicacion else '', 1)
            self.cell(16, 6, f'{precio_compra:.2f}', 1)
            self.cell(16, 6, f'{producto.precio:.2f}', 1)
            self.cell(16, 6, f'{valor_total:.2f}', 1)
            self.ln()

def generar_reporte_inventario(fecha_inicio=None, fecha_fin=None):
    db = SessionLocal()
    productos, _ = get_productos_por_fecha(db, fecha_inicio, fecha_fin)

    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    pdf = PDF()
    pdf.add_page()
    pdf.titulo(fecha_actual, fecha_inicio, fecha_fin)
    pdf.tabla_productos(productos, db)

    os.makedirs("reportes", exist_ok=True)
    pdf_output = "reportes/reporte_inventario.pdf"
    pdf.output(pdf_output)

    return pdf_output

import random
import string
from fpdf import FPDF
from datetime import date
import os
from sqlalchemy.orm import Session
from models.models import Pedido, DetallePedido, Cliente

class PDF(FPDF):
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

    def cliente_info(self, cliente):
        self.set_font('Arial', 'B', 10)
        self.cell(0, 10, 'Información del Cliente:', 0, 1)
        self.set_font('Arial', '', 10)
        self.cell(0, 5, f"Nombre: {cliente['nombre']}", 0, 1)
        self.cell(0, 5, f"Teléfono: {cliente['telefono']}", 0, 1)
        self.cell(0, 5, f"Correo electrónico: {cliente['email']}", 0, 1)
        self.cell(0, 5, f"Dirección: {cliente['direccion']}", 0, 1)
        self.ln(10)

    def pedido_info(self, numero_pedido, fecha, estado):
        self.set_xy(130, 60)
        self.set_font('Arial', 'B', 10)
        self.cell(0, 5, f'Pedido Nº: 000{numero_pedido}', 0, 1, 'R')
        self.cell(0, 5, f'Fecha: {fecha}', 0, 1, 'R')
        self.cell(0, 5, f'Estado: {estado}', 0, 1, 'R')
        self.ln(10)

    def productos_table(self, productos):
        self.set_y(self.get_y() + 10)
        self.set_font('Arial', 'B', 10)
        self.cell(20, 10, 'Cantidad', 1, 0, 'C')
        self.cell(80, 10, 'Producto', 1, 0, 'C')
        self.cell(30, 10, 'Precio Unitario', 1, 0, 'C')
        self.cell(30, 10, 'Monto Total', 1, 1, 'C')
        self.set_font('Arial', '', 10)

        subtotal = 0
        total_iva = 0
        iva_porcentaje = 0.16

        for prod in productos:
            cantidad = prod["cantidad"]
            descripcion = prod["descripcion"]
            precio_unitario = prod["precio_unitario"]
            tiene_iva = prod["tiene_iva"]
            monto_total = cantidad * precio_unitario

            self.cell(20, 10, str(cantidad), 1, 0, 'C')
            self.cell(80, 10, descripcion, 1, 0, 'L')
            self.cell(30, 10, f"{precio_unitario:.2f}", 1, 0, 'C')
            self.cell(30, 10, f"{monto_total:.2f}", 1, 1, 'C')

            subtotal += monto_total
            if tiene_iva:
                total_iva += monto_total * iva_porcentaje

        total = subtotal + total_iva
        self.ln(10)
        self.cell(0, 10, f'Subtotal: {subtotal:.2f}', 0, 1, 'R')
        self.cell(0, 10, f'IVA (16%): {total_iva:.2f}', 0, 1, 'R')
        self.cell(0, 10, f'Total a Pagar: {total:.2f}', 0, 1, 'R')

    def metodos_pago(self, metodos):
        self.set_font('Arial', 'B', 10)
        self.cell(0, 10, 'Métodos de Pago:', 0, 1)
        self.set_font('Arial', '', 10)
        for metodo in metodos:
            self.cell(0, 5, metodo, 0, 1)
        self.ln(10)

    def firmas(self):
        firma_y = self.get_y() + 20

        # Primera línea de firma a la izquierda
        self.set_xy(10, firma_y)
        self.cell(60, 10, '_________________________', 0, 0, 'L')
        self.cell(60, 10, '', 0, 0)  # Espacio entre firmas
        self.cell(60, 10, '_________________________', 0, 1, 'L')

        # Etiquetas de firma
        self.set_xy(10, firma_y + 10)
        self.cell(60, 10, 'Firma del Representante', 0, 0, 'L')
        self.cell(60, 10, '', 0, 0)
        self.cell(60, 10, 'Firma del Cliente', 0, 1, 'L')

def generar_pedido(cliente, pedido_info, productos, metodos_pago):
    pdf = PDF()
    pdf.add_page()
    pdf.cliente_info(cliente)
    pdf.pedido_info(pedido_info['numero'], date.today().isoformat(), pedido_info['estado'])
    pdf.productos_table(productos)
    pdf.metodos_pago(metodos_pago)
    pdf.firmas()

    pdf_output = f"./pedidos/Pedido_{pedido_info['numero']}.pdf"
    pdf.output(pdf_output)

    return pdf_output

def generate_unique_order_number(db: Session):
    while True:
        numero_pedido = 'PED' + ''.join(random.choices(string.digits, k=6))
        pedido_existente = db.query(Pedido).filter(Pedido.numero_pedido == numero_pedido).first()
        if not pedido_existente:
            return numero_pedido


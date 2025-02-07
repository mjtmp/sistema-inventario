import random  # Módulo para generar números aleatorios
import string  # Módulo para trabajar con cadenas de texto
from fpdf import FPDF  # Librería para generar archivos PDF
from datetime import date  # Módulo para trabajar con fechas
import os  # Módulo para interactuar con el sistema operativo (por ejemplo, manejar archivos y directorios)
from sqlalchemy.orm import Session  # Importación de la sesión de SQLAlchemy para consultas a la base de datos
from models.models import Factura  # Importación del modelo Factura (asegúrate de tener este modelo definido)

# Clase PDF personalizada para generar facturas en formato PDF
class PDF(FPDF):
    # Cabecera del PDF, se muestra al principio de cada página
    def header(self):
        self.image('utils/logo/invermaur.png', 10, 8, 33)  # Logo de la empresa
        self.set_font('Arial', 'B', 12)  # Definir fuente para la cabecera
        self.cell(0, 10, 'Invermaur, C.A.', 0, 1, 'C')  # Nombre de la empresa en el centro
        self.set_font('Arial', '', 10)  # Cambiar la fuente para la siguiente línea
        # Información de la dirección y contacto de la empresa
        self.cell(0, 5, 'Av. Juan de Urpin, Residencia Vittoria III, Piso PB, Local 6,', 0, 1, 'C')
        self.cell(0, 5, 'Barrio El Espejo, Barcelona - Edo. Anzoátegui', 0, 1, 'C')
        self.cell(0, 5, 'Teléfono: (0281) 274.07.27 / 276.98.35', 0, 1, 'C')
        self.ln(10)  # Espacio en blanco
        self.cell(0, 0, '_____________________________________________________________________________________________', 0, 1, 'C')  # Línea separadora
        self.ln(10)

    # Pie de página que se muestra al final de cada página
    def footer(self):
        self.set_y(-15)  # Posicionar a 15 unidades desde el fondo de la página
        self.set_font('Arial', 'I', 8)  # Cambiar la fuente para el pie de página
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')  # Número de página en el centro

    # Información del cliente que se incluye en la factura
    def cliente_info(self, cliente):
        self.set_font('Arial', 'B', 10)  # Fuente en negrita
        self.cell(0, 10, 'Información del Cliente:', 0, 1)  # Título
        self.set_font('Arial', '', 10)  # Cambiar la fuente a normal
        # Mostrar los datos del cliente en la factura
        self.cell(0, 5, f"Nombre: {cliente['nombre']}", 0, 1)
        self.cell(0, 5, f"Teléfono: {cliente['telefono']}", 0, 1)
        self.cell(0, 5, f"Correo electrónico: {cliente['email']}", 0, 1)
        self.cell(0, 5, f"Dirección: {cliente['direccion']}", 0, 1)
        self.ln(100)  # Aumentar el espacio entre la información del cliente y la tabla de productos

    # Información de la factura, como número y fecha
    def factura_info(self, numero_factura, fecha):
        self.set_xy(130, 60)  # Posicionar el texto en la coordenada indicada
        self.set_font('Arial', 'B', 10)  # Fuente en negrita
        # Mostrar número de factura y fecha
        self.cell(0, 5, f'Factura Nº: {numero_factura}', 0, 1, 'R')  # Alineado a la derecha
        self.cell(0, 5, f'Fecha: {fecha}', 0, 1, 'R')
        self.ln(10)

    # Tabla de productos con la cantidad, descripción, precio unitario y monto total
    def productos_table(self, productos):
        self.set_y(self.get_y() + 10)  # Posicionar la tabla un poco más abajo
        self.set_font('Arial', 'B', 10)  # Fuente en negrita para los encabezados
        # Encabezados de la tabla
        self.cell(20, 10, 'Cantidad', 1, 0, 'C')
        self.cell(80, 10, 'Producto', 1, 0, 'C')
        self.cell(30, 10, 'Precio Unitario', 1, 0, 'C')
        self.cell(30, 10, 'Monto Total', 1, 1, 'C')
        self.set_font('Arial', '', 10)  # Fuente normal para el contenido de la tabla

        subtotal = 0  # Inicializar el subtotal
        total_iva = 0  # Inicializar el total del IVA
        iva_porcentaje = 0.16  # Porcentaje de IVA

        for prod in productos:
            # Accedemos a los atributos de cada producto
            cantidad = prod["cantidad"]
            descripcion = prod["descripcion"]
            precio_unitario = prod["precio_unitario"]
            tiene_iva = prod["tiene_iva"]
            monto_total = cantidad * precio_unitario  # Calcular el monto total del producto

            # Imprimir los datos del producto en la tabla
            self.cell(20, 10, str(cantidad), 1, 0, 'C')
            self.cell(80, 10, descripcion, 1, 0, 'L')
            self.cell(30, 10, f"{precio_unitario:.2f}", 1, 0, 'C')
            self.cell(30, 10, f"{monto_total:.2f}", 1, 1, 'C')

            subtotal += monto_total  # Sumar al subtotal
            if tiene_iva:  # Si el producto tiene IVA
                total_iva += monto_total * iva_porcentaje  # Calcular el IVA

        # Mostrar el subtotal, el IVA y el total
        total = subtotal + total_iva
        self.ln(10)
        self.cell(0, 10, f'Subtotal: {subtotal:.2f}', 0, 1, 'R')
        self.cell(0, 10, f'IVA (16%): {total_iva:.2f}', 0, 1, 'R')
        self.cell(0, 10, f'Total a Pagar: {total:.2f}', 0, 1, 'R')

# Función para generar un número de factura único
def generate_unique_invoice_number(db: Session):
    while True:
        # Generar un número de factura único con 6 dígitos aleatorios
        numero_factura = 'FACT' + ''.join(random.choices(string.digits, k=6))
        # Verificar si el número de factura ya existe en la base de datos
        factura_existente = db.query(Factura).filter(Factura.numero_factura == numero_factura).first()
        if not factura_existente:  # Si no existe, devolver el número de factura
            return numero_factura

# Función para obtener el número de factura
def obtener_numero_factura(db: Session):
    return generate_unique_invoice_number(db)

# Función para generar una factura en formato PDF
def generar_factura(cliente, factura_info, productos):
    # Crear el objeto PDF
    pdf = PDF()
    pdf.add_page()  # Agregar una página
    pdf.cliente_info(cliente)  # Agregar la información del cliente
    pdf.factura_info(factura_info['numero'], date.today().isoformat())  # Agregar la información de la factura
    pdf.productos_table(productos)  # Agregar la tabla de productos

    # Guardar el PDF en el sistema de archivos
    pdf_output = f"./facturas/Factura_{factura_info['numero']}.pdf"
    pdf.output(pdf_output)

    return pdf_output  # Retornar la ruta del archivo PDF generado


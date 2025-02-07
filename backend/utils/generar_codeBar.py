import barcode
from barcode.writer import ImageWriter
import uuid
import os


class BarcodeGenerator:
    def __init__(self, path='media/'):
        self.path = path
        os.makedirs(self.path, exist_ok=True)  # Crear el directorio si no existe

    def generate(self, ean):
        try:
            # Crear el código de barras utilizando Code128
            code_class = barcode.get_barcode_class('code128')
            code = code_class(ean, writer=ImageWriter())

            # Generar un código único para el archivo
            code_unico = str(uuid.uuid4())
            print(f"Código único generado: {code_unico}")

            # Guardar el archivo con el código único como nombre
            output_file = code.save(os.path.join(self.path, code_unico))
            print(f"Código de barras generado y guardado en: {output_file}")

            return output_file
        except Exception as e:
            print(f"Error al generar el código de barras: {e}")
            return None

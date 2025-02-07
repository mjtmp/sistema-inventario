from weasyprint import HTML

# Variables dinámicas
cliente = "YEFERSON CASIQUE"
rif = "V1955961189"
condicion_pago = "5 DÍAS DE CRÉDITO"
vencimiento = "23/05/2020"
entrega_numero = "00000097"
fecha_emision = "23/05/2020"
productos = [
    {"codigo": "1DCANUMSIM01", "descripcion": "CANULA DE MAYO # 0 (60 MM) NEGRA", "unidad": "DOCENA", "cantidad": 20, "precio_unit": 3000.00, "impuesto": 12, "total": 60000.00},
    {"codigo": "0000043", "descripcion": "Artículo para prueba de envío (TEALCA YTA)", "unidad": "UNIDAD", "cantidad": 4, "precio_unit": 30000.00, "impuesto": 12, "total": 120000.00}
]

subtotal = sum(producto['total'] for producto in productos)
iva = subtotal * 0.12
total = subtotal + iva

# Construcción de filas de la tabla dinámicamente
tabla_filas = ""
for producto in productos:
    tabla_filas += f"""
    <tr>
        <td>{producto['codigo']}</td>
        <td>{producto['descripcion']}</td>
        <td>{producto['unidad']}</td>
        <td>{producto['cantidad']}</td>
        <td>{producto['precio_unit']:.2f}</td>
        <td>{producto['impuesto']}%</td>
        <td>{producto['total']:.2f}</td>
    </tr>
    """

# Plantilla HTML con datos dinámicos
html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nota de Entrega</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
        }}
        .container {{
            padding: 20px;
        }}
        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }}
        .logo {{
            width: 150px;
        }}
        .title {{
            text-align: right;
        }}
        .title h1 {{
            margin: 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }}
        th, td {{
            border: 1px solid black;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
        }}
        .footer {{
            text-align: right;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <img src="https://via.placeholder.com/150" alt="Logo" class="logo">
            <div class="title">
                <h1>NOTA DE ENTREGA</h1>
                <p>Fecha Emisión: {fecha_emision}</p>
                <p>Entrega Número: {entrega_numero}</p>
            </div>
        </header>
        <div class="details">
            <p><strong>Cliente:</strong> {cliente}</p>
            <p><strong>RIF:</strong> {rif}</p>
            <p><strong>Condición de Pago:</strong> {condicion_pago}</p>
            <p><strong>Vencimiento:</strong> {vencimiento}</p>
        </div>
        <table>
            <tr>
                <th>Código</th>
                <th>Descripción</th>
                <th>Unidad</th>
                <th>Cantidad</th>
                <th>Precio Unit.</th>
                <th>% Imp</th>
                <th>Total</th>
            </tr>
            {tabla_filas}
        </table>
        <div class="footer">
            <p><strong>Subtotal:</strong> {subtotal:.2f}</p>
            <p><strong>I.V.A. (12%):</strong> {iva:.2f}</p>
            <p><strong>Total:</strong> {total:.2f}</p>
        </div>
    </div>
</body>
</html>
"""

# Generar el PDF
HTML(string=html).write_pdf("nota_entrega_dinamica.pdf")

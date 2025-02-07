from fastapi import HTTPException
from bs4 import BeautifulSoup
import httpx

async def get_dollar_rate():
    url = "https://www.bcv.org.ve"  # URL del Banco Central de Venezuela
    valor_dolar_predeterminado = 54.9113  # Valor predeterminado del dólar

    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(url)
            response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        
        div_dolar = soup.find('div', id='dolar')
        dolar = div_dolar.find('strong').text
        dolar_limpio = dolar.replace(' ', '').replace(',', '.')
        valor_dolar = float(dolar_limpio)
        valor_dolar_redondeado = round(valor_dolar, 4)

        return {"dolar": valor_dolar_redondeado}

    except httpx.HTTPError as e:
        # Retornar valor predeterminado en caso de error
        return {"dolar": valor_dolar_predeterminado, "error": f"Error al acceder a la URL: {str(e)}"}


from pydantic import BaseModel

class ProductoEntradasSalidasResponse(BaseModel):
    producto: str
    total_entradas: int
    valor_entradas: float
    total_salidas: int
    valor_salidas: float

    class Config:
        from_attributes = True

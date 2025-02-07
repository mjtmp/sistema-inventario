from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/")
def get_manual():
    return FileResponse(path="./manuals/manual_de_usuario.pdf", media_type='application/pdf')

from fastapi import APIRouter
from presentation.generate_full_presentation import generate_presentation
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/presentation", summary="Скачать презентацию PPTX")
def get_presentation():
    fname = generate_presentation()
    return FileResponse(fname, media_type='application/vnd.openxmlformats-officedocument.presentationml.presentation', filename=fname)

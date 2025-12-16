from fastapi import APIRouter, UploadFile
from imports.vtd_loader import load_vtd_csv

router = APIRouter()

@router.post("/import/vtd")
async def import_vtd(file: UploadFile):
    path = f"/tmp/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())

    data = load_vtd_csv(path)
    return {"defects_loaded": len(data)}

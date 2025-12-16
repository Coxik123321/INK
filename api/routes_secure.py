from fastapi import APIRouter, Depends
from api.auth import get_current_user

router = APIRouter()

@router.get("/secure/info")
def secure_info(user=Depends(get_current_user)):
    return {"role": user["role"], "status": "ok"}

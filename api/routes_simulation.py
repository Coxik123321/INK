from fastapi import APIRouter
from pydantic import BaseModel
from simulation.whatif import what_if_scenario

router = APIRouter()

class ScenarioRequest(BaseModel):
    defect: dict
    changes: dict

@router.post("/whatif", summary="What-if сценарий для дефекта")
def run_scenario(req: ScenarioRequest):
    return what_if_scenario(req.defect, req.changes)

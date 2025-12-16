from fastapi import APIRouter
from economics.economics import total_cost, risk_penalty
from economics.repair_cost import repair_cost
# pipeline_ai/api/routes_economics.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from economics.economics import total_economic_impact
from reports.economics_report import generate_econ_pdf
from fastapi.responses import FileResponse


router = APIRouter()

@router.post("/economics/calc")
def calc_economics(data: dict):
    penalty = risk_penalty(data["risk"])
    cost = total_cost(
        data["repair_cost"],
        data["downtime_cost"],
        penalty
    )
    return {
        "total_cost": cost,
        "risk_penalty": penalty
    }
@router.post("/cost")
def estimate_cost(data: dict):
    cost = repair_cost(data["priority_score"])
    return {"estimated_cost": cost}



class EconRequest(BaseModel):
    base_cost: float = Field(..., description="Базовая стоимость ремонта (руб)")
    complexity_factor: float = Field(1.0, description="Сложность (1..3)")
    urgency_factor: float = Field(1.0, description="Срочность (1..2)")
    downtime_days: float = Field(0.0, description="Ожидаемые дни простоя")
    daily_loss: float = Field(0.0, description="Потеря в день (руб)")
    risk_level: float = Field(..., ge=0.0, le=1.0, description="Интегральный риск (0..1)")

@router.post("/estimate", summary="Оценка экономического воздействия")
def estimate(data: EconRequest):
    try:
        res = total_economic_impact(
            data.base_cost,
            data.complexity_factor,
            data.urgency_factor,
            data.downtime_days,
            data.daily_loss,
            data.risk_level
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
@router.post("/report", summary="PDF-отчет по экономике")
def economy_report(data: EconRequest):
    res = total_economic_impact(
        data.base_cost,
        data.complexity_factor,
        data.urgency_factor,
        data.downtime_days,
        data.daily_loss,
        data.risk_level
    )
    filename = generate_econ_pdf(data.dict(), res)
    return FileResponse(filename, media_type="application/pdf", filename="economics_report.pdf")
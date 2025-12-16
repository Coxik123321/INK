from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
from defects.defect_growth import defect_priority
from fuzzy.rules import evaluate_priority
from fuzzy.defuzzification import defuzzify
from reports.pdf_report import generate_pdf
from fastapi.responses import FileResponse


router = APIRouter()

# ===============================
# INPUT SCHEMA
# ===============================

class DefectRankRequest(BaseModel):
    risk: float = Field(..., ge=0, le=1, description="Интегральный риск (0–1)")
    remaining_life: float = Field(..., gt=0, description="Остаточный ресурс, лет")

# ===============================
# ENDPOINT
# ===============================

@router.post(
    "/rank",
    summary="Ранжирование дефекта",
    description="Возвращает приоритет ремонта дефекта"
)
def rank_defect(data: DefectRankRequest):
    try:
        score = defect_priority(
            data.risk,
            data.remaining_life
        )
        return {
            "priority_score": round(score, 3)
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
class DefectItem(BaseModel):
    risk: float = Field(..., ge=0, le=1)
    remaining_life: float = Field(..., gt=0)

@router.post("/rank/batch", summary="Групповое ранжирование дефектов")
def rank_defects_batch(defects: List[DefectItem]):
    results = []

    for d in defects:
        score = defect_priority(d.risk, d.remaining_life)
        results.append({
            "risk": d.risk,
            "remaining_life": d.remaining_life,
            "priority_score": round(score, 3)
        })

    return results



@router.post(
    "/rank/fuzzy",
    summary="Нечеткое ранжирование дефекта"
)
def rank_defect_fuzzy(data: DefectRankRequest):
    rules = evaluate_priority(
        data.risk,
        data.remaining_life
    )

    score = defuzzify(rules)

    return {
        "priority_score": round(score, 3),
        "rules_fired": [
            {
                "rule": r[0],
                "strength": round(r[1], 3),
                "normative": r[2]
            }
            for r in rules if r[1] > 0
        ]
    }
    


@router.post("/rank/fuzzy/report", summary="PDF-отчет по дефекту")
def rank_defect_fuzzy_report(data: DefectRankRequest):
    rules = evaluate_priority(data.risk, data.remaining_life)
    score = defuzzify(rules)

    rules_fired = [
        {
            "rule": r[0],
            "strength": round(r[1], 3),
            "normative": r[2]
        }
        for r in rules if r[1] > 0
    ]

    filename = generate_pdf(
        data={"risk": data.risk, "remaining_life": data.remaining_life},
        result=score,
        rules=rules_fired
    )

    return FileResponse(
        filename,
        media_type="application/pdf",
        filename="defect_analysis_report.pdf"
    )
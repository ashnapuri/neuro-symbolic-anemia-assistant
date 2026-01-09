from pydantic import BaseModel
from typing import Optional

class PatientData(BaseModel):
    hemoglobin: float
    ferritin: Optional[float]
    mcv: Optional[float]
    symptoms: list[str]

class DiagnosisResponse(BaseModel):
    diagnosis: str
    probability: float
    reasoning: dict
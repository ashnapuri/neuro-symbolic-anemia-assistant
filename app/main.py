from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
import joblib

from app.rules_engine import evaluate_rules

# -------------------------------------------------
# App setup
# -------------------------------------------------

app = FastAPI(
    title="Neuro-Symbolic Anemia Assistant",
    description="""
Clinical decision support prototype combining:
- Machine learning risk estimation
- Symbolic medical rules
- Transparent clinical explanations

⚠️ For educational and research use only.
Not intended for diagnosis or treatment decisions.
""",
    version="0.1.0"
)

templates = Jinja2Templates(directory="app/templates")

# -------------------------------------------------
# Load ML model
# -------------------------------------------------

model = joblib.load("baseline_anemia_model.joblib")

# -------------------------------------------------
# Data models
# -------------------------------------------------

class PatientInput(BaseModel):
    hemoglobin: float = Field(
        ...,
        example=10.5,
        description="Hemoglobin level in g/dL"
    )
    ferritin: float = Field(
        ...,
        example=12,
        description="Serum ferritin in ng/mL"
    )
    mcv: float = Field(
        ...,
        example=72,
        description="Mean corpuscular volume (fL)"
    )
    symptoms: list[str] = Field(
        default=[],
        example=["fatigue", "dizziness"],
        description="Patient-reported symptoms"
    )


class RuleExplanation(BaseModel):
    rule: str
    summary: str
    clinical_basis: str
    recommended_next_step: str
    weight: float


class PredictionOutput(BaseModel):
    ml_prediction: str = Field(example="anemia")
    ml_confidence: str = Field(example="high")
    rule_score: float = Field(example=0.8)
    rule_confidence: str = Field(example="high")
    overall_confidence: str = Field(example="high")
    explanations: list[RuleExplanation]

# -------------------------------------------------
# UI endpoint
# -------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

# -------------------------------------------------
# Prediction endpoint
# -------------------------------------------------

@app.post(
    "/predict",
    response_model=PredictionOutput,
    summary="Assess anemia likelihood",
    description="""
Evaluates anemia likelihood using a neuro-symbolic approach.

- ML estimates statistical risk
- Rules apply clinical thresholds
- Outputs are combined into an interpretable result
"""
)
def predict_anemia(data: PatientInput):

    # ---------- ML prediction ----------
    features = [[
        data.hemoglobin,
        data.ferritin,
        data.mcv,
        len(data.symptoms)
    ]]

    ml_proba = model.predict_proba(features)[0][1]

    if ml_proba > 0.8:
        ml_confidence = "high"
    elif ml_proba > 0.6:
        ml_confidence = "moderate"
    else:
        ml_confidence = "low"

    ml_label = "anemia" if ml_proba >= 0.5 else "no anemia"

    # ---------- Rule engine ----------
    rule_score, explanations = evaluate_rules(
        hemoglobin=data.hemoglobin,
        ferritin=data.ferritin,
        mcv=data.mcv,
        symptoms=data.symptoms
    )

    rule_conf_value = min(rule_score / 1.0, 1.0)

    if rule_conf_value > 0.7:
        rule_confidence = "high"
    elif rule_conf_value > 0.4:
        rule_confidence = "moderate"
    else:
        rule_confidence = "low"

    # ---------- Clinical triangulation ----------
    overall_confidence = "low"

    if ml_confidence == "high" and rule_confidence == "high":
        overall_confidence = "high"
    elif ml_confidence in ["moderate", "high"] and rule_confidence in ["moderate", "high"]:
        overall_confidence = "moderate"

    return PredictionOutput(
        ml_prediction=ml_label,
        ml_confidence=ml_confidence,
        rule_score=round(rule_score, 2),
        rule_confidence=rule_confidence,
        overall_confidence=overall_confidence,
        explanations=explanations
    )

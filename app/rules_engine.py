import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def load_rules():
    rules_path = BASE_DIR / "sample_rules.json"
    with open(rules_path) as f:
        return json.load(f)


RULES = load_rules()


def evaluate_rules(hemoglobin, ferritin, mcv, symptoms):
    score = 0.0
    explanations = []

    field_values = {
        "hemoglobin": hemoglobin,
        "ferritin": ferritin,
        "mcv": mcv
    }

    for rule in RULES.get("anemia_rules", []):
        condition = rule.get("condition", {})
        triggered = True

        for field, check in condition.items():
            value = field_values.get(field)
            if value is None:
                triggered = False
                break

            if "lt" in check and not value < check["lt"]:
                triggered = False
                break

        if triggered:
            score += rule.get("weight", 0.0)
            conclusion = rule.get("conclusion", {})
            explanations.append({
                "rule": rule.get("name"),
                "summary": conclusion.get("summary"),
                "clinical_basis": conclusion.get("clinical_basis"),
                "recommended_next_step": conclusion.get("recommended_next_step"),
                "weight": rule.get("weight")
            })

    return score, explanations

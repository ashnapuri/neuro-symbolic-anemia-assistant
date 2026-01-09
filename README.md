# Neuro-Symbolic Anemia Assistant

This project predicts anemia using a combination of:
- Machine Learning (Logistic Regression)
- Rule-based clinical reasoning

The system provides both a prediction and clear explanations.

---

## Features
- Predicts anemia using hemoglobin, ferritin, MCV, and symptoms
- Uses a trained ML model
- Provides explainable rule-based reasoning
- Built using FastAPI with Swagger UI

---

## Project Structure

project-folder/
│
├── app/
│   ├── main.py
│   ├── rules_engine.py
│   ├── sample_rules.json
│   ├── requirements.txt
|   ├── synthetic_data_generator.py
|   ├── train_baseline_model.py
|   ├── baseline_anemia_model.joblib
└── README.txt

---

## How to Run the Project

Run the following commands in order:

python synthetic_data_generator.py
python train_baseline_model.py
pip install -r app/requirements.txt
pip install jinja2
uvicorn app.main:app --reload


## Example Test Input
{
  "hemoglobin": 10.0,
  "ferritin": 8.0,
  "mcv": 72.0,
  "symptoms": ["fatigue", "pallor"]
}

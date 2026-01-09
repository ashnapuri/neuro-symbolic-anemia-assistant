# Neuro-Symbolic Anemia Assistant

This project predicts anemia using a combination of:
- Machine Learning (Logistic Regression)
- Rule-based clinical reasoning

## Features
- Predicts anemia using hemoglobin, ferritin, MCV, and symptoms
- Provides rule-based explanations
- Uses FastAPI with Swagger UI

## How to Run the Project

1. Clone the repository
git clone <your-repo-link>

3. Install dependencies
pip install -r app/requirements.txt

4. Run the FastAPI server
uvicorn main:app --reload

5. Open SwaggerUI
http://127.0.0.1:8000/docs

6. Open UI Interface
 http://127.0.0.1:8000/

## Example Test Input
{
  "hemoglobin": 10.0,
  "ferritin": 8.0,
  "mcv": 72.0,
  "symptoms": ["fatigue", "pallor"]
}

import random
import pandas as pd

N = 500

symptom_pool = [
    "fatigue", "pale skin", "dizziness", "shortness of breath",
    "headache", "cold hands", "chest pain"
]


def generate_case():
    #Random hemoglobin
    hb = round(random.uniform(7.5, 16.0), 1)

    # Ferritin depends partly on Hb
    if hb < 12:
        ferritin = round(random.uniform(5, 40), 1)
    else:
        ferritin = round(random.uniform(20, 150), 1)

    # MCV: microcytic vs normal vs macrocytic
    if ferritin < 25:
        mcv = round(random.uniform(60, 78), 1) # iron deficiency pattern
    else:
        mcv = round(random.uniform(78, 100), 1)

    # Symptoms weighted toward low Hb
    num_symptoms = 1 if hb > 13 else random.randint(2, 5)
    symptoms = random.sample(symptom_pool, num_symptoms)

    # Label
    anemia_label = 1 if hb < 12 else 0

    return {
        "hemoglobin": hb,
        "ferritin": ferritin,
        "mcv": mcv,
        "symptoms": ",".join(symptoms),
        "anemia": anemia_label
    }

def generate_dataset(n=N):
    records = [generate_case() for _ in range(n)]
    df = pd.DataFrame(records)
    df.to_csv("synthetic_anemia_data.csv", index=False)
    print("Dataset saved as synthetic_anemia_data.csv with", len(df), "rows.")

if __name__ == "__main__":
    generate_dataset()
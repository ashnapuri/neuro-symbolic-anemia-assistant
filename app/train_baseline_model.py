import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib

# Load dataset generated earlier
df = pd.read_csv("synthetic_anemia_data.csv")

# Preprocess
# Convert symptoms into simple feature: count of symptoms
df["symptom_count"] = df["symptoms"].apply(lambda x: len(str(x).split(",")))

X = df[["hemoglobin", "ferritin", "mcv", "symptom_count"]]
y = df["anemia"]

# Split
tX, vX, ty, vy = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LogisticRegression(max_iter=500)
model.fit(tX, ty)

# Evaluate
pred = model.predict(vX)
print(classification_report(vy, pred))

# Save the model
joblib.dump(model, "baseline_anemia_model.joblib")
print("Model saved as baseline_anemia_model.joblib")
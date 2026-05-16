import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# ── Load Dataset ─────────────────────────────────────
# Replace with your dataset file name
df = pd.read_csv("water_quality.csv")

# ── Preview Dataset ──────────────────────────────────
print(df.head())

# ── Features and Target ──────────────────────────────
# Example columns:
# pH, Hardness, Solids, Chloramines, Sulfate, Conductivity, Organic_carbon, Trihalomethanes, Turbidity, Potability

X = df.drop("Potability", axis=1)
y = df["Potability"]

# ── Train Test Split ─────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

# ── Model Training ───────────────────────────────────
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# ── Prediction ───────────────────────────────────────
y_pred = model.predict(X_test)

# ── Accuracy ─────────────────────────────────────────
accuracy = accuracy_score(y_test, y_pred)

print(f"\nModel Accuracy: {accuracy * 100:.2f}%")

# ── Save Model ───────────────────────────────────────
joblib.dump(model, "water_quality_model.pkl")

print("\n✅ Model saved as water_quality_model.pkl")
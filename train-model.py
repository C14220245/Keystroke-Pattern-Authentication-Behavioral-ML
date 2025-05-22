#AI Sys. Ketikan sendiri/One CLass -> IsoFor, OC SVM, LOF. BinSVM perlu >=2 org
#Cek ExIsoFor

import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
import os

USERNAME = input("Enter the username: ").strip()
CSV_PATH = f"user_data/{USERNAME}_behav.csv"
MODEL_PATH = "model.pkl"


df = pd.read_csv(CSV_PATH)
X = df.drop(columns=["label"])


scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


model = IsolationForest(
    n_estimators=500, # Tree setting(?) semakin tinggi = semakin banyak decision proC = semakin akurat. Default 100
    contamination=0.1,  # Labelling anomali data. semakin kecil = data semakin bersih. Perlu fine-tune, try from 0.1
    #contamination=0.0001,  # Data bersih, gunakan untuk tes otomatik (macro key)
    random_state=123 # Random seed. Bebas
)

model.fit(X_scaled)

# Save model and scaler
joblib.dump(model, MODEL_PATH)
joblib.dump(scaler, "scaler.pkl")

print(f"✓ Model saved to {MODEL_PATH}")
print("✓ Scaler saved to scaler.pkl")

#Scoring (debug)
#scores = model.decision_function(X_scaled)
print("\nScoring (ambil modus):")
#print(scores)
print(model.decision_function(X_scaled))

"""
knngenerator.py

This script loads a labeled dataset, balances class distribution using SMOTE,
trains a K-Nearest Neighbours (KNN) classifier, and saves the model for use
in the detection module. It also outputs a classification report and confusion matrix.

Outputs:
- Trained model: ownmodel/knn_model.pkl
- Classification report: classification_report.csv
- Confusion matrix: displayed with seaborn
"""

import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

# ---------- CONFIGURATION ----------
DATASET_PATH = "DBDoS2025.csv"
MODEL_DIR = "ownmodel"
MODEL_PATH = os.path.join("../DoSDetector/models",MODEL_DIR, "knn_model.pkl")
REPORT_PATH = "classification_report.csv"
K_NEIGHBORS = 5

LABEL_MAP = {
    "benigno": 0,
    "hulk": 1,
    "synflood": 2,
    "udpflood": 3,
    "postflood": 4
}
TARGET_NAMES = list(LABEL_MAP.keys())

# ---------- LOAD DATA ----------
print("[INFO] Loading dataset...")
df = pd.read_csv(DATASET_PATH)

if "label" not in df.columns:
    raise ValueError("Dataset must include a 'label' column.")

# Normalize label casing and map to integers
df["label"] = df["label"].str.lower().map(LABEL_MAP)
if df["label"].isnull().any():
    raise ValueError("Unrecognized labels found. Check LABEL_MAP and dataset contents.")

X = df.drop("label", axis=1)
y = df["label"]
print(f"[INFO] Original class distribution: {y.value_counts().to_dict()}")

# ---------- APPLY SMOTE ----------
print("[INFO] Applying SMOTE to balance class distribution...")
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)
print(f"[INFO] Resampled class distribution: {pd.Series(y_resampled).value_counts().to_dict()}")

# ---------- TRAINING ----------
print(f"[INFO] Training KNN model with k={K_NEIGHBORS}...")
X_train, X_test, y_train, y_test = train_test_split(
    X_resampled, y_resampled, test_size=0.3, random_state=42, stratify=y_resampled
)

knn = KNeighborsClassifier(n_neighbors=K_NEIGHBORS, metric='euclidean')
knn.fit(X_train, y_train)
y_pred = knn.predict(X_test)

# ---------- REPORT ----------
print("[INFO] Generating classification report...")
report = classification_report(y_test, y_pred, target_names=TARGET_NAMES, output_dict=True)
report_df = pd.DataFrame(report).transpose()
print(report_df.round(4))
report_df.to_csv(REPORT_PATH)
print(f"[INFO] Report saved to {REPORT_PATH}")

# ---------- CONFUSION MATRIX ----------
print("[INFO] Displaying confusion matrix...")
conf_matrix = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues",
            xticklabels=TARGET_NAMES, yticklabels=TARGET_NAMES)
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.tight_layout()
plt.show()

# ---------- SAVE MODEL ----------
print(f"[INFO] Saving model to {MODEL_PATH}...")
os.makedirs(MODEL_DIR, exist_ok=True)
joblib.dump(knn, MODEL_PATH)
print("[SUCCESS] Model trained and saved.")

# ---------- CROSS-VALIDATION (Optional) ----------
scores = cross_val_score(knn, X_resampled, y_resampled, cv=5)
print(f"[INFO] Cross-validated accuracy: {scores.mean():.4f}")

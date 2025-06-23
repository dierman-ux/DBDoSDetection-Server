"""
RandomForestClassifiergenerator.py

This script loads a labeled dataset, balances class distribution using SMOTE,
trains a Random Forest classifier, and saves the model for use
in the detection module. It also outputs a classification report and confusion matrix.

Outputs:
- Trained model: ownmodel/model.pkl
- Classification report: classification_report.csv
- Confusion matrix: displayed with seaborn
"""

import os
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier

from sklearn.preprocessing import StandardScaler, label_binarize
from sklearn.decomposition import PCA
from sklearn.metrics import roc_curve, auc

# ---------- CONFIGURATION ----------
DATASET_PATH = "DBDoS2025.csv"
MODEL_PATH = os.path.join("../DoSDetector/models/ownmodel", "model.pkl")
REPORT_PATH = os.path.join("./", "classification_report_random_forest.csv")
EXCEL_PATH = "../DoSDetector/models/model_stats.xlsx"

LABEL_MAP = {
    "benigno": 0,
    "hulk": 1,
    "synflood": 2,
    "udpflood": 3,
    "postflood": 4
}
TARGET_NAMES = list(LABEL_MAP.keys())

print("[INFO] Loading dataset...")
df = pd.read_csv(DATASET_PATH)
df["label"] = df["label"].str.lower().map(LABEL_MAP)

X = df.drop("label", axis=1)
y = df["label"]

print("[INFO] Applying SMOTE...")
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

X_train, X_test, y_train, y_test = train_test_split(
    X_resampled, y_resampled, test_size=0.3, random_state=42, stratify=y_resampled
)

# ---------- MODEL ----------
print(f"[INFO] Training RandomForestClassifier...")
start_train = time.time()
model = RandomForestClassifier()
model.fit(X_train, y_train)
end_train = time.time()

# ---------- PREDICTION ----------
print("[INFO] Predicting...")
start_pred = time.time()
y_pred = model.predict(X_test)
end_pred = time.time()

# ---------- METRICS ----------
report = classification_report(y_test, y_pred, target_names=TARGET_NAMES, output_dict=True)
report_df = pd.DataFrame(report).transpose()
report_df.to_csv(REPORT_PATH)

conf_matrix = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues",
            xticklabels=TARGET_NAMES, yticklabels=TARGET_NAMES)
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix - RandomForestClassifier")
plt.tight_layout()
plt.savefig(f"confusion_matrix_random_forest.png")
plt.close()

# ---------- ROC CURVES ----------
print("[INFO] Generating ROC curves...")

N_CLASSES = len(LABEL_MAP)

y_test_bin = label_binarize(y_test, classes=range(N_CLASSES))
y_score = model.predict_proba(X_test)

plt.figure(figsize=(8, 6))
for i in range(N_CLASSES):
    fpr, tpr, _ = roc_curve(y_test_bin[:, i], y_score[:, i])
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr, tpr, label=f'{TARGET_NAMES[i]} (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], 'k--')
plt.title("ROC Curve - Decision Tree")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig("roc_curve_decision_tree.png")
plt.close()

# ---------- PCA PLOT ----------
print("[INFO] Generating PCA scatter plot...")
X_scaled = StandardScaler().fit_transform(X_resampled)
pca = PCA(n_components=2)
pca_result = pca.fit_transform(X_scaled)
df_pca = pd.DataFrame({
    'PC1': pca_result[:, 0],
    'PC2': pca_result[:, 1],
    'Label': [TARGET_NAMES[i] for i in y_resampled]
})
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df_pca, x='PC1', y='PC2', hue='Label', palette='tab10', alpha=0.7)
plt.title("PCA of Network Traffic - Resampled")
plt.tight_layout()
plt.savefig("pca_plot_decision_tree.png")
plt.close()


# ---------- SAVE MODEL ----------
print(f"[INFO] Saving model in: {MODEL_PATH}")
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
joblib.dump(model, MODEL_PATH)

# ---------- STATS ----------
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='macro', zero_division=0)
recall = recall_score(y_test, y_pred, average='macro', zero_division=0)
f1 = f1_score(y_test, y_pred, average='macro', zero_division=0)
pred_time = (end_pred - start_pred)
train_time = (end_train - start_train)
avg_pred_time = pred_time / len(y_test)
cv_scores = cross_val_score(model, X_resampled, y_resampled, cv=5)

row = {
    "Modelo": "RandomForestClassifier",
    "Accuracy": accuracy,
    "Precision": precision,
    "Recall": recall,
    "F1-Score": f1,
    "Tiempo entrenamiento (s)": train_time,
    "Tiempo total inferencia (s)": pred_time,
    "Tiempo medio por predicción (s)": avg_pred_time,
    "Accuracy Cross-Val (media)": np.mean(cv_scores),
    "Cross-Val Std": np.std(cv_scores)
}

print(f"[INFO] Model Stats: {row}")

if os.path.exists(EXCEL_PATH):
    df_stats = pd.read_excel(EXCEL_PATH)
    df_stats = pd.concat([df_stats, pd.DataFrame([row])], ignore_index=True)
else:
    df_stats = pd.DataFrame([row])

df_stats.to_excel(EXCEL_PATH, index=False)
print("[SUCCESS] Model trained y statistics saved.")

import pandas as pd
from detection import AttackDetector
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import time

# ---------- CONFIGURATION ----------
CSV_DATASET_PATH = "dataset.csv"     # Parsed and labeled dataset

# ---------- LOAD DETECTION MODEL ----------
print("[INFO] Loading detection model...")
model = AttackDetector()

# ---------- LOAD DATASET ----------
print("[INFO] Loading parsed dataset...")
df = pd.read_csv(CSV_DATASET_PATH)

# ---------- CLEAN LABELS ----------
label_map = {
    "BENIGN": 0,
    "HULK": 1,
    "SYNFLOOD": 2,
    "UDPFLOOD": 3,
    "POSTFLOOD": 4
}
df["label"] = df["label"].str.upper().str.strip()
df["label"] = df["label"].replace({"BENIGNO": "BENIGN"})
df["Label"] = df["label"].map(label_map)

# ---------- PREDICTIONS WITH LATENCY ----------
print("[INFO] Running predictions with latency measurement...")
def predict_with_latency(row):
    features = row.drop(["label", "Label"]).to_dict()
    start = time.perf_counter()
    prediction = model.predict(features)
    end = time.perf_counter()
    latency_ms = (end - start) * 1000
    return label_map.get(prediction, -1), latency_ms

results = df.apply(lambda row: pd.Series(predict_with_latency(row), index=["Predicted", "Latency_ms"]), axis=1)
df = pd.concat([df, results], axis=1)

# ---------- CLASSIFICATION REPORT ----------
print("[INFO] Generating classification report...")
report = classification_report(df["Label"], df["Predicted"], target_names=label_map.keys(), output_dict=True)
report_df = pd.DataFrame(report).transpose()
print(report_df)

# ---------- LATENCY STATISTICS ----------
print("[INFO] Latency statistics (ms):")
print(df["Latency_ms"].describe())
df["Latency_ms"].to_csv("latency_values.csv", index=False)

# ---------- CONFUSION MATRIX ----------
conf_matrix = confusion_matrix(df["Label"], df["Predicted"])
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues",
            xticklabels=label_map.keys(), yticklabels=label_map.keys())
plt.xlabel("Predicted")
plt.ylabel("True Label")
plt.title("Confusion Matrix")
plt.tight_layout()
plt.savefig("confusion_matrix.png")
plt.show()

# ---------- SAVE REPORT ----------
report_df.to_csv("evaluation_report.csv")
print("[INFO] Classification report saved as 'evaluation_report.csv'")

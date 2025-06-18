import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load and clean latency data
df = pd.read_csv("latency_values.csv")

# Ensure the column exists and clean it
df["Latency_ms"] = pd.to_numeric(df["Latency_ms"], errors="coerce")
df = df[np.isfinite(df["Latency_ms"])]  # Remove NaN, inf

# Optional: filter out extreme outliers for plot clarity
df_capped = df[df["Latency_ms"] < 500]

# Set seaborn style
sns.set(style="whitegrid", font_scale=1.2)

# ----------- FIGURE 4.X – KDE Plot -----------
plt.figure(figsize=(6, 4))
sns.kdeplot(df_capped["Latency_ms"], fill=True, color="#4682B4", linewidth=2)
plt.title("Inference latency density (latencies < 500 ms)")
plt.xlabel("Latency (ms)")
plt.ylabel("Density")
plt.tight_layout()
plt.savefig("figure_4X_kde_latency.png", dpi=300)

# ----------- FIGURE 4.Y – Violin Plot -----------
plt.figure(figsize=(6, 3.5))
sns.violinplot(x=df["Latency_ms"], color="#F08080", inner="box", cut=0, linewidth=1)
plt.title("Inference latency distribution (with outliers)")
plt.xlabel("Latency (ms)")
plt.tight_layout()
plt.savefig("figure_4Y_violin_latency.png", dpi=300)

print("✅ Figures saved: figure_4X_kde_latency.png and figure_4Y_violin_latency.png")

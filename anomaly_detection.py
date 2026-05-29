"""
Retail Sales Anomaly Detection
Detects unusual sales patterns using Z-score and rolling statistics.
Author: Sahithi Vogeti
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# ---------- 1. Generate sample data (replace with real CSV in production) ----------
np.random.seed(42)
dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq="D")
base_sales = 5000 + np.sin(np.arange(len(dates)) * 2 * np.pi / 7) * 800  # weekly seasonality
noise = np.random.normal(0, 300, len(dates))
sales = base_sales + noise

# Inject anomalies
anomaly_idx = [45, 120, 200, 280, 330]
for idx in anomaly_idx:
    sales[idx] *= np.random.choice([0.3, 2.5])  # large drop or spike

df = pd.DataFrame({"date": dates, "sales": sales})

# ---------- 2. Rolling stats + Z-score ----------
window = 14
df["rolling_mean"] = df["sales"].rolling(window=window, center=True).mean()
df["rolling_std"] = df["sales"].rolling(window=window, center=True).std()
df["z_score"] = (df["sales"] - df["rolling_mean"]) / df["rolling_std"]

# ---------- 3. Flag anomalies ----------
threshold = 2.5
df["is_anomaly"] = df["z_score"].abs() > threshold

anomalies = df[df["is_anomaly"]]
print(f"Detected {len(anomalies)} anomalies out of {len(df)} days")
print(anomalies[["date", "sales", "z_score"]].to_string(index=False))

# ---------- 4. Visualize ----------
plt.figure(figsize=(14, 6))
plt.plot(df["date"], df["sales"], label="Daily Sales", alpha=0.6)
plt.plot(df["date"], df["rolling_mean"], label=f"{window}-Day Rolling Mean", color="orange")
plt.scatter(anomalies["date"], anomalies["sales"], color="red", s=80, label="Anomaly", zorder=5)
plt.title("Retail Sales Anomaly Detection (Z-score Method)")
plt.xlabel("Date")
plt.ylabel("Sales ($)")
plt.legend()
plt.tight_layout()
plt.savefig("anomaly_detection_output.png", dpi=120)
plt.show()

# ---------- 5. Export flagged anomalies for stakeholder review ----------
anomalies.to_csv("flagged_anomalies.csv", index=False)
print("\nFlagged anomalies exported to flagged_anomalies.csv")

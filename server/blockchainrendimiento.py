import time
import pandas as pd
from blacklist import log_attack

# ---------- CONFIGURATION ----------
NUM_TESTS = 5
IP_BASE = "192.168.1."
ATTACK_TYPE = "DoS Test"

latencies = []
tx_ids = []

print("[INFO] Starting blockchain logging latency measurement...")

for i in range(NUM_TESTS):
    ip = IP_BASE + str(100 + i)

    print(f"[INFO] Sending simulated attack from IP {ip}...")
    start = time.perf_counter()
    result = log_attack(ip, ATTACK_TYPE)
    end = time.perf_counter()

    elapsed = end - start
    latencies.append(elapsed)
    tx_ids.append(result.get("tx_id") if result else "ERROR")

    print(f"[OK] Latency: {elapsed:.3f} s - TxID: {tx_ids[-1]}")

# ---------- EXPORT RESULTS ----------
df = pd.DataFrame({
    "IP": [IP_BASE + str(100 + i) for i in range(NUM_TESTS)],
    "Latency_s": latencies,
    "TxID": tx_ids
})

df.to_csv("blockchain_latency.csv", index=False)
print("\n[INFO] Results saved to 'blockchain_latency.csv'")
print("\nLatency summary statistics:\n")
print(df["Latency_s"].describe())

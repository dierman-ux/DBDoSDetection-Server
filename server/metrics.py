"""
metrics.py

Functions to calculate network traffic metrics from timestamps and byte records.

Features:
- Computes inter-arrival times (IAT) and idle times from request timestamps.
- Calculates statistical features such as total, max, mean, min, and standard deviation.
- Supports incremental data collection per IP address.
- Provides output compatible with detection model feature input.
- Handles cases with insufficient data gracefully.

Author: Rafael Malla Martinez
Date: 2025-06-06
"""


from statistics import mean, stdev
import time
from logger import setup_logger

def calcular_metricas(ip, registro):
    """
    Calculate network traffic metrics for a given IP address.

    Args:
        ip (str): The IP address to calculate metrics for.
        registro (dict): A dictionary containing timestamps and byte counts per IP.

    Returns:
        dict: A dictionary with computed features used for traffic classification.
    """

    # Retrieve the list of timestamps and byte sizes for the IP
    t = registro[ip]["timestamps"]
    sizes = registro[ip]["bytes"]

    # If there are fewer than 2 timestamps, not enough data to compute metrics
    if len(t) < 2:
        return {"message": "Waiting for more data..."}

    # Calculate inter-arrival times (IAT) between consecutive packets
    iats = [t[i+1] - t[i] for i in range(len(t)-1)]

    # Define idle times as IATs longer than 1 second (threshold for inactivity)
    idle_times = [iat for iat in iats if iat > 1.0]

    # Compute metrics and round to 4 decimal places
    resultado = {
        "Fwd IAT Total": round(sum(iats), 4),               # Total forward inter-arrival time
        "Flow Duration": round(t[-1] - t[0], 4),            # Duration of the flow
        "Idle Max": round(max(idle_times), 4) if idle_times else 0.0,  # Maximum idle time
        "Fwd IAT Max": round(max(iats), 4),                  # Maximum forward IAT
        "Flow IAT Max": round(max(iats), 4),                 # Maximum flow IAT (same as forward here)
        "Idle Mean": round(mean(idle_times), 4) if idle_times else 0.0,  # Mean idle time
        "Idle Min": round(min(idle_times), 4) if idle_times else 0.0,   # Minimum idle time
        "Bwd IAT Total": round(sum(iats), 4),                # Simulated backward IAT total (placeholder)
        "Bwd IAT Max": round(max(iats), 4),                   # Simulated backward IAT max (placeholder)
        "Fwd IAT Std": round(stdev(iats), 4) if len(iats) > 1 else 0.0,  # Std deviation of forward IAT
        "Flow IAT Std": round(stdev(iats), 4) if len(iats) > 1 else 0.0, # Std deviation of flow IAT
        "Fwd IAT Mean": round(mean(iats), 4),                 # Mean forward IAT
        "Bwd IAT Std": round(stdev(iats), 4) if len(iats) > 1 else 0.0,  # Simulated backward IAT std dev
        "Bwd IAT Mean": round(mean(iats), 4),                  # Simulated backward IAT mean
    }

    return resultado

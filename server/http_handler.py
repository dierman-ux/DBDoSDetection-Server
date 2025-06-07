"""
http_handler.py

HTTP request handler for traffic detection and IP blacklist management.

Features:
- Handles GET requests, collects metrics per IP.
- Uses DetectionEngine to classify traffic type (BENIGN or attack).
- Maintains a local blacklist with warning counts before blocking IPs.
- Registers detected attacks on a blockchain via an external Node.js script.
- Thread-safe management of shared data structures.
- Logs events and errors for auditing and debugging.

Author: Rafael Malla Martinez
Date: 2025-06-06
"""



from http.server import BaseHTTPRequestHandler
import time
import json
import pandas as pd
import requests
from metrics import calcular_metricas
from logger import setup_logger
from detection import DetectionEngine  # Import the detection engine class
import subprocess
import threading

# Local in-memory blacklist to block IP addresses
blacklist_local = {} # Dictionary to store blacklisted IPs and their warning counts
blacklist_lock = threading.Lock()  # Lock to synchronize access to blacklist

# Track warnings per IP before blocking
warning_counts = {}
warning_lock = threading.Lock()  # Lock for warning counts
MAX_WARNINGS = 3  # Number of warnings before blocking an IP

# Dictionary to store connection info per IP
registro = {}
registro_lock = threading.Lock()  # Lock for access to registro dictionary

# Initialize logger using custom setup
logger = setup_logger()

# Create a global instance of DetectionEngine to predict traffic type
detection_engine = DetectionEngine(base_dir='.')  # Load model and scaler from current directory

class MyHandler(BaseHTTPRequestHandler):
    registrado = False  # Class variable, tracks if IP has been registered as blocked

    def do_GET(self):
        """
        Handle GET requests from clients:
        - Extract client IP and current timestamp.
        - Reject request if IP is blacklisted.
        - Update tracking info in registro dictionary.
        - Calculate traffic metrics.
        - Use DetectionEngine to predict if traffic is benign or malicious.
        - Manage warnings and blocking logic.
        - Return JSON response with metrics or errors.
        """
        ip = self.client_address[0]
        ahora = time.time()

        # Reject immediately if IP is blacklisted locally
        with blacklist_lock:
            if ip in blacklist_local and blacklist_local[ip].get("blacklisted", False):
                self.send_response(403)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                response = {"error": "Access denied: IP in local blacklist"}
                self.wfile.write(json.dumps(response).encode())
                logger.warning(f"[BLACKLISTED] Connection rejected from {ip}")
                return

        # Initialize registro entry for new IP
        with registro_lock:
            if ip not in registro:
                registro[ip] = {
                    "timestamps": [],
                    "bytes": [],
                    "last_time": ahora,
                    "registrado": False
                }
            registro[ip]["timestamps"].append(ahora)
            registro[ip]["bytes"].append(int(self.headers.get('Content-Length', 0)))
            registro[ip]["last_time"] = ahora


        # Append current timestamp and request size to registro for the IP
        registro[ip]["timestamps"].append(ahora)
        registro[ip]["bytes"].append(int(self.headers.get('Content-Length', 0)))
        registro[ip]["last_time"] = ahora

        registrado_antes = registro[ip]["registrado"]

        # Calculate traffic metrics using custom function
        metricas = calcular_metricas(ip, registro)

        # If metrics calculation did not return an error message, continue
        if "message" not in metricas:
            try:
                # Prepare DataFrame with features expected by the detection engine
                df = pd.DataFrame([[metricas[col] for col in detection_engine.feature_names]],
                                  columns=detection_engine.feature_names)

                # Predict traffic type (e.g., BENIGN or attack type)
                tipo_trafico = detection_engine.predecir(df)
                metricas["Predicted Traffic Type"] = tipo_trafico

                # Log prediction info
                logger.info(f"Prediction - IP: {ip}, Time: {ahora}, Prediction: {tipo_trafico}, Metrics: {metricas}")

                # Handle detected malicious traffic
                if tipo_trafico != "BENIGN":
                    with blacklist_lock:
                        info = blacklist_local.get(ip, {"warnings": 0, "blacklisted": False})
                        info["warnings"] += 1  # Increase warnings count

                        # If max warnings reached, blacklist IP and register it
                        if info["warnings"] >= MAX_WARNINGS:
                            info["blacklisted"] = True
                            registro[ip]["registrado"] = True
                            self.enviar_a_blockchain(ip, tipo_trafico)  # Log attack on blockchain
                            print(f"🚨 IP {ip} blocked and registered after {info['warnings']} warnings.")
                        else:
                            print(f"⚠️ IP {ip} - Warning {info['warnings']}/{MAX_WARNINGS}")

                        blacklist_local[ip] = info  # Update blacklist info
                else:
                    # If traffic is benign, reduce warnings count if present
                    with blacklist_lock:
                        if ip in blacklist_local and not blacklist_local[ip]["blacklisted"]:
                            blacklist_local[ip]["warnings"] = max(0, blacklist_local[ip]["warnings"] - 1)

            except Exception as e:
                # Log errors during prediction
                logger.error(f"Error during prediction: {str(e)}")
                metricas = {"error": str(e)}

        # Send back the metrics or error as JSON response
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(metricas, indent=2).encode())

    def enviar_a_blockchain(self, ip, tipo):
        """
        Send the detected attack info to the blockchain:
        - Run a Node.js script with IP and attack type as arguments.
        - Parse output for transaction ID (Tx Id).
        - Log success or failure accordingly.
        """
        try:
            print(f"Sending attack to blockchain - IP: {ip}, Type: {tipo}")
            result = subprocess.run(
                ["node", "./blacklist/sendAttackLog.cjs", ip, tipo],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                output = result.stdout.strip()
                tx_id = None
                for line in output.splitlines():
                    if line.startswith("Tx Id:"):
                        tx_id = line.split("Tx Id:")[1].strip()
                        break

                if tx_id:
                    print(f"🚨 Attack registered on blockchain with Tx ID: {tx_id}")
                    logger.info(f"🚨 Attack registered on blockchain with Tx ID: {tx_id}")
                else:
                    print("⚠️ Stored in DoSAttackRegistry but Tx ID missing.")
                    logger.warning("Tx ID not found in Node.js script output.")
            else:
                logger.error(f"Node.js script error: {result.stderr.strip()}")
        except Exception as e:
            logger.error(f"Failed to execute Node.js script: {str(e)}")

    def log_message(self, format, *args):
        # Override to disable default HTTP server logging
        return

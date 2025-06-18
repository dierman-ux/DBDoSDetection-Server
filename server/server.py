import socket
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import json
import signal
import threading
import subprocess
from blacklist import get_blacklist, log_attack, force_update, fetch_blacklist, clear_blacklist, delete_attack
import time
from urllib.parse import urlparse
import os


# Variable global para el intervalo y control del evento
auto_update_interval = 10
auto_update_event = threading.Event()
stop_event = threading.Event()

httpd=None

# Ruta absoluta al HTML frontend
frontend_path = os.path.join(os.path.dirname(__file__), "frontend", "frontend.html")
with open(frontend_path, "r", encoding="utf-8") as f:
    FRONTEND_HTML = f.read()

def periodic_update():
    while not stop_event.is_set():
        start = time.time()

        print(f"[INFO] Running periodic blacklist update...")
        try:
            fetch_blacklist()
        except Exception as e:
            print(f"[ERROR] Error updating blacklist: {e}")

        print(f"[INFO] Waiting {auto_update_interval:.2f}s until next update.")
        if stop_event.wait(timeout=auto_update_interval):
            break

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

class SimpleRESTHandler(BaseHTTPRequestHandler):
    blacklist_ips = set()

    def load_blacklist(self):
        attacks = get_blacklist()
        self.blacklist_ips = set(attack['ip'] for attack in attacks if 'ip' in attack)

    def client_ip_blocked(self):
        client_ip = self.client_address[0]
        return client_ip in self.blacklist_ips
    
    def do_GET(self):
        self.load_blacklist()

        if self.client_ip_blocked():
            self.send_response(403)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Access denied: IP blocked"}).encode("utf-8"))
            return
        if self.path == "/blacklist":
            attacks = get_blacklist()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {
                "status": "Blacklist fetched",
                "attacks": attacks
            }
            self.wfile.write(json.dumps(response).encode("utf-8"))
            return

        if self.path == "/":
            # Main page with buttons and JS to interact with the blacklist
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            html = FRONTEND_HTML
            
            self.wfile.write(html.encode("utf-8"))
            return
        
        self.send_response(404)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode("utf-8"))

    def do_POST(self):
        self.load_blacklist()
        global auto_update_interval

        if self.client_ip_blocked():
            self.send_response(403)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Access denied: IP blocked"}).encode("utf-8"))
            return

        if self.path == "/blacklist/set-interval":
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self.send_error(400, "No data received")
                return
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                data = json.loads(body)
                new_interval = int(data.get("interval", 0))
                if new_interval < 1:
                    raise ValueError("Interval must be >= 1")
            except Exception as e:
                self.send_error(400, f"Invalid data: {e}")
                return

            auto_update_interval = new_interval
            print(f"[INFO] Auto update interval set to {auto_update_interval} seconds")
            auto_update_event.set()  # Despertar hilo para que tome el nuevo intervalo

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {"status": "success", "new_interval": auto_update_interval}
            self.wfile.write(json.dumps(response).encode('utf-8'))
            return

        elif self.path == "/blacklist/update":
            force_update()
            attacks = get_blacklist()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {
                "status": "Blacklist updated",
                "attacks": attacks
            }
            self.wfile.write(json.dumps(response).encode("utf-8"))
            return

        elif self.path == "/blacklist/clear":
            clear_blacklist()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "Blacklist cleared"}).encode("utf-8"))
            return

        elif self.path == "/blacklist/log":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body)
                ip = data.get("ip")
                attack_type = data.get("attack_type")
                if not ip or not attack_type:
                    raise ValueError("Missing ip or attack_type")
            except Exception:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid JSON or missing fields"}).encode("utf-8"))
                return

            log_attack(ip, attack_type)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": f"Attack from IP {ip} logged"}).encode("utf-8"))
            return
        elif self.path == "/blacklist/addTestAttacks":
            add_test_attacks()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Test attacks added successfully"}).encode("utf-8"))
        else:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode("utf-8"))
    from http.server import BaseHTTPRequestHandler

    def do_DELETE(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')
        # Esperamos algo como ['blacklist', 'delete', '5']
        if len(path_parts) == 3 and path_parts[0] == 'blacklist' and path_parts[1] == 'delete':
            try:
                index = int(path_parts[2])
            except ValueError:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Index must be an integer"}).encode("utf-8"))
                return
            
            success = delete_attack(index)
            if success:
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"message": f"Attack at index {index} deleted"}).encode("utf-8"))
            else:
                self.send_response(404)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": f"No attack found at index {index}"}).encode("utf-8"))
        else:
            self.send_error(404, "Path not found")

    # Opcionalmente también implementa do_GET, do_POST, etc.

def add_test_attacks():
    test_attacks = [
        ("1.1.1.1", "DoS Test"),
        ("2.2.2.2", "DoS Test"),
        ("3.3.3.3", "DoS Test"),
        ("4.4.4.4", "DoS Test"),
        ("5.5.5.5", "DoS Test"),
    ]
    for ip, attack_type in test_attacks:
        log_attack(ip, attack_type)

def signal_handler(sig, frame):
    print("\n[INFO] Shutting down server...")
    stop_event.set()
    auto_update_event.set()  
    if httpd:
        httpd.shutdown()
        httpd.server_close()
    print("[INFO] Server shutdown complete.")
    exit(0)


def main():
    ip = get_local_ip()
    port = 8080
    server_address = (ip, port)
    httpd = ThreadedHTTPServer(server_address, SimpleRESTHandler)

    # Lanzar hilo que actualiza blacklist
    update_thread = threading.Thread(target=periodic_update, daemon=True)
    

    # Capturar Ctrl+C para parada limpia
    signal.signal(signal.SIGINT, signal_handler)

    print(f"Updating blacklist & Starting HTTP server at http://{ip}:{port}")
    update_thread.start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped by user")

    # Esperar a que el hilo de actualización termine
    stop_event.set()
    auto_update_event.set()
    update_thread.join(timeout=5)
    print("[INFO] Server and update thread stopped cleanly.")

    


if __name__ == "__main__":
    main()

import subprocess
import json
import threading
import time
import re
import os

_blacklist = []
_blacklist_lock = threading.Lock()

def _run_node_script(script: str, args: list = []):
    script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "blacklist"))
    script_path = os.path.join(script_dir, script)

    ext = os.path.splitext(script_path)[1]

    if ext == '.ts':
        cmd = ['ts-node', script_path]
    elif ext in ['.js', '.cjs']:
        cmd = ['node', script_path]
    else:
        print(f"[ERROR] Unsupported script extension for {script}")
        return None

    try:
        result = subprocess.run(
            cmd + args,
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"[ERROR] Script {script} failed: {result.stderr.strip()}")
            return None
    except Exception as e:
        print(f"[EXCEPTION] Running {script}: {e}")
        return None

def _parse_total_attacks(output: str):
    # Example output: "Number of Registered Attacks: [ 4n ]"
    match = re.search(r"Number of Registered Attacks:\s*\[?\s*(\d+)n?\s*\]?", output)
    if match:
        return int(match.group(1))
    else:
        print(f"[ERROR] Could not parse total attacks from output: {output}")
        return None


def fetch_blacklist():
    global _blacklist
    with _blacklist_lock:
        _blacklist = []
        output = _run_node_script("getTotalAttacks.cjs")
        if output is None:
            print("[ERROR] Could not get output from getTotalAttacks.cjs script")
            return

        total_attacks = _parse_total_attacks(output)
        if total_attacks is None:
            print("[ERROR] Could not obtain a valid total number of attacks.")
            return

        print(f"[INFO] Total attacks on VeChain: {total_attacks}")

        for i in range(total_attacks):
            print(f"[INFO] Fetching attack {i}")
            data = _run_node_script("getAttack.cjs", [str(i)])
            if data:
                try:
                    # Manually parse expected lines
                    lines = data.strip().splitlines()
                    if len(lines) >= 3:
                        ip = lines[0].split("IP:")[1].strip()
                        attack_type = lines[1].split("Attack type:")[1].strip()
                        timestamp = lines[2].split("Timestamp:")[1].strip()
                        _blacklist.append({
                            "ip": ip,
                            "attack_type": attack_type,
                            "timestamp": timestamp
                        })
                    else:
                        print(f"[WARNING] Unexpected format in attack output {i}: {data}")
                except Exception as e:
                    print(f"[ERROR] Failed to parse attack {i}: {e}")
            else:
                print(f"[WARNING] Could not fetch attack {i}.")


def get_blacklist():
    with _blacklist_lock:
        return list(_blacklist)

def start_periodic_update(interval=10):
    def update_loop():
        while True:
            print("[INFO] Updating blacklist...")
            fetch_blacklist()
            print(f"[INFO] Blacklist updated with {len(_blacklist)} attacks.")
            time.sleep(interval)

    thread = threading.Thread(target=update_loop, daemon=True)
    thread.start()

def force_update():
    print("[INFO] Forcing manual blacklist update...")
    fetch_blacklist()
    print(f"[INFO] Blacklist manually updated with {len(_blacklist)} attacks.")
    for i, attack in enumerate(_blacklist):
        print(f" Attack {i}:")
        print(f"   IP: {attack['ip']}")
        print(f"   Attack Type: {attack['attack_type']}")
        print(f"   Timestamp: {attack['timestamp']}")
        print(f"   Tx ID: {attack.get('tx_id', 'N/A')}")
        print("-" * 40)
        
def clear_blacklist():
    """Runs the deleteAllAttacks.cjs script to remove all attacks from VeChain."""
    output = _run_node_script("deleteAllAttacks.cjs")
    if output:
        print(f"[INFO] All attacks deleted successfully. Tx Id: {output}")
    else:
        print("[ERROR] Failed to delete attacks.")

def log_attack(ip, attack_type):
    # Absolute path to the Node.js script directory
    script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "blacklist"))
    script_path = os.path.join(script_dir, "sendAttackLog.cjs")

    try:
        result = subprocess.run(
            ["node", script_path, ip, attack_type],
            capture_output=True,
            text=True,
            check=True
        )
        stdout  = result.stdout.strip()
         # Extract the transaction ID
        tx_match = re.search(r"Transaction sent, ID:\s*(0x[a-fA-F0-9]+)", stdout)
        tx_id = tx_match.group(1) if tx_match else "Not found"

        # Extract estimated gas
        gas_match = re.search(r"totalGas:\s*(\d+)", stdout)
        gas = gas_match.group(1) if gas_match else "Unknown"

        print("=== Transaction Summary ===")
        print(f"Transaction ID : {tx_id}")
        print(f"Estimated Gas  : {gas}")
        print(f"Status         : Attack logged successfully")
        
        return {
            "status": "Attack logged",
            "tx_id": tx_id,
            "gas": gas
        }

    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else "Unknown error"
        print(f"[ERROR] Failed to log attack: {error_msg}")
        return None
    
def delete_attack(index):
    # Ejecuta el script deleteAttack.cjs con el índice del ataque a borrar
    output = _run_node_script("deleteAttack.cjs", [str(index)])

    if output:
        # Extraer el ID de la transacción (asumiendo que el script imprime algo como "Transaction sent, ID: 0x...")
        tx_match = re.search(r"Transaction sent, ID:\s*(0x[a-fA-F0-9]+)", output)
        tx_id = tx_match.group(1) if tx_match else "Not found"

        # Extraer gas estimado si está presente
        gas_match = re.search(r"totalGas:\s*(\d+)", output)
        gas = gas_match.group(1) if gas_match else "Unknown"

        print("=== Transaction Summary ===")
        print(f"Transaction ID : {tx_id}")
        print(f"Estimated Gas  : {gas}")
        print(f"Status         : Attack deleted successfully")

        return {
            "status": "Attack deleted",
            "tx_id": tx_id,
            "gas": gas
        }
    else:
        print(f"[ERROR] Failed to delete attack at index {index}.")
        return None

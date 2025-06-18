import subprocess
from logger import setup_logger
import os

class BlacklistManager:
    def __init__(self, logger='blacklist.log', max_warnings=3):
        self.blacklist_local = {}
        self.max_warnings = max_warnings
        self.logger = setup_logger(logger)

    def is_blacklisted(self, ip):
        return self.blacklist_local.get(ip, {}).get("blacklisted", False)

    def get_warnings(self, ip):
        return self.blacklist_local.get(ip, {}).get("warnings", 0)

    def reset_warnings(self, ip):
        self.blacklist_local[ip] = {"warnings": 0, "blacklisted": False}
        self.logger.info(f"Warnings reset for {ip}")

    def add_warning(self, ip, attack_type="DoS Attack"):
        warnings = self.get_warnings(ip) + 1
        blacklisted = False
        if warnings >= self.max_warnings:
            blacklisted = True
            self.logger.warning(f"{ip} reached max warnings ({warnings}). Adding to blacklist.")
            self.log_attack(ip, attack_type)
        self.blacklist_local[ip] = {"warnings": warnings, "blacklisted": blacklisted}
        return warnings, blacklisted

    def log_attack(self, ip, attack_type):
        self.logger.info(f"Logging attack for {ip}: {attack_type}")
        
        # Ruta absoluta al directorio donde está el script Node.js
        script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "blacklist"))
        script_path = os.path.join(script_dir, "sendAttackLog.cjs")

        try:
            # Log para verificar la ruta y el comando ejecutado
            self.logger.debug(f"Executing command: node {script_path} {ip} {attack_type}")
            self.logger.debug(f"Working directory: {script_dir}")

            result = subprocess.run(
                ["node", script_path, ip, attack_type],
                capture_output=True,
                text=True,
                check=True
            )
            tx_id = result.stdout.strip()
            self.logger.info(f"Attack logged successfully for {ip}. Tx Id: {tx_id}")
            return tx_id

        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() if e.stderr else "Unknown error"
            self.logger.error(f"Failed to log attack for {ip}. Error: {error_msg}")
            return None


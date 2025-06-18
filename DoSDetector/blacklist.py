import subprocess
from logger import setup_logger
import os

class BlacklistManager:
    """
    Manages a local in-memory blacklist with IP warning counters,
    and logs confirmed attacks to VeChain via Node.js script.
    """

    def __init__(self, logger='blacklist.log', max_warnings=3):
        """
        Initialize the blacklist manager with a logger and warning threshold.
        """
        self.blacklist_local = {}  # Dict to store IP warning states
        self.max_warnings = max_warnings
        self.logger = setup_logger(logger)

    def is_blacklisted(self, ip):
        """
        Check if the given IP is currently blacklisted.
        """
        return self.blacklist_local.get(ip, {}).get("blacklisted", False)

    def get_warnings(self, ip):
        """
        Return the number of warnings associated with an IP.
        """
        return self.blacklist_local.get(ip, {}).get("warnings", 0)

    def reset_warnings(self, ip):
        """
        Reset warning count and blacklist status for a specific IP.
        """
        self.blacklist_local[ip] = {"warnings": 0, "blacklisted": False}
        self.logger.info(f"Warnings reset for {ip}")

    def add_warning(self, ip, attack_type="DoS Attack"):
        """
        Add a warning to the IP and blacklist it if it exceeds the threshold.
        Logs the attack to VeChain if blacklisted.
        """
        warnings = self.get_warnings(ip) + 1
        blacklisted = False

        if warnings >= self.max_warnings:
            blacklisted = True
            self.logger.warning(f"{ip} reached max warnings ({warnings}). Adding to blacklist.")
            self.log_attack(ip, attack_type)

        self.blacklist_local[ip] = {"warnings": warnings, "blacklisted": blacklisted}
        return warnings, blacklisted

    def log_attack(self, ip, attack_type):
        """
        Log a blacklisted IP and attack type using a Node.js script that
        writes the event to the VeChain blockchain.
        """
        self.logger.info(f"Logging attack for {ip}: {attack_type}")
        
        # Construct the absolute path to the script directory
        script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "blacklist"))
        script_path = os.path.join(script_dir, "sendAttackLog.cjs")

        try:
            # Debugging logs: show the executed command and working directory
            self.logger.debug(f"Executing command: node {script_path} {ip} {attack_type}")
            self.logger.debug(f"Working directory: {script_dir}")

            # Execute Node.js script to log attack
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

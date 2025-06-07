"""
utils.py

Utility functions for network and system operations.

Includes:
- get_local_ip: Retrieves the local machine's active IPv4 address by opening
  a dummy UDP connection. Falls back to localhost if unable to determine.
"""

import socket

def get_local_ip():
    """
    Get the local IP address of the current machine.

    Attempts to create a UDP socket connection to an unreachable IP address to
    force the OS to assign the local IP of the active network interface.
    Returns '127.0.0.1' if this process fails.

    Returns:
        str: Local IP address as a string.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Connect to an unreachable IP to get local IP without sending packets
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'  # Fallback to localhost
    finally:
        s.close()
    return ip

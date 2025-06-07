"""
server.py

Multi-threaded HTTP server setup that runs the detection HTTP handler.

Features:
- Uses ThreadedHTTPServer to handle multiple simultaneous requests.
- Dynamically obtains local IP address to bind the server.
- Runs the server in a background thread to allow graceful shutdown.
- Handles KeyboardInterrupt (Ctrl+C) to stop the server cleanly.
- Integrates with a logging system to report server events.

Author: Rafael Malla Martinez
Date: 2025-06-06
"""

from http.server import HTTPServer
from socketserver import ThreadingMixIn
import threading
import signal
import sys
from utils import get_local_ip
from http_handler import MyHandler
from logger import setup_logger
import time

# Custom HTTP server class supporting multithreading
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True  # Threads will automatically close when main thread exits

def run_server():
    """
    Sets up and runs the HTTP server in a separate thread.
    Handles graceful shutdown on KeyboardInterrupt (Ctrl+C).
    """
    logger = setup_logger()  # Initialize logger
    ip = get_local_ip()  # Get local machine IP address dynamically
    port = 8080  # Define server port
    server = ThreadedHTTPServer((ip, port), MyHandler)  # Create server instance with request handler

    def serve():
        # Log and print server start info
        logger.info(f"Starting server on {ip}:{port}")
        print(f"Server running on {ip}:{port}. Press Ctrl+C to stop.")
        server.serve_forever()  # Start serving requests indefinitely

    # Run server in a dedicated thread to allow main thread to manage shutdown
    server_thread = threading.Thread(target=serve)
    server_thread.start()

    try:
        # Keep main thread alive while server thread runs
        while server_thread.is_alive():
            time.sleep(0.5)
    except KeyboardInterrupt:
        # Handle Ctrl+C for graceful shutdown
        server.shutdown()  # Stop accepting new requests and close existing ones
        server.server_close()  # Close server socket
        server_thread.join()  # Wait for server thread to finish
        logger.info("Server stopped.")
        print("Server stopped. Exiting now.")
        sys.exit(0)  # Exit program cleanly

if __name__ == "__main__":
    run_server()

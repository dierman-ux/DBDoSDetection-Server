"""
logger.py

This module provides a simple logging setup function for the application.
It configures a logger to write INFO and higher level logs to a file named 'server.log',
including timestamps and log levels in each log entry.

Usage:
    logger = setup_logger()
    logger.info("This is an info message")
"""


import logging

def setup_logger():
    """
    Configure and return a logger instance for the application.

    The logger writes INFO level and above messages to 'server.log' file,
    including timestamp, log level, and message in each log entry.
    """
    logging.basicConfig(
        filename='server.log',          # Log output file
        level=logging.INFO,             # Minimum log level to capture
        format='%(asctime)s - %(levelname)s - %(message)s'  # Log message format
    )
    return logging.getLogger(__name__)  # Return a logger named after the current module

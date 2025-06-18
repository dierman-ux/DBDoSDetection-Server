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

def setup_logger(filename='server.log', logger_name=__name__):
    """
    Configure and return a logger instance for the application.

    The logger writes INFO level and above messages to 'server.log' file,
    including timestamp, log level, and message in each log entry.

    Args:
        filename (str): The file where logs will be saved.
        logger_name (str): The name of the logger to create/use.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(logger_name)
    if not logger.hasHandlers():
        # Configure handler only if not already configured
        handler = logging.FileHandler(filename)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False  # Prevent double logging if root logger configured elsewhere

    return logger

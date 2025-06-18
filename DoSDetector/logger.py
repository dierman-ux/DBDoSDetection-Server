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
    # Retrieve or create a logger with the given name
    logger = logging.getLogger(logger_name)

    # Only configure the logger once to avoid duplicate handlers
    if not logger.hasHandlers():
        # Define a file handler that logs to the specified file
        handler = logging.FileHandler(filename)

        # Define log format: timestamp - log level - message
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # Add handler to the logger
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        # Prevent propagation to root logger to avoid duplicate logs
        logger.propagate = False

    return logger

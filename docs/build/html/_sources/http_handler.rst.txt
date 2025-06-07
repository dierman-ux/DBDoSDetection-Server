http_handler module
====================

HTTP request handler for traffic detection and IP blacklist management.

Features:
- Handles GET requests, collects metrics per IP.
- Uses DetectionEngine to classify traffic type (BENIGN or attack).
- Maintains a local blacklist with warning counts before blocking IPs.
- Registers detected attacks on a blockchain via an external Node.js script.
- Thread-safe management of shared data structures.
- Logs events and errors for auditing and debugging.

Author: Rafael Malla Martinez
Date: 2025-06-06

.. automodule:: http_handler
   :members:
   :show-inheritance:
   :undoc-members:
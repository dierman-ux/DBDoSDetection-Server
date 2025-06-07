metrics module
==============

This module provides functions to calculate network traffic metrics from timestamps and byte records.

Features:
- Computes inter-arrival times (IAT) and idle times from request timestamps.
- Calculates statistical features such as total, max, mean, min, and standard deviation.
- Supports incremental data collection per IP address.
- Provides output compatible with detection model feature input.
- Handles cases with insufficient data gracefully.

.. automodule:: metrics
   :members:
   :show-inheritance:
   :undoc-members:

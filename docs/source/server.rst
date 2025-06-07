server module
=============

Multi-threaded HTTP server setup that runs the detection HTTP handler.

Features:
- Uses ThreadedHTTPServer to handle multiple simultaneous requests.
- Dynamically obtains local IP address to bind the server.
- Runs the server in a background thread to allow graceful shutdown.
- Handles KeyboardInterrupt (Ctrl+C) to stop the server cleanly.
- Integrates with a logging system to report server events.

.. automodule:: server
   :members:
   :show-inheritance:
   :undoc-members:

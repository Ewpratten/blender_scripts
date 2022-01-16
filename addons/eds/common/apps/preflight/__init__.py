# The main window, also the entrypoint for the application
from ...qt.qt_app_wrapper import QtAppWrapper
from ...qt import pyside_loader
from . import window

# Load the logging system
import logging
logger = logging.getLogger("eds.apps.preflight")

def launch_preflight(checks: list, parent=None):
    global preflight_app
    logger.info("Starting Preflight")

    # Create an application wrapper and run the app
    with QtAppWrapper(parent=parent):
        # Create and show the Preflight window
        w = window.PreflightWindow(parent=parent, checks=checks)
        w.show()

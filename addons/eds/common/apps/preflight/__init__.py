# The main window, also the entrypoint for the application
from ...qt import pyside_loader
from . import window

# Load the logging system
import logging
logger = logging.getLogger("eds.apps.preflight")

# There is a chance that this will be run in an environment where a Qt application is not created
# We will use this global var to create our own app
preflight_app = None


def launch_preflight(checks: list, parent=None):
    global preflight_app
    logger.info("Starting Preflight")

    # If there is no parent, we must make a QApplication
    if parent is None:
        logger.info("No parent specified. Creating QApplication")
        from PySide2 import QtWidgets
        try:
            if not preflight_app:
                preflight_app = QtWidgets.QApplication([])
        except RuntimeError:
            logger.error(
                "Could not create QApplication. Is it already running?")

    # Create and show the Preflight window
    w = window.PreflightWindow(parent=parent, checks=checks)
    w.show()

    # If there is no parent, we must run the QApplication
    if parent is None:
        logger.info("Running QApplication")
        if preflight_app:
            preflight_app.exec_()

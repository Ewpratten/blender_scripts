# The main window, also the entrypoint for the application
from ...qt.qt_app_wrapper import QtAppWrapper
from ...qt import pyside_loader
from . import window

# Load the logging system
import logging
logger = logging.getLogger("eds.apps.updater")


def launch_self_updater(parent=None):
    logger.info("Starting Self-Updater")

    # Create an application wrapper and run the app
    with QtAppWrapper(parent=parent):
        # Create and show the Preflight window
        w = window.SelfUpdaterWindow(parent=parent)
        w.show()

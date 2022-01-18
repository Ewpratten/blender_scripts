# The main window, also the entrypoint for the application
from ...qt.qt_app_wrapper import QtAppWrapper
from ...qt import pyside_loader
from . import window
from typing import Optional

# Load the logging system
import logging
logger = logging.getLogger("eds.dialogs")


def launch_monocular_importer(parent=None) -> Optional[window.MonocularOutputs]:
    logger.info("Starting monocular depth import dialog")

    # Create an application wrapper and run the app
    with QtAppWrapper(parent=parent):
        # Create and show the window
        w = window.MonocularImportWindow(parent=parent)
        w.show()

    return w.get_output()

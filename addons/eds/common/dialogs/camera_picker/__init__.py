# The main window, also the entrypoint for the application
from ...qt.qt_app_wrapper import QtAppWrapper
from ...qt import pyside_loader
from . import window
from typing import Optional

# Load the logging system
import logging
logger = logging.getLogger("eds.dialogs")


def launch_camera_picker(camera_names, parent=None) -> Optional[window.CameraPickerResponse]:
    logger.info("Starting camera picker dialog")

    # Create an application wrapper and run the app
    with QtAppWrapper(parent=parent):
        # Create and show the window
        w = window.CameraPickerWindow(
            camera_names, parent=parent)
        w.show()

    return w.get_output()

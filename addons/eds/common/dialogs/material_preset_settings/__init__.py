# The main window, also the entrypoint for the application
from ...qt.qt_app_wrapper import QtAppWrapper
from ...qt import pyside_loader
from . import window
from typing import Optional

# Load the logging system
import logging
logger = logging.getLogger("eds.apps.preflight")


def launch_material_preset_settings(material_names, preset_name, parent=None) -> Optional[window.MaterialPresetSettingsResponse]:
    global preflight_app
    logger.info("Starting material preset settings select dialog")

    # Create an application wrapper and run the app
    with QtAppWrapper(parent=parent):
        # Create and show the Preflight window
        w = window.MaterialPresetSettingsWindow(
            material_names, preset_name,  parent=parent)
        w.show()

    return w.get_settings()

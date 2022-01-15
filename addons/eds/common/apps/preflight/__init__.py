
# Load the logging system
import logging
logger = logging.getLogger("eds.apps.preflight")

# We'll try to import PySide2
# In some DCCs, this may not be available by default, thus a useful error should be raised
try:
    import PySide2
except ImportError:
    logger.error("Could not import PySide2. Is it in your PYTHONPATH?")
    logger.error("If this is Blender, you'll need to install it yourself through Pip.")
    raise

# The main window, also the entrypoint for the application
from . import window

def launch_preflight(parent=None):
    logger.info("Starting Preflight")

    # If there is no parent, we must make a QApplication
    if parent is None:
        logger.info("No parent specified. Creating QApplication")
        from PySide2 import QtWidgets
        app = QtWidgets.QApplication([])

    # Create and show the Preflight window
    w = window.PreflightWindow(parent=parent)
    w.show()

    # If there is no parent, we must run the QApplication
    if parent is None:
        logger.info("Running QApplication")
        app.exec_()
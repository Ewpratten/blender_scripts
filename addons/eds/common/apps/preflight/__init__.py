from eds.common.utils.system_site_packages import load_system_site_packages

# Load the logging system
import logging
logger = logging.getLogger("eds.apps.preflight")

# We'll try to import PySide2
# In some DCCs, this may not be available by default, thus a useful error should be raised
try:
    import PySide2
except ImportError:
    logger.error("Could not import PySide2. Is it in your PYTHONPATH?")
    logger.error(
        "If this is Blender, you'll need to install it yourself through Pip.")

    # We'll try to load the system site-packages
    system_load_ok = False
    logger.info("Attempting to load PySide2 from your LOCAL site-packages")
    try:
        load_system_site_packages()
        import PySide2
        system_load_ok = True
        logger.info("Successfully loaded PySide2 from your LOCAL site-packages")
    except ImportError:
        logger.error("Loading PySide2 from your local site-packages failed.")
        raise
    
    if not system_load_ok:
        logger.error("Loading PySide2 from your system site-packages failed.")
        raise

# The main window, also the entrypoint for the application
from . import window 

# There is a chance that this will be run in an environment where a Qt application is not created
# We will use this global var to create our own app
preflight_app = None

def launch_preflight(parent=None):
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
            logger.error("Could not create QApplication. Is it already running?")

    # Create and show the Preflight window
    w = window.PreflightWindow(parent=parent)
    w.show()

    # If there is no parent, we must run the QApplication
    if parent is None:
        logger.info("Running QApplication")
        if preflight_app:
            preflight_app.exec_()

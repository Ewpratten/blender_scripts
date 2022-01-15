# Load the logging system
import logging
logger = logging.getLogger("eds.apps.preflight")

from eds.common.utils.system_site_packages import load_system_site_packages

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
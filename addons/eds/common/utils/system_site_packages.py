import sys
import os

# Load the logging system
import logging
logger = logging.getLogger("eds.apps.preflight")

def find_system_site_packages():
    """Attempts to find the system site-packages directory. This could be used to side-load local libraries"""

    # Attempt to call system python to get the system PYTHONPATH
    system_path = eval(os.popen("python3 -c 'import sys; print(sys.path)'").read())

    for path in system_path:
        if "site-packages" in path:
            yield path

    return None

def load_system_site_packages():
    """Attempts to load the system site-packages directories into the current python environment"""

    # Get the system site-packages directories
    system_site_packages = find_system_site_packages()

    # If we found any, add them to the current python environment
    if system_site_packages is not None:
        for path in system_site_packages:
            logger.info(f"Appending new site-packages path: {path}")
            sys.path.append(path)

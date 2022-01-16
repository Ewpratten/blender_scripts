bl_info = { # Blender requires this
    "name": "Evan's DCC Scripts (EDS)",
    "author": "Evan Pratten <ewpratten@gmail.com>",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "description": "Adds a bunch of small utilities to Blender",
    "category": "General",
}

# Set up logging
import logging
from . import log_cfg
log_cfg.configure_eds_logging()
logger = logging.getLogger("eds")

# Keep track of the path to this module for reference by other scripts
import pathlib
MODULE_PATH = pathlib.Path(__file__).parent.resolve()

# Handle attempting to load the blender modules
try:
    logger.info("Attempting to load blender modules")

    # We load bpy itself to quickly check if we can load more blender plugins
    import bpy

    # We can now pull in the methods blender is looking for from the blender module
    from .dcc.blender import register, unregister
except ImportError as e:
    logger.warning("Could not import Blender modules. This probably isn't Blender.")
    logger.exception(e)
    pass
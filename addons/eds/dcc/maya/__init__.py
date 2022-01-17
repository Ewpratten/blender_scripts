
import logging
logger = logging.getLogger("eds.blender")


def initializePlugin(plugin):
    logger.info("Initializing Maya plugin")


def uninitializePlugin(plugin):
    logger.info("Uninitializing Maya plugin")

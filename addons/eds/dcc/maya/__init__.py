

from eds.dcc.maya.modules.topbar import createMayaTopBarMenus
from . import preflight

import logging
logger = logging.getLogger("eds.maya")


def initializePlugin(plugin):
    logger.info("Initializing Maya plugin")

    # Set up the top bar menu
    createMayaTopBarMenus()


def uninitializePlugin(plugin):
    logger.info("Uninitializing Maya plugin")

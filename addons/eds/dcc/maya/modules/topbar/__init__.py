import pymel.core as pm
import logging
logger = logging.getLogger("eds.maya")


def createMayaTopBarMenus():
    """Sets up the top bar menus for Maya"""
    logger.info("Creating EDS top bar menus")

    # Get the main window
    main_window = pm.language.melGlobals['gMainWindow']

    # Create the top bar menu
    top_bar_menu = pm.menu(label="[EDS]", parent=main_window)

    # Add menu children
    pm.menuItem(label="Launch Preflight",
                command="from eds.dcc.maya.preflight import launchMayaPreflight;launchMayaPreflight()", parent=top_bar_menu)
    # pm.menuItem(label="Camera Picker", command="", parent=top_bar_menu)
    pm.menuItem(divider=True, parent=top_bar_menu)
    pm.menuItem(label="Launch Updater",
                command="from eds.dcc.maya.modules.topbar.launchers import launchMayaPluginUpdater;launchMayaPluginUpdater()", parent=top_bar_menu)

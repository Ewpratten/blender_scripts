
from eds.dcc.maya.utils.maya_qt import getMayaQtParent
from eds.common.apps.updater import launch_self_updater


def launchMayaPluginUpdater():
    """Launches the plugin updater window in Maya. (to be called from mel)"""
    launch_self_updater(parent=getMayaQtParent())

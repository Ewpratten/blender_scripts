
from eds.dcc.maya.utils.maya_qt import getMayaQtParent
from eds.common.apps.preflight import launch_preflight


def launchMayaPreflight():
    """Launches the preflight check window in Maya. (to be called from mel)"""
    launch_preflight([], parent=getMayaQtParent())
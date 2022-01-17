from shiboken2 import wrapInstance 
from PySide2 import QtWidgets
from maya import OpenMayaUI as omui 

def getMayaQtParent():
    """Get the Maya's main window as a QWidget."""
    maya_main_window_ptr = omui.MQtUtil.mainWindow()
    maya_main_window = wrapInstance(int(maya_main_window_ptr), QtWidgets.QWidget)
    return maya_main_window
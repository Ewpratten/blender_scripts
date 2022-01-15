import logging
logger = logging.getLogger("eds.apps.preflight")

import pkgutil

from PySide2.QtCore import Qt, QEventLoop
from PySide2 import QtWidgets
from ...qt.qt_lines import QHLine

class PreflightWindow(QtWidgets.QWidget):
    
    def __init__(self, parent=None):
        super(PreflightWindow, self).__init__(parent)

        # Configure the window's display settings
        self.setWindowFlags(
            self.windowFlags() ^ Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Preflight")
        self.resize(400, 600)

        # Set the root of the application to be a vertical list
        self.setLayout(QtWidgets.QVBoxLayout())

        # Load the stylesheet for this app
        stylesheet = pkgutil.get_data(__name__, "preflight.css")
        self.setStyleSheet(stylesheet.decode("utf-8"))

        # Configure the title at the top of the window
        self.label = QtWidgets.QLabel("Evan's Preflight Checklist")
        self.label.setProperty('labelClass', 'label-title')
        self.layout().addWidget(self.label)

        # Set some info text below the title
        self.info_text = QtWidgets.QLabel("Various automated checks for your projects.")
        self.layout().addWidget(self.info_text)
        self.layout().addWidget(QHLine())

        # Fill in remaining space with a stretch
        self.layout().addStretch()
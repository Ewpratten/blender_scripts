import os

from eds import MODULE_PATH
from ...qt.qt_lines import QHLine
from PySide2 import QtWidgets
from PySide2.QtCore import Qt
import pkgutil
import logging
logger = logging.getLogger("eds.apps.updater")


class SelfUpdaterWindow(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(SelfUpdaterWindow, self).__init__(parent)

        # Configure the window's display settings
        self.setWindowFlags(
            self.windowFlags() ^ Qt.WindowStaysOnTopHint)
        self.setWindowTitle("EDS Self-Updater")
        self.resize(400, 300)

        # Set the root of the application to be a vertical list
        self.setLayout(QtWidgets.QVBoxLayout())

        # Load the stylesheet for this app
        stylesheet = pkgutil.get_data(__name__, "updater.css")
        self.setStyleSheet(stylesheet.decode("utf-8"))

        # Configure the title at the top of the window
        self.label = QtWidgets.QLabel("EDS Self-Updater")
        self.label.setProperty('labelClass', 'label-title')
        self.layout().addWidget(self.label)
        self.subtitle = QtWidgets.QLabel(
            "This tool is for updating Evan's DCC Scripts.")
        self.layout().addWidget(self.subtitle)
        self.layout().addWidget(QHLine())

        # Add a "Check for Updates" button
        self.check_updates_button = QtWidgets.QPushButton("Check for Updates")
        self.check_updates_button.setProperty('buttonClass', 'button-primary')
        self.check_updates_button.clicked.connect(self.check_for_updates)
        self.layout().addWidget(self.check_updates_button)

        # Add an "Allow development versions" checkbox
        self.allow_dev_checkbox = QtWidgets.QCheckBox(
            "Allow development versions")
        self.allow_dev_checkbox.setChecked(False)
        self.layout().addWidget(self.allow_dev_checkbox)

        # Add a list for all available versoins
        self.versions_list = QtWidgets.QListWidget()
        self.layout().addWidget(self.versions_list)
        self.redraw_versions_list()

        # Add an update and close buttons beside eachother
        self.action_layout = QtWidgets.QHBoxLayout()
        self.update_button = QtWidgets.QPushButton("Update")
        self.update_button.clicked.connect(self.update)
        self.close_button = QtWidgets.QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        self.action_layout.addWidget(self.update_button)
        self.action_layout.addWidget(self.close_button)
        self.layout().addLayout(self.action_layout)

        # Add a spacer to handle window resizing
        self.layout().addStretch()

    def redraw_versions_list(self):
        self.versions_list.clear()
        logger.info(f"Module path is: {MODULE_PATH}")

        # Call git to get a list of all local branches
        git_output = os.popen("git branch").read()

        # Parse the output to get the branch names
        git_output = git_output.split("\n")
        git_output = [x.strip() for x in git_output if x.strip()]
        git_output = [x for x in git_output if not x.startswith("*")]
        

    def check_for_updates(self):
        logger.info("Checking for updates")
        pass

    def update(self):
        logger.info("Update button pressed. Attempting to update.")
        pass

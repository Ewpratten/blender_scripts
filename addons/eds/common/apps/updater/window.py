import os

from eds import MODULE_PATH
from eds.common.qt.qt_window_center import center_window
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
            self.windowFlags() ^ Qt.WindowStaysOnTopHint ^ Qt.Window)
        self.setWindowTitle("EDS Self-Updater")
        self.resize(400, 300)
        center_window(self)

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
        self.allow_dev_checkbox.stateChanged.connect(lambda state: self.redraw_versions_list())
        self.layout().addWidget(self.allow_dev_checkbox)

        # Add a list for all available versoins
        self.versions_list = QtWidgets.QListWidget()
        self.versions_list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
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

        # Navigate to the directory containing the plugin
        curdir = os.getcwd()
        os.chdir(MODULE_PATH)

        # Call git to get a list of all local branches and tags
        git_branches = os.popen("git branch").read()
        git_tags = os.popen("git tag").read()

        # Parse the output to get the branch names
        git_branches = git_branches.split("\n")
        git_branches = [x.strip() for x in git_branches if x.strip()]
        current_branch = [x for x in git_branches if x.startswith("*")][0].replace("*", "").strip()
        git_branches = [x for x in git_branches if not x.startswith("*")]
        try:
            git_branches.remove("list")
        except ValueError:
            pass

        # Parse the output to get the tag names
        git_tags = git_tags.split("\n")
        git_tags = [x.strip() for x in git_tags if x.strip()]

        # Add the current branch to the list and select it
        current_branch_label = QtWidgets.QListWidgetItem(current_branch)
        current_branch_label.setSelected(True)
        self.versions_list.addItem(current_branch_label)
        self.versions_list.setCurrentItem(current_branch_label)

        # Add all tags to the list
        for tag in git_tags:
            tag_label = QtWidgets.QListWidgetItem(tag)
            self.versions_list.addItem(tag_label)

        # Check if we should be showing development versions
        if self.allow_dev_checkbox.isChecked():
            # Add all branches to the list
            for branch in git_branches:
                branch_label = QtWidgets.QListWidgetItem(branch)
                self.versions_list.addItem(branch_label)

        # Return to the original directory
        os.chdir(curdir)

    def check_for_updates(self):
        logger.info("Checking for updates")
        
        # Navigate to the directory containing the plugin
        curdir = os.getcwd()
        os.chdir(MODULE_PATH)

        # Fetch from git
        os.system("git fetch")
        
        # Return to the original directory
        os.chdir(curdir)

    def update(self):
        logger.info("Update button pressed. Attempting to update.")
        
        # Navigate to the directory containing the plugin
        curdir = os.getcwd()
        os.chdir(MODULE_PATH)

        # Get the selected version
        selected_version = self.versions_list.currentItem().text()

        # Check out the selected version
        os.system("git checkout " + selected_version)

        # Pull the selected version
        os.system("git pull")
        
        # Return to the original directory
        os.chdir(curdir)

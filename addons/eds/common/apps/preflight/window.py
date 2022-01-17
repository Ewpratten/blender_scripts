from eds.common.qt.qt_window_center import center_window
from .preflight_check import PreflightCheck
from ...qt.qt_lines import QHLine
from PySide2 import QtWidgets
from PySide2.QtCore import Qt, QEventLoop
import pkgutil
import logging
logger = logging.getLogger("eds.apps.preflight")


class PreflightWindow(QtWidgets.QWidget):

    def __init__(self, checks: list, parent=None):
        super(PreflightWindow, self).__init__(parent)

        # Populate a cache of checks and their last known result
        self.checks = {}
        for check in checks:
            self.checks[check()] = None

        # Configure the window's display settings
        self.setWindowFlags(
            self.windowFlags() ^ Qt.WindowStaysOnTopHint ^ Qt.Window)
        self.setWindowTitle("Preflight")
        self.resize(400, 600)
        center_window(self)

        # Set the root of the application to be a vertical list
        self.setLayout(QtWidgets.QVBoxLayout())

        # Load the stylesheet for this app
        stylesheet = pkgutil.get_data(__name__, "preflight.css")
        self.setStyleSheet(stylesheet.decode("utf-8"))

        # Configure the title at the top of the window
        self.label = QtWidgets.QLabel("Preflight Checklist")
        self.label.setProperty('labelClass', 'label-title')
        self.layout().addWidget(self.label)

        # Set some info text below the title
        self.info_text = QtWidgets.QLabel(
            "Various automated checks for your projects.\nYour DCC may freeze while this is open.")
        self.layout().addWidget(self.info_text)
        self.layout().addWidget(QHLine())

        # Create the list of checks
        # self.check_scroll_area = QtWidgets.QScrollArea()
        # self.check_scroll_area.horizontalScrollBarPolicy = Qt.ScrollBarAlwaysOff
        # self.check_scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.check_table = QtWidgets.QTableWidget()
        self.check_table.setColumnCount(1)
        self.check_table.setRowCount(len(self.checks))
        self.check_table.horizontalHeader().setVisible(False)
        self.check_table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch)
        self.check_table.verticalHeader().setVisible(False)
        self.check_table.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.check_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.check_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # self.check_scroll_area.addWidget(self.check_table)
        self.layout().addWidget(self.check_table)

        # Populate the list of checks
        self.repopulate_check_list()

        # Add a button to run all checks and a button to run all fixes
        self.action_layout = QtWidgets.QHBoxLayout()
        self.action_layout.setAlignment(Qt.AlignVCenter)
        self.layout().addLayout(self.action_layout)

        self.run_all_button = QtWidgets.QPushButton("Check All")
        self.run_all_button.setMinimumHeight(20)
        self.run_all_button.clicked.connect(lambda: self.run_all_checks())
        self.action_layout.addWidget(self.run_all_button)

        self.fix_all_button = QtWidgets.QPushButton("Fix All")
        self.fix_all_button.setMinimumHeight(20)
        self.fix_all_button.clicked.connect(lambda: self.fix_all_checks())
        self.action_layout.addWidget(self.fix_all_button)

    def repopulate_check_list(self):
        # Clear the check list
        self.check_table.setRowCount(0)
        self.check_table.setRowCount(len(self.checks))

        for i, check in enumerate(self.checks):
            check_result = self.checks[check]

            # Build a widget for this check
            check_widget = QtWidgets.QWidget()
            check_layout = QtWidgets.QHBoxLayout()
            check_layout.setMargin(0)
            check_layout.setAlignment(Qt.AlignVCenter)
            check_widget.setLayout(check_layout)

            # If the check has a result, set the widget's background color
            if check_result is not None:
                if check_result.success:
                    check_widget.setStyleSheet("background-color: green")
                else:
                    check_widget.setStyleSheet("background-color: red")

            # Build the row for this check
            check_label = QtWidgets.QLabel(check.get_name())
            check_label.setMargin(5)
            check_layout.addWidget(check_label)
            check_layout.addStretch()

            # If the check has auto-fix, add a button to it
            if check.can_auto_fix():
                fix_button = QtWidgets.QPushButton("Fix")
                fix_button.setMinimumHeight(20)
                fix_button.clicked.connect(
                    lambda: self.fix_check(check))
                check_layout.addWidget(fix_button)

            # Add a button to manually run the check
            run_button = QtWidgets.QPushButton("Check")
            run_button.setMinimumHeight(20)
            run_button.clicked.connect(
                lambda: self.run_check(check))
            check_layout.addWidget(run_button)

            # Add the check widget to the list
            self.check_table.setCellWidget(i, 0, check_widget)

    def run_check(self, check: PreflightCheck, skip_repopulate=False):
        # Run the check and update the UI
        self.checks[check] = check.run_check()
        if not skip_repopulate:
            self.repopulate_check_list()

    def fix_check(self, check: PreflightCheck, skip_repopulate=False):
        # This only works if the check has an auto-fix flag, and has been run before
        last_check_result = self.checks[check]
        if check.can_auto_fix() and last_check_result is not None:
            check.run_fix(last_check_result)
            if not skip_repopulate:
                self.repopulate_check_list()

    def run_all_checks(self):
        # Run all checks and update the UI
        for check in self.checks:
            self.run_check(check, skip_repopulate=True)
        self.repopulate_check_list()

    def fix_all_checks(self):
        # This only works if the check has an auto-fix flag, and has been run before
        for check in self.checks:
            self.fix_check(check, skip_repopulate=True)
        self.repopulate_check_list()
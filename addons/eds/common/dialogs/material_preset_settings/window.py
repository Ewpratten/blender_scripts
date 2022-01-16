from typing import Optional

from eds.common.qt.qt_window_center import center_window
from ...qt.qt_lines import QHLine
from PySide2 import QtWidgets
from PySide2.QtCore import Qt
import pkgutil
import logging
logger = logging.getLogger("eds.dialogs")


class MaterialPresetSettingsResponse:
    world_bg_material: str = None
    create_regular: bool = True
    create_grease_pencil: bool = True
    create_grease_pencil_fills: bool = False


class MaterialPresetSettingsWindow(QtWidgets.QWidget):

    _settings = None

    def __init__(self, material_names, preset_name, parent=None):
        super(MaterialPresetSettingsWindow, self).__init__(parent)

        # Configure the window's display settings
        self.setWindowFlags(
            self.windowFlags() ^ Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Preset Loading Options")
        self.resize(300, 200)
        center_window(self)

        # Set the root of the application to be a vertical list
        self.setLayout(QtWidgets.QVBoxLayout())

        # Load the stylesheet for this app
        stylesheet = pkgutil.get_data(__name__, "../dialog.css")
        self.setStyleSheet(stylesheet.decode("utf-8"))

        # Configure the title at the top of the window
        self.label = QtWidgets.QLabel("Preset Loading Options")
        self.label.setProperty('labelClass', 'label-title')
        self.layout().addWidget(self.label)
        self.layout().addWidget(QHLine())

        # Add a selection for if the background should be updated
        self.bg_set_layout = QtWidgets.QHBoxLayout()
        self.bg_set_layout.setAlignment(Qt.AlignLeft)
        self.bg_set_label = QtWidgets.QLabel("Update Background Material")
        self.bg_set_layout.addWidget(self.bg_set_label)
        self.bg_set_layout.addStretch()
        self.bg_set_checkbox = QtWidgets.QCheckBox()
        self.bg_set_checkbox.setChecked(True)
        self.bg_set_checkbox.stateChanged.connect(
            lambda state: self.bg_material_dropdown.setEnabled(state))
        self.bg_set_layout.addWidget(self.bg_set_checkbox)
        self.layout().addLayout(self.bg_set_layout)

        # Add a dropdown for the background material
        self.bg_material_layout = QtWidgets.QHBoxLayout()
        self.bg_material_layout.setAlignment(Qt.AlignLeft)
        self.bg_material_label = QtWidgets.QLabel("Background Material")
        self.bg_material_layout.addWidget(self.bg_material_label)
        self.bg_material_layout.addStretch()
        self.bg_material_dropdown = QtWidgets.QComboBox()
        self.bg_material_dropdown.addItems(material_names)
        self.bg_material_dropdown.setCurrentIndex(0)
        self.bg_material_layout.addWidget(self.bg_material_dropdown)
        self.layout().addLayout(self.bg_material_layout)

        # Add a selection for if the regular material should be created
        self.regular_set_layout = QtWidgets.QHBoxLayout()
        self.regular_set_layout.setAlignment(Qt.AlignLeft)
        self.regular_set_label = QtWidgets.QLabel("Create Regular Material")
        self.regular_set_layout.addWidget(self.regular_set_label)
        self.regular_set_layout.addStretch()
        self.regular_set_checkbox = QtWidgets.QCheckBox()
        self.regular_set_checkbox.setChecked(True)
        self.regular_set_layout.addWidget(self.regular_set_checkbox)
        self.layout().addLayout(self.regular_set_layout)

        # Add a selection for if the grease pencil material should be created
        self.grease_pencil_set_layout = QtWidgets.QHBoxLayout()
        self.grease_pencil_set_layout.setAlignment(Qt.AlignLeft)
        self.grease_pencil_set_label = QtWidgets.QLabel(
            "Create Grease Pencil Material")
        self.grease_pencil_set_layout.addWidget(self.grease_pencil_set_label)
        self.grease_pencil_set_layout.addStretch()
        self.grease_pencil_set_checkbox = QtWidgets.QCheckBox()
        self.grease_pencil_set_checkbox.setChecked(True)
        self.grease_pencil_set_checkbox.stateChanged.connect(
            lambda state: self.grease_pencil_fill_checkbox.setEnabled(state))
        self.grease_pencil_set_layout.addWidget(
            self.grease_pencil_set_checkbox)
        self.layout().addLayout(self.grease_pencil_set_layout)

        # Add a selection for if the grease pencil material should have a separate "fills" counterpart
        self.grease_pencil_fill_layout = QtWidgets.QHBoxLayout()
        self.grease_pencil_fill_layout.setAlignment(Qt.AlignLeft)
        self.grease_pencil_fill_label = QtWidgets.QLabel(
            "Create explicit Grease Pencil fill materials")
        self.grease_pencil_fill_layout.addWidget(self.grease_pencil_fill_label)
        self.grease_pencil_fill_layout.addStretch()
        self.grease_pencil_fill_checkbox = QtWidgets.QCheckBox()
        self.grease_pencil_fill_checkbox.setChecked(False)
        self.grease_pencil_fill_layout.addWidget(
            self.grease_pencil_fill_checkbox)
        self.layout().addLayout(self.grease_pencil_fill_layout)

        # Add a horizontal line to separate the buttons
        self.layout().addWidget(QHLine())

        # Add a button to close the window
        self.close_button = QtWidgets.QPushButton("Done")
        self.close_button.clicked.connect(self._save_and_exit)
        self.layout().addWidget(self.close_button)

        # Add space at the bottom in case window size is wrong
        self.layout().addStretch()

    def _save_and_exit(self):
        # Create a response object
        self._settings = MaterialPresetSettingsResponse()

        # Set the background material
        if self.bg_set_checkbox.isChecked():
            self._settings.world_bg_material = self.bg_material_dropdown.currentText()
        self._settings.create_grease_pencil = self.grease_pencil_set_checkbox.isChecked()
        self._settings.create_regular = self.regular_set_checkbox.isChecked()
        self._settings.create_grease_pencil_fills = self.grease_pencil_fill_checkbox.isChecked()

        # Close the window
        self.close()

    def get_settings(self) -> Optional[MaterialPresetSettingsResponse]:

        # To handle a user setting a background, then turning off backgrounds,
        # we shall do a quick check for this
        if not self.bg_material_dropdown.isEnabled():
            self._settings.world_bg_material = None

        return self._settings

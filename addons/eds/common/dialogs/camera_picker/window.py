from typing import Optional

from eds.common.qt.qt_window_center import center_window
from ...qt.qt_lines import QHLine
from PySide2 import QtWidgets
from PySide2.QtCore import Qt
import pkgutil
import logging
logger = logging.getLogger("eds.dialogs")


class CameraPickerResponse:
    new_active_camera: Optional[str] = None
    camera_for_image_render: Optional[str] = None
    camera_for_animation_render: Optional[str] = None


class CameraPickerWindow(QtWidgets.QWidget):

    _output = None

    def __init__(self, cameras, parent=None):
        super(CameraPickerWindow, self).__init__(parent)

        # Configure the window's display settings
        self.setWindowFlags(
            self.windowFlags() ^ Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Camera Picker")
        self.resize(300, 300)
        center_window(self)

        # Set the root of the application to be a vertical list
        self.setLayout(QtWidgets.QVBoxLayout())

        # Load the stylesheet for this app
        stylesheet = pkgutil.get_data(__name__, "../dialog.css")
        self.setStyleSheet(stylesheet.decode("utf-8"))

        # Configure the title at the top of the window
        self.label = QtWidgets.QLabel("Camera Picker")
        self.label.setProperty('labelClass', 'label-title')
        self.layout().addWidget(self.label)
        self.layout().addWidget(QHLine())

        # Add a list of cameras to the window
        self.camera_list = QtWidgets.QListWidget()
        self.camera_list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.layout().addWidget(self.camera_list)
        for camera in cameras:
            camera_item = QtWidgets.QListWidgetItem(camera)
            self.camera_list.addItem(camera_item)

        # Add a "make active" button
        self.make_active_button = QtWidgets.QPushButton("Make Active")
        self.make_active_button.clicked.connect(self.update_active_camera)
        self.layout().addWidget(self.make_active_button)

        # Add  "Render Image" and "Render Animation" buttons beside eachother
        self.action_layout = QtWidgets.QHBoxLayout()
        self.render_image_button = QtWidgets.QPushButton("Render Image")
        self.render_image_button.clicked.connect(self.render_image)
        self.render_animation_button = QtWidgets.QPushButton("Render Animation")
        self.render_animation_button.clicked.connect(self.render_animation)
        self.action_layout.addWidget(self.render_image_button)
        self.action_layout.addWidget(self.render_animation_button)
        self.layout().addLayout(self.action_layout)

        # Add space at the bottom in case window size is wrong
        self.layout().addStretch()

    def get_output(self) -> Optional[CameraPickerResponse]:
        return self._output

    def update_active_camera(self):
        # If nothing is selected, just exit
        if self.camera_list.selectedItems() == []:
            self._output = None
            self.close()

        # Get the currently selected camera
        camera_name = self.camera_list.currentItem().text()
        logger.info(f"Setting active camera to: {camera_name}")        

        # Create a response object if needed
        if self._output is None:
            self._output = CameraPickerResponse()
        
        # Set the new active camera
        self._output.new_active_camera = camera_name

        # Close the window
        self.close()

    def render_image(self):
        # If nothing is selected, just exit
        if self.camera_list.selectedItems() == []:
            self._output = None
            self.close()

        # Get the currently selected camera
        camera_name = self.camera_list.currentItem().text()
        logger.info(f"Image render requested for: {camera_name}")        

        # Create a response object if needed
        if self._output is None:
            self._output = CameraPickerResponse()
        
        # Set the new active camera
        self._output.camera_for_image_render = camera_name

        # Close the window
        self.close()
    
    def render_animation(self):
        # If nothing is selected, just exit
        if self.camera_list.selectedItems() == []:
            self._output = None
            self.close()

        # Get the currently selected camera
        camera_name = self.camera_list.currentItem().text()
        logger.info(f"Animation render requested for: {camera_name}")        

        # Create a response object if needed
        if self._output is None:
            self._output = CameraPickerResponse()
        
        # Set the new active camera
        self._output.camera_for_animation_render = camera_name

        # Close the window
        self.close()

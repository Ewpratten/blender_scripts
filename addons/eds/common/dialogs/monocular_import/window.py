from typing import Optional

import tempfile
import subprocess
import os
from eds.common.qt.qt_window_center import center_window
from ...qt.qt_lines import QHLine
from PySide2 import QtWidgets
from PySide2.QtCore import Qt
import pkgutil
import shutil
import logging
logger = logging.getLogger("eds.dialogs")


class MonocularOutputs:
    depth_map_texture_location: str
    primary_texture_location: str
    tempdir = None


class MonocularImportWindow(QtWidgets.QWidget):

    _output = None

    def __init__(self, parent=None):
        super(MonocularImportWindow, self).__init__(parent)

        # Configure the window's display settings
        self.setWindowFlags(
            self.windowFlags() ^ Qt.WindowStaysOnTopHint ^ Qt.Window)
        self.setWindowTitle("Import Monocular Image")
        self.resize(300, 400)
        center_window(self)

        # Set the root of the application to be a vertical list
        self.setLayout(QtWidgets.QVBoxLayout())

        # Load the stylesheet for this app
        stylesheet = pkgutil.get_data(__name__, "../dialog.css")
        self.setStyleSheet(stylesheet.decode("utf-8"))

        # Configure the title at the top of the window
        self.label = QtWidgets.QLabel("Import Monocular Image")
        self.label.setProperty('labelClass', 'label-title')
        self.subtitle = QtWidgets.QLabel(
            "This tool converts a monocular image to a 3D object.")
        self.layout().addWidget(self.label)
        self.layout().addWidget(self.subtitle)
        self.layout().addWidget(QHLine())

        # Add an import button
        self.import_button = QtWidgets.QPushButton("Select input image")
        self.import_button.clicked.connect(self.import_monocular_image)
        self.layout().addWidget(self.import_button)

        # Add a divider
        self.layout().addWidget(QHLine())

        # Add a dropdown to select the desired complexity
        self.complexity_layout = QtWidgets.QHBoxLayout()
        self.complexity_label = QtWidgets.QLabel("Model complexity")
        self.complexity_layout.addWidget(self.complexity_label)
        self.complexity_dropdown = QtWidgets.QComboBox()
        self.complexity_dropdown.addItem("High")
        self.complexity_dropdown.addItem("Medium")
        self.complexity_dropdown.addItem("Low")
        self.complexity_layout.addWidget(self.complexity_dropdown)
        self.layout().addLayout(self.complexity_layout)

        # Add an option to force CPU compute
        self.force_cpu_button = QtWidgets.QCheckBox("Force CPU compute")
        self.force_cpu_button.setChecked(False)
        self.layout().addWidget(self.force_cpu_button)

        # Add a divider
        self.layout().addWidget(QHLine())

        # Add a read-only text box to display the output of the background task
        self.output_text = QtWidgets.QTextEdit()
        self.output_text.setReadOnly(True)
        self.layout().addWidget(self.output_text)

        # Add space at the bottom in case window size is wrong
        self.layout().addStretch()

        # Add a button to start the process
        self.start_button = QtWidgets.QPushButton("Process and Import")
        self.start_button.clicked.connect(self.process_image)
        self.start_button.setEnabled(False)
        self.layout().addWidget(self.start_button)

        # Quickly check to ensure this device can actually run the tool
        if not self.check_device_capabilities():
            self.import_button.setEnabled(False)
            self.complexity_dropdown.setEnabled(False)
            self.force_cpu_button.setEnabled(False)
            self.start_button.setEnabled(False)
            self.output_text.setText(
                "Docker must be installed to run this tool.")

    def get_output(self) -> Optional[MonocularOutputs]:
        return self._output

    def check_device_capabilities(self) -> bool:
        # Check for either `docker` or `nvidia-docker` in the system path
        return shutil.which("docker") is not None or shutil.which("nvidia-docker") is not None

    def import_monocular_image(self):
        # (re)set the outputs
        self._output = MonocularOutputs()

        # Open a file picker to search for the desired image
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Image Files (*.png *.jpg *.jpeg)")
        file_dialog.setViewMode(QtWidgets.QFileDialog.Detail)
        file_dialog.setLabelText(QtWidgets.QFileDialog.Accept, "Import")
        file_dialog.setLabelText(QtWidgets.QFileDialog.Reject, "Cancel")
        file_dialog.setWindowTitle("Import Monocular Image")
        file_dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)

        # If the user selected an image, import it
        if file_dialog.exec_():
            self._output.primary_texture_location = file_dialog.selectedFiles()[
                0]
            logger.info(
                f"Selected base image: {self._output.primary_texture_location}")
            self.output_text.setText(
                f"Loaded: {self._output.primary_texture_location}")
            self.start_button.setEnabled(True)
        else:
            logger.warning("No image selected")
            return

    def process_image(self):
        logger.info("Begining to process selected image")

        # Add more info to the output
        self.output_text.setText(self.output_text.toPlainText(
        ) + "\nBegining image processing...\n\nWindow will close when complete.")
        self.output_text.repaint()

        # Determine which docker binary we should use
        docker_binary = shutil.which("nvidia-docker") or shutil.which("docker")
        logger.debug(f"Using docker binary: {docker_binary}")

        # Get the execution parameters
        model_complexity = self.complexity_dropdown.currentText()
        force_cpu = self.force_cpu_button.isChecked()
        logger.info(f"Model complexity: {model_complexity}")
        logger.info(f"Force CPU compute: {force_cpu}")

        # Make a temporary directory to work in
        temp_dir = tempfile.mkdtemp()
        logger.debug(f"Working in temporary directory: {temp_dir}")
        os.mkdir(os.path.join(temp_dir, "input"))
        os.mkdir(os.path.join(temp_dir, "output"))

        # Copy the input image to the temporary directory
        temp_input_image_path = os.path.join(
            temp_dir, "input", os.path.basename(self._output.primary_texture_location))
        logger.debug(
            f"Copying input image to temporary directory: {temp_input_image_path}")
        shutil.copy(self._output.primary_texture_location,
                    temp_input_image_path)

        # Convert model complexity to their real values
        model_complexity_map = {
            "High": "DPT_Large",
            "Medium": "DPT_Hybrid",
            "Low": "MiDaS_small"
        }

        # Use docker to process the image
        logger.debug("Running sub-task in docker")
        docker_command = [
            docker_binary,
            "run",
            "-it",
            "-v",
            f"{temp_dir}/input:/input",
            "-v",
            f"{temp_dir}/output:/output",
            "-v",
            "midas_cache:/root/.cache",
            "-e",
            f"MIDAS_MODEL={model_complexity_map[model_complexity]}",
        ]
        if force_cpu:
            docker_command.append("-e")
            docker_command.append("FORCE_CPU_COMPUTE=true")
        docker_command.append("ewpratten/midas-depth-solver")
        logger.debug(f"Docker command: {docker_command}")

        # Run the docker command
        docker_process = subprocess.run(docker_command)

        # Save the generated depth map to the output
        depth_map_path = os.path.join(
            temp_dir, "output", os.path.basename(self._output.primary_texture_location))
        logger.debug(f"Saved depth map to: {depth_map_path}")
        self._output.depth_map_texture_location = depth_map_path

        # Exit
        logger.info("Finished processing image")
        self._output.tempdir = temp_dir
        self.close()

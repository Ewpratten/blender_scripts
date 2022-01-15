from eds.common.apps.preflight.preflight_check import PreflightCheck, PreflightCheckResult

import bpy

class PreflightCheckHasCamera(PreflightCheck):
    """Checks if there is a camera in the scene"""

    def __init__(self):
        super().__init__(True)

    def run_check(self) -> PreflightCheckResult:
        """Runs the check and returns the result"""
        if bpy.context.scene.camera is None:
            return PreflightCheckResult(success=False)
        else:
            return PreflightCheckResult(success=True)

    def run_fix(self, result: PreflightCheckResult) :
        """Tries to auto-fix the check"""
        if result.success:
            return
        else:
            # Create a new camera
            bpy.ops.object.camera_add()

            # Set the camera to be the active camera
            bpy.context.scene.camera = bpy.context.object

            # Set the camera's name
            bpy.context.object.name = "Camera"

    def get_name(self) -> str:
        """Returns the name of the check"""
        return "Check for a camera"
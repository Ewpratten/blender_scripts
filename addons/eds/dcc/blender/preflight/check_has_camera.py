from eds.common.apps.preflight.preflight_check import PreflightCheck, PreflightCheckResult

import bpy
import math

class PreflightCheckHasCamera(PreflightCheck):
    """Checks if there is a camera in the scene"""

    def __init__(self):
        super().__init__(True)

    def run_check(self) -> PreflightCheckResult:
        """Runs the check and returns the result"""
        for object in bpy.context.scene.objects:
            if object.type == 'CAMERA':
                return PreflightCheckResult(success=True)
        return PreflightCheckResult(success=False)

    def run_fix(self, result: PreflightCheckResult) :
        """Tries to auto-fix the check"""
        if result.success:
            return
        else:
            # Create a new camera
            bpy.ops.object.camera_add()

            # Set the camera to be the active camera
            bpy.context.scene.camera = bpy.context.object

            # Rotate the camera to be looking down the +Y axis
            bpy.context.object.rotation_euler = (math.radians(90), 0, 0)

            # Set the camera's name
            bpy.context.object.name = "Camera"

    def get_name(self) -> str:
        """Returns the name of the check"""
        return "Scene has camera"
from eds.common.apps.preflight.preflight_check import PreflightCheck, PreflightCheckResult

import bpy

class PreflightCheckSceneHasActiveCamera(PreflightCheck):
    """Checks if there is an active camera in the scene"""

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
            
            # Get the first camera in the scene and make it the active camera
            for object in bpy.context.scene.objects:
                if object.type == 'CAMERA':
                    bpy.context.scene.camera = object
                    break

    def get_name(self) -> str:
        """Returns the name of the check"""
        return "Scene has active camera"
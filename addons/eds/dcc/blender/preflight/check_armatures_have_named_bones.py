from eds.common.apps.preflight.preflight_check import PreflightCheck, PreflightCheckResult

import bpy
import logging
logger = logging.getLogger("eds.preflight")


class PreflightCheckArmaturesHaveNamedBones(PreflightCheck):
    """Checks if all armatures have named bones (not just Bone.xxx)"""

    def __init__(self):
        super().__init__(False)

    def run_check(self) -> PreflightCheckResult:
        """Runs the check and returns the result"""
        
        for object in bpy.data.objects:
            if object.type == 'ARMATURE':
                logger.debug("Checking armature: %s", object.name)

                for bone in object.data.bones:
                    logger.debug("Checking bone: %s", bone.name)

                    if bone.name.startswith('Bone.') or bone.name == 'Bone':
                        return PreflightCheckResult(success=False)
        return PreflightCheckResult(success=True)

    def run_fix(self, result: PreflightCheckResult):
        pass

    def get_name(self) -> str:
        """Returns the name of the check"""
        return "Armatures have named bones"

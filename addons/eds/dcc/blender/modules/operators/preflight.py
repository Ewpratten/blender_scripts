
from eds.dcc.blender.module import BlenderModule
from eds.common.apps.preflight import launch_preflight

import bpy
import logging
logger = logging.getLogger("eds.blender")


class ModuleOperatorPreflightLaunch(BlenderModule):
    """This operator will launch the preflight tool"""

    class PreflightToolLaunchOperator(bpy.types.Operator):
        bl_idname = "scene.launch_preflight"
        bl_label = "Launch Preflight"

        def execute(self, context):
            logger.info("Launching preflight tool")
            launch_preflight()
            return {"FINISHED"}

    def register_blender_module(self):
        bpy.utils.register_class(
            ModuleOperatorPreflightLaunch.PreflightToolLaunchOperator)

    def unregister_blender_module(self):
        bpy.utils.unregister_class(
            ModuleOperatorPreflightLaunch.PreflightToolLaunchOperator)

    def get_name(self):
        return "Launch Preflight Tool"

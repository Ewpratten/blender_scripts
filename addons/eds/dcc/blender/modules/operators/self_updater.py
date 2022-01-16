
from eds.common.apps.updater import launch_self_updater
from eds.dcc.blender.module import BlenderModule

import bpy
import logging
logger = logging.getLogger("eds.blender")


class ModuleOperatorSelfUpdaterLaunch(BlenderModule):
    """This operator will launch the preflight tool"""

    class SelfUpdaterLaunchOperator(bpy.types.Operator):
        bl_idname = "scene.launch_self_updater"
        bl_label = "Launch Updater"

        def execute(self, context):
            logger.info("Launching self-update tool")
            launch_self_updater()
            return {"FINISHED"}

    def register_blender_module(self):
        bpy.utils.register_class(
            ModuleOperatorSelfUpdaterLaunch.SelfUpdaterLaunchOperator)

    def unregister_blender_module(self):
        bpy.utils.unregister_class(
            ModuleOperatorSelfUpdaterLaunch.SelfUpdaterLaunchOperator)

    def get_name(self):
        return "Launch Self-Update Tool"

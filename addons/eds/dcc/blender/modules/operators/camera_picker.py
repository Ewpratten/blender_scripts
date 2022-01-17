
from eds.common.apps.updater import launch_self_updater
from eds.common.dialogs.camera_picker import launch_camera_picker
from eds.dcc.blender.module import BlenderModule

import bpy
import logging
logger = logging.getLogger("eds.blender")


class ModuleOperatorCameraPickerLaunch(BlenderModule):
    """This operator will launch the camera picker tool"""

    class CameraPickerLaunchOperator(bpy.types.Operator):
        bl_idname = "scene.launch_camera_picker"
        bl_label = "Camera Picker"
        bl_description = "A tool for working with multiple cameras"

        def execute(self, context):
            logger.info("Launching camera picker tool")

            # Get a list of all cameras in the scene
            cameras = [obj.name for obj in bpy.data.objects if obj.type == "CAMERA"]

            # Launch the picker
            repsonse = launch_camera_picker(cameras)

            # Handle the response being None
            if repsonse is None:
                logger.info("Camera picker was cancelled")
                return {"CANCELLED"}

            # Handle the response being a new active camera
            if repsonse.new_active_camera is not None:
                logger.info(f"Setting active camera to: {repsonse.new_active_camera}")
                bpy.context.scene.camera = bpy.data.objects[repsonse.new_active_camera]

            # Handle the response being a camera for image render
            if repsonse.camera_for_image_render is not None:
                logger.info(f"Rendering image from: {repsonse.camera_for_image_render}")

                # Save the current active camera and set the new one
                active_camera = bpy.context.scene.camera
                bpy.context.scene.camera = bpy.data.objects[repsonse.camera_for_image_render]

                # Build a function that will restore the active camera
                def restore_active_camera():
                    bpy.context.scene.camera = active_camera

                # Render the image
                bpy.ops.render.render('INVOKE_DEFAULT', use_viewport=True)

                # Register a handler to restore the active camera after rendering
                bpy.app.handlers.render_complete.append(lambda scene: restore_active_camera())
                bpy.app.handlers.render_cancel.append(lambda scene: restore_active_camera())

            # Handle the response being a camera for animation render
            if repsonse.camera_for_animation_render is not None:
                logger.info(f"Rendering animation from: {repsonse.camera_for_animation_render}")

                # Save the current active camera and set the new one
                active_camera = bpy.context.scene.camera
                bpy.context.scene.camera = bpy.data.objects[repsonse.camera_for_animation_render]

                # Build a function that will restore the active camera
                def restore_active_camera():
                    bpy.context.scene.camera = active_camera

                # Render the animation
                bpy.ops.render.render('INVOKE_DEFAULT', animation=True, use_viewport=True)

                # Register a handler to restore the active camera after rendering
                bpy.app.handlers.render_complete.append(lambda scene: restore_active_camera())
                bpy.app.handlers.render_cancel.append(lambda scene: restore_active_camera())
            
            return {"FINISHED"}

    def register_blender_module(self):
        bpy.utils.register_class(
            ModuleOperatorCameraPickerLaunch.CameraPickerLaunchOperator)

    def unregister_blender_module(self):
        bpy.utils.unregister_class(
            ModuleOperatorCameraPickerLaunch.CameraPickerLaunchOperator)

    def get_name(self):
        return "Launch Camera picker Tool"

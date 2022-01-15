
import bpy
from bpy.types import Operator
from bpy_extras.object_utils import AddObjectHelper
import math

from eds.dcc.blender.module import BlenderModule


class ModuleAddYAlignedCamera(BlenderModule):
    """This module adds a "Shift+A" item for creating a camera that is aligned to the Y axis"""

    # This is the blender operator itself
    class OBJECT_OT_add_object(Operator, AddObjectHelper):
        """Create a new Camera Object facting +Y"""
        bl_idname = "mesh.add_y_camera"
        bl_label = "Add Camera Object facing +Y"
        bl_options = {'REGISTER', 'UNDO'}

        def execute(self, context):
            print("[+Y Camera] Creating new camera and adding to scene at origin")

            # Create a new camera, facing +Y
            camera_data = bpy.data.cameras.new(name='Y Facing Camera')
            camera_object = bpy.data.objects.new('Camera', camera_data)
            camera_object.rotation_euler[0] = math.radians(90)

            # Add the camera to the scene
            bpy.context.scene.collection.objects.link(camera_object)

            return {'FINISHED'}

    @staticmethod
    def blender_button_add_y_camera(self, context):
        self.layout.operator(
            ModuleAddYAlignedCamera.OBJECT_OT_add_object.bl_idname,
            text="+Y Camera",
            icon='CAMERA_DATA')

    def register_blender_module(self):
        bpy.utils.register_class(ModuleAddYAlignedCamera.OBJECT_OT_add_object)
        bpy.types.VIEW3D_MT_add.append(
            lambda x, y: ModuleAddYAlignedCamera.blender_button_add_y_camera(x, y))

    def unregister_blender_module(self):
        bpy.utils.unregister_class(
            ModuleAddYAlignedCamera.OBJECT_OT_add_object)
        bpy.types.VIEW3D_MT_add.remove(
            lambda x, y: ModuleAddYAlignedCamera.blender_button_add_y_camera(x, y))

    def get_name(self):
        return "Add Y Aligned Camera"

bl_info = {
    "name": "+Y Camera",
    "author": "Evan Pratten <ewpratten@gmail.com>",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Add > +Y Camera",
    "description": "Adds a new camera with 90-degree rotation, facing +Y",
    "category": "Add Camera",
}


import bpy
from bpy.types import Operator
from bpy_extras.object_utils import AddObjectHelper
import math


class OBJECT_OT_add_object(Operator, AddObjectHelper):
    """Create a new Camera Object facting +Y"""
    bl_idname = "mesh.add_y_camera"
    bl_label = "Add Camera Object facing +Y"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        # Create a new camera, facing +Y
        camera_data = bpy.data.cameras.new(name='Y Facing Camera')
        camera_object = bpy.data.objects.new('Camera', camera_data)
        camera_object.rotation_euler[0] = math.radians(90)
        
        # Add the camera to the scene
        bpy.context.scene.collection.objects.link(camera_object)

        return {'FINISHED'}


# Registration
def add_y_camera_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_object.bl_idname,
        text="+Y Camera",
        icon='CAMERA_DATA')


def register():
    bpy.utils.register_class(OBJECT_OT_add_object)
    bpy.types.VIEW3D_MT_add.append(add_y_camera_button)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_object)
    bpy.types.VIEW3D_MT_add.remove(add_y_camera_button)


if __name__ == "__main__":
    register()

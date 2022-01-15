
import bpy

from eds.dcc.blender.module import BlenderModule


class ModuleCameraUtils(BlenderModule):
    """This module adds a "Camera Utils" menu to the object panel for cameras"""

    class CameraUtilsPanel(bpy.types.Panel):
        """Creates a Panel in the Object properties window"""
        bl_label = "Camera Utils"
        bl_idname = "OBJECT_PT_camera_utils"
        bl_space_type = 'PROPERTIES'
        bl_region_type = 'WINDOW'
        bl_context = "object"

        def draw(self, context):
            layout = self.layout

            # Get the current object
            obj = context.object

            # We only want to fill in this panel if the object is a camera, otherwise show a message saying so
            if obj.type != 'CAMERA':
                row = layout.row()
                row.label(text="Only available for cameras", icon='ERROR')
                return
            
            # Add a button for using the mouse to rotate the camera
            row = layout.row()
            row.operator("object.mouse_delta_rotate", text="Mouse Delta Look")

            # row = layout.row()
            # row.label(text="Hello world!", icon='WORLD_DATA')

            # row = layout.row()
            # row.label(text="Active object is: " + obj.name)
            # row = layout.row()
            # row.prop(obj, "name")

            # row = layout.row()
            # row.operator("mesh.primitive_cube_add")

    def register_blender_module(self):
        bpy.utils.register_class(ModuleCameraUtils.CameraUtilsPanel)

    def unregister_blender_module(self):
        bpy.utils.unregister_class(ModuleCameraUtils.CameraUtilsPanel)

    def get_name(self):
        return "Camera Utils Panel"

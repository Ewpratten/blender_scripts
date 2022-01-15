
import bpy
from bpy.props import IntProperty, FloatProperty

from eds.dcc.blender.module import BlenderModule


class ModuleOperatorMouseDeltaRotate(BlenderModule):
    """This operator will delta-rotate an object using the mouse"""

    class MouseDeltaRotateOperator(bpy.types.Operator):
        bl_idname = "object.mouse_delta_rotate"
        bl_label = "Delta-Rotate Object With Mouse"

        # Mouse origins
        mouse_origin_x: IntProperty()
        mouse_origin_y: IntProperty()

        # Object delta origins
        obj_rotation_delta_origin_x: FloatProperty()
        obj_rotation_delta_origin_z: FloatProperty()

        def modal(self, context, event):
            if event.type == 'MOUSEMOVE':

                # Get the mouse X and Y deltas
                mouse_delta_x = event.mouse_x - self.mouse_origin_x
                mouse_delta_y = event.mouse_y - self.mouse_origin_y

                # Set the rotation delta values to match the mouse deltas
                context.object.delta_rotation_euler.x = self.obj_rotation_delta_origin_x + mouse_delta_y * 0.01
                context.object.delta_rotation_euler.z = -1.0 * (self.obj_rotation_delta_origin_z + mouse_delta_x * 0.01)

            # Left click to confirm
            elif event.type == 'LEFTMOUSE':
                return {'FINISHED'}

            # Right click or ESC cancels
            elif event.type in {'RIGHTMOUSE', 'ESC'}:

                # Restore the delta values to their original values
                context.object.delta_rotation_euler.x = self.obj_rotation_delta_origin_x
                context.object.delta_rotation_euler.z = self.obj_rotation_delta_origin_z

                # Signal to blender that the action was cancelled
                return {'CANCELLED'}

            return {'RUNNING_MODAL'}

        def invoke(self, context, event):
            if context.object:

                # Configure the origin values so we know where we started
                self.mouse_origin_x = event.mouse_x
                self.mouse_origin_y = event.mouse_y
                self.obj_rotation_delta_origin_x = context.object.delta_rotation_euler.x
                self.obj_rotation_delta_origin_z = context.object.delta_rotation_euler.z

                context.window_manager.modal_handler_add(self)
                return {'RUNNING_MODAL'}
            else:
                self.report({'WARNING'}, "No active object, could not finish")
                return {'CANCELLED'}

    def register_blender_module(self):
        bpy.utils.register_class(
            ModuleOperatorMouseDeltaRotate.MouseDeltaRotateOperator)

    def unregister_blender_module(self):
        bpy.utils.unregister_class(
            ModuleOperatorMouseDeltaRotate.MouseDeltaRotateOperator)

    def get_name(self):
        return "Mouse Delta Rotation"

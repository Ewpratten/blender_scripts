
import bpy

from eds.dcc.blender.module import BlenderModule


class ModuleEdsTopbar(BlenderModule):
    """This module adds an extensible menu to the editor top bar"""

    class TOPBAR_MT_eds_menu(bpy.types.Menu):
        bl_label = "[EDS]"

        def draw(self, context):
            layout = self.layout
            layout.operator("scene.launch_preflight")
            layout.menu("TOPBAR_MT_eds_material_menu")
            layout.operator("scene.launch_camera_picker")
            layout.separator()
            layout.operator("scene.launch_self_updater")

        def menu_draw(self, context):
            """Drawing entrypoint for the root of this menu structure"""
            self.layout.menu("TOPBAR_MT_eds_menu")



    def register_blender_module(self):
        bpy.utils.register_class(ModuleEdsTopbar.TOPBAR_MT_eds_menu)
        bpy.types.TOPBAR_MT_editor_menus.append(ModuleEdsTopbar.TOPBAR_MT_eds_menu.menu_draw)

    def unregister_blender_module(self):
        bpy.types.TOPBAR_MT_editor_menus.remove(ModuleEdsTopbar.TOPBAR_MT_eds_menu.menu_draw)
        bpy.utils.unregister_class(ModuleEdsTopbar.TOPBAR_MT_eds_menu)

    def get_name(self):
        return "EDS Topbar Menu"

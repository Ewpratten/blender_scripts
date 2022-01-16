
import bpy

from eds.dcc.blender.module import BlenderModule


class ModuleEdsTopbarMaterialLoader(BlenderModule):
    """This module adds a material preset loader to the top bar"""

    class TOPBAR_MT_eds_material_menu(bpy.types.Menu):
        bl_label = "Load Material Preset"
        bl_icon = "MATERIAL"

        def draw(self, context):
            layout = self.layout
            layout.operator("scene.load_nord_material_preset")
            layout.operator("scene.load_miwu_material_preset")
            layout.operator("scene.load_freya_material_preset")


    def register_blender_module(self):
        bpy.utils.register_class(ModuleEdsTopbarMaterialLoader.TOPBAR_MT_eds_material_menu)

    def unregister_blender_module(self):
        bpy.utils.unregister_class(ModuleEdsTopbarMaterialLoader.TOPBAR_MT_eds_material_menu)

    def get_name(self):
        return "EDS Topbar Menu Material Loader"

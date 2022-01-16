NORD_MATERIALS = {
    "Nord 0": 0x2e3440,
    "Nord 1": 0x3b4252,
    "Nord 2": 0x434c5e,
    "Nord 3": 0x4c566a,
    "Nord 4": 0xd8dee9,
    "Nord 5": 0xe5e9f0,
    "Nord 6": 0xeceff4,
    "Nord Teal": 0x8fbcbb,
    "Nord Light Blue": 0x88c0d0,
    "Nord 9": 0x81a1c1,
    "Nord Blue": 0x5e81ac,
    "Nord Red": 0xbf616a,
    "Nord Orange": 0xd08770,
    "Nord Yellow": 0xebcb8b,
    "Nord Green": 0xa3be8c,
    "Nord Purple": 0xb48ead,
}


from .op_load_material_preset import AbstractMaterialLoadOperator
from eds.dcc.blender.module import BlenderModule
from eds.common.utils.hex_rgb import hex_to_rgb

import bpy
import logging
logger = logging.getLogger("eds.blender")


class ModuleLoadMaterialPresetNord(BlenderModule):

    class LoadNordMaterialOperator(AbstractMaterialLoadOperator):
        bl_idname = "scene.load_nord_material_preset"
        bl_label = "Load Nord Materials"

        def __init__(self):
            super().__init__("Nord", NORD_MATERIALS)
        # bl_idname = "scene.load_nord_material_preset"
        # bl_label = "Load Nord Materials"

        # def execute(self, context):
        #     logger.info("Loading the Nord materials")

        #     # For every material name defined, load it
        #     is_first = True
        #     for material_name, material_color in NORD_MATERIALS.items():
        #         logger.info("Loading material: %s", material_name)

        #         # Skip if already created
        #         if material_name in bpy.data.materials:
        #             logger.info("Material already created: %s", material_name)
        #             continue

        #         # Create a new material
        #         material = bpy.data.materials.new(material_name)
        #         # Set the material color
        #         material.diffuse_color = (*hex_to_rgb(material_color), 1.0)

        #         # Add grease pencil version material
        #         material_gp = bpy.data.materials.new(material_name + " (GP)")
        #         bpy.data.materials.create_gpencil_data(material_gp)
        #         material_gp.grease_pencil.color = material.diffuse_color

        #         # Set the first material as world material
        #         if is_first:
        #             bpy.context.scene.world.node_tree.nodes["Background"].inputs[0].default_value = material.diffuse_color
        #             is_first = False


        #     return {"FINISHED"}

    def register_blender_module(self):
        bpy.utils.register_class(
            ModuleLoadMaterialPresetNord.LoadNordMaterialOperator)

    def unregister_blender_module(self):
        bpy.utils.unregister_class(
            ModuleLoadMaterialPresetNord.LoadNordMaterialOperator)

    def get_name(self):
        return "Load Nord Materials"

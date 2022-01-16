
from eds.common.utils.hex_rgb import hex_to_rgb
from eds.dcc.blender.module import BlenderModule
from .op_load_material_preset import AbstractMaterialLoadOperator

import bpy
import logging
logger = logging.getLogger("eds.blender")

class ModuleLoadMaterialPresetNord(BlenderModule):

    class LoadNordMaterialOperator(AbstractMaterialLoadOperator):
        bl_idname = "scene.load_nord_material_preset"
        bl_label = "Load Nord Materials"

        def __init__(self):
            super().__init__("Nord", {
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
            })

    def register_blender_module(self):
        bpy.utils.register_class(
            ModuleLoadMaterialPresetNord.LoadNordMaterialOperator)

    def unregister_blender_module(self):
        bpy.utils.unregister_class(
            ModuleLoadMaterialPresetNord.LoadNordMaterialOperator)

    def get_name(self):
        return "Load Nord Materials"

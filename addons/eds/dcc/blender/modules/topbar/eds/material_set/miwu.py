
from eds.common.utils.hex_rgb import hex_to_rgb
from eds.dcc.blender.module import BlenderModule
from .op_load_material_preset import AbstractMaterialLoadOperator

import bpy
import logging
logger = logging.getLogger("eds.blender")


class ModuleLoadMaterialPresetMiwu(BlenderModule):

    class LoadMiwuMaterialOperator(AbstractMaterialLoadOperator):
        bl_idname = "scene.load_miwu_material_preset"
        bl_label = "Load Miwu Materials"

        def __init__(self):
            super().__init__("Miwu", {
                "Miwu Pale White": 0xf0decd,
                "Miwu White": 0xf9ede4,
                "Miwu Brown": 0x6a4937,
                "Miwu Blue": 0x6a7974,
                "Miwu Red-Brown": 0xae6543,
                "Miwu Green": 0xa7926b,
                "Miwu Tan": 0xe7b482,
                "Miwu Dark Brown": 0x523c30,
                "Miwu Pale Pink": 0xeaae90,
                "Miwu Orange": 0xdf805c,
                "Miwu Light Blue": 0x96aaa2,
                "Miwu Pink": 0xd394a3,
                "Miwu Pink-Red": 0xd66e5e,
                "Miwu Red": 0xb76347,
                "Miwu Grey Blue": 0xb3bbb6
            })

    def register_blender_module(self):
        bpy.utils.register_class(
            ModuleLoadMaterialPresetMiwu.LoadMiwuMaterialOperator)

    def unregister_blender_module(self):
        bpy.utils.unregister_class(
            ModuleLoadMaterialPresetMiwu.LoadMiwuMaterialOperator)

    def get_name(self):
        return "Load Miwu Materials"

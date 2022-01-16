
from eds.common.utils.hex_rgb import hex_to_rgb
from eds.dcc.blender.module import BlenderModule
from .op_load_material_preset import AbstractMaterialLoadOperator

import bpy
import logging
logger = logging.getLogger("eds.blender")


class ModuleLoadMaterialPresetFreya(BlenderModule):

    class LoadFreyaMaterialOperator(AbstractMaterialLoadOperator):
        bl_idname = "scene.load_freya_material_preset"
        bl_label = "Load Freya Materials"

        def __init__(self):
            super().__init__("Freya", {
                "Freya Black": 0x191919,
                "Freya White": 0xfefefe,
                "Freya Red": 0xf91657,
                "Freya Green": 0x10fea9,
                "Freya Blue": 0x31bcfd,
                "Freya Yellow": 0xfee156,
            })

    def register_blender_module(self):
        bpy.utils.register_class(
            ModuleLoadMaterialPresetFreya.LoadFreyaMaterialOperator)

    def unregister_blender_module(self):
        bpy.utils.unregister_class(
            ModuleLoadMaterialPresetFreya.LoadFreyaMaterialOperator)

    def get_name(self):
        return "Load Freya Materials"

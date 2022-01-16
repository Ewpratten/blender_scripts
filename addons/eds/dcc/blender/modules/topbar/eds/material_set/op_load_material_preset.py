"""This file contains an abstract operator for loading material presets."""

import bpy
import logging
logger = logging.getLogger("eds.blender")


class AbstractMaterialLoadOperator(bpy.types.Operator):
    """To be implemented by the material preset classes."""

    def __init__(self, theme_name: str, material_set: dict):
        self.material_set = material_set
        self.theme_name = theme_name

    def execute(self, context):
        logger.info(f"Loading the {self.theme_name} material preset")

        # # For every material name defined, load it
        # is_first = True
        # for material_name, material_color in NORD_MATERIALS.items():
        #     logger.info("Loading material: %s", material_name)

        #     # Skip if already created
        #     if material_name in bpy.data.materials:
        #         logger.info("Material already created: %s", material_name)
        #         continue

        #     # Create a new material
        #     material = bpy.data.materials.new(material_name)
        #     # Set the material color
        #     material.diffuse_color = (*hex_to_rgb(material_color), 1.0)

        #     # Add grease pencil version material
        #     material_gp = bpy.data.materials.new(material_name + " (GP)")
        #     bpy.data.materials.create_gpencil_data(material_gp)
        #     material_gp.grease_pencil.color = material.diffuse_color

        #     # Set the first material as world material
        #     if is_first:
        #         bpy.context.scene.world.node_tree.nodes["Background"].inputs[0].default_value = material.diffuse_color
        #         is_first = False

        return {"FINISHED"}

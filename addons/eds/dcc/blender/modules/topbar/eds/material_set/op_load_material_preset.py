"""This file contains an abstract operator for loading material presets."""

from eds.common.dialogs.material_preset_settings import launch_material_preset_settings
from eds.common.utils.hex_rgb import hex_to_rgb

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

        # We need to ask the user how to load the materials
        settings = launch_material_preset_settings(
            self.material_set.keys(), self.theme_name)

        # If the user canceled, we don't do anything
        if settings is None:
            logger.debug("User canceled the material preset settings")
            return {"CANCELLED"}

        # We can now iterate over the material names and load them
        for material_name, material_color in self.material_set.items():
            logger.info("Loading material: %s", material_name)

            # If the user wanted to load this as a "normal material", do that
            if settings.create_regular:

                # Skip if already created
                if material_name in bpy.data.materials:
                    logger.info("Material already created: %s", material_name)
                    continue

                # Create a new material
                material = bpy.data.materials.new(material_name)
                logger.debug("Created material: %s", material_name)
                material.diffuse_color = (*hex_to_rgb(material_color), 1.0)

            # If the user wanted to load this as a grease pencil material, do that
            if settings.create_grease_pencil:

                # We use a different name format to distinguish the grease pencil versions of materials
                material_gp_name = f"{material_name} (GP)"

                # Skip if already created
                if material_gp_name in bpy.data.materials:
                    logger.info("Material already created: %s", material_name)
                    continue

                # Create a new material
                material_gp = bpy.data.materials.new(material_gp_name)
                logger.debug("Created material: %s", material_gp_name)
                bpy.data.materials.create_gpencil_data(material_gp)
                material_gp.grease_pencil.color = (
                    *hex_to_rgb(material_color), 1.0)

        # If the user wanted to set the background, do that
        if settings.world_bg_material:
            logger.info(f"Setting world background to: {settings.world_bg_material}")
            bpy.context.scene.world.node_tree.nodes["Background"].inputs[0].default_value = (
                *hex_to_rgb(self.material_set[settings.world_bg_material]), 1.0)

        return {"FINISHED"}

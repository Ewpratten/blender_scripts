
from eds.common.dialogs.monocular_import import launch_monocular_importer
from eds.dcc.blender.preflight import BLENDER_PREFLIGHT_CHECK_LIST
from eds.dcc.blender.module import BlenderModule
from eds.common.apps.preflight import launch_preflight

import bpy
import logging
import os
import shutil
logger = logging.getLogger("eds.blender")


class ModuleOperatorMonocularDepthImport(BlenderModule):
    """This operator will launch the monocular depth importer tool"""

    class MonocularDepthLaunchOperator(bpy.types.Operator):
        bl_idname = "scene.launch_monocular_depth_import"
        bl_label = "Monocular Extrapolation"
        bl_description = "Imports a 2D image as a 3D object"

        def execute(self, context):
            logger.info("Launching monocular depth tool")

            # Get the solved data from the tool
            data = launch_monocular_importer()

            # If the tool was cancelled, return
            if data is None:
                return {'CANCELLED'}

            # Import the image using images as planes
            logger.info(
                f"Importing base image as plane: {data.primary_texture_location}")
            bpy.ops.import_image.to_plane(shader='SHADELESS', files=[
                                          {'name': data.primary_texture_location}])

            # Subdivide the plane 12 times
            logger.info("Subdividing plane")
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.subdivide(number_cuts=48)
            bpy.ops.object.mode_set(mode='OBJECT')

            # Apply a displace modifier to the plane
            logger.info("Applying displace modifier")
            displace_modifier = bpy.context.active_object.modifiers.new(
                "", 'DISPLACE')
            displace_modifier.strength = 1.0

            # Set the depth map as the displacement map
            logger.info("Setting depth map as displacement map")
            depth_texture = bpy.data.textures.new(
                name=f"Tex_Displace_{os.path.basename(data.depth_map_texture_location)}", type="IMAGE")
            depth_image = bpy.data.images.load(data.depth_map_texture_location)
            depth_texture.image = depth_image
            depth_texture.extension = 'EXTEND'
            displace_modifier.texture_coords = 'UV'
            displace_modifier.texture = depth_texture

            # Tell blender to bring the textures into the project file via "Pack Resources"
            logger.info("Adding texture to project")
            bpy.ops.file.pack_all()

            # Delete the temporary data
            logger.info("Deleting temporary data")
            shutil.rmtree(data.tempdir)

            return {"FINISHED"}

    def register_blender_module(self):
        bpy.utils.register_class(
            ModuleOperatorMonocularDepthImport.MonocularDepthLaunchOperator)

    def unregister_blender_module(self):
        bpy.utils.unregister_class(
            ModuleOperatorMonocularDepthImport.MonocularDepthLaunchOperator)

    def get_name(self):
        return "Launch Monocular Depth Tool"

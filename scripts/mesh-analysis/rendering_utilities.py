####################################################################################################
# Copyright (c) 2020, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of NeuroMorphoVis <https://github.com/BlueBrain/NeuroMorphoVis>
#
# This program is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This Blender-based tool is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
####################################################################################################

# Blender imports
import bpy

# Internal imports
import nmv.scene
import nmv.interface
import nmv.bbox
import nmv.utilities
import nmv.shading
import nmv.rendering


def render_mesh_object(mesh_object,
                       mesh_name,
                       mesh_color,
                       output_directory,
                       resolution=2000):

    # Get the bounding box and compute the unified one, to render the astrocyte in the middle
    mesh_bbox = nmv.bbox.compute_scene_bounding_box_for_meshes()
    mesh_bbox = nmv.bbox.compute_unified_bounding_box(mesh_bbox)

    # Create the illumination
    nmv.shading.create_lambert_ward_illumination()

    # Create a simple shader
    color = mesh_color #nmv.utilities.parse_color_from_argument(mesh_color)
    mesh_material = nmv.shading.create_lambert_ward_material(
        name='mesh-color-%s' % mesh_name, color=color)

    # Assign the wire-frame shader, using an input color
    nmv.shading.set_material_to_object(mesh_object=mesh_object, material_reference=mesh_material)

    # Set the background to WHITE for the compositing
    bpy.context.scene.render.film_transparent = False
    bpy.context.scene.world.color[0] = 10
    bpy.context.scene.world.color[1] = 10
    bpy.context.scene.world.color[2] = 10

    # Render based on the bounding box
    nmv.rendering.render(bounding_box=mesh_bbox,
                         image_directory=output_directory,
                         image_name=mesh_name,
                         image_resolution=resolution,
                         keep_camera_in_scene=True)
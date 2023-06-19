####################################################################################################
# Copyright (c) 2020, EPFL / Blue Brain Project
# Author: Marwan Abdellah <marwan.abdellah@epfl.ch>
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
from mathutils import Vector

# Internal imports
import nmv.scene
import nmv.interface
import nmv.bbox
import nmv.utilities
import nmv.shading
import nmv.rendering
import nmv.enums


####################################################################################################
# @create_area_light_from_bounding_box
####################################################################################################
def create_point_light_from_bounding_box(location):
    """Create an area light source that is above the mesh

    :param location:
        Mesh bounding box.
    :return:
        Reference to the light source
    """

    # Deselect all
    nmv.scene.deselect_all()

    # Create the light source
    bpy.ops.object.light_add(type='POINT', radius=1, location=(0, 0, 0))

    # Get a reference to the light source
    light_reference = nmv.scene.get_active_object()

    # Adjust the position
    light_reference.location = location

    # Adjust the orientation
    light_reference.rotation_euler[0] = 0

    # Adjust the power
    light_reference.data.energy = 1e4

    # Return the light source
    return light_reference


####################################################################################################
# @load_sss_material
####################################################################################################
def load_sss_material(material_name='material',
                      material_color=(1, 1, 1)):

    # Import the material from the library
    material_reference = nmv.shading.import_shader(shader_name='eevee-sss')

    # Rename the material
    material_reference.name = str(material_name)

    # Update the color
    rgb = material_reference.node_tree.nodes["RGB"]
    rgb.outputs[0].default_value[0] = material_color[0]
    rgb.outputs[0].default_value[1] = material_color[1]
    rgb.outputs[0].default_value[2] = material_color[2]

    # Switch the view port shading
    nmv.scene.switch_scene_shading('MATERIAL')

    # Return a reference to the material
    return material_reference


####################################################################################################
# @load_wireframe_material
####################################################################################################
def load_wireframe_material(material_name='material',
                            material_color=(1, 1, 1),
                            thickness=0.025):

    # Import the material from the library
    material_reference = nmv.shading.import_shader(shader_name='wireframe')

    # Rename the material
    material_reference.name = str(material_name)

    # Update the color
    bsdf = material_reference.node_tree.nodes["Diffuse BSDF"]
    bsdf.inputs[0].default_value[0] = material_color[0]
    bsdf.inputs[0].default_value[1] = material_color[1]
    bsdf.inputs[0].default_value[2] = material_color[2]

    # Wireframe
    material_reference.node_tree.nodes["Wireframe"].inputs[0].default_value = thickness

    # Return a reference to the material
    return material_reference


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


####################################################################################################
# @render_mesh_with_lambert_shader
####################################################################################################
def render_mesh_with_lambert_shader(mesh_object,
                                    output_directory,
                                    mesh_color,
                                    resolution=4000,
                                    camera_view=nmv.enums.Camera.View.FRONT,
                                    add_scale_bar=True):

    # Construct a default mesh material
    mesh_material = nmv.shading.create_lambert_ward_material(name='mesh_material', color=mesh_color)

    # Assign the material
    nmv.shading.set_material_to_object(mesh_object=mesh_object, material_reference=mesh_material)

    # Add lambert illumination
    nmv.shading.create_lambert_ward_illumination()

    # Get the bounding box and compute the unified one, to render the astrocyte in the middle
    mesh_bbox = nmv.bbox.compute_scene_bounding_box_for_meshes()

    # Draw the scale bar
    if add_scale_bar:
        nmv.interface.draw_scale_bar(
            bounding_box=mesh_bbox, view=camera_view, material_type=nmv.enums.Shader.LAMBERT_WARD)

    # Nice material
    bpy.context.scene.display.shading.light = 'MATCAP'
    bpy.context.scene.display.shading.studio_light = 'basic_side.exr'

    # Render based on the bounding box
    nmv.rendering.render(bounding_box=mesh_bbox,
                         camera_view=camera_view,
                         image_directory=output_directory,
                         image_name=mesh_object.name,
                         image_resolution=resolution,
                         keep_camera_in_scene=True)


####################################################################################################
# @render_mesh_with_wireframe_shader
####################################################################################################
def render_mesh_with_wireframe_shader(mesh_object,
                                      output_directory,
                                      mesh_color,
                                      resolution=4000,
                                      camera_view=nmv.enums.Camera.View.FRONT,
                                      wireframe_thickness=0.025,
                                      add_scale_bar=False):

    # Load the material
    mesh_material = load_wireframe_material(
        material_name='mesh_material', material_color=mesh_color, thickness=wireframe_thickness)

    # Assign the material
    nmv.shading.set_material_to_object(mesh_object=mesh_object, material_reference=mesh_material)

    # Add lambert illumination
    nmv.shading.create_lambert_ward_illumination()

    # Get the bounding box and compute the unified one, to render the astrocyte in the middle
    mesh_bbox = nmv.bbox.compute_scene_bounding_box_for_meshes()

    # Light location
    light_location = Vector((mesh_bbox.center[0],
                             mesh_bbox.center[1],
                             mesh_bbox.center[2] + mesh_bbox.bounds[2] * 0.7))
    create_point_light_from_bounding_box(light_location)

    # Draw the scale bar
    if add_scale_bar:
        nmv.interface.draw_scale_bar(
            bounding_box=mesh_bbox, view=camera_view, material_type=nmv.enums.Shader.LAMBERT_WARD)

    # Switch to EEVEE
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'

    # Render based on the bounding box
    nmv.rendering.render(bounding_box=mesh_bbox,
                         camera_view=camera_view,
                         image_directory=output_directory,
                         image_name=mesh_object.name,
                         image_resolution=resolution,
                         keep_camera_in_scene=True)

####################################################################################################
# Copyright (c) 2020 - 2024, EPFL / Blue Brain Project
# Author(s): Marwan Abdellah <marwan.abdellah@epfl.ch>
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
import nmv.bbox
import nmv.enums
import nmv.consts
import nmv.scene
import nmv.interface
import nmv.rendering


####################################################################################################
# @enable_transparency
####################################################################################################
def enable_transparency(alpha=0.5):

    bpy.context.scene.display.shading.light = 'FLAT'
    bpy.context.scene.display.shading.show_xray = True
    bpy.context.scene.display.shading.xray_alpha = alpha


####################################################################################################
# @disable_transparency
####################################################################################################
def disable_transparency():
    bpy.context.scene.display.shading.show_xray = False


####################################################################################################
# @set_rendering_mode
####################################################################################################
def set_rendering_mode(mode):

    if mode == 'FLAT':
        bpy.context.scene.display.shading.light = 'FLAT'
    else:
        if mode == 'DEFAULT':
            bpy.context.scene.display.shading.light = 'STUDIO'
        else:
            bpy.context.scene.display.shading.light = 'MATCAP'
            if mode == 'TOON':
                bpy.context.scene.display.shading.studio_light = 'toon.exr'
            elif mode == 'CERAMIC':
                bpy.context.scene.display.shading.studio_light = 'ceramic_lightbulb.exr'
            elif mode == 'NORMALS':
                bpy.context.scene.display.shading.studio_light = 'check_normal+y.exr'
            elif mode == 'PEARL':
                bpy.context.scene.display.shading.studio_light = 'pearl.exr'
            elif mode == 'SHADED':
                bpy.context.scene.shading.studio_light = 'check_rim_dark.exr'
            else:
                bpy.context.scene.display.shading.light = 'STUDIO'


####################################################################################################
# @center_scene
####################################################################################################
def center_scene(view='TOP'):

    # Select all the meshes in the scene
    nmv.scene.select_all_meshes_in_scene()

    # Adjust the clipping plane
    for a in bpy.context.screen.areas:
        if a.type == 'VIEW_3D':
            for s in a.spaces:
                if s.type == 'VIEW_3D':
                    s.clip_end = 1e5

    # Ensure there's an active 3D Viewport
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            context = bpy.context.copy()
            context['area'] = area
            context['region'] = area.regions[-1]
            bpy.ops.view3d.view_selected(context)

    # Center the scene
    area_type = 'VIEW_3D'
    areas = [area for area in bpy.context.window.screen.areas if area.type == area_type]
    with bpy.context.temp_override(
            window=bpy.context.window,
            area=areas[0],
            region=[region for region in areas[0].regions if region.type == 'WINDOW'][0],
            screen=bpy.context.window.screen):
        bpy.ops.view3d.view_axis(type=view, align_active=True)


####################################################################################################
# @set_rendering_mode
####################################################################################################
def set_flat_rendering_mode():
    set_rendering_mode(mode='FLAT')


####################################################################################################
# @set_rendering_mode
####################################################################################################
def set_toon_rendering_mode():
    set_rendering_mode(mode='TOON')


####################################################################################################
# @set_rendering_mode
####################################################################################################
def set_ceramic_rendering_mode():
    set_rendering_mode(mode='CERAMIC')


####################################################################################################
# @set_rendering_mode
####################################################################################################
def set_normals_rendering_mode():
    set_rendering_mode(mode='NORMALS')


####################################################################################################
# @set_rendering_mode
####################################################################################################
def set_pearl_rendering_mode():
    set_rendering_mode(mode='PEARL')


####################################################################################################
# @set_rendering_mode
####################################################################################################
def set_shaded_rendering_mode():
    set_rendering_mode(mode='SHADED')


####################################################################################################
# @render_scene
####################################################################################################
def render_scene(images_directory,
                 image_name,
                 bounding_box=None,
                 edge_gap_percentage=0.1,
                 resolution_scale_factor=10,
                 material=nmv.enums.Shader.LAMBERT_WARD,
                 render_scale_bar=False,
                 delete_scale_bar=True):

    # Compute the scene bounding box
    if bounding_box is None:
        bounding_box = nmv.bbox.compute_scene_bounding_box_for_meshes()

        # Add a slight space to be able to see the largest bounding box
        delta = bounding_box.p_max - bounding_box.p_min
        bounding_box.p_min = bounding_box.p_min - 0.5 * edge_gap_percentage * delta
        bounding_box.p_max = bounding_box.p_max + 0.5 * edge_gap_percentage * delta
        bounding_box.bounds = bounding_box.bounds + edge_gap_percentage * delta

    # Draw the morphology scale bar
    scale_bar = None
    if render_scale_bar:
        scale_bar = nmv.interface.draw_scale_bar(
            bounding_box=bounding_box,
            material_type=material,
            view=nmv.enums.Camera.View.FRONT)

    # Render to scale
    nmv.rendering.render_to_scale(
        bounding_box=bounding_box,
        camera_view=nmv.enums.Camera.View.FRONT,
        image_scale_factor=resolution_scale_factor,
        image_name=image_name,
        image_directory=images_directory,
        keep_camera_in_scene=False)

    # Delete the scale bar, if rendered
    if scale_bar is not None and delete_scale_bar:
        nmv.scene.delete_object_in_scene(scene_object=scale_bar)

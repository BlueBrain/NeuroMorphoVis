####################################################################################################
# Copyright (c) 2025, Open Brain Institute
# Author(s): Marwan Abdellah <marwan.abdellah@openbraininstitute.org>
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

import bpy
import mathutils
import numpy as np 
import os 

####################################################################################################
# @create_camera
####################################################################################################
def create_camera(resolution=1024, 
                  camera_name="OrthoCamera", 
                  square_resolution=False):
    # Delete existing camera with the same name
    if camera_name in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects[camera_name], do_unlink=True)

    # Get all mesh objects
    mesh_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']

    if not mesh_objects:
        print("No mesh objects in the scene.")
        return None

    # Compute global bounding box
    min_corner = mathutils.Vector((float('inf'),) * 3)
    max_corner = mathutils.Vector((float('-inf'),) * 3)

    for obj in mesh_objects:
        for corner in obj.bound_box:
            world_corner = obj.matrix_world @ mathutils.Vector(corner)
            min_corner = mathutils.Vector(map(min, min_corner, world_corner))
            max_corner = mathutils.Vector(map(max, max_corner, world_corner))

    center = (min_corner + max_corner) * 0.5
    size = max_corner - min_corner

    # Determine ortho scale (fit X and Y)
    ortho_scale = max(size.x, size.y)

    # Create orthographic camera
    cam_data = bpy.data.cameras.new(name=camera_name)
    cam_data.type = 'ORTHO'
    cam_data.ortho_scale = ortho_scale

    cam_obj = bpy.data.objects.new(camera_name, cam_data)
    bpy.context.collection.objects.link(cam_obj)

    # Position the camera above the center and look down -Z (top-down)
    cam_height = size.z + 1.0  # 1 unit above the bounding box
    cam_obj.location = (center.x, center.y, max_corner.z + cam_height)
    cam_obj.data.clip_end = 100000


    
    # Set this camera as active
    bpy.context.scene.camera = cam_obj
 
    # Set render resolution proportionally
    if square_resolution:
        bpy.context.scene.render.resolution_y = resolution
        bpy.context.scene.render.resolution_x = resolution
    else:
        
        aspect_x = size.x
        aspect_y = size.y
        if aspect_x > aspect_y:
            bpy.context.scene.render.resolution_x = resolution
            bpy.context.scene.render.resolution_y = int(resolution * (aspect_y / aspect_x))
        else:
            bpy.context.scene.render.resolution_y = resolution
            bpy.context.scene.render.resolution_x = int(resolution * (aspect_x / aspect_y))

        return cam_obj

####################################################################################################
# @render_scene_to_png
####################################################################################################
def render_scene_to_png(filepath, add_white_background=False, add_shadow=False):
    
    # Ensure correct file format and transparency settings
    scene = bpy.context.scene
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'  # Enable alpha
    
    if add_white_background:
        scene.render.film_transparent = False  # Make background opaque

        # Set world background to white
        world = scene.world
        if not world:
            world = bpy.data.worlds.new("World")
            scene.world = world
        world.use_nodes = False  # Disable nodes for simplicity
        world.color = (1.0, 1.0, 1.0)  # RGB white
    else:
        
        scene.render.film_transparent = True  # Needed for transparent background

        # Optional: turn off overlays and set shading to render mode
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.shading.type = 'RENDERED'
                        space.shading.show_shadows = False  # or False
                break

    # Set output filepath (ensure absolute path)
    filepath = os.path.abspath(filepath)
    scene.render.filepath = filepath

    # Render the image
    bpy.ops.render.render(write_still=True)

    print(f"Image rendered and saved to: {filepath}")
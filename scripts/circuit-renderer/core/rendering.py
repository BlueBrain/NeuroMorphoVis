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
# @enable_effects
####################################################################################################
def enable_effects(shadows=True, outline=True):
    
    # Set the render engine to Workbench
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_WORKBENCH'
    print("Render engine set to Workbench.")

    # Configure Workbench shadow settings
    scene.display.shading.show_shadows = shadows
    scene.display.shading.shadow_intensity = 0.5  # Adjust shadow strength (0.0 to 1.0)
    
    # Configure Workbench outline settings
    scene.display.shading.show_object_outline = outline
    scene.display.shading.object_outline_color = (0.0, 0.0, 0.0)  # Black outline (RGB, 0.0 to 1.0)
    
    # Access the 3D Viewport's space data and enable shadows
    viewport_found = False
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            space = area.spaces.active
            space.shading.show_shadows = shadows
            space.shading.show_object_outline = outline
            space.shading.object_outline_color = (0.0, 0.0, 0.0)  # Black outline

            space.shading.type = 'RENDERED'  # Ensure viewport uses Workbench rendering
            viewport_found = True
            print("Shadows enabled in 3D Viewport shading settings.")
            break

    if not viewport_found:
        print("Error: No 3D Viewport found in the current screen layout.")

    # Force viewport redraw to update the scene
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            area.tag_redraw()
            print("Viewport redrawn.")

    # Ensure a light source exists for shadows
    if not any(obj.type == 'LIGHT' for obj in scene.objects):
        bpy.ops.object.light_add(type='SUN')
        print("Added a Sun light to enable shadows.")
        
####################################################################################################
# @create_camera
####################################################################################################
import bpy
import mathutils

def create_camera(resolution=1024,
                  pmin=None, pmax=None,
                  camera_name="Camera",
                  aspect_ratio="1:1",
                  padding=1.05):
    """
    Create a top-down orthographic camera that frames all visible mesh objects
    according to a user-specified aspect ratio.

    Parameters:
        resolution (int): Base resolution (width or height depending on aspect).
        pmin, pmax (tuple): Optional bounding box override (min, max corners).
        camera_name (str): Name of the camera.
        aspect_ratio (str): Desired aspect ratio, e.g., "16:9", "1:1", "3:2".
        padding (float): Optional padding factor to avoid tight framing.
    """
    # Delete existing camera with the same name
    if camera_name in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects[camera_name], do_unlink=True)

    # Parse aspect ratio string
    try:
        aspect_x, aspect_y = map(float, aspect_ratio.strip().split(":"))
        image_aspect = aspect_x / aspect_y
        print(f"[create_camera] Aspect ratio set to {aspect_x}:{aspect_y}.")
    except Exception:
        print(f"[create_camera] Invalid aspect ratio format '{aspect_ratio}'. "
              "Expected format 'width:height' (e.g., '16:9').")
        return None

    # Compute scene bounding box
    if pmin is None or pmax is None:
        mesh_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
        if not mesh_objects:
            print("[create_camera] No mesh objects in the scene.")
            return None

        min_corner = mathutils.Vector((float('inf'),) * 3)
        max_corner = mathutils.Vector((float('-inf'),) * 3)

        for obj in mesh_objects:
            for corner in obj.bound_box:
                world_corner = obj.matrix_world @ mathutils.Vector(corner)
                min_corner = mathutils.Vector(map(min, min_corner, world_corner))
                max_corner = mathutils.Vector(map(max, max_corner, world_corner))
    else:
        min_corner = mathutils.Vector(pmin)
        max_corner = mathutils.Vector(pmax)

    center = (min_corner + max_corner) * 0.5
    size = max_corner - min_corner
    scene_width = size.x
    scene_height = size.y

    # Compute ortho scale to preserve full scene with aspect ratio
    scene_aspect = scene_width / scene_height
    if scene_aspect > image_aspect:
        # Scene is wider than desired image: fit width, extend height
        ortho_scale = (scene_width / image_aspect)
    else:
        # Scene is taller or equal: fit height directly
        ortho_scale = scene_height

    ortho_scale *= padding  # Add optional margin

    # Create orthographic camera
    cam_data = bpy.data.cameras.new(name=camera_name)
    cam_data.type = 'ORTHO'
    cam_data.ortho_scale = ortho_scale

    cam_obj = bpy.data.objects.new(camera_name, cam_data)
    bpy.context.collection.objects.link(cam_obj)

    # Position camera above the center and look down
    cam_height = size.z + 1.0
    cam_obj.location = (center.x, center.y, max_corner.z + cam_height)
    cam_obj.rotation_euler = (0, 0, 0)  # Pointing -Z in Blender's default orientation
    cam_data.clip_end = 1e5

    # Set as active camera
    bpy.context.scene.camera = cam_obj

    # Apply render resolution based on aspect ratio
    bpy.context.scene.render.resolution_x = resolution
    bpy.context.scene.render.resolution_y = int(resolution * (aspect_y / aspect_x))

    print(f"[create_camera] Camera '{camera_name}' created with resolution "
          f"{bpy.context.scene.render.resolution_x}x{bpy.context.scene.render.resolution_y} "
          f"and ortho scale {ortho_scale:.3f}")

    return cam_obj


####################################################################################################
# @render_scene_to_png
####################################################################################################
def render_scene_to_png(filepath, add_white_background=False, add_shadow=False, add_outline=False):
    
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

    # Enable effects if specified
    enable_effects(shadows=add_shadow, outline=add_outline)
    
    # Set output filepath (ensure absolute path)
    filepath = os.path.abspath(filepath)
    scene.render.filepath = filepath

    # Render the image
    bpy.ops.render.render(write_still=True)

    print(f"Image rendered and saved to: {filepath}")
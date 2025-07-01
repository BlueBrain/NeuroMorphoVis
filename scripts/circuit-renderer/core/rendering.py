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
import bmesh
import mathutils
import os 
from PIL import Image

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
# @draw_bounding_box
####################################################################################################
def draw_bounding_box(pmin, pmax, name="BoundingBox"):
    """
    Draw a wireframe box from pmin to pmax coordinates in the scene.
    """
    # Delete existing object with the same name if it exists
    if name in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects[name], do_unlink=True)

    # Create a new mesh
    mesh = bpy.data.meshes.new(name + "_mesh")
    bm = bmesh.new()

    # Define the 8 corners of the box
    corners = [
        (pmin[0], pmin[1], pmin[2]),  # 0: Bottom-front-left
        (pmax[0], pmin[1], pmin[2]),  # 1: Bottom-front-right
        (pmax[0], pmax[1], pmin[2]),  # 2: Bottom-back-right
        (pmin[0], pmax[1], pmin[2]),  # 3: Bottom-back-left
        (pmin[0], pmin[1], pmax[2]),  # 4: Top-front-left
        (pmax[0], pmin[1], pmax[2]),  # 5: Top-front-right
        (pmax[0], pmax[1], pmax[2]),  # 6: Top-back-right
        (pmin[0], pmax[1], pmax[2])   # 7: Top-back-left
    ]

    # Add vertices to bmesh
    for x, y, z in corners:
        bm.verts.new((x, y, z))

    bm.verts.ensure_lookup_table()

    # Define edges (wireframe connections)
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # Bottom face
        (4, 5), (5, 6), (6, 7), (7, 4),  # Top face
        (0, 4), (1, 5), (2, 6), (3, 7)   # Vertical edges
    ]

    for v1, v2 in edges:
        bm.edges.new((bm.verts[v1], bm.verts[v2]))

    # Convert bmesh to mesh
    bm.to_mesh(mesh)
    bm.free()

    # Create object from mesh
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    # Set object as wireframe
    obj.show_wire = True
    obj.show_all_edges = True
    
####################################################################################################
# @create_camera
####################################################################################################
def create_camera(resolution=1024,
                  pmin=None, pmax=None,
                  camera_name="Camera", 
                  square_aspect=False):
    """
    Create a top-down orthographic camera that frames all visible mesh objects
    according to a user-specified aspect ratio.

    Parameters:
        resolution (int): Base resolution (width or height depending on aspect).
        pmin, pmax (tuple): Optional bounding box override (min, max corners).
        camera_name (str): Name of the camera.
    """
    # Delete existing camera with the same name
    if camera_name in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects[camera_name], do_unlink=True)

    # Compute scene bounding box
    if pmin is None or pmax is None:
        mesh_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
        if not mesh_objects:
            print("[create_camera] No mesh objects in the scene.")
            return None

        depsgraph = bpy.context.evaluated_depsgraph_get()

        min_corner = mathutils.Vector((float('inf'),) * 3)
        max_corner = mathutils.Vector((float('-inf'),) * 3)

        for obj in mesh_objects:
            eval_obj = obj.evaluated_get(depsgraph)
            mesh = eval_obj.to_mesh()

            for vertex in mesh.vertices:
                world_vertex = eval_obj.matrix_world @ vertex.co
                min_corner = mathutils.Vector(map(min, min_corner, world_vertex))
                max_corner = mathutils.Vector(map(max, max_corner, world_vertex))

            eval_obj.to_mesh_clear()
    else:
        min_corner = mathutils.Vector(pmin)
        max_corner = mathutils.Vector(pmax)

    center = (min_corner + max_corner) * 0.5
    size = max_corner - min_corner
    
    # 'FRONT' : bounds[0] & bounds[1]
    orthographic_scale = size[0]
    if orthographic_scale < size[1]:
        orthographic_scale = size[1]

    x_bounds = size[0]
    y_bounds = size[1]

    # Create orthographic camera
    cam_data = bpy.data.cameras.new(name=camera_name)
    cam_data.type = 'ORTHO'
    cam_data.clip_end = 1000000
    cam_data.ortho_scale = orthographic_scale

    cam_obj = bpy.data.objects.new(camera_name, cam_data)
    bpy.context.collection.objects.link(cam_obj)

    # Position the camera above the center and look down -Z (top-down)
    cam_height = size.z + 1.0  # 1 unit above the bounding box
    cam_obj.location = (center.x, center.y, max_corner.z + cam_height)
    cam_obj.data.clip_end = 1e5 # Set a large clip end for visibility
    
    # Set this camera as active
    bpy.context.scene.camera = cam_obj
 
    # Set render resolution proportionally
    if square_aspect:
        bpy.context.scene.render.resolution_x = resolution
        bpy.context.scene.render.resolution_y = resolution
    else:
        
        bpy.context.scene.render.resolution_x = int(resolution * x_bounds / orthographic_scale)
        bpy.context.scene.render.resolution_y = int(resolution * y_bounds / orthographic_scale)

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
    

####################################################################################################
# @adjust_aspect_ratio
####################################################################################################
def adjust_aspect_ratio(image_path, required_aspect_ratio):
    """
    Adjusts the aspect ratio of an image by padding it to match the desired aspect ratio.

    Parameters:
        image_path (str): Path to the input image.
        required_aspect_ratio (str): Desired aspect ratio as a string, e.g., "16:9".
    """
    try:
        width_ratio, height_ratio = map(float, required_aspect_ratio.split(':'))
        required_aspect_ratio_float = width_ratio / height_ratio
    except ValueError:
        print(f"Invalid aspect ratio format: {required_aspect_ratio}. Expected 'width:height'.")
        return

    with Image.open(image_path) as img:
        original_width, original_height = img.size
        current_aspect_ratio = original_width / original_height

        if current_aspect_ratio > required_aspect_ratio_float:
            # Too wide → pad vertically
            new_height = int(round(original_width / required_aspect_ratio_float))
            new_width = original_width
        elif current_aspect_ratio < required_aspect_ratio_float:
            # Too tall → pad horizontally
            new_width = int(round(original_height * required_aspect_ratio_float))
            new_height = original_height
        else:
            # Already correct aspect ratio
            print("Image already matches the required aspect ratio.")
            return

        # Calculate even padding (left/right or top/bottom)
        pad_x = (new_width - original_width)
        pad_y = (new_height - original_height)
        paste_x = pad_x // 2
        paste_y = pad_y // 2

        # Create padded image
        background_color = (255, 255, 255) if img.mode == 'RGBA' else (255, 255, 255)
        new_img = Image.new(img.mode, (new_width, new_height), color=background_color)
        new_img.paste(img, (paste_x, paste_y))
        new_img.save(image_path)

        print(f"Aspect ratio adjusted and saved to: {image_path}")

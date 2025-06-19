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
from mathutils import Vector

import random 
import numpy as np
import matplotlib.pyplot as plt

####################################################################################################
# @generate_random_rgba_colors
####################################################################################################
def generate_random_rgba_colors(n=6, alpha=1.0):
    return [tuple(random.random() for _ in range(3)) + (alpha,) for _ in range(n)]

####################################################################################################
# @generate_random_rgba_colors_with_transparency
####################################################################################################
def generate_random_rgba_colors_with_transparency(n=6):
    return [tuple(random.random() for _ in range(4)) for _ in range(n)]

####################################################################################################
# @clear_scene
####################################################################################################
def clear_scene():
    scene = bpy.context.scene

    # Delete all objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Optionally, remove orphan data-blocks (meshes, materials, etc.)
    # This requires saving & reloading or manually purging
    # bpy.ops.outliner.orphans_purge(do_recursive=True)
    
    # Delete all collections
    for collection in bpy.data.collections:
        bpy.data.collections.remove(collection)

    # Optionally: remove orphan data (meshes, materials, etc.)
    bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

####################################################################################################
# @sample_list_randomly
####################################################################################################
def sample_list_randomly(input_list, n_samples):
    if n_samples > len(input_list):
        sampled_indices = list(range(len(input_list)))
    else:
        sampled_indices = random.sample(range(len(input_list)), n_samples)

    sampled_items = [input_list[i] for i in sampled_indices]
    return sampled_items, sampled_indices

####################################################################################################
# @remove_materials
####################################################################################################
def remove_materials():
    # Remove material slots from all objects
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            obj.data.materials.clear()

    # Remove materials from the data-block
    for material in bpy.data.materials:
        bpy.data.materials.remove(material, do_unlink=True)

####################################################################################################
# @remove_neuron_materials
####################################################################################################
def remove_neuron_materials():
    # Remove material slots from all objects
    for obj in bpy.data.objects:
        if 'FIXED:' in obj.name: continue
        if obj.type == 'MESH':
            obj.data.materials.clear()
    
    # Remove materials from the data-block
    for material in bpy.data.materials:
        if 'FIXED:' in material.name: continue
        bpy.data.materials.remove(material, do_unlink=True)
    
####################################################################################################
# @remove_cross_sections
####################################################################################################   
def remove_cross_sections():        
    # Iterate over all objects in the scene
    for obj in bpy.data.objects:
        if 'Cross Section' in obj.name:
            bpy.data.objects.remove(obj, do_unlink=True)
            
####################################################################################################
# @get_all_meshes_in_scene
####################################################################################################         
def get_all_meshes_in_scene():
    """
    Returns a list of all mesh objects in the current Blender scene.
    """
    return [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']

####################################################################################################
# @get_colors_from_palette
####################################################################################################
def get_colors_from_palette(palette, number_colors=10):
    
    # Get tab10 colormap
    rgb_colors = plt.get_cmap(palette)
    return rgb_colors(np.linspace(0, 1, number_colors))
    
####################################################################################################
# @compute_bounds_from_positions
####################################################################################################
def compute_bounds_from_positions(positions):
    """
    Computes the bounding box from a list of positions.
    
    :param positions: List of (x, y, z) tuples representing positions.
    :return: Tuple of (min_x, min_y, min_z, max_x, max_y, max_z).
    """
    if not positions:
        pmin = Vector((0, 0, 0))
        pmax = Vector((0, 0, 0))  
        return pmin, pmax

    positions = np.array(positions)
    min_coords = np.min(positions, axis=0)
    max_coords = np.max(positions, axis=0)

    pmin = Vector(min_coords)
    pmax = Vector(max_coords)
    
    return pmin, pmax

####################################################################################################
# @parse_colormap_file
####################################################################################################
def parse_colormap_file(file_path):
    """
    Parses a colormap file and returns a list of RGBA colors.
    
    :param file_path: Path to the colormap file.
    :return: List of RGBA colors.
    """
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        colors = []
        for line in lines:
            if line.strip() and not line.startswith('#'):  # Ignore empty lines and comments
                rgba = tuple(map(float, line.strip().split(',')))
                if len(rgba) == 4:  # Ensure it has 4 components (R, G, B, A)
                    colors.append(rgba)
        
        return colors
    except Exception as e:
        raise ValueError(f"Failed to parse colormap file: {e}")

####################################################################################################
# @compute_bounds_from_positions
####################################################################################################
def save_scene_as_blend_file(file_path):
    """
    Saves the current Blender scene to a .blend file.
    
    :param file_path: Path where the .blend file will be saved.
    """
    if not file_path.endswith('.blend'):
        raise ValueError("File path must end with '.blend'")
    
    bpy.ops.wm.save_as_mainfile(filepath=file_path)
    print(f"Scene saved as {file_path}")
    
####################################################################################################
# @get_neurons_colors
####################################################################################################
def get_neurons_colors(options, number_neurons):
    """
    Returns a list of colors based on the options provided.
    
    :param options: Options object containing color settings.
    :return: List of colors.
    """
     
    if "custom" in options.colormap_palette:
        # If a custom colormap is specified, load it from the file
        if options.colormap_file is None:
            raise ValueError("Custom colormap specified but no file provided.")
        else:
            # Parse the colormap file
            colormap = parse_colormap_file(file_path=options.colormap_file)
            if len(colormap) < number_neurons or len(colormap) > number_neurons:
                raise ValueError(f"Custom colormap file must contain {number_neurons} colors.")
            return colormap
    else:
        try:
            # Load the colormap from the specified file
            return get_colors_from_palette(palette=options.colormap_palette, number_colors=number_neurons)
        except Exception as e:
            raise ValueError(f"Failed to load colormap from file: {e}")
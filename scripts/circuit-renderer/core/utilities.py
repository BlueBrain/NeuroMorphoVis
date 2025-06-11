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
# @get_colors
####################################################################################################
def get_colors(palette='tab10'):
    
    # Get tab10 colormap
    tab10 = plt.get_cmap(palette)

    # Sample first 10 colors (tab10 has 10 discrete colors)
    colors = np.array([tab10(i)[:3] for i in range(10)])  # RGB only, drop alpha
    return colors
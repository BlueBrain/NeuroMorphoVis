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

# System imports
import random
import tqdm


# Blender improts
from mathutils import Vector

# Internal imports
import nmv.bmeshi
import nmv.consts
import nmv.mesh
import nmv.shading
import nmv.scene
import nmv.utilities


####################################################################################################
# @compute_number_of_vertices_of_mesh
####################################################################################################
def import_spines_terminals(file_path):

    spines_terminals = list()
    f = open(file_path, 'r')
    for line in f:
        data = line.strip('\n').split(' ')
        spines_terminals.append(Vector((float(data[0]), float(data[1]), float(data[2]))))
    f.close()
    return spines_terminals


####################################################################################################
# @compute_number_of_vertices_of_mesh
####################################################################################################
def draw_spines_terminals(spines_terminals,
                          radius=0.1):

    # Construct terminal spheres
    terminals_spheres = list()
    for spines_terminal in spines_terminals:
        terminal_sphere = nmv.bmeshi.create_ico_sphere(
            radius=radius, location=spines_terminal, subdivisions=2)
        terminals_spheres.append(terminal_sphere)

    # Join into a single bmesh
    terminals_bmesh = nmv.bmeshi.join_bmeshes_list(terminals_spheres)

    # Convert it to a mesh and return it
    return nmv.bmeshi.convert_bmesh_to_mesh(terminals_bmesh, name='Spine Terminals')


####################################################################################################
# @compute_number_of_vertices_of_mesh
####################################################################################################
def import_and_draw_spines_terminals(file_path,
                                     radius=0.1,
                                     color=nmv.consts.Color.BLACK):

    # Import
    spines_terminals = import_spines_terminals(file_path=file_path)

    # Draw
    terminals_mesh_object = draw_spines_terminals(spines_terminals=spines_terminals, radius=radius)

    # Create the material and assign it
    material = nmv.shading.create_flat_material(name='Spines Material', color=color)
    nmv.shading.set_material_to_object(
        mesh_object=terminals_mesh_object, material_reference=material)

    # Return the resulting mesh object
    return terminals_mesh_object


####################################################################################################
# @import_spines_bounds
####################################################################################################
def import_spines_bounds(file_path):

    spines_bounds = list()
    f = open(file_path, 'r')
    for line in f:
        data = line.strip('\n').split(' ')
        spines_bounds.append([Vector((float(data[0]), float(data[1]), float(data[2]))),
                              Vector((float(data[3]), float(data[4]), float(data[5])))])
    f.close()
    return spines_bounds


####################################################################################################
# @draw_spines_bounds
####################################################################################################
def draw_spines_bounds(spines_bounds):

    bounds_cubes = list()
    for i, spine_bound in enumerate(spines_bounds):
        center = spine_bound[0]
        scale = spine_bound[1]
        spine_bbox = nmv.mesh.create_cube(location=center, name='Spine %d' % i)
        nmv.scene.scale_object(spine_bbox, scale[0], scale[1], scale[2])
        bounds_cubes.append(spine_bbox)

    # Return the meshes
    return bounds_cubes


####################################################################################################
# @import_and_draw_spines_bounds
####################################################################################################
def import_and_draw_spines_bounds(file_path,
                                  color=nmv.consts.Color.BLACK):

    spines_bounds = import_spines_bounds(file_path=file_path)

    spines_bound_mesh = draw_spines_bounds(spines_bounds=spines_bounds)

    return spines_bound_mesh


####################################################################################################
# @import_spine_meshes
####################################################################################################
def import_and_draw_spine_meshes(spines_directory,
                                 meshes_extension,
                                 draw_refined=True):

    # Load all the spine meshes
    files = nmv.file.get_files_in_directory(spines_directory, meshes_extension)

    filtered_files = list()
    if draw_refined:
        for f in files:
            if 'refined' in f:
                filtered_files.append(f)
    else:
        for f in files:
            if 'refined' in f:
                continue
            else:
                filtered_files.append(f)

    # Create a set of materials
    materials = nmv.shading.create_random_materials(number_materials=50, name='Spines')

    spine_meshes = list()
    for file in tqdm.tqdm(filtered_files, bar_format=nmv.consts.Messages.TQDM_FORMAT):
        spine_mesh = nmv.file.import_obj_file(spines_directory, file, verbose=False)
        nmv.shading.set_material_to_object(spine_mesh, random.choice(materials))
        spine_meshes.append(spine_mesh)

    # Move spine meshes to collection
    nmv.utilities.create_collection_with_objects(name='Segmented Spines', objects_list=spine_meshes)
    return spine_meshes
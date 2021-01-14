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

# System imports
import sys
import os
import subprocess
import argparse
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# Blender imports
import bpy
from mathutils import Vector

# Internal imports
import nmv.scene
import nmv.mesh
import nmv.enums
import nmv.file
import nmv.utilities

# BBP imports
from archngv import NGVCircuit

import astrocyte_data
import astro_meta_builder


####################################################################################################
# @create_end_feet_proxy_mesh
####################################################################################################
def create_end_feet_proxy_mesh(area,
                               index,
                               soma_centroid=None):
    """Creates the end-feet proxy mesh.

    :param area:
        The area of the end feet.
    :param index:
        The index.
    :return:
        A reference to the created proxy mesh.
    """

    # List of vertices and faces of the created mesh
    verts = list()
    faces = list()

    # Points and triangles from the area
    points = area.points
    triangles = area.triangles

    # Append verts
    for point in points:
        if soma_centroid is None:
            location = Vector((point[0], point[1], point[2]))
        else:
            location = Vector((point[0], point[1], point[2])) - soma_centroid

        verts.append(location)

    # Append faces
    for triangle in triangles:
        face = Vector((int(triangle.data[0]), int(triangle.data[1]), int(triangle.data[2])))
        faces.append(face)
    thickness = area.thickness

    # Create the end feet proxy mesh
    end_feet_proxy_mesh = nmv.mesh.create_mesh_from_raw_data(verts=verts, faces=faces,
                                                             name='%s_endfeet' % index)

    # Resample the mesh
    bpy.ops.object.modifier_add(type='SUBSURF')
    bpy.context.object.modifiers["Subdivision"].subdivision_type = 'SIMPLE'
    bpy.context.object.modifiers["Subdivision"].levels = 4
    bpy.context.object.modifiers["Subdivision"].show_only_control_edges = True
    bpy.context.object.modifiers["Subdivision"].uv_smooth = 'PRESERVE_CORNERS'

    if nmv.utilities.is_blender_290():
        bpy.ops.object.modifier_apply(modifier="Subdivision")
    else:
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subdivision")

    # Return a reference to the mesh
    return end_feet_proxy_mesh


####################################################################################################
# @create_end_feet_proxy_mesh
####################################################################################################
def generate_astrocyte(circuit_path,
                       astrocyte_gid,
                       soma_style):
    """Generate astrocyte mesh for a specific GID in the circuit.

    :param circuit_path:
        The NGV circuit.
    :param astrocyte_gid:
        The GID of the astrocyte.
    :param soma_style:
        The style of the soma, whether metaball or softbody.
    :return:
        A reference to the astrocyte mesh
    """

    # List astrocyte GIDs
    gids = [astrocyte_gid]

    circuit = NGVCircuit(circuit_path)

    # End-feet areas
    areas = circuit.data.endfeetome.areas

    # Access the astrocytes data
    astrocytes_data = astrocyte_data.get_astrocyte_data(gids, circuit_path)

    # Clear the scene
    nmv.scene.clear_scene()

    # Center the morphology at the origin
    center_morphology = True

    # Astrocyte data
    for astro_generator in astrocytes_data:

        soma_centroid = astro_generator.circuit_data['soma_position']
        soma_centroid = Vector((soma_centroid[0], soma_centroid[1], soma_centroid[2]))
        soma_radius = astro_generator.circuit_data['soma_radius']

        # Load the .h5 morphology
        reader = nmv.file.readers.H5Reader(h5_file=astro_generator.filepath,
                                           center_morphology=center_morphology)
        morphology_object = reader.read_file()

        end_feet_proxy_meshes = list()
        end_feet_thicknesses = list()
        for j, process in enumerate(astro_generator.perivascular_processes):

            # Area
            area = areas[process.endfoot_area_mesh.index]

            # Proxy end feet
            if center_morphology:
                end_feet_proxy_meshes.append(create_end_feet_proxy_mesh(area, j, soma_centroid))
            else:
                end_feet_proxy_meshes.append(create_end_feet_proxy_mesh(area, j))

            end_feet_thicknesses.append(area.thickness)

        # Create the builder
        builder = astro_meta_builder.AstroMetaBuilder(
            morphology=morphology_object,
            soma_radius=soma_radius,
            end_feet_proxy_meshes=end_feet_proxy_meshes,
            end_feet_thicknesses=end_feet_thicknesses,
            soma_style=soma_style)

        # Reconstructing the mesh and return a reference to the astrocyte mesh
        astrocyte_mesh = builder.reconstruct_mesh()

        print(end_feet_proxy_meshes)
        # Delete all the end-feet data
        nmv.scene.delete_list_objects(end_feet_proxy_meshes)

        # Return a reference to the astrocyte mesh
        return astrocyte_mesh


####################################################################################################
# @create_optimized_mesh
####################################################################################################
def create_optimized_mesh(skinned_obj_mesh,
                          ultra_clean_mesh_executable,
                          output_directory):
    """Creates an optimized mesh from the skinned one.

    :param skinned_obj_mesh:
        A reference to the obj file of the skinned mesh.
    :param ultra_clean_mesh_executable:
        Ultraliser mesh cleaner.
    :param output_directory:
        Output directory where the final mesh will be written
    """

    # Create the shell command
    shell_command = '%s --mesh=%s --output-directory %s' % (ultra_clean_mesh_executable,
                                                            skinned_obj_mesh,
                                                            output_directory)
    subprocess.call(shell_command, shell=True)


####################################################################################################
# @parse_command_line_arguments
####################################################################################################
def parse_command_line_arguments(arguments=None):
    """Parses the input arguments.

    :param arguments:
        Command line arguments.
    :return:
        Arguments list.
    """

    description = 'Generating astrocytes'
    parser = argparse.ArgumentParser(description=description)

    arg_help = 'An input morphology'
    parser.add_argument('--morphology',
                        action='store', dest='morphology', help=arg_help)

    arg_help = 'Output directory where the generated astrocyte will be written'
    parser.add_argument('--output-directory',
                        action='store', dest='output_directory', help=arg_help)

    arg_help = 'The path to the NGV circuit'
    parser.add_argument('--circuit-path',
                        action='store', dest='circuit_path', help=arg_help)

    arg_help = 'The GID of the astrocyte'
    parser.add_argument('--gid',
                        action='store', dest='gid', help=arg_help)

    arg_help = 'The style of the soma'
    parser.add_argument('--soma-style',
                        action='store', dest='soma_style', help=arg_help)

    arg_help = 'The type of the resulting mesh, [simulation], [visualization] or [both]'
    parser.add_argument('--mesh-type',
                        action='store', dest='mesh_type', help=arg_help)

    arg_help = 'Decimation factor, between 1.0 and 0.01'
    parser.add_argument('--decimation-factor',
                        action='store', dest='decimation_factor', default=1.0, help=arg_help)

    arg_help = 'Export the result into an .OBJ file'
    parser.add_argument('--export-obj',
                        action='store_true', default=False, help=arg_help)

    arg_help = 'Export the result into an .BLEND file'
    parser.add_argument('--export-blend',
                        action='store_true', default=False, help=arg_help)

    arg_help = 'Create the optimized mesh'
    parser.add_argument('--create-optimized',
                        action='store_true', dest='create_optimized', default=False, help=arg_help)

    arg_help = 'ultraCleanMesh executable'
    parser.add_argument('--ultra-clean-mesh-executable',
                        action='store', dest='ultra_clean_mesh_executable', help=arg_help)

    # Parse the arguments
    return parser.parse_args()


####################################################################################################
# @ Main
####################################################################################################
if __name__ == "__main__":

    # Get all arguments after the '--'
    args = sys.argv
    sys.argv = args[args.index("--") + 0:]

    # Parse the command line arguments
    args = parse_command_line_arguments()

    # One must export a valid mesh
    if (not args.export_blend) and (not args.export_obj):
        print('You must export either a .BLEND or .OBJ mesh')
        exit(0)

    # Generate the astrocyte
    astrocyte_mesh = generate_astrocyte(circuit_path=args.circuit_path,
                                        astrocyte_gid=int(args.gid),
                                        soma_style=args.soma_style)

    # Export the meshes for simulation
    if 'simulation' in args.mesh_type or 'both' in args.mesh_type:

        # Create the output directory if it doesn't exist
        simulation_directory = '%s/simulation' % args.output_directory
        if not os.path.exists(simulation_directory):
            os.makedirs(simulation_directory)

        # Skinned directory
        skinned_directory = '%s/skinned' % simulation_directory
        if not os.path.exists(skinned_directory):
            os.makedirs(skinned_directory)

        # Export the mesh to a .BLEND file
        if args.export_blend:
            nmv.file.export_scene_to_blend_file(output_directory=skinned_directory,
                                                output_file_name=args.gid)

        # Export the mesh to an .OBJ file
        nmv.file.export_mesh_object_to_file(mesh_object=astrocyte_mesh,
                                            output_file_name=args.gid,
                                            output_directory=skinned_directory,
                                            file_format=nmv.enums.Meshing.ExportFormat.OBJ)

        # Create the optimized mesh
        if args.create_optimized:
            optimized_directory = '%s/optimized' % simulation_directory
            if not os.path.exists(optimized_directory):
                os.makedirs(optimized_directory)

            skinned_obj_mesh = '%s/%s.obj' % (simulation_directory, args.gid)
            create_optimized_mesh(skinned_obj_mesh=skinned_obj_mesh,
                                  ultra_clean_mesh_executable=args.ultra_clean_mesh_executable,
                                  output_directory=optimized_directory)

    # Export the meshes for visualization
    if 'visualization' in args.mesh_type or 'both' in args.mesh_type:

        # Decimate the mesh
        nmv.logger.info('Decimating Mesh')
        if float(args.decimation_factor) > 1.0 or float(args.decimation_factor) < 0.0:
            decimation_factor = 0.1
        else:
            decimation_factor = float(args.decimation_factor)
        nmv.mesh.decimate_mesh_object(mesh_object=astrocyte_mesh,
                                      decimation_ratio=decimation_factor)

        # Create the output directory if it doesn't exist
        visualization_directory = '%s/visualization' % args.output_directory
        if not os.path.exists(visualization_directory):
            os.makedirs(visualization_directory)

        # Export the mesh to a .BLEND file
        nmv.file.export_scene_to_blend_file(output_directory=visualization_directory,
                                            output_file_name=args.gid)

        # Export the mesh to an .OBJ file
        nmv.file.export_mesh_object_to_file(mesh_object=astrocyte_mesh,
                                            output_file_name=args.gid,
                                            output_directory=visualization_directory,
                                            file_format=nmv.enums.Meshing.ExportFormat.OBJ)

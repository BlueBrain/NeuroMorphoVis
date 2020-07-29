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

# BBP imports
from archngv import NGVCircuit

import astrocyte_data
import astro_meta_builder


####################################################################################################
# @create_end_feet_proxy_mesh
####################################################################################################
def create_end_feet_proxy_mesh(area,
                               index):
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
        location = Vector((point[0], point[1], point[2]))
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
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subdivision")

    # Return a reference to the mesh
    return end_feet_proxy_mesh


####################################################################################################
# @create_end_feet_proxy_mesh
####################################################################################################
def generate_astrocyte(circuit_path,
                       astrocyte_gid):
    """Generate astrocyte mesh for a specific GID in the circuit.

    :param circuit_path:
        The NGV circuit.
    :param astrocyte_gid:
        The GID of the astrocyte.
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

    for astro_generator in astrocytes_data:

        # Load the .h5 morphology
        reader = nmv.file.readers.H5Reader(h5_file=astro_generator.filepath,
                                           center_morphology=False)

        # Get the morphology object
        morphology_object = reader.read_file()

        soma_centroid = astro_generator.circuit_data['soma_position']
        soma_centroid = Vector((soma_centroid[0], soma_centroid[1], soma_centroid[2]))
        soma_radius = astro_generator.circuit_data['soma_radius']

        end_feet_proxy_meshes = list()
        end_feet_thicknesses = list()
        for j, process in enumerate(astro_generator.perivascular_processes):

            # Area
            area = areas[process.endfoot_area_mesh.index]

            # Proxy end feet
            end_feet_proxy_meshes.append(create_end_feet_proxy_mesh(area, j))
            end_feet_thicknesses.append(area.thickness)

            # Build the builder
        builder = astro_meta_builder.AstroMetaBuilder(
            morphology=morphology_object, soma_centroid=soma_centroid, soma_radius=soma_radius,
            end_feet_proxy_meshes=end_feet_proxy_meshes, end_feet_thicknesses=end_feet_thicknesses)

        # Reconstructing the mesh and return a reference to the astrocyte mesh
        return builder.reconstruct_mesh()


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

    arg_help = 'Decimation factor, between 1.0 and 0.01'
    parser.add_argument('--decimation-factor',
                        action='store', dest='decimation_factor', default=1.0, help=arg_help)

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

    # Generate the astrocyte
    astrocyte_mesh = generate_astrocyte(circuit_path=args.circuit_path, astrocyte_gid=int(args.gid))

    # Decimate the mesh on two iterations
    nmv.mesh.decimate_mesh_object(
        mesh_object=astrocyte_mesh, decimation_ratio=float(args.decimation_factor))

    # Export the mesh
    nmv.file.export_mesh_object_to_file(mesh_object=astrocyte_mesh,
                                        output_file_name=args.gid,
                                        output_directory=args.output_directory,
                                        file_format=nmv.enums.Meshing.ExportFormat.OBJ)

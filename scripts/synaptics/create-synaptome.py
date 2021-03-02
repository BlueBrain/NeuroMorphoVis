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

sys.path.append(('%s/../../' % (os.path.dirname(os.path.realpath(__file__)))))
sys.path.append(('%s/core' % (os.path.dirname(os.path.realpath(__file__)))))

# Blender imports
import parsing
import color_map
import synaptome
import rendering

# Blender imports
import bpy

# NeuroMorphoVis imports
import nmv.scene
import nmv.enums
import nmv.bbox


################################################################################
# @ Main
################################################################################
if __name__ == "__main__":

    # Get all arguments after the '--'
    args = sys.argv
    sys.argv = args[args.index("--") + 0:]

    # Parse the command line arguments
    args = parsing.parse_synaptome_command_line_arguments()

    # Clear the scene
    nmv.scene.clear_scene()

    # Add a flat shader to forc NMV to switch to Blender workbench render
    shader = nmv.enums.Shader.LAMBERT_WARD

    # Neuron material
    neuron_material = color_map.create_neuron_material(neuron_color=args.neuron_color,
                                                       shader=shader)

    # Create the color-map dictionary of the synapses
    synaptome_color_map_materials = color_map.create_color_map(color_map_file=args.color_map_file,
                                                               material_type=shader)

    # Create the synaptome
    synaptome_mesh = synaptome.create_synaptome(
        circuit_config=args.circuit_config,
        gid=args.gid,
        synapse_size=args.synapse_size,
        synapse_percentage=args.synapse_percentage,
        synaptome_color_map_materials=synaptome_color_map_materials,
        neuron_material=neuron_material,
        show_excitatory_inhibitory=args.show_exc_inh)

    # Compute the mesh bounding box
    synaptome_bounding_box = nmv.bbox.compute_scene_bounding_box_for_meshes()

    # Create the dummy material to adjust the renderer
    dummy_material = color_map.create_dummy_material(shader=shader)

    # Create the output directory where the artifacts will be created
    output_directory = args.output_directory + '/%s' % synaptome_mesh.name

    # Create the output directory if it does not exist
    if not nmv.file.ops.path_exists(output_directory):
        nmv.file.ops.clean_and_create_directory(output_directory)

    # Use the denoiser with cycles
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 16
    bpy.context.scene.view_layers[0].cycles.use_denoising = True

    # Render a 360 of the full view
    full_view_frames = rendering.render_synaptome_full_view_360(
        output_directory=output_directory, resolution=args.full_view_resolution)

    # Render a 360 of the soma close up
    close_up_frames = rendering.render_synaptome_close_up_on_soma_360(
        output_directory=output_directory, close_up_size=args.close_up_size,
        resolution=args.close_up_resolution)

    # Compose the 360 frames on the background
    frames_directory, composed_frames = rendering.compose_360_frames(
        full_view_frames=full_view_frames, close_up_frames=close_up_frames,
        background_image_file=args.background_image, output_directory=output_directory,
        bounding_box=synaptome_bounding_box)

    # Create a movie from the final frames
    rendering.create_movie(frames_directory=frames_directory, movie_name=synaptome_mesh.name,
                           output_directory=output_directory)

    # Export the scene into a blender file for reference
    nmv.file.export_scene_to_blend_file(output_directory=output_directory,
                                        output_file_name='%s' % synaptome_mesh.name)

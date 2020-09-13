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

# NeuroMorphoVis imports
import nmv.scene
import nmv.file
import nmv.enums


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
        neuron_material=neuron_material)

    # Create the dummy material to adjust the renderer
    dummy_material = color_map.create_dummy_material(shader=shader)

    # Render the image
    rendering.render_image(output_directory=args.output_directory,
                           image_name=synaptome_mesh.name,
                           resolution=args.video_resolution)
    # Render a 360
    frames = rendering.render_360(output_directory=args.output_directory,
                                  label=synaptome_mesh.name,
                                  resolution=args.video_resolution)

    # Compose the frames with the background and the 360 frames
    rendering.add_background_and_360_to_raw_frames(
        raw_frames_list=frames, background_image_file=args.background_image,
        rotation_frames_directory=args.rotation_360_directory)

    # Export
    nmv.file.export_scene_to_blend_file(output_directory=args.output_directory,
                                        output_file_name='%s' % synaptome_mesh.name)

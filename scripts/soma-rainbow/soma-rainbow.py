####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
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
import sys, os, bpy

sys.path.append(('%s/../../' %(os.path.dirname(os.path.realpath(__file__)))))
sys.path.append(('%s/core' %(os.path.dirname(os.path.realpath(__file__)))))


# Blender imports
import loading
import parsing
import styling

# NeuroMorphoVis imports
import nmv
import nmv.scene
import nmv.rendering
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
    args = parsing.parse_command_line_arguments()

    # Parse the rendering configuration and return a list of neurons
    neurons = parsing.parse_rendering_configuration(args.config)

    # Parse the style map
    styles = parsing.parse_style_file(args.style_file)

    # Clear the scene
    nmv.scene.clear_scene()

    if args.use_spheres:

        # Draw the neurons as spheres to know their positions
        neuron_objects = styling.draw_spheres(neurons, styles)
    else:
        print('Importing [%d] neurons' % len(neurons))

        # Load the neurons into the scene
        neuron_objects = loading.load_neurons_membrane_meshes_into_scene(
            args.input_directory, neurons, args.input_type, args.transform)

        # Apply the style
        # styling.apply_style(neurons, styles)

    # Setup the camera
    camera = nmv.rendering.Camera('%s_camera' % args.prefix)
    bb = nmv.bbox.compute_scene_bounding_box_for_meshes()

    # Color based on the height
    styling.apply_rainbow_style(neurons, styles, bb.p_min[1], bb.p_max[1])

    # Use Cycles renderer
    bpy.context.scene.render.engine = 'CYCLES'

    # Render the scene
    print('* Rendering')
    camera.render_scene(
        bounding_box=bb,
        camera_view=nmv.enums.Camera.View.SIDE,
        camera_projection=nmv.enums.Camera.Projection.get_enum(args.projection),
        image_resolution=int(args.resolution),
        image_name='%s/%s_SIDE' % (args.output_directory, args.prefix))

    camera.render_scene(
        bounding_box=bb,
        camera_view=nmv.enums.Camera.View.FRONT,
        camera_projection=nmv.enums.Camera.Projection.get_enum(args.projection),
        image_resolution=int(args.resolution),
        image_name='%s/%s_FRONT' % (args.output_directory, args.prefix))

    # Save the scene
    nmv.file.export_object_to_blend_file(None, args.output_directory, args.prefix)

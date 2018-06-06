####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of NeuroMorphoVis <https://github.com/BlueBrain/NeuroMorphoVis>
#
# This library is free software; you can redistribute it and/or modify it under the terms of the
# GNU Lesser General Public License version 3.0 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with this library;
# if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA.
####################################################################################################

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2016 - 2018, Blue Brain Project / EPFL"
__credits__     = ["Ahmet Bilgili", "Juan Hernando", "Stefan Eilemann"]
__version__     = "1.0.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"


# System imports
import sys, os
import_paths = ['core',
                '/../neuromorphovis'
                '/../neuromorphovis/interface/cli', ]
for import_path in import_paths:
    sys.path.append(('%s/%s' %(os.path.dirname(os.path.realpath(__file__)), import_path)))

# Blender imports
import loading
import parsing
import styling

# NeuroMorphoVis imports
import neuromorphovis as nmv
import neuromorphovis.scene
import neuromorphovis.rendering
import neuromorphovis.enums


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
        styling.apply_style(neurons, styles)

    # Setup the camera
    camera = nmv.rendering.Camera('%s_camera' % args.prefix)

    # Render the scene
    print('* Rendering')
    camera.render_scene(
        bounding_box=None,
        camera_view=nmv.enums.Camera.View.SIDE,
        camera_projection=nmv.enums.Camera.Projection.get_enum(args.projection),
        image_resolution=int(args.resolution),
        image_name='%s/%s_SIDE' % (args.output_directory, args.prefix))

    camera.render_scene(
        bounding_box=None,
        camera_view=nmv.enums.Camera.View.FRONT,
        camera_projection=nmv.enums.Camera.Projection.get_enum(args.projection),
        image_resolution=int(args.resolution),
        image_name='%s/%s_FRONT' % (args.output_directory, args.prefix))

    # Save the scene
    nmv.file.export_object_to_blend_file(None, args.output_directory, args.prefix)

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

# System imports
import sys, os
sys.path.append(('%s/../../' %(os.path.dirname(os.path.realpath(__file__)))))
sys.path.append(('%s/core' %(os.path.dirname(os.path.realpath(__file__)))))

from mathutils import Vector, Matrix

# System imports
import argparse
import sonata
import utilities
import rendering
import morphology

####################################################################################################
# @run_rendering_tasks
####################################################################################################
def run_rendering_tasks(options):
    
    # Scen prefix
    prefix = f'{options.output_directory}/{options.population}'
    
    # Clearing the scene 
    utilities.clear_scene()
    
    # Loaded circuit 
    print(f'The circuit config is {options.circuit_config}')
    circuit = sonata.import_circuit(options.circuit_config)

    # Population 
    population = options.population

    # Get number of cells in population 
    n_cells = circuit.node_population(population).size
    gids = range(n_cells)
    print(f'The circuit has {n_cells} neurons')

    # Getting the nodes to directly access the data 
    nodes = circuit.node_population(population)
    
    # TODO: Add a check for the colormap file
    colors = utilities.get_neurons_colors(options, n_cells)
    
    # Global triansformation for the orienation of the circuit
    global_orientation_matrix = sonata.get_global_inverse_transformation(nodes)
    
    # The positions of the somata are required to calculate the bounds for the close-up rendering
    soma_positions = list()
    
    # Draw the gids and get the neuron objects 
    for gid in gids:
        neuron_object = morphology.draw_morphology_in_position(
            options.circuit_config, gid, population, color=colors[gid])
        
        # In case needed for any processing
        position = sonata.get_position(nodes, gid)
        soma_positions.append(position)
        
        # Get the neuron transformation 
        transformation =  Matrix(sonata.get_transformation(nodes, gid).tolist())
        
        # Apply the transformation 
        neuron_object.matrix_world = transformation @ neuron_object.matrix_world
        
        # If the circuit is oriented upwards, we need to rotate the neuron object
        if options.orient_circuit_upwards:
            neuron_object.matrix_world = global_orientation_matrix @ neuron_object.matrix_world
    
    # Create the default camera 
    rendering.create_camera(
        resolution=options.image_resolution, square_resolution=options.square_aspect_ratio, 
        camera_name='Main Camera')
    
    # Render the full scene 
    rendering.render_scene_to_png(
        f'{prefix}.png', add_white_background=options.transparent_background, 
        add_shadow=False, add_outline=False) # Do not use any effects for the main image
    
    # Only for close up rendering
    if options.render_closeup:
        
        # If the circuit is oriented upwards, we need to apply the global orientation matrix
        if options.orient_circuit_upwards:
            soma_positions = [global_orientation_matrix @ Vector(pos) for pos in soma_positions]
        
        # From the soma positions, get the bounds 
        pmin, pmax = utilities.compute_bounds_from_positions(positions=soma_positions)
        
        # Add an extra margin to the bounds to capture all the somata 
        bounds = pmax - pmin
        margin = 0.75 * bounds
        pmin -= margin
        pmax += margin
                
        # Create the close-up camera 
        rendering.create_camera(
            resolution=options.image_resolution, square_resolution=options.square_aspect_ratio, 
            camera_name='CloseUp Camera', pmin=pmin, pmax=pmax)
        
        # Render the close-up image
        rendering.render_scene_to_png(f'{prefix}_closeup.png', 
            add_white_background=options.transparent_background, add_shadow=options.render_shadows,
            add_outline=options.render_outlines)
    
    # Save the scene as a Blender file
    if options.save_blender_scene:
        blend_file_path = f'{prefix}.blend'
        utilities.save_scene_as_blend_file(blend_file_path)
        print(f'Saved Blender scene to {blend_file_path}')
    

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

    # add all the options
    description = 'Resampling neurons to make them lighter while preserving skeletons'
    parser = argparse.ArgumentParser(description=description)
    
    arg_help = 'A circuit in sonata format'
    parser.add_argument('--circuit-config',
                        action='store', dest='circuit_config', help=arg_help)
    
    arg_help = 'The population name'
    parser.add_argument('--population',
                        action='store', dest='population', help=arg_help)
    
    arg_help = 'The RGBA color map to use for the circuit'
    parser.add_argument('--colormap-file',
                        action='store', dest='colormap_file', help=arg_help)
    
    args_help = 'The RGBA color map to use for the circuit (e.g., "tab10", "viridis")'
    parser.add_argument('--colormap-palette',
                        action='store', dest='colormap_palette', default='tab10', help=args_help)
    
    arg_help = 'Image resolution for the circuit rendering (for the shortest side of the image)'
    parser.add_argument('--image-resolution',
                        action='store', dest='image_resolution', type=int, help=arg_help)
    
    arg_help = 'Rendering view or the camera view to use for the circuit rendering (e.g., "top", "side", "front")'
    parser.add_argument('--rendering-view',
                        action='store', dest='rendering_view', help=arg_help)
    
    arg_help = 'Output directory where the resulting data or images will be written'
    parser.add_argument('--output-directory',
                        action='store', dest='output_directory', help=arg_help)
    
    arg_help = 'Save the circuit as a Blender file'
    parser.add_argument('--save-blender-scene',
                        action='store_true', dest='save_blender_scene', 
                        default=False, help=arg_help)
    
    arg_help = 'Render close-up images of the circuit based on the somata positions'
    parser.add_argument('--render-closeup',
                        action='store_true', dest='render_closeup', 
                        default=False, help=arg_help)
    
    arg_help = 'Use a unified radius for the branches of the morphology'
    parser.add_argument('--unify-branch-radii',
                        action='store_true', dest='unify_branch_radii', 
                        default=False, help=arg_help)
    
    arg_help = 'Orient the circuit upwards'
    parser.add_argument('--orient-circuit-upwards',
                        action='store_true', dest='orient_circuit_upwards', 
                        default=False, help=arg_help)
    
    arg_help = 'Render the circuit with shadows'
    parser.add_argument('--render-shadows',
                        action='store_true', dest='render_shadows', 
                        default=False, help=arg_help)
    
    arg_help = 'Render the circuit with an outline'
    parser.add_argument('--render-outlines',
                        action='store_true', dest='render_outlines', 
                        default=False, help=arg_help)
    
    # Transparent background
    arg_help = 'Render the circuit with a transparent background'
    parser.add_argument('--transparent-background',
                        action='store_true', dest='transparent_background', 
                        default=False, help=arg_help)
    
    arg_help = 'Use a square aspect ratio for the rendered images'
    parser.add_argument('--square-aspect-ratio',
                        action='store_true', dest='square_aspect_ratio', 
                        default=False, help=arg_help)
                        
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
    
    # Run the rendering task
    run_rendering_tasks(options=args)    
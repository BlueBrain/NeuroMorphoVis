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

from mathutils import Matrix

# System imports
import argparse
import sonata
import utilities
import camera
import morphology

####################################################################################################
# @run_rendering_taks
####################################################################################################
def run_rendering_taks(options):
    
    # Clearing the scene 
    utilities.clear_scene()

    # Path to config 
    print(f'The circuit config is {options.circuit_config}')

    # Loaded circuit 
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
    colors = utilities.get_colors()
    
    soma_positions = []
    
    # Draw the gids and get the neuron objects 
    for gid in gids:
        neuron_object = morphology.draw_morphology_in_position(
            options.circuit_config, gid, population, color=colors[gid])
        
        # In case needed for any processing
        position = sonata.get_position(nodes, gid)
        soma_positions.append(position)
        rotation = sonata.get_orientation(nodes, gid)
        
        # Get the neuron transformation 
        transformation =  Matrix(sonata.get_transformation(nodes, gid).tolist())
        
        # Apply the transformation 
        neuron_object.matrix_world = transformation @ neuron_object.matrix_world
        
        # neuron_object.matrix_world = gloabl_inverse_transformation @ neuron_object.matrix_world
    
    # Default rendering 
    camera.create_camera(resolution=options.image_resolution, square_resolution=True, camera_name='Main Camera')
    
    camera.render_scene_to_png(f'{options.output_directory}/{options.population}.png', 
                               add_white_background=True, add_shadow=False)
    
    if options.render_closeup:
        
        # From the soma positions, get the bounds 
        pmin, pmax = utilities.compute_bounds_from_positions(positions=soma_positions)
        
        # Create the new camera 
        camera.create_camera(
            resolution=options.image_resolution, square_resolution=True, camera_name='CloseUp Camera', 
            pmin=pmin, pmax=pmax)
        
        camera.render_scene_to_png(f'{options.output_directory}/{options.population}_closeup.png', 
                               add_white_background=True, add_shadow=False)
    

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
                        action='store_true', dest='save_blender_scene', default=False, help=arg_help)
    
    arg_help = 'Render close-up images of the circuit based on the somata positions'
    parser.add_argument('--render-closeup',
                        action='store_true', dest='render_closeup', default=False, help=arg_help)
    
    arg_help = 'Use a unified radius for the branches of the morphology'
    parser.add_argument('--unify-branch-radii',
                        action='store_true', dest='unify_branch_radii', default=False, help=arg_help)
    
    arg_help = 'Orient the circuit upwards'
    parser.add_argument('--orient-circuit-upwards',
                        action='store_true', dest='orient_circuit_upwards', default=False, help=arg_help)
                        
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
    run_rendering_taks(options=args)    
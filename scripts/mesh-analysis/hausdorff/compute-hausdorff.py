#!/usr/bin/python 

import sys
import os
import subprocess
import argparse


####################################################################################################
# @compute_hausdorff
####################################################################################################
def compute_hausdorff(target_mesh,
                      sampled_mesh,
                      mlx_script,
                      output_directory):

    # Target reference
    reference = os.path.splitext(os.path.basename(sampled_mesh))[0]

    # Shell command
    shell_command = 'meshlabserver '
    shell_command += '-i %s ' % target_mesh
    shell_command += '-i %s ' % sampled_mesh
    # shell_command += '-o \"HausdorffClosestPoints.xyz\" '
    shell_command += '-s %s' % mlx_script
    shell_command += '>%s/%s.hausdorff' % (output_directory, reference)
    print(shell_command)
    subprocess.call(shell_command, shell=True)


####################################################################################################
# @parse_command_line_arguments
####################################################################################################
def parse_command_line_arguments(arguments=None):

    # Add all the options
    description = 'Computes the Hausdorff distance!'
    parser = argparse.ArgumentParser(description=description)

    arg_help = 'The target mesh'
    parser.add_argument('--target-mesh', action='store', help=arg_help)

    arg_help = 'The sampled mesh'
    parser.add_argument('--sampled-mesh', action='store', help=arg_help)

    arg_help = 'The MLX script'
    parser.add_argument('--mlx-script', action='store', help=arg_help)

    arg_help = 'Output directory, where the final results will be written'
    parser.add_argument('--output-directory', action='store', help=arg_help)

    # Parse the arguments
    return parser.parse_args()


####################################################################################################
# @ Main
####################################################################################################
if __name__ == "__main__":

    # Parse the command line arguments
    args = parse_command_line_arguments()

    # Create Hausdorff directory
    hausdorff_directory = '%s/hausdorff' % args.output_directory
    if not os.path.exists(hausdorff_directory):
        os.mkdir(hausdorff_directory)

    # Compute the hausdorff distance
    compute_hausdorff(args.target_mesh, args.sampled_mesh, args.mlx_script, hausdorff_directory)

        

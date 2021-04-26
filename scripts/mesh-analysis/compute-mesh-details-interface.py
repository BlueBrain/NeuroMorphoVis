#!/usr/bin/python

import sys, os
import subprocess, shutil
import argparse


####################################################################################################
# @parse_command_line_arguments
####################################################################################################
def parse_command_line_arguments():

    # Create an argument parser, and then add the options one by one
    parser = argparse.ArgumentParser()
    
    # Morphology directory
    arg_help = 'Input mesh'
    parser.add_argument('--mesh', action='store', help=arg_help)
    
    # Blender
    arg_help = 'Blender'
    parser.add_argument('--blender', action='store', default='blender', help=arg_help)
                        
    # Output directory
    arg_help = 'Output directory'
    parser.add_argument('--output-directory', action='store', default=None, help=arg_help)
                        
    # Parse the arguments, and return a list of them
    return parser.parse_args()


####################################################################################################
# @ Run the main function if invoked from the command line.
####################################################################################################
if __name__ == "__main__":

    # Parse arguments 
    args = parse_command_line_arguments()

    # Output arguments 
    args_string = '--mesh=%s ' % (args.mesh)
    args_string += '--output-directory=%s ' % (args.output_directory)

    # Setup the shell command
    shell_command = '%s -b --verbose 0 --python %s -- %s' % (args.blender, 'core.py', args_string)
    print(shell_command)
    subprocess.call(shell_command, shell=True)








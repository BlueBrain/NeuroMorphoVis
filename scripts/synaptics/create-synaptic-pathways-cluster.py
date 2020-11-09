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

#!/usr/bin/python

# System imports
import sys
import os
import subprocess
import argparse
import shutil

sys.path.append(('%s/../../' % (os.path.dirname(os.path.realpath(__file__)))))
sys.path.append(('%s/core' % (os.path.dirname(os.path.realpath(__file__)))))

# Blender imports
import parsing

# NeuroMorphoVis imports
import nmv.scene
import nmv.file
import nmv.enums
import nmv.bbox
import nmv.slurm


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
    description = 'Synaptic pathway creator: creates static images synaptic pairs'
    parser = argparse.ArgumentParser(description=description)

    arg_help = 'Blender executable'
    parser.add_argument('--blender',
                        action='store', dest='blender', help=arg_help)

    arg_help = 'Circuit configuration file'
    parser.add_argument('--circuit-config',
                        action='store', dest='circuit_config', help=arg_help)

    arg_help = 'Pair script'
    parser.add_argument('--pair-script',
                        action='store', dest='pair_script', help=arg_help)

    arg_help = 'Synaptic pairs file'
    parser.add_argument('--synaptic-pairs-file',
                        action='store', dest='synaptic_pairs_file', help=arg_help)

    arg_help = 'Output directory, where the final image/movies and scene will be stored'
    parser.add_argument('--output-directory',
                        action='store', dest='output_directory', help=arg_help)

    arg_help = 'Pre-GID Neuron color in R_G_B format, for example: 255_231_192'
    parser.add_argument('--pre-neuron-color',
                        action='store', dest='pre_neuron_color', help=arg_help)

    arg_help = 'Post-GID Neuron color in R_G_B format, for example: 255_231_192'
    parser.add_argument('--post-neuron-color',
                        action='store', dest='post_neuron_color', help=arg_help)

    arg_help = 'Synapse color in R_G_B format, for example: 255_231_192'
    parser.add_argument('--synapse-color',
                        action='store', dest='synapse_color', help=arg_help)

    arg_help = 'Synapse size (in um)'
    parser.add_argument('--synapse-size',
                        action='store', dest='synapse_size', type=float, help=arg_help)

    arg_help = 'Base image resolution'
    parser.add_argument('--image-resolution',
                        action='store', default=2000, type=int, dest='image_resolution',
                        help=arg_help)

    arg_help = 'Background image'
    parser.add_argument('--background-image',
                        action='store', dest='background_image', help=arg_help)

    # Parse the arguments
    return parser.parse_args()


####################################################################################################
# @create_synaptic_pair_script
####################################################################################################
def create_synaptic_pair_script(blender_executable,
                                pre_gid,
                                post_gid,
                                arguments,
                                jobs_directory,
                                logs_directory):

    script_string = ''
    script_string += '#!/bin/bash \n'
    script_string += '#SBATCH --job-name=\"%s\" \n' % '%s_%s' % (pre_gid, post_gid)
    script_string += '#SBATCH --nodes=1 \n'
    script_string += '#SBATCH --cpus-per-task=1 \n'
    script_string += '#SBATCH --ntasks=1 \n'
    script_string += '#SBATCH --mem=6000 \n'
    script_string += '#SBATCH --time=1:00:00 \n'
    script_string += '#SBATCH --partition=prod \n'
    script_string += '#SBATCH --account=proj3 \n'
    script_string += '#SBATCH --output=%s/slurm-stdout_%s_%s.log \n' % (logs_directory,
                                                                        pre_gid, post_gid)
    script_string += '#SBATCH --error=%s/slurm-stderr_%s_%s.log \n\n' % (logs_directory,
                                                                         pre_gid, post_gid)

    script_string += '%s -b --verbose 0 --python %s -- ' % (blender_executable,
                                                            arguments.pair_script)
    script_string += ' --circuit-config=%s ' % arguments.circuit_config
    script_string += ' --pre-gid=%s ' % pre_gid
    script_string += ' --post-gid=%s ' % post_gid
    script_string += ' --output-directory=%s ' % arguments.output_directory
    script_string += ' --pre-neuron-color=%s ' % arguments.pre_neuron_color
    script_string += ' --post-neuron-color=%s ' % arguments.post_neuron_color
    script_string += ' --synapse-color=%s ' % arguments.synapse_color
    script_string += ' --synapse-size=%s ' % arguments.synapse_size
    script_string += ' --background-image=%s ' % arguments.background_image
    script_string += '\n'

    # Write the script to a file
    script_file_path = '%s/%s_%s.sh' % (jobs_directory, pre_gid, post_gid)
    script_file = open(script_file_path, 'w')
    script_file.write(script_string)
    script_file.close()

    # Change the script to +x
    shell_command = 'chmod +x %s' % script_file_path
    subprocess.call(shell_command, shell=True)

    # Return the script file
    return script_file_path


####################################################################################################
# @__main__
####################################################################################################
if __name__ == "__main__":

    # Get all arguments after the '--'
    args = sys.argv
    blender_executable = args[0]

    sys.argv = args[args.index("--") + 0:]

    # Parse the command line arguments
    args = parse_command_line_arguments()

    # Parse the pairs file
    pairs = parsing.parse_synaptic_pairs(args.synaptic_pairs_file)

    # Make sure that the given output directory exists
    if not nmv.file.ops.path_exists(args.output_directory):
        nmv.file.ops.clean_and_create_directory(args.output_directory)

    # Create the slurm directory
    slurm_directory = '%s/slurm' % args.output_directory
    if not nmv.file.ops.path_exists(slurm_directory):
        nmv.file.ops.clean_and_create_directory(slurm_directory)

    # Jobs directory
    jobs_directory = '%s/jobs' % slurm_directory
    if not nmv.file.ops.path_exists(jobs_directory):
        nmv.file.ops.clean_and_create_directory(jobs_directory)

    # Logs directory
    logs_directory = '%s/logs' % slurm_directory
    if not nmv.file.ops.path_exists(logs_directory):
        nmv.file.ops.clean_and_create_directory(logs_directory)

    # Create the meshes directory
    meshes_directory = '%s/meshes' % args.output_directory
    if not nmv.file.ops.path_exists(meshes_directory):
        nmv.file.ops.clean_and_create_directory(meshes_directory)

    # Create the scenes directory
    scenes_directory = '%s/scenes' % args.output_directory
    if not nmv.file.ops.path_exists(scenes_directory):
        nmv.file.ops.clean_and_create_directory(scenes_directory)

    # Create the images directory
    images_directory = '%s/images' % args.output_directory
    if not nmv.file.ops.path_exists(images_directory):
        nmv.file.ops.clean_and_create_directory(images_directory)

    # Create the compositing directory
    composite_directory = '%s/composite' % args.output_directory
    if not nmv.file.ops.path_exists(composite_directory):
        nmv.file.ops.clean_and_create_directory(composite_directory)

    # Create a job for every pair
    jobs = list()
    for pair in pairs:
        job = create_synaptic_pair_script(
            blender_executable=blender_executable, pre_gid=str(pair[0]), post_gid=str(pair[1]),
            arguments=args, jobs_directory=jobs_directory, logs_directory=logs_directory)
        print(job)
        jobs.append(job)

    # Submit the slurm jobs
    nmv.slurm.submit_batch_jobs(user_name='abdellah', slurm_jobs_directory=jobs_directory)


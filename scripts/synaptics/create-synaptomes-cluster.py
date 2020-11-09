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
import subprocess

sys.path.append(('%s/../../' % (os.path.dirname(os.path.realpath(__file__)))))
sys.path.append(('%s/core' % (os.path.dirname(os.path.realpath(__file__)))))

# Blender imports
import parsing
import color_map
import synaptome
import rendering
import slurm

# NeuroMorphoVis imports
import nmv.scene
import nmv.enums
import nmv.bbox


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
    description = 'Synaptome creator: creates static images and 360s of synaptomes'
    parser = argparse.ArgumentParser(description=description)

    arg_help = 'Synaptome script'
    parser.add_argument('--synaptome-script',
                        action='store', dest='synaptome_script', help=arg_help)

    arg_help = 'Circuit configuration file'
    parser.add_argument('--circuit-config',
                        action='store', dest='circuit_config', help=arg_help)

    arg_help = 'Neuron GID'
    parser.add_argument('--gid-list',
                        action='store', dest='gid_list', help=arg_help)

    arg_help = 'The percentage of synapses to be drawn in the rendering'
    parser.add_argument('--synapse-percentage',
                        action='store', dest='synapse_percentage', type=float, help=arg_help)

    arg_help = 'Output directory, where the final image/movies and scene will be stored'
    parser.add_argument('--output-directory',
                        action='store', dest='output_directory', help=arg_help)

    arg_help = 'Synaptic color map'
    parser.add_argument('--color-map',
                        action='store', dest='color_map_file', help=arg_help)

    arg_help = 'Neuron color in R_G_B format, for example: 255_231_192'
    parser.add_argument('--neuron-color',
                        action='store', dest='neuron_color', help=arg_help)

    arg_help = 'Synapse size (in um)'
    parser.add_argument('--synapse-size',
                        action='store', dest='synapse_size', type=float, help=arg_help)

    arg_help = 'Close-up view size'
    parser.add_argument('--close-up-size',
                        action='store', default=50, type=int, dest='close_up_size',
                        help=arg_help)

    arg_help = 'Base full-view resolution'
    parser.add_argument('--full-view-resolution',
                        action='store', default=2000, type=int, dest='full_view_resolution',
                        help=arg_help)

    arg_help = 'Base close-up resolution'
    parser.add_argument('--close-up-resolution',
                        action='store', default=1000, type=int, dest='close_up_resolution',
                        help=arg_help)

    arg_help = 'Background image'
    parser.add_argument('--background-image',
                        action='store', dest='background_image', help=arg_help)

    # Parse the arguments
    return parser.parse_args()


####################################################################################################
# @create_synaptome_script
####################################################################################################
def create_synaptome_script(blender_executable,
                            synaptome_gid,
                            arguments,
                            results_directory,
                            jobs_directory,
                            logs_directory):

    script_string = ''
    script_string += '#!/bin/bash \n'
    script_string += '#SBATCH --job-name=\"%s\" \n' % '%s' % synaptome_gid
    script_string += '#SBATCH --nodes=1 \n'
    script_string += '#SBATCH --cpus-per-task=1 \n'
    script_string += '#SBATCH --ntasks=1 \n'
    script_string += '#SBATCH --mem=6000 \n'
    script_string += '#SBATCH --time=1:00:00 \n'
    script_string += '#SBATCH --partition=prod \n'
    script_string += '#SBATCH --account=proj3 \n'
    script_string += '#SBATCH --output=%s/slurm-stdout_%s.log \n' % (logs_directory, synaptome_gid)
    script_string += '#SBATCH --error=%s/slurm-stderr_%s.log \n\n' % (logs_directory, synaptome_gid)

    script_string += '%s -b --verbose 0 --python %s -- ' % (blender_executable,
                                                            arguments.synaptome_script)
    script_string += ' --circuit-config=%s ' % arguments.circuit_config
    script_string += ' --gid=%s ' % synaptome_gid
    script_string += ' --output-directory=%s ' % results_directory
    script_string += ' --synapse-percentage=%s ' % arguments.synapse_percentage
    script_string += ' --color-map=%s ' % arguments.color_map_file
    script_string += ' --neuron-color=%s ' % arguments.neuron_color
    script_string += ' --synapse-size=%s ' % arguments.synapse_size
    script_string += ' --close-up-size=%s ' % arguments.close_up_size
    script_string += ' --full-view-resolution=%s ' % arguments.full_view_resolution
    script_string += ' --close-up-resolution=%s ' % arguments.close_up_resolution
    script_string += ' --background-image=%s ' % arguments.background_image
    script_string += '\n'

    # Write the script to a file
    script_file_path = '%s/%s.sh' % (jobs_directory, synaptome_gid)
    script_file = open(script_file_path, 'w')
    script_file.write(script_string)
    script_file.close()

    # Change the script to +x
    shell_command = 'chmod +x %s' % script_file_path
    subprocess.call(shell_command, shell=True)

    # Return the script file
    return script_file_path


################################################################################
# @ Main
################################################################################
if __name__ == "__main__":

    # Get all arguments after the '--'
    args = sys.argv
    blender_executable = args[0]
    sys.argv = args[args.index("--") + 0:]

    # Parse the command line arguments
    args = parse_command_line_arguments()

    # Parse the GIDs file
    gids = parsing.parse_synaptomes_gids(args.gid_list)

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

    # Results directory
    results_directory = '%s/results' % args.output_directory
    if not nmv.file.ops.path_exists(results_directory):
        nmv.file.ops.clean_and_create_directory(results_directory)

    # Create a job for every GID
    jobs = list()
    for gid in gids:
        job = create_synaptome_script(
            blender_executable=blender_executable, synaptome_gid=str(gid),
            arguments=args, results_directory=results_directory, jobs_directory=jobs_directory,
            logs_directory=logs_directory)
        print(job)
        jobs.append(job)

    # Submit the slurm jobs
    slurm.submit_batch_jobs(user_name='abdellah', slurm_jobs_directory=jobs_directory)


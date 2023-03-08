#!/usr/bin/python
####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
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

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2016 - 2023, Blue Brain Project / EPFL"
__credits__     = ["Ahmet Bilgili", "Juan Hernando", "Stefan Eilemann"]
__version__     = "1.0.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"

####################################################################################################

# System imports
import os
import sys
import subprocess

# Append the internal modules into the system paths to avoid Blender importing conflicts
import_paths = ['nmv/interface/cli', 'nmv/file/ops', 'nmv/slurm']
for import_path in import_paths:
    sys.path.append(('%s/%s' % (os.path.dirname(os.path.realpath(__file__)), import_path)))
    
# Internal imports
import arguments_parser
import file_ops
import slurm


####################################################################################################
# @execute_shell_command
####################################################################################################
def execute_shell_command(shell_command):
    subprocess.call(shell_command, shell=True)


####################################################################################################
# @create_shell_commands
####################################################################################################
def create_shell_commands_for_local_execution(arguments,
                                              arguments_string):
    """Creates a list of all the shell commands that are needed to run the different tasks set
    in the configuration file.

    Notes:
        # -b : Blender background mode
        # --verbose : Turn off all the verbose messages
        # -- : Separate the framework arguments from those given to Blender
    :param arguments:
        Input arguments.
    :param arguments_string:
        A string that will be given to each CLI command.
    :return:
        A list of commands to be appended to the SLURM scripts or directly executed on a local node.
    """

    shell_commands = list()

    # Retrieve the path to the CLIs
    cli_interface_path = os.path.dirname(os.path.realpath(__file__)) + '/nmv/interface/cli'
    cli_soma_reconstruction = '%s/soma_reconstruction.py' % cli_interface_path
    cli_morphology_reconstruction = '%s/neuron_morphology_reconstruction.py' % cli_interface_path
    cli_morphology_analysis = '%s/morphology_analysis.py' % cli_interface_path
    cli_mesh_reconstruction = '%s/neuron_mesh_reconstruction.py' % cli_interface_path

    # Morphology analysis task
    if arguments.analyze_morphology:
        
        # Add this command to the list
        shell_commands.append('%s -b --verbose 0 --python %s -- %s' %
                              (arguments.blender, cli_morphology_analysis, arguments_string))
                              
    # Morphology reconstruction task: call the @cli_morphology_reconstruction interface
    if arguments.render_neuron_morphology or                \
       arguments.render_neuron_morphology_360 or            \
       arguments.render_neuron_morphology_progressive or    \
       arguments.export_morphology_swc or                   \
       arguments.export_morphology_segments or              \
       arguments.export_morphology_blend:

        # Add this command to the list
        shell_commands.append('%s -b --verbose 0 --python %s -- %s' %
                              (arguments.blender, cli_morphology_reconstruction, arguments_string))

    # Soma-related task: call the @cli_soma_reconstruction interface
    if arguments.render_soma_mesh or                        \
       arguments.render_soma_mesh_360 or                    \
       arguments.render_soma_mesh_progressive or            \
       arguments.export_soma_mesh_ply or                    \
       arguments.export_soma_mesh_obj or                    \
       arguments.export_soma_mesh_stl or                    \
       arguments.export_soma_mesh_blend:

        # Add this command to the list
        shell_commands.append('%s -b --verbose 0 --python %s -- %s' %
                              (arguments.blender, cli_soma_reconstruction, arguments_string))

    # Neuron mesh reconstruction related task: call the @cli_mesh_reconstruction interface
    if arguments.render_neuron_mesh or                      \
       arguments.render_neuron_mesh_360 or                  \
       arguments.export_neuron_mesh_ply or                  \
       arguments.export_neuron_mesh_obj or                  \
       arguments.export_neuron_mesh_stl or                  \
       arguments.export_neuron_mesh_blend:

        # Add this command to the list
        shell_commands.append('%s -b --verbose 0 --python %s -- %s' %
                              (arguments.blender, cli_mesh_reconstruction, arguments_string))

    # Return a list of commands
    return shell_commands


####################################################################################################
# @execute_command
####################################################################################################
def execute_command(shell_command):
    subprocess.call(shell_command, shell=True)


####################################################################################################
# @execute_commands
####################################################################################################
def execute_commands(shell_commands):
    for shell_command in shell_commands:
        print('RUNNING: **********************************************************************')
        print(shell_command)
        print('*******************************************************************************')
        execute_command(shell_command)


####################################################################################################
# @execute_commands_parallel
####################################################################################################
def execute_commands_parallel(shell_commands):

    from joblib import Parallel, delayed
    Parallel(n_jobs=1)(delayed(execute_command)(i) for i in shell_commands)


####################################################################################################
# @run_local_neuromorphovis
####################################################################################################
def run_local_neuromorphovis(arguments):
    """Run the framework on a local node, basically your machine.

    :param arguments:
        Command line arguments.
    """

    # Use a specific circuit target
    if arguments.input == 'target':

        # Log
        print('Loading a target [%s] in circuit [%s]' % (arguments.target, arguments.blue_config))

        # Ensure a valid blue config and a target
        if arguments.blue_config is None or arguments.target is None:
            print('ERROR: Empty circuit configuration file or target')
            exit(0)

        # Import BluePy
        try:
            import bluepy
        except ImportError:
            print('ERROR: Cannot import [BluePy], please install it')
            exit(0)

        from bluepy import Circuit

        # Loading a circuit
        circuit = Circuit(arguments.blue_config)

        # Loading the GIDs of the sample target within the circuit
        gids = circuit.cells.ids(arguments.target)

        shell_commands = list()
        for gid in gids:

            # Get the argument string for an individual file
            arguments_string = arguments_parser.get_arguments_string_for_individual_gid(
                arguments=arguments, gid=gid)

            # Construct the shell command to run the workflow
            shell_commands.extend(
                create_shell_commands_for_local_execution(arguments, arguments_string))

        # Run NeuroMorphoVis from Blender in the background mode
        for shell_command in shell_commands:
            subprocess.call(shell_command, shell=True)

    # Use a single GID
    elif arguments.input == 'gid':

        print('Loading a gid [%s] in circuit [%s]' % (str(arguments.gid), arguments.blue_config))

        # Ensure a valid blue config and a GID
        if arguments.blue_config is None or arguments.gid is None:
            print('ERROR: Empty circuit configuration file or GID')
            exit(0)

            # Get the argument string for an individual file
            arguments_string = arguments_parser.get_arguments_string_for_individual_gid(
                arguments=arguments, gid=arguments.gid)

            # Construct the shell command to run the workflow
            shell_commands = create_shell_commands_for_local_execution(arguments, arguments_string)

            # Run NeuroMorphoVis from Blender in the background mode
            for shell_command in shell_commands:
                subprocess.call(shell_command, shell=True)

        # Run the jobs on the cluster
        slurm.run_gid_jobs_on_cluster(arguments=arguments, gids=[str(arguments.gid)])

    # Load morphology files (.H5 or .SWC)
    elif arguments.input == 'file':

        # Get the arguments string list
        arguments_string = arguments_parser.get_arguments_string(arguments=arguments)

        # NOTE: Using a morphology file, either in .H5 or .SWC formats is straightforward and
        # therefore the arguments will not change at all. In this case it is safe to pass the
        # arguments as they were received without any change.

        # Construct the shell command to run the workflow
        shell_commands = create_shell_commands_for_local_execution(arguments, arguments_string)

        # Run NeuroMorphoVis from Blender in the background mode
        for shell_command in shell_commands:
            subprocess.call(shell_command, shell=True)

    # Load a directory morphology files (.H5 or .SWC)
    elif arguments.input == 'directory':

        # Get all the morphology files in this directory
        morphology_files = file_ops.get_files_in_directory(arguments.morphology_directory, '.h5')
        morphology_files.extend(file_ops.get_files_in_directory(
            arguments.morphology_directory, '.swc'))

        # If the directory is empty, give an error message
        if len(morphology_files) == 0:
            print('ERROR: The directory [%s] does NOT contain any morphology files' %
                  arguments.morphology_directory)

        # A list of all the commands to be executed
        shell_commands = list()

        # Construct the commands for every individual morphology file
        for morphology_file in morphology_files:

            # Get the argument string for an individual file
            arguments_string = arguments_parser.get_arguments_string_for_individual_file(
                arguments=arguments, morphology_file=morphology_file)

            # Construct the shell command to run the workflow
            shell_commands.extend(
                create_shell_commands_for_local_execution(arguments, arguments_string))

        # execute_commands(shell_commands=shell_commands)
        execute_commands_parallel(shell_commands=shell_commands)

    else:
        print('ERROR: Input data source, use \'file, gid, target or directory\'')
        exit(0)


####################################################################################################
# @run_cluster_neuromorphovis
####################################################################################################
def run_cluster_neuromorphovis(arguments):
    """Run the NeuroMorphoVis framework on the BBP visualization cluster using SLURM.

    :param arguments:
        Command line arguments.
    """

    # Use a specific circuit target
    if arguments.input == 'target':

        # Log
        print('Loading a target [%s] in circuit [%s]' % (arguments.target, arguments.blue_config))

        # Ensure a valid blue config and a target
        if arguments.blue_config is None or arguments.target is None:
            print('ERROR: Empty circuit configuration file or target')
            exit(0)

        # Import BluePy
        try:
            import bluepy
        except ImportError:
            print('ERROR: Cannot import [BluePy], please install it')
            exit(0)

        from bluepy import Circuit

        # Loading a circuit
        circuit = Circuit(arguments.blue_config)

        # Loading the GIDs of the sample target within the circuit
        gids = circuit.cells.ids(arguments.target)

        # Run the jobs on the cluster
        slurm.run_gid_jobs_on_cluster(arguments=arguments, gids=gids)

    # Use a single GID
    elif arguments.input == 'gid':

        print('Loading a gid [%s] in circuit [%s]' % (str(arguments.gid), arguments.blue_config))

        # Ensure a valid blue config and a GID
        if arguments.blue_config is None or arguments.gid is None:
            print('ERROR: Empty circuit configuration file or GID')
            exit(0)

        # Run the jobs on the cluster
        slurm.run_gid_jobs_on_cluster(arguments=arguments, gids=[str(arguments.gid)])

    # Use the morphology file (.H5 or .SWC)
    elif arguments.input == 'file':

        # Get the arguments string list
        arguments_string = arguments_parser.get_arguments_string(arguments=arguments)

        # Run the job on the cluster
        slurm.run_morphology_files_jobs_on_cluster(
            arguments=arguments, morphology_files=arguments.morphology_file)

    # Operate on a directory
    elif arguments.input == 'directory':

        # Get all the morphology files in this directory
        morphology_files = file_ops.get_files_in_directory(arguments.morphology_directory, '.h5')

        # Run the jobs on the cluster
        slurm.run_morphology_files_jobs_on_cluster(
            arguments=arguments, morphology_files=morphology_files)

    else:
        print('ERROR: Input data source, use [file, gid, target or directory]')
        exit(0)


####################################################################################################
# @ Run the main function if invoked from the command line.
####################################################################################################
if __name__ == "__main__":

    # Parse the command line arguments
    arguments = arguments_parser.parse_command_line_arguments()

    # Verify the output directory before screwing things !
    if not file_ops.path_exists(arguments.output_directory):
        print('ERROR: Please set the output directory to a valid path')
        exit(0)

    # Otherwise, create the output tree
    else:
        file_ops.create_output_tree(arguments.output_directory)

    # LOCAL EXECUTION: Compile the corresponding command and launch it on the current machine
    if arguments.execution_node == 'local':
        run_local_neuromorphovis(arguments=arguments)

    # BBP CLUSTER EXECUTION: Create the SLURM scripts and run them on the cluster (only @ BBP)
    else:
        run_cluster_neuromorphovis(arguments=arguments)

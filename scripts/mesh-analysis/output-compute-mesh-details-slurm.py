####################################################################################################
# Copyright (c) 2020 - 2021, EPFL / Blue Brain Project
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

import sys, os
import subprocess, shutil, time
import argparse, ntpath


################################################################################
# @slurm_configuration
################################################################################
class SlurmConfiguration:
    """
    SLURM configuration parameters.
    """
    def __init__(self):
        """
        Constructor
        """

        # Job name
        self.job_name = 'NMV-Analysis'

        # Job number
        self.job_number = 0

        # Number of requested nodes for the job
        self.num_nodes = 1

        # Number of tasks per node
        self.num_tasks_per_node = 1

        # Number of CPUs required to run the task
        self.num_cpus_per_task = 1

        # Running partition
        self.partition = 'prod'

        # Required memory
        self.memory_mb = '3000'

        # Session time
        self.session_time = '1:00:00'

        # Session profile
        self.profile = '. /etc/profile'

        # Modules
        self.modules = ['gcc/6.2.0']

        # Execution directory where the scripts will run
        self.execution_directory = ''

        # Logs directory, where the logs will be written
        self.logs_directory = ''


####################################################################################################
# @get_files_in_directory
####################################################################################################
def get_files_in_directory(directory,
                           file_extension=None):
    """Gets all the files in a directory, similar to ls command in linux. If the file extension
    is not specified, it returns a list of all the files.

    :param directory:
        Given directory.
    :param file_extension:
        The extension of requested file.
    :return:
        A list of the requested files.
    """

    # A list of all the files that exist in a directory
    files = []

    # If the extension is not specified
    if file_extension is None:
        for file in os.listdir(directory):
            files.append(file)

    # Otherwise, return files that have specific extensions
    else:
        for file in os.listdir(directory):
            if file.endswith(file_extension):
                files.append(file)

    # Return the list
    return files
    
    
####################################################################################################
# @squeue
####################################################################################################
def squeue():
    """Return a list of all the current jobs on the cluster.

    :return:
        A list of all the current jobs on the cluster.
    """

    # Get the current processes running on the cluster
    result = subprocess.check_output(['squeue'])
    result = str(result)
    return result.split("\\n")


####################################################################################################
# @get_current_number_jobs_for_user
####################################################################################################
def get_current_number_jobs_for_user(user_name):
    """Get the current number of jobs running on the cluster for a specific user identified by his
    user name.

    :param user_name:
        The user name of the user.
    :return:
        The current number of jobs running on the cluster for a specific user identified by his
        user name.
    """

    number_jobs = 0
    jobs = squeue()
    for job in jobs:
        if user_name in job:
            number_jobs += 1
    return number_jobs


####################################################################################################
# @create_batch_job_config_string
####################################################################################################
def create_batch_job_config_string(slurm_config):
    """Create a string header for the batch job.

    :param slurm_config :
        SLURM configuration parameters.
    :rtype
        Batch configuration string.
    """

    # This is for compactness !
    sl = "\n"  # single new line
    dl = "\n\n"  # double new line

    # Magic number
    b = "#!/bin/bash%s" % sl

    """ Auto-generated header """
    b += "######################################################%s" % sl
    b += "# WARNING - AUTO GENERATED FILE%s" % sl
    b += "# Please don't modify that file manually%s" % sl
    b += "######################################################%s" % sl

    """ Node configuration """
    # Job name
    b += "#SBATCH --job-name=\"%s%s\"%s" % (slurm_config.job_name, str(slurm_config.job_number), sl)

    # Number of nodes required to execute the job
    b += "#SBATCH --nodes=%s%s" % (slurm_config.num_nodes, sl)

    # Number of cpus per tasks
    b += "#SBATCH --cpus-per-task=%s%s" % (slurm_config.num_cpus_per_task, sl)

    # Number of tasks
    b += "#SBATCH --ntasks=%s%s" % (slurm_config.num_tasks_per_node, sl)

    # Memory required per task in MBytes
    b += "#SBATCH --mem=%s%s" % (slurm_config.memory_mb, sl)

    # slurm session time
    b += "#SBATCH --time=%s%s" % (slurm_config.session_time, sl)

    # Job partition
    b += "#SBATCH --partition=%s%s" % (slurm_config.partition, sl)

    # Job account
    b += "#SBATCH --account=%s%s" % ("proj3", sl)

    # Reservation
    # b += "#SBATCH --reservation=%s%s" % ("viz_team", sl)

    """ Logs """
    std_out = "%s/slurm-stdout_%s.log" % (slurm_config.logs_directory, str(slurm_config.job_number))
    std_err = "%s/slurm-stderr_%s.log" % (slurm_config.logs_directory, str(slurm_config.job_number))
    b += "#SBATCH --output=%s%s" % (std_out, sl)
    b += "#SBATCH --error=%s%s" % (std_err, dl)

    # Load the modules
    b += '# Loading modules %s' % sl
    for module in slurm_config.modules:
        b+= 'module load %s \n' % module

    """ System variables """
    #  slurm profile
    b += "%s%s%s" % (sl, slurm_config.profile, dl)

    # Job home
    b += "#JOB_HOME=\"%s\"%s" % (slurm_config.execution_directory, sl)

    # Kerberos renewal
    b += "# Renewal of KERBEROS periodically for the length of the job%s" % sl
    b += "krenew -b -K 30%s" % dl

    # Node list
    b += "echo \"On which node your job has been scheduled :\"%s" % sl
    b += "echo $SLURM_JOB_NODELIST%s" % dl

    # Shell limits
    b += "echo \"Print current shell limits :\"%s" % sl
    b += "ulimit -a%s" % dl

    # Running the serial tasks.
    b += "echo \"Running ...\"%s" % sl
    b += "cd %s%s" % (slurm_config.execution_directory, dl)
    ####################################################################

    return b
    
    
####################################################################################################
# @submit_batch_jobs
####################################################################################################
def submit_batch_jobs(user_name,
                      slurm_jobs_directory):
    """Submits all the batch jobs found in the jobs directory.

    This function takes into account the maximum limit imposed by the cluster (500 jobs per user).

    :param user_name:
        The user name of the current user.
    :param slurm_jobs_directory:
        The directory where the batch jobs are created. .
    """

    # Get all the scripts in the slurm jobs directory to submit them
    scripts = get_files_in_directory(slurm_jobs_directory, file_extension='.sh')

    # Use an index to keep track on the number of jobs submitted to the cluster.
    script_index = 0

    # Submit the jobs taking into account the maximum number of jobs dedicated per user
    while True:

        # Just sleep for a second
        time.sleep(1)

        # Get the number of jobs active for that user
        number_active_jobs = get_current_number_jobs_for_user(user_name=user_name)

        # If the number of jobs is greater than 500, then wait a second and try again
        if number_active_jobs >= 500:
            print('Waiting for resources ...')
            continue

        # Otherwise, you can submit some jobs
        else:

            # Get the number of jobs that are available to submit
            number_available_jobs = 500 - number_active_jobs

            # Submit as many jobs as you can
            for i in range(number_available_jobs):

                # Make sure that we still have some jobs to submit, otherwise break
                if script_index >= len(scripts):
                    return

                # Get the script full path
                script_full_path = '%s/%s' % (slurm_jobs_directory, scripts[script_index])

                # 'chmod' the script to be able to execute it
                shell_command = 'chmod +x %s' % script_full_path

                # Execute the command
                subprocess.call(shell_command, shell=True)

                # Format the shell command
                shell_command = 'sbatch %s' % script_full_path

                # Execute the command
                print('Submitting [%s]' % shell_command)
                subprocess.call(shell_command, shell=True)

                # Increment the script index
                script_index += 1
                

####################################################################################################
# @parse_command_line_arguments
####################################################################################################
def parse_command_line_arguments():

    # Create an argument parser, and then add the options one by one
    parser = argparse.ArgumentParser()
    
    # Morphology directory
    arg_help = 'Input meshes directory'
    parser.add_argument('--input-directory', action='store', help=arg_help)
    
    # Output meshes directory 
    arg_help = 'Output meshes directory'
    parser.add_argument('--output-meshes-directory', action='store', help=arg_help)
    
    # Blender
    arg_help = 'Blender'
    parser.add_argument('--blender', action='store', default='blender', help=arg_help)
    
    # Script
    arg_help = 'script'
    parser.add_argument('--script', action='store', help=arg_help)
    
                        
    # Output directory
    arg_help = 'Output directory'
    parser.add_argument('--output-directory', action='store', help=arg_help)
                        
    # Parse the arguments, and return a list of them
    return parser.parse_args()
    

####################################################################################################
# @create_batch_job_script_for_morphology_file
####################################################################################################
def create_batch_jobs(args):
    """Create a batch job file for a morphology file.

    :param arguments:
        Command line arguments.
    :param morphology_file:
        Neuron morphology_file.
    """
    
    # A list of all the batch scripts 
    batch_scripts = list()
    
    # Input meshes list
    input_meshes = os.listdir(args.input_directory)
    
    i = 0
    for input_mesh in input_meshes:
        
        print(i)
            
        # get mesh file name
        mesh_name = ntpath.basename(input_mesh)
        mesh_name = os.path.splitext(mesh_name)[0]
        
        if 'pericyte' in mesh_name:
            continue
        
        # compute info of the dmc meshes
        dmc_meshes_directory = '%s/%s/%s' % (args.output_meshes_directory, mesh_name, 'dmc')

        # get a list of all the dmc meshes 
        dmc_meshes = os.listdir(dmc_meshes_directory)

        for dmc_mesh in dmc_meshes:
            
            i += 1

            # make sure that's an .obj file
            if dmc_mesh.endswith(".obj"):

                # get mesh file name
                dmc_mesh_name = ntpath.basename(dmc_mesh)
                dmc_mesh_name = os.path.splitext(dmc_mesh_name)[0]
                
                # Create slurm configuration
                slurm_config = SlurmConfiguration()

                # Update slurm configuration data
                # Job number should match the gid
                slurm_config.job_number = i

                # Execution directory, same as output directory
                slurm_config.execution_directory = '%s' % args.output_directory
            
                # Log directory
                logs_directory = '%s/%s' % (args.output_directory, 'logs')
                slurm_config.logs_directory = logs_directory
                
                # Generate the batch job configuration string
                batch_job_config_string = create_batch_job_config_string(slurm_config)

                # Setup the shell command
                # Output arguments 
                args_string = '--mesh=%s/%s ' % (dmc_meshes_directory, dmc_mesh)
                args_string += '--output-directory=%s/result ' % (args.output_directory)
                shell_command = '%s -b --verbose 0 --python %s -- %s' % (args.blender, args.script, args_string)

                # Add the command to the batch job config string
                batch_job_config_string += shell_command

                # Write the batch job script to file in the slurm jobs directory
                slurm_jobs_directory = '%s/%s' % (args.output_directory, 'jobs')
                
                job_file_path = '%s/%d.sh' % (slurm_jobs_directory, i)
                f = open(job_file_path, 'w')
                f.write(batch_job_config_string)
                f.close()
                
                batch_scripts.append(job_file_path)
                
        
        # compute info of the laplacian meshes
        laplacian_meshes_directory = '%s/%s/%s' % (args.output_meshes_directory, mesh_name, 'laplacian')

        # get a list of all the laplacian meshes 
        laplacian_meshes = os.listdir(laplacian_meshes_directory)
        
        for laplacian_mesh in laplacian_meshes:
            
            i += 1

            # make sure that's an .obj file
            if laplacian_mesh.endswith(".ply"):

                # get mesh file name
                laplacian_mesh_name = ntpath.basename(laplacian_mesh)
                laplacian_mesh_name = os.path.splitext(laplacian_mesh_name)[0]
                
                # Create slurm configuration
                slurm_config = SlurmConfiguration()

                # Update slurm configuration data
                # Job number should match the gid
                slurm_config.job_number = i

                # Execution directory, same as output directory
                slurm_config.execution_directory = '%s' % args.output_directory
            
                # Log directory
                logs_directory = '%s/%s' % (args.output_directory, 'logs')
                slurm_config.logs_directory = logs_directory
                
                # Generate the batch job configuration string
                batch_job_config_string = create_batch_job_config_string(slurm_config)

                # Setup the shell command
                # Output arguments 
                args_string = '--mesh=%s/%s ' % (laplacian_meshes_directory, laplacian_mesh)
                args_string += '--output-directory=%s/result ' % (args.output_directory)
                shell_command = '%s -b --verbose 0 --python %s -- %s' % (args.blender, args.script, args_string)

                # Add the command to the batch job config string
                batch_job_config_string += shell_command

                # Write the batch job script to file in the slurm jobs directory
                slurm_jobs_directory = '%s/%s' % (args.output_directory, 'jobs')
                
                job_file_path = '%s/%d.sh' % (slurm_jobs_directory, i)
                f = open(job_file_path, 'w')
                f.write(batch_job_config_string)
                f.close()
                
                batch_scripts.append(job_file_path)
                
    return batch_scripts
    

####################################################################################################
# @mkdir
####################################################################################################
def mkdir(directory):
    if os.path.isdir(directory):
        return 
    else:
         os.mkdir(directory)

         
####################################################################################################
# @ Run the main function if invoked from the command line.
####################################################################################################
if __name__ == "__main__":

    # Parse arguments 
    args = parse_command_line_arguments()
    
    mkdir(args.output_directory)
    mkdir('%s/logs' % args.output_directory)
    mkdir('%s/jobs' % args.output_directory)
    mkdir('%s/result' % args.output_directory)
    
    # Create batch script for every mesh 
    batch_jobs = create_batch_jobs(args)
    
    # Submit them 
    # TODO: Add an option for the user
    slurm_jobs_directory = '%s/%s' % (args.output_directory, 'jobs')
    submit_batch_jobs(user_name='abdellah', slurm_jobs_directory=slurm_jobs_directory)



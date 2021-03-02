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
import subprocess
import time

# Internal imports
import nmv.file


####################################################################################################
# @squeue
####################################################################################################
def squeue():
    """Return a list of all the current jobs on the cluster.

    :
    :return:
        A list of all the current jobs on the cluster.
    """

    # Get the current processes running on the cluster
    result = str(subprocess.check_output(['squeue']))
    return result.split('\\n')
    # return result.splitlines()  # Works only with python3.5


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
# @submit_batch_jobs
####################################################################################################
def submit_batch_jobs(user_name,
                      slurm_jobs_directory,
                      maximum_number_jobs=4000):
    """Submits all the batch jobs found in the jobs directory.

    This function takes into account the maximum limit imposed by the cluster (500 jobs per user).

    :param user_name:
        The user name of the current user.
    :param slurm_jobs_directory:
        The directory where the batch jobs are created.
    :param maximum_number_jobs:
        Maximum number of jobs per user.
    """

    # Get all the scripts in the slurm jobs directory to submit them
    scripts = nmv.file.get_files_in_directory(slurm_jobs_directory, file_extension='.sh')

    print(len(scripts))

    # Use an index to keep track on the number of jobs submitted to the cluster.
    script_index = 0

    # Submit the jobs taking into account the maximum number of jobs dedicated per user
    while True:

        # Just sleep for a second
        time.sleep(1)

        # Get the number of jobs active for that user
        number_active_jobs = get_current_number_jobs_for_user(user_name=user_name)
        print(number_active_jobs)
        # If the number of jobs is greater than 500, then wait a second and try again
        if number_active_jobs >= maximum_number_jobs:
            print('Waiting for resources ...')
            continue

        # Otherwise, you can submit some jobs
        else:

            # Get the number of jobs that are available to submit
            number_available_jobs = maximum_number_jobs - number_active_jobs

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

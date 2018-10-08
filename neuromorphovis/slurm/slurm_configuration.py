####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
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
__copyright__   = "Copyright (c) 2016 - 2018, Blue Brain Project / EPFL"
__credits__     = ["Ahmet Bilgili", "Juan Hernando", "Stefan Eilemann"]
__version__     = "1.0.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"


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
        self.job_name = 'NMV'

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
        # self.modules = ['nix/python/3.6-full',
        #                 'nix/blender/2.79-nantille',
        #                 'nix/viz/brion-py3/3.0-dev2017.10']
        self.modules = ['BBP/viz/latest']

        # Execution directory where the scripts will run
        self.execution_directory = ''

        # Logs directory, where the logs will be written
        self.logs_directory = ''
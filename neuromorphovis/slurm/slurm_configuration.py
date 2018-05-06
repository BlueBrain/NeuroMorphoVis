####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of NeuroMorphoVis <https://github.com/BlueBrain/NeuroMorphoVis>
#
# This library is free software; you can redistribute it and/or modify it under the terms of the
# GNU Lesser General Public License version 3.0 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with this library;
# if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA.
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

        empty = ''
        self.job_name = 'MSH'
        self.job_number = 0
        self.num_nodes = 1
        self.num_tasks_per_node = 1
        self.num_cpus_per_task = 1
        self.partition = 'prod'
        self.memory_mb = '3000'
        self.session_time = '1:00:00'
        self.profile = '. /etc/profile'
        #self.modules = ['nix/python/3.6-full',
        #                'nix/blender/2.79-nantille',
        #                'nix/viz/brion-py3/3.0-dev2017.10']
        self.modules = ['BBP/viz/latest']
        self.execution_directory = empty
        self.logs_directory = empty
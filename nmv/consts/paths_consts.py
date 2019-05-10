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

# System imports
import os


####################################################################################################
# Paths
####################################################################################################
class Paths:
    """Paths constants
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    # The folder where the data is stored
    DATA_FOLDER = 'data'

    # The folder where the images will be generated
    IMAGES_FOLDER = 'images'

    # The folder where the output morphologies will be generated
    MORPHOLOGIES_FOLDER = 'morphologies'

    # The folder where the meshes will be generated
    MESHES_FOLDER = 'meshes'

    # The folder where the sequences will be generated
    SEQUENCES_FOLDER = 'sequences'

    # The folder where the stats. will be generated
    STATS_FOLDER = 'stats'

    # The folder where the analysis files will be generated
    ANALYSIS_FOLDER = 'analysis'

    # The folder where SLURM files will be generated
    SLURM_FOLDER = 'slurm'

    # The folder where SLURM jobs will be generated
    SLURM_JOBS_FOLDER = '%s/jobs' % SLURM_FOLDER

    # The folder where SLURM log files will be generated
    SLURM_LOGS_FOLDER = '%s/logs' % SLURM_FOLDER

    # Keep a reference to the current directory
    current_directory = os.path.dirname(os.path.realpath(__file__))

    # The directory where the spines morphologies are located
    SPINES_MORPHOLOGIES_DIRECTORY = '%s/../../data/spines-morphologies' % current_directory

    # The directory where the high quality spine meshes are located
    SPINES_MESHES_HQ_DIRECTORY = '%s/../../data/spines-meshes/hq' % current_directory

    # The directory where the low quality spine meshes are located
    SPINES_MESHES_LQ_DIRECTORY = '%s/../../data/spines-meshes/lq' % current_directory

    # The directory where the high quality nuclei are located
    NUCLEI_MESHES_HQ_DIRECTORY = '%s/../../data/nuclei-meshes/hq' % current_directory

    # The directory where the low quality nuclei are located
    NUCLEI_MESHES_LQ_DIRECTORY = '%s/../../data/nuclei-meshes/lq' % current_directory

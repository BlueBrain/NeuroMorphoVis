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

    # The folder where the analysis files will be generated
    ANALYSIS_FOLDER = 'sequences'

    # The folder where SLURM files will be generated
    SLURM_FOLDER = 'slurm'

    # The folder where SLURM jobs will be generated
    SLURM_JOBS_FOLDER = '%s/jobs' % SLURM_FOLDER

    # The folder where SLURM log files will be generated
    SLURM_LOGS_FOLDER = '%s/logs' % SLURM_FOLDER

    # Keep a reference to the current directory
    current_directory = os.path.dirname(os.path.realpath(__file__))

    # The directory where the spines meshes are located
    SPINES_MESHES_DIRECTORY = '%s/../../data/spines-meshes' % current_directory

    # The directory where the spines morphologies are located
    SPINES_MORPHOLOGIES_DIRECTORY = '%s/../../data/spines-morphologies' % current_directory

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


####################################################################################################
# @IOOptions
####################################################################################################
class IOOptions:
    """Input / Output options.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        """Constructor
        """

        # The root output directory where the results will be generated
        self.output_directory = None

        # Images directory, where the images will be rendered
        self.images_directory = None

        # Sequences directory, where the movies will be rendered
        self.sequences_directory = None

        # Meshes directory, where the reconstructed meshes will be saved
        self.meshes_directory = None

        # Morphologies directory, where the repaired morphologies will be saved
        self.morphologies_directory = None

        # Analysis directory, where the analysis reports will be saved
        self.analysis_directory = None

        # Statistics directory, where the stats. will be saved
        self.statistics_directory = None



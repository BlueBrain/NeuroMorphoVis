####################################################################################################
# Copyright (c) 2016 - 2019, EPFL / Blue Brain Project
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

# Blender imports
import bpy
from bpy.props import IntProperty
from bpy.props import FloatProperty


####################################################################################################
# AnalysisDistribution
####################################################################################################
class AnalysisDistribution:
    """The distribution of a certain analysis item.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 name,
                 kernel=None,
                 description='',
                 data_format='FLOAT',
                 unit='NONE',
                 figure_title=None,
                 figure_label=None,
                 figure_axis_label=None):
        """Constructor

        :param name:
            The name of the entry as appears in the GUI.
        :param kernel:
            The kernel function that will be applied on the morphology when analyzed.
         :param description:
            A little description of the entry to appear as a tooltip in the GUI.
        :param data_format:
            The format of the entry. This could be one of the following options:
                'INT', 'FLOAT'.
        :param unit:
            The unit of the entry. This could be one of the following options:
                NONE, LENGTH, AREA, VOLUME, ROTATION, TIME, VELOCITY, ACCELERATION.
        """

        # Entry name
        self.name = name

        # Analysis filter
        self.kernel = kernel

        # Entry description
        self.description = description

        # Entry format
        self.data_format = data_format

        # Entry unit
        self.unit = unit

        # The title of the figure
        self.figure_title = figure_title

        # The label of the independent axis
        self.figure_axis_label = figure_axis_label

        # The label of the figure that is used to name the file
        self.figure_label = figure_label

        # Analysis result for the entire morphology of type @MorphologyAnalysisResult
        self.result = None

    ################################################################################################
    # @apply_per_arbor_analysis_kernel
    ################################################################################################
    def apply_kernel(self,
                     morphology,
                     options):
        """Applies the analysis kernels 'per-arbor' on the entire morphology.

        :param morphology:
            A given morphology to analyze.
        :param options:
            User defined options.
        """

        if self.kernel is not None:

            # Get the result from applying the kernel on the entire morphology skeleton
            self.result = self.kernel(morphology,
                                      options,
                                      figure_title=self.figure_title,
                                      figure_axis_label=self.figure_axis_label,
                                      figure_label=self.figure_label)

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

# Internal imports
import nmv
import nmv.analysis
import nmv.enums


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
                 description,
                 data_format,
                 figure_title,
                 figure_name,
                 figure_xlabel,
                 compute_total_kernel=None,
                 compute_min_kernel=None,
                 compute_avg_kernel=None,
                 compute_max_kernel=None,
                 add_percentage=False):
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

        # Entry description
        self.description = description

        # Entry format
        self.data_format = data_format

        # The kernel used to compute the total count of a specific property (per arbor)
        self.compute_total_kernel = compute_total_kernel

        # The kernel used to compute the minimum value of a specific property (per arbor)
        self.compute_min_kernel = compute_min_kernel

        # The kernel used to compute the average value of a specific property (per arbor)
        self.compute_avg_kernel = compute_avg_kernel

        # The kernel used to compute the maximum value of a specific property (per arbor)
        self.compute_max_kernel = compute_max_kernel

        # The title of the figure
        self.figure_title = figure_title

        # The label of the independent axis
        self.figure_xlabel = figure_xlabel

        # The label of the figure that is used to name the file
        self.figure_name = figure_name

        # Add percentage to the bars
        self.add_percentage = add_percentage

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

        # Kernel name
        nmv.logger.info('Analysis: %s' % self.name)

        # Compute the total number per arbor
        if nmv.enums.Analysis.Distribution.NUMBER_PER_ARBOR in self.data_format:

            # Total
            analysis_results = nmv.analysis.invoke_kernel(
                morphology,
                self.compute_total_kernel,
                nmv.analysis.compute_total_analysis_result_of_morphology)

            # Plot the distribution
            nmv.analysis.plot_per_arbor_result(analysis_results=analysis_results,
                                               morphology=morphology,
                                               options=options,
                                               figure_name=self.figure_name,
                                               figure_title=self.figure_title,
                                               figure_xlabel=self.figure_xlabel,
                                               add_percentage=self.add_percentage)

        # Compute the range, then plot the average with error bars to show the range of the result
        elif nmv.enums.Analysis.Distribution.RANGE_PER_ARBOR in self.data_format:

            # Minimum
            minimum_results = nmv.analysis.invoke_kernel(
                morphology,
                self.compute_min_kernel,
                nmv.analysis.compute_minimum_analysis_result_of_morphology)

            # Average
            average_results = nmv.analysis.invoke_kernel(
                morphology,
                self.compute_avg_kernel,
                nmv.analysis.compute_average_analysis_result_of_morphology)

            # Maximum
            maximum_results = nmv.analysis.invoke_kernel(
                morphology,
                self.compute_max_kernel,
                nmv.analysis.compute_maximum_analysis_result_of_morphology)

            # Plot the result
            nmv.analysis.plot_per_arbor_range(minimum_results=minimum_results,
                                              maximum_results=maximum_results,
                                              average_results=average_results,
                                              morphology=morphology,
                                              options=options,
                                              figure_name=self.figure_name,
                                              figure_title=self.figure_title,
                                              figure_xlabel=self.figure_xlabel)

        # Non reported kernel
        else:
            nmv.logger.log('A kernel is not implemented')

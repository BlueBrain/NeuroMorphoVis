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

# System imports
import copy

# Internal imports
import nmv.analysis
import nmv.mesh
import nmv.enums
import nmv.skeleton
import nmv.consts
import nmv.geometry
import nmv.scene
import nmv.bmeshi
import nmv.shading
import nmv.utilities


####################################################################################################
# @DendrogramBuilder
####################################################################################################
class DendrogramBuilder:
    """Builds and draws the morphology as a series of samples where each sample is represented by
    a sphere.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 morphology,
                 options):
        """Constructor.

        :param morphology:
            A given morphology.
        """

        # Morphology
        self.morphology = copy.deepcopy(morphology)

        # System options
        self.options = copy.deepcopy(options)

        # All the reconstructed objects of the morphology, for example, poly-lines, spheres etc...
        self.morphology_objects = []

        # A list of the colors/materials of the soma
        self.soma_materials = None

        # A list of the colors/materials of the axon
        self.axon_materials = None

        # A list of the colors/materials of the basal dendrites
        self.basal_dendrites_materials = None

        # A list of the colors/materials of the apical dendrite
        self.apical_dendrite_materials = None

        # A list of the colors/materials of the articulation spheres
        self.articulation_materials = None

        # An aggregate list of all the materials of the skeleton
        self.skeleton_materials = list()

    ################################################################################################
    # @create_single_skeleton_materials_list
    ################################################################################################
    def create_single_skeleton_materials_list(self):
        """Creates a list of all the materials required for coloring the skeleton.

        NOTE: Before drawing the skeleton, create the materials, once and for all, to improve the
        performance since this is way better than creating a new material per section or segment
        or any individual object.
        """
        nmv.logger.info('Creating materials')

        # Create the default material list
        nmv.builders.skeleton.create_skeleton_materials_and_illumination(builder=self)

        # Index: 0 - 1
        self.skeleton_materials.extend(self.soma_materials)

        # Index: 2 - 3
        self.skeleton_materials.extend(self.apical_dendrite_materials)

        # Index: 4 - 5
        self.skeleton_materials.extend(self.basal_dendrites_materials)

        # Index: 6 - 7
        self.skeleton_materials.extend(self.axon_materials)

    ################################################################################################
    # @draw_morphology_skeleton
    ################################################################################################
    def draw_morphology_skeleton(self):
        """Reconstruct and draw the morphological skeleton.

        :return
            A list of all the drawn morphology objects including the soma and arbors.
        """

        nmv.logger.header('Building skeleton using SamplesBuilder')

        nmv.logger.info('Updating Radii')
        nmv.skeleton.update_arbors_radii(self.morphology, self.options.morphology)

        # Create the skeleton materials
        self.create_single_skeleton_materials_list()

        # Resample the sections of the morphology skeleton
        nmv.builders.skeleton.resample_skeleton_sections(builder=self)

        # Get the maximum radius to make it easy to compute the deltas
        maximum_radius = nmv.analysis.kernel_maximum_sample_radius(
            morphology=self.morphology).morphology_result

        # Compute the dendrogram of the morphology
        nmv.skeleton.compute_morphology_dendrogram(
            morphology=self.morphology, delta=maximum_radius * 4)

        # A list of all the skeleton poly-lines
        skeleton_poly_lines = list()

        if not self.options.morphology.ignore_apical_dendrite:
            if self.morphology.apical_dendrite is not None:
                nmv.skeleton.create_dendrogram_poly_lines_list_of_arbor(
                    section=self.morphology.apical_dendrite,
                    poly_lines_data=skeleton_poly_lines,
                    max_branching_order=self.options.morphology.apical_dendrite_branch_order)

        if not self.options.morphology.ignore_basal_dendrites:
            if self.morphology.dendrites is not None:
                for basal_dendrite in self.morphology.dendrites:
                    nmv.skeleton.create_dendrogram_poly_lines_list_of_arbor(
                        section=basal_dendrite,
                        poly_lines_data=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.basal_dendrites_branch_order)

        if not self.options.morphology.ignore_axon:
            if self.morphology.axon is not None:
                nmv.skeleton.create_dendrogram_poly_lines_list_of_arbor(
                    section=self.morphology.axon,
                    poly_lines_data=skeleton_poly_lines,
                    max_branching_order=self.options.morphology.axon_branch_order)

        # The soma to stems line
        center = nmv.skeleton.add_soma_to_stems_line(
            morphology=self.morphology, poly_lines_data=skeleton_poly_lines,
            ignore_apical_dendrite=self.options.morphology.ignore_apical_dendrite,
            ignore_basal_dendrites=self.options.morphology.ignore_basal_dendrites,
            ignore_axon=self.options.morphology.ignore_axon)

        bevel_object = nmv.mesh.create_bezier_circle(
            radius=1.0, vertices=self.options.morphology.bevel_object_sides, name='bevel')
        nmv.scene.hide_object(bevel_object)

        # Draw the poly-lines as a single object
        morphology_object = nmv.geometry.draw_poly_lines_in_single_object(
            poly_lines=skeleton_poly_lines, object_name=self.morphology.label,
            edges=self.options.morphology.edges, bevel_object=bevel_object,
            materials=self.skeleton_materials)

        nmv.scene.set_object_location(morphology_object, center)

        # Always switch to the top view to see the dendrogram quite well
        nmv.scene.view_axis(axis='TOP')

        # Return the list of the drawn morphology objects
        nmv.logger.info('Done')
        return self.morphology_objects

    ################################################################################################
    # @draw_morphology_skeleton
    ################################################################################################
    def draw_morphology_skeleton_with_matplotlib(self):
        """Draws the morphology skeleton dendrogram with matplotlib. The resulting file should be
        included in the analysis fact sheet.
        """

        # Verify the presence of the plotting packages
        nmv.utilities.verify_plotting_packages()

        # Plotting imports
        import numpy
        import seaborn
        import matplotlib.pyplot as pyplot
        from matplotlib import font_manager

        # Import the fonts
        font_dirs = [nmv.consts.Paths.FONTS_DIRECTORY]
        font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
        font_list = font_manager.createFontList(font_files)
        font_manager.fontManager.ttflist.extend(font_list)

        # Create the color palette
        self.morphology.create_morphology_color_palette()

        # Resample the sections of the morphology skeleton
        nmv.builders.skeleton.resample_skeleton_sections(builder=self)

        # Get the maximum radius to make it easy to compute the deltas
        maximum_radius = nmv.analysis.kernel_maximum_sample_radius(
            morphology=self.morphology).morphology_result

        # Compute the dendrogram of the morphology
        nmv.skeleton.compute_morphology_dendrogram(
            morphology=self.morphology, delta=maximum_radius * 8)

        # Clean the environment
        pyplot.clf()

        # Adjust seaborn configuration
        seaborn.set_style("white")

        # The width of each bar
        bar_width = 0.65

        # Adjust seaborn configuration
        seaborn.set_style("white")

        # Adjusting the matplotlib parameters
        pyplot.rcParams['axes.grid'] = 'False'
        pyplot.rcParams['font.family'] = 'NimbusSanL'
        pyplot.rcParams['axes.linewidth'] = 0.0
        pyplot.rcParams['axes.labelsize'] = bar_width * 10
        pyplot.rcParams['axes.labelweight'] = 'regular'
        pyplot.rcParams['xtick.labelsize'] = bar_width * 10
        pyplot.rcParams['ytick.labelsize'] = bar_width * 10
        pyplot.rcParams['legend.fontsize'] = 10
        pyplot.rcParams['axes.titlesize'] = bar_width * 1.25 * 10
        pyplot.rcParams['axes.axisbelow'] = True
        pyplot.rcParams['axes.edgecolor'] = '0.1'
        pyplot.axis('off')

        if not self.options.morphology.ignore_apical_dendrite:

            # A list of all the skeleton poly-lines
            skeleton_poly_lines = list()

            if self.morphology.apical_dendrite is not None:
                nmv.skeleton.create_dendrogram_poly_lines_list_of_arbor(
                    section=self.morphology.apical_dendrite,
                    poly_lines_data=skeleton_poly_lines,
                    max_branching_order=self.options.morphology.apical_dendrite_branch_order,
                    stretch_legs=False)

                for poly_line in skeleton_poly_lines:

                    x_list = list()
                    y_list = list()

                    for i, sample in enumerate(poly_line.samples):
                        x_list.append(sample[0][0])
                        y_list.append(sample[0][1])

                    x = numpy.array(x_list)
                    y = numpy.array(y_list)

                    ax = pyplot.plot([x_list[0], x_list[1]], [y_list[0], y_list[1]], lw=1.0,
                                     color=self.morphology.apical_dendrite_color)

        if not self.options.morphology.ignore_axon:
            if self.morphology.axon is not None:
                # A list of all the skeleton poly-lines
                skeleton_poly_lines = list()

                nmv.skeleton.create_dendrogram_poly_lines_list_of_arbor(
                    section=self.morphology.axon,
                    poly_lines_data=skeleton_poly_lines,
                    max_branching_order=self.options.morphology.axon_branch_order,
                    stretch_legs=False)

                for poly_line in skeleton_poly_lines:

                    x_list = list()
                    y_list = list()

                    for i, sample in enumerate(poly_line.samples):
                        x_list.append(sample[0][0])
                        y_list.append(sample[0][1])

                    x = numpy.array(x_list)
                    y = numpy.array(y_list)

                    ax = pyplot.plot([x_list[0], x_list[1]], [y_list[0], y_list[1]], lw=1.0,
                                  color=self.morphology.axon_color)

        if not self.options.morphology.ignore_basal_dendrites:
            if self.morphology.dendrites is not None:
                for i, basal_dendrite in enumerate(self.morphology.dendrites):

                    # A list of all the skeleton poly-lines
                    skeleton_poly_lines = list()

                    nmv.skeleton.create_dendrogram_poly_lines_list_of_arbor(
                        section=basal_dendrite,
                        poly_lines_data=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.basal_dendrites_branch_order,
                        stretch_legs=False)

                    color = self.morphology.basal_dendrites_colors[i]
                    for poly_line in skeleton_poly_lines:

                        x_list = list()
                        y_list = list()

                        for i, sample in enumerate(poly_line.samples):
                            x_list.append(sample[0][0])
                            y_list.append(sample[0][1])

                        x = numpy.array(x_list)
                        y = numpy.array(y_list)

                        ax = pyplot.plot([x_list[0], x_list[1]], [y_list[0], y_list[1]], lw=1.0,
                                         color=color)

        # The soma to stems line
        skeleton_poly_lines = list()
        center = nmv.skeleton.add_soma_to_stems_line(
            morphology=self.morphology, poly_lines_data=skeleton_poly_lines,
            ignore_apical_dendrite=self.options.morphology.ignore_apical_dendrite,
            ignore_basal_dendrites=self.options.morphology.ignore_basal_dendrites,
            ignore_axon=self.options.morphology.ignore_axon)

        for poly_line in skeleton_poly_lines:

            x_list = list()
            y_list = list()

            for i, sample in enumerate(poly_line.samples):
                x_list.append(sample[0][0])
                y_list.append(sample[0][1])

            x = numpy.array(x_list)
            y = numpy.array(y_list)

            ax = pyplot.plot([x_list[0], x_list[1]], [y_list[0], y_list[1]], lw=1.0,
                             color=self.morphology.soma_color)

        # Draw PNG figure
        png_file_path = '%s/%s/dendrogram.png' % \
                        (self.options.io.analysis_directory, self.morphology.label)
        pyplot.savefig(png_file_path, bbox_inches='tight', transparent=True, dpi=300)

        # Draw PDF figure
        pdf_file_path = '%s/%s/dendrogram.pdf' % \
                        (self.options.io.analysis_directory, self.morphology.label)
        pyplot.savefig(pdf_file_path, bbox_inches='tight', transparent=True, dpi=300)

        # Return the file path
        return pdf_file_path

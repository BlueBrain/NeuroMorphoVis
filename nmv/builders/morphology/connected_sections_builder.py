####################################################################################################
# Copyright (c) 2016 - 2019, EPFL / Blue Brain Project
# Author: Marwan Abdellah <marwan.abdellah@epfl.ch>
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
import numpy
import seaborn

# Internal imports
from .base import MorphologyBuilderBase
import nmv.mesh
import nmv.enums
import nmv.skeleton
import nmv.consts
import nmv.geometry
import nmv.scene
import nmv.utilities


####################################################################################################
# @ConnectedSectionsBuilder
####################################################################################################
class ConnectedSectionsBuilder(MorphologyBuilderBase):
    """Builds and draws the morphology as a series of connected sections like a stream from the
    root section to the leaf on every arbor."""

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

        # Initialize the parent with the common parameters
        MorphologyBuilderBase.__init__(self, morphology, options)

        # Validate the arbors connectivity to the soma
        nmv.skeleton.verify_arbors_connectivity_to_soma(self.morphology)

    ################################################################################################
    # @create_arbor_component
    ################################################################################################
    def create_arbor_component(self,
                               arbor,
                               bevel_object,
                               arbor_name,
                               max_branching_order):
        """Creates a single polyline of the given arbor and add it to the morphology objects list.

        :param arbor:
        :param bevel_object:
            Bevel object used to extrude the arbors.
        :param arbor_name:
            The name of the arbor.
        :param max_branching_order:
            The maximum branching order of the arbor.
        """

        # A list of all the skeleton poly-lines
        skeleton_poly_lines = list()

        # Construct the poly-line objects
        nmv.skeleton.get_arbor_poly_lines_as_connected_sections(
            root=arbor,
            soma_center=self.morphology.soma.centroid,
            poly_lines_data=skeleton_poly_lines,
            connection_to_soma=self.options.morphology.arbors_to_soma_connection,
            max_branching_order=max_branching_order)

        # Draw the poly-lines as a single object
        arbor_object = nmv.geometry.draw_poly_lines_in_single_object(
            poly_lines=skeleton_poly_lines, object_name=arbor_name,
            edges=self.options.morphology.edges, bevel_object=bevel_object,
            materials=self.skeleton_materials)

        # Append it to the morphology objects
        self.morphology_objects.append(arbor_object)

    ################################################################################################
    # @create_all_arbors_as_single_component
    ################################################################################################
    def create_each_arbor_as_separate_component(self):
        """Creates each arbor in the morphology as a single separate component."""

        nmv.logger.info('Reconstructing arbors')

        # Apical dendrites
        if not self.options.morphology.ignore_apical_dendrites:
            if self.morphology.has_apical_dendrites():
                for arbor in self.morphology.apical_dendrites:
                    nmv.logger.detail(arbor.label)
                    self.create_arbor_component(
                        arbor=arbor, bevel_object=self.bevel_object, arbor_name=arbor.label,
                        max_branching_order=self.options.morphology.apical_dendrite_branch_order)

        # Basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:
            if self.morphology.has_basal_dendrites():
                for arbor in self.morphology.basal_dendrites:
                    nmv.logger.detail(arbor.label)
                    self.create_arbor_component(
                        arbor=arbor, bevel_object=self.bevel_object, arbor_name=arbor.label,
                        max_branching_order=self.options.morphology.basal_dendrites_branch_order)

        # Axons
        if not self.options.morphology.ignore_axons:
            if self.morphology.has_axons():
                for arbor in self.morphology.axons:
                    nmv.logger.detail(arbor.label)
                    self.create_arbor_component(
                        arbor=arbor, bevel_object=self.bevel_object, arbor_name=arbor.label,
                        max_branching_order=self.options.morphology.axon_branch_order)

    ################################################################################################
    # @create_all_arbors_as_single_component
    ################################################################################################
    def create_all_arbors_as_single_component(self,
                                              bevel_object):
        """Creates all the arbors in the morphology as a single component.

        :param bevel_object:
            Bevel object used to interpolate the polyline.
        """

        # A list of all the skeleton poly-lines
        skeleton_poly_lines = list()

        # Apical dendrite
        nmv.logger.info('Reconstructing arbors')
        if not self.options.morphology.ignore_apical_dendrites:
            if self.morphology.has_apical_dendrites():
                for arbor in self.morphology.apical_dendrites:
                    nmv.logger.detail(arbor.label)
                    nmv.skeleton.get_arbor_poly_lines_as_connected_sections(
                        root=arbor,
                        soma_center=self.morphology.soma.centroid,
                        poly_lines_data=skeleton_poly_lines,
                        connection_to_soma=self.options.morphology.arbors_to_soma_connection,
                        max_branching_order=self.options.morphology.apical_dendrite_branch_order)

        # Basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:
            if self.morphology.has_basal_dendrites():
                for arbor in self.morphology.basal_dendrites:
                    nmv.logger.detail(arbor.label)
                    nmv.skeleton.get_arbor_poly_lines_as_connected_sections(
                        root=arbor,
                        soma_center=self.morphology.soma.centroid,
                        poly_lines_data=skeleton_poly_lines,
                        connection_to_soma=self.options.morphology.arbors_to_soma_connection,
                        max_branching_order=self.options.morphology.basal_dendrites_branch_order)

        # Axon
        if not self.options.morphology.ignore_axons:
            if self.morphology.has_axons():
                for arbor in self.morphology.axons:
                    nmv.logger.detail(arbor.label)
                    nmv.skeleton.get_arbor_poly_lines_as_connected_sections(
                        root=arbor,
                        soma_center=self.morphology.soma.centroid,
                        poly_lines_data=skeleton_poly_lines,
                        connection_to_soma=self.options.morphology.arbors_to_soma_connection,
                        max_branching_order=self.options.morphology.axon_branch_order)

        # Draw the poly-lines as a single object
        morphology_object = nmv.geometry.draw_poly_lines_in_single_object(
            poly_lines=skeleton_poly_lines, object_name=self.morphology.label,
            edges=self.options.morphology.edges, bevel_object=bevel_object,
            materials=self.skeleton_materials)

        # Append it to the morphology objects
        self.morphology_objects.append(morphology_object)

    ################################################################################################
    # @draw_poly_line_list_at_fixed_thickness
    ################################################################################################
    @staticmethod
    def draw_poly_line_list_at_fixed_thickness(poly_lines,
                                               color,
                                               thickness=0.5,
                                               projection=nmv.enums.Camera.View.FRONT):
        """Draws the poly-line using seaborn with a fixed line thickness.

        :param poly_lines:
            A list of all the poly-lines.
        :param color:
            Color.
        :param thickness:
            Thickness.
        :param projection:
            Projection.
        :return:
            A handle to the figure.
        """

        # Verify the presence of the plotting packages
        nmv.utilities.verify_plotting_packages()

        # Plotting imports
        import numpy
        import seaborn

        # A handle to the figure
        figure = None

        # Line by line
        for poly_line in poly_lines:

            # Lists to compile the data
            x_list = []
            y_list = []

            # Append the samples
            for sample in poly_line.samples:
                if projection == nmv.enums.Camera.View.FRONT:
                    x_list.append(sample[0][0])
                    y_list.append(sample[0][1])
                elif projection == nmv.enums.Camera.View.SIDE:
                    x_list.append(sample[0][2])
                    y_list.append(sample[0][1])
                elif projection == nmv.enums.Camera.View.TOP:
                    x_list.append(sample[0][0])
                    y_list.append(sample[0][2])
                else:
                    x_list.append(sample[0][0])
                    y_list.append(sample[0][1])

            # Convert the lists to numpy arrays for the plotting function
            x = numpy.array(x_list)
            y = numpy.array(y_list)

            # Plot the data with seaborn
            figure = seaborn.lineplot(x=x, y=y, sort=False, lw=thickness, color=color)

        # Return the handle to the figure
        return figure

    ################################################################################################
    # @draw_poly_line_list_at_scale
    ################################################################################################
    @staticmethod
    def draw_poly_line_list_at_scale(poly_lines,
                                     color,
                                     scale=1.0,
                                     projection=nmv.enums.Camera.View.FRONT):
        """Draws the poly-line using seaborn according to the actual radii.

        :param poly_lines:
            A list of all the poly-lines.
        :param color:
            Color.
        :param scale: 
            A scale value that will be used to scale the radii.
       :param projection:
            Projection.
        :return:
            A handle to the figure.
        :return: 
        """

        # Verify the presence of the plotting packages
        nmv.utilities.verify_plotting_packages()

        # A handle to the figure
        figure = None

        # Line by line
        for poly_line in poly_lines:

            # Segment by segment in the line
            for i in range(len(poly_line.samples) - 1):

                # Segment samples
                sample_0 = poly_line.samples[i]
                sample_1 = poly_line.samples[i + 1]

                # Data
                x_list = list()
                y_list = list()

                # Append the samples
                if projection == nmv.enums.Camera.View.FRONT:
                    x_list.append(sample_0[0][0])
                    x_list.append(sample_1[0][0])
                    y_list.append(sample_0[0][1])
                    y_list.append(sample_1[0][1])
                elif projection == nmv.enums.Camera.View.SIDE:
                    x_list.append(sample_0[0][1])
                    x_list.append(sample_1[0][1])
                    y_list.append(sample_0[0][2])
                    y_list.append(sample_1[0][2])
                elif projection == nmv.enums.Camera.View.TOP:
                    x_list.append(sample_0[0][0])
                    x_list.append(sample_1[0][0])
                    y_list.append(sample_0[0][2])
                    y_list.append(sample_1[0][2])
                else:
                    x_list.append(sample_0[0][0])
                    x_list.append(sample_1[0][0])
                    y_list.append(sample_0[0][1])
                    y_list.append(sample_1[0][1])

                # Radius value
                radius = 0.5 * (sample_0[1] + sample_1[1]) * scale

                # Convert the lists to numpy array
                x = numpy.array(x_list)
                y = numpy.array(y_list)

                # Plot the data
                figure = seaborn.lineplot(x=x, y=y, sort=False, lw=radius, color=color)

        # Return the handle to the figure
        return figure

    ################################################################################################
    # @draw_soma_projection
    ################################################################################################
    def draw_soma_projection(self,
                             projection=nmv.enums.Camera.View.FRONT):
        """Draws the projection of the soma.

        :param projection:
            Projection.
        """

        # Verify the presence of the plotting packages
        nmv.utilities.verify_plotting_packages()

        # Plotting imports
        import numpy
        import matplotlib
        matplotlib.use('agg')
        import matplotlib.pyplot as pyplot

        # The soma
        soma_builder_object = nmv.builders.SomaMetaBuilder(self.morphology, self.options)
        vertices = soma_builder_object.get_soma_profile()

        # Project to xy
        x_list = list()
        y_list = list()

        # Compile the data
        for vertex in vertices:

            if projection == nmv.enums.Camera.View.FRONT:
                x_list.append(vertex[0])
                y_list.append(vertex[1])
            elif projection == nmv.enums.Camera.View.SIDE:
                x_list.append(vertex[1])
                y_list.append(vertex[2])
            elif projection == nmv.enums.Camera.View.TOP:
                x_list.append(vertex[0])
                y_list.append(vertex[2])
            else:
                x_list.append(vertex[0])
                y_list.append(vertex[1])

        # Convert the lists to numpy arrays
        x = numpy.asarray(x_list)
        y = numpy.asarray(y_list)

        # Plot
        matplotlib.pyplot.scatter(x, y, c=self.morphology.soma_color, sizes=(0.25, 0.5), alpha=0.25)

    ################################################################################################
    # @draw_morphology_skeleton_with_matplotlib
    ################################################################################################
    def draw_morphology_skeleton_with_matplotlib(self,
                                                 projection=nmv.enums.Camera.View.FRONT):
        """Draws the morphology skeleton with matplotlib.

        :param projection:
            The view of projection of the neuron, by default front view.

        :return
            The path to the generated PDF file.
        """

        # Update the radii of the arbors according to the given options
        nmv.skeleton.update_arbors_radii(
            morphology=self.morphology, morphology_options=self.options.morphology)

        # Update the branching
        nmv.skeleton.update_skeleton_branching(morphology=self.morphology,
                                               branching_method=self.options.morphology.branching)

        # Update the style of the arbors
        nmv.skeleton.ops.update_arbors_style(
            morphology=self.morphology, arbor_style=self.options.morphology.arbor_style)

        # Verify the presence of the plotting packages
        nmv.utilities.verify_plotting_packages()

        # Plotting imports
        import seaborn
        import matplotlib
        matplotlib.use('agg')
        import matplotlib.pyplot as pyplot

        # Create the color palette
        self.morphology.create_morphology_color_palette()

        # Clear the figure
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

        # A handle to the figure
        figure = None

        # Apical dendrite
        nmv.logger.info('Reconstructing arbors')
        if not self.options.morphology.ignore_apical_dendrites:
            if self.morphology.has_apical_dendrites():
                for i, arbor in enumerate(self.morphology.apical_dendrites):
                    nmv.logger.detail(arbor.label)

                    # Get the lines
                    apical_dendrite_poly_lines = list()
                    nmv.skeleton.get_arbor_poly_lines_as_connected_sections(
                        root=arbor,
                        soma_center=self.morphology.soma.centroid,
                        poly_lines_data=apical_dendrite_poly_lines,
                        connection_to_soma=self.options.morphology.arbors_to_soma_connection,
                        max_branching_order=self.options.morphology.apical_dendrite_branch_order)

                    # Plot the lines
                    figure = self.draw_poly_line_list_at_fixed_thickness(
                        poly_lines=apical_dendrite_poly_lines,
                        color=self.morphology.apical_dendrites_colors[i], thickness=0.5,
                        projection=projection)

        # Basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:
            if self.morphology.has_basal_dendrites():
                for i, arbor in enumerate(self.morphology.basal_dendrites):
                    nmv.logger.detail(arbor.label)

                    # Get the lines
                    basal_dendrite_poly_lines = list()
                    nmv.skeleton.get_arbor_poly_lines_as_connected_sections(
                        root=arbor,
                        soma_center=self.morphology.soma.centroid,
                        poly_lines_data=basal_dendrite_poly_lines,
                        connection_to_soma=self.options.morphology.arbors_to_soma_connection,
                        max_branching_order=self.options.morphology.basal_dendrites_branch_order)

                    # Plot the lines
                    figure = self.draw_poly_line_list_at_fixed_thickness(
                        poly_lines=basal_dendrite_poly_lines,
                        color=self.morphology.basal_dendrites_colors[i], thickness=0.5,
                        projection=projection)

        # Axon
        if not self.options.morphology.ignore_axons:
            if self.morphology.has_axons():
                for i, arbor in enumerate(self.morphology.axons):
                    nmv.logger.detail(arbor.label)

                    # Get the lines
                    axon_poly_lines = list()
                    nmv.skeleton.get_arbor_poly_lines_as_connected_sections(
                        root=arbor,
                        soma_center=self.morphology.soma.centroid,
                        poly_lines_data=axon_poly_lines,
                        connection_to_soma=self.options.morphology.arbors_to_soma_connection,
                        max_branching_order=self.options.morphology.axon_branch_order)

                    # Plot the lines
                    figure = self.draw_poly_line_list_at_fixed_thickness(
                        poly_lines=axon_poly_lines,
                        color=self.morphology.axons_colors[i], thickness=0.5,
                        projection=projection)

        # Soma
        self.draw_soma_projection()

        # Adjust the scale
        figure.set_aspect(aspect='equal')

        # PNG figure
        pdf_file_path = '%s/%s/%s.png' % (self.options.io.analysis_directory,
                                          self.morphology.label, projection)
        pyplot.savefig(pdf_file_path, bbox_inches='tight', transparent=True, dpi=300)

        # PDF figure
        pdf_file_path = '%s/%s/%s.pdf' % (self.options.io.analysis_directory,
                                          self.morphology.label, projection)
        pyplot.savefig(pdf_file_path, bbox_inches='tight', transparent=True, dpi=300)

        if projection == nmv.enums.Camera.View.FRONT:
            figure.set_xlim(
                (self.morphology.bounding_box.p_min.x, self.morphology.bounding_box.p_max.x))
            figure.set_ylim(
                (self.morphology.bounding_box.p_min.y, self.morphology.bounding_box.p_max.y))
        elif projection == nmv.enums.Camera.View.SIDE:
            figure.set_xlim(
                (self.morphology.bounding_box.p_min.z, self.morphology.bounding_box.p_max.z))
            figure.set_ylim(
                (self.morphology.bounding_box.p_min.y, self.morphology.bounding_box.p_max.y))
        elif projection == nmv.enums.Camera.View.TOP:
            figure.set_xlim(
                (self.morphology.bounding_box.p_min.x, self.morphology.bounding_box.p_max.x))
            figure.set_ylim(
                (self.morphology.bounding_box.p_min.z, self.morphology.bounding_box.p_max.z))
        else:
            pass

        # Title
        figure.set(xlabel=projection)

        # PNG figure
        pdf_file_path = '%s/%s/%s.png' % (self.options.io.analysis_directory,
                                          self.morphology.label, projection)
        pyplot.savefig(pdf_file_path, bbox_inches='tight', transparent=True, dpi=300)

        # PDF figure
        pdf_file_path = '%s/%s/%s.pdf' % (self.options.io.analysis_directory,
                                          self.morphology.label, projection)
        pyplot.savefig(pdf_file_path, bbox_inches='tight', transparent=True, dpi=300)

        return pdf_file_path

    ################################################################################################
    # @draw_morphology_skeleton
    ################################################################################################
    def draw_morphology_skeleton(self,
                                 context=None):
        """Reconstruct and draw the morphological skeleton.

        :return
            A list of all the drawn morphology objects including the soma and arbors.
        """

        # Update the context
        self.context = context

        nmv.logger.header('Building Skeleton: ConnectedSectionsBuilder')

        # Initializes the builder
        self.initialize_builder()

        # Create each arbor as a separate component
        self.create_each_arbor_as_separate_component()

        # TODO: Add an option to handle this.
        # Create all the arbors as a single component
        # self.create_all_arbors_as_single_component(bevel_object=bevel_object)

        # Draw the soma
        self.draw_soma()

        # Draw the endfeet, if applicable
        self.draw_endfeet_if_applicable()

        # Add the morphology objects to a collection
        self.collection_morphology_objects_in_collection()

        # Return the list of the drawn morphology objects
        return self.morphology_objects

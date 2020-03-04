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

# Blender imports
import bpy

# Internal imports
import nmv.mesh
import nmv.enums
import nmv.skeleton
import nmv.consts
import nmv.geometry
import nmv.scene
import nmv.utilities


####################################################################################################
# @DisconnectedSectionsBuilder
####################################################################################################
class ConnectedSectionsBuilder:
    """Builds and draws the morphology as a series of connected sections like a stream from the
    root section to the leaf on every arbor.
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
    # @create_arbor_component
    ################################################################################################
    def create_arbor_component(self,
                               arbor,
                               bevel_object,
                               component_name,
                               max_branching_level):

        # A list of all the skeleton poly-lines
        skeleton_poly_lines = list()

        # Construct the poly-line objects
        nmv.skeleton.get_arbor_poly_lines_as_connected_sections(
            root=arbor,
            poly_lines_data=skeleton_poly_lines,
            connection_to_soma=self.options.morphology.arbors_to_soma_connection,
            max_branching_level=max_branching_level)

        # Draw the poly-lines as a single object
        morphology_object = nmv.geometry.draw_poly_lines_in_single_object(
            poly_lines=skeleton_poly_lines, object_name=component_name,
            edges=self.options.morphology.edges, bevel_object=bevel_object,
            materials=self.skeleton_materials)

        # Append it to the morphology objects
        self.morphology_objects.append(morphology_object)

    ################################################################################################
    # @create_all_arbors_as_single_component
    ################################################################################################
    def create_each_arbor_as_separate_component(self,
                                                bevel_object):

        # Apical dendrite
        nmv.logger.info('Constructing poly-lines')
        if not self.options.morphology.ignore_apical_dendrite:
            if self.morphology.apical_dendrite is not None:
                nmv.logger.detail('Apical dendrite')
                self.create_arbor_component(
                    arbor=self.morphology.apical_dendrite,
                    bevel_object=bevel_object, component_name='ApicalDendrite',
                    max_branching_level=self.options.morphology.apical_dendrite_branch_order)

        # Axon
        if not self.options.morphology.ignore_axon:
            if self.morphology.axon is not None:
                nmv.logger.detail('Axon')
                self.create_arbor_component(
                    arbor=self.morphology.axon, bevel_object=bevel_object, component_name='Axon',
                    max_branching_level=self.options.morphology.axon_branch_order)

        # Basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:
            if self.morphology.dendrites is not None:
                for i, basal_dendrite in enumerate(self.morphology.dendrites):
                    nmv.logger.detail('Basal dendrite [%d]' % i)
                    self.create_arbor_component(
                        arbor=basal_dendrite, bevel_object=bevel_object,
                        component_name='BasalDendrite_%d' % i,
                        max_branching_level=self.options.morphology.basal_dendrites_branch_order)

    ################################################################################################
    # @create_all_arbors_as_single_component
    ################################################################################################
    def create_all_arbors_as_single_component(self,
                                              bevel_object):
        """Creates all the arbors in the morphology as a single component
        """

        # A list of all the skeleton poly-lines
        skeleton_poly_lines = list()

        # Apical dendrite
        nmv.logger.info('Constructing poly-lines')
        if not self.options.morphology.ignore_apical_dendrite:
            if self.morphology.apical_dendrite is not None:
                nmv.logger.detail('Apical dendrite')

                # Construct the poly-line objects
                nmv.skeleton.get_arbor_poly_lines_as_connected_sections(
                    root=self.morphology.apical_dendrite,
                    poly_lines_data=skeleton_poly_lines,
                    connection_to_soma=self.options.morphology.arbors_to_soma_connection,
                    max_branching_level=self.options.morphology.apical_dendrite_branch_order)

        # Axon
        if not self.options.morphology.ignore_axon:
            if self.morphology.axon is not None:
                nmv.logger.detail('Axon')
                nmv.skeleton.get_arbor_poly_lines_as_connected_sections(
                    root=self.morphology.axon,
                    poly_lines_data=skeleton_poly_lines,
                    connection_to_soma=self.options.morphology.arbors_to_soma_connection,
                    max_branching_level=self.options.morphology.axon_branch_order)

        # Basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:
            if self.morphology.dendrites is not None:
                for i, basal_dendrite in enumerate(self.morphology.dendrites):
                    nmv.logger.detail('Basal dendrite [%d]' % i)
                    nmv.skeleton.get_arbor_poly_lines_as_connected_sections(
                        root=basal_dendrite,
                        poly_lines_data=skeleton_poly_lines,
                        connection_to_soma=self.options.morphology.arbors_to_soma_connection,
                        max_branching_level=self.options.morphology.basal_dendrites_branch_order)

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

        # Installing dependencies
        try:
            import numpy
        except ValueError:
            print('Package *numpy* is not installed. Installing it.')
            nmv.utilities.pip_wheel(package_name='numpy')

        try:
            import matplotlib
        except ValueError:
            print('Package *matplotlib* is not installed. Installing it.')
            nmv.utilities.pip_wheel(package_name='matplotlib')

        try:
            import seaborn
        except ValueError:
            print('Package *seaborn* is not installed. Installing it.')
            nmv.utilities.pip_wheel(package_name='seaborn')

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
    # @    def draw_poly_line_list_at_scale
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

        # Installing dependencies
        try:
            import numpy
        except ValueError:
            print('Package *numpy* is not installed. Installing it.')
            nmv.utilities.pip_wheel(package_name='numpy')

        try:
            import matplotlib
        except ValueError:
            print('Package *matplotlib* is not installed. Installing it.')
            nmv.utilities.pip_wheel(package_name='matplotlib')

        try:
            import seaborn
        except ValueError:
            print('Package *seaborn* is not installed. Installing it.')
            nmv.utilities.pip_wheel(package_name='seaborn')

        # Plotting imports
        import numpy
        import seaborn
        import matplotlib.pyplot as pyplot
        from matplotlib import font_manager

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

        # Installing dependencies
        try:
            import numpy
        except ValueError:
            print('Package *numpy* is not installed. Installing it.')
            nmv.utilities.pip_wheel(package_name='numpy')

        try:
            import matplotlib
        except ValueError:
            print('Package *matplotlib* is not installed. Installing it.')
            nmv.utilities.pip_wheel(package_name='matplotlib')

        # Plotting imports
        import numpy
        import matplotlib

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

        nmv.skeleton.update_arbors_radii(
            morphology=self.morphology, morphology_options=self.options.morphology)

        nmv.logger.info('Updating Branching to Primary / Secondary')
        nmv.builders.skeleton.update_sections_branching(builder=self)

        # Update the style of the arbors
        nmv.skeleton.ops.update_arbors_style(
            morphology=self.morphology, arbor_style=self.options.morphology.arbor_style)

        # A list of all the skeleton poly-lines

        # Installing dependencies
        try:
            import numpy
        except ValueError:
            print('Package *numpy* is not installed. Installing it.')
            nmv.utilities.pip_wheel(package_name='numpy')

        try:
            import matplotlib
        except ValueError:
            print('Package *matplotlib* is not installed. Installing it.')
            nmv.utilities.pip_wheel(package_name='matplotlib')

        try:
            import seaborn
        except ValueError:
            print('Package *seaborn* is not installed. Installing it.')
            nmv.utilities.pip_wheel(package_name='seaborn')

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

        # Clear the figure
        matplotlib.pyplot.clf()

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
        nmv.logger.info('Constructing poly-lines')
        if not self.options.morphology.ignore_apical_dendrite:
            if self.morphology.apical_dendrite is not None:
                nmv.logger.detail('Apical dendrite')

                # Get the lines
                apical_dendrite_poly_lines = list()
                nmv.skeleton.get_arbor_poly_lines_as_connected_sections(
                    root=self.morphology.apical_dendrite,
                    poly_lines_data=apical_dendrite_poly_lines,
                    connection_to_soma=self.options.morphology.arbors_to_soma_connection,
                    max_branching_level=self.options.morphology.apical_dendrite_branch_order)

                # Plot the lines
                figure = self.draw_poly_line_list_at_fixed_thickness(
                    poly_lines=apical_dendrite_poly_lines,
                    color=self.morphology.apical_dendrite_color, thickness=0.5,
                    projection=projection)

        # Basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:
            if self.morphology.dendrites is not None:
                for i, basal_dendrite in enumerate(self.morphology.dendrites):
                    nmv.logger.detail('Basal dendrite [%d]' % i)

                    # Get the lines
                    basal_dendrite_poly_lines = list()
                    nmv.skeleton.get_arbor_poly_lines_as_connected_sections(
                        root=basal_dendrite,
                        poly_lines_data=basal_dendrite_poly_lines,
                        connection_to_soma=self.options.morphology.arbors_to_soma_connection,
                        max_branching_level=self.options.morphology.basal_dendrites_branch_order)

                    # Plot the lines
                    figure = self.draw_poly_line_list_at_fixed_thickness(
                        poly_lines=basal_dendrite_poly_lines,
                        color=self.morphology.basal_dendrites_colors[i], thickness=0.5)

        # Axon
        if not self.options.morphology.ignore_axon:
            if self.morphology.axon is not None:

                nmv.logger.detail('Axon')

                # Get the lines
                axon_poly_lines = list()
                nmv.skeleton.get_arbor_poly_lines_as_connected_sections(
                    root=self.morphology.axon,
                    poly_lines_data=axon_poly_lines,
                    connection_to_soma=self.options.morphology.arbors_to_soma_connection,
                    max_branching_level=self.options.morphology.axon_branch_order)

                # Plot the lines
                figure = self.draw_poly_line_list_at_fixed_thickness(
                    poly_lines=axon_poly_lines,
                    color=self.morphology.axon_color, thickness=0.5)

        # Soma
        self.draw_soma_projection()

        # Adjust the scale
        figure.set_aspect(aspect='equal')



        # Title
        figure.set(xlabel=projection)

        pdf_file_path = '%s/%s-%s.pdf' % \
                        (self.options.io.analysis_directory, self.morphology.label, projection)
        # Save the figure
        matplotlib.pyplot.savefig(pdf_file_path, bbox_inches='tight', transparent=True, dpi=300)

        return pdf_file_path

    ################################################################################################
    # @draw_morphology_skeleton
    ################################################################################################
    def draw_morphology_skeleton(self):
        """Reconstruct and draw the morphological skeleton.

        :return
            A list of all the drawn morphology objects including the soma and arbors.
        """

        nmv.logger.header('Building skeleton using ConnectedSectionsBuilder')

        nmv.logger.info('Updating Radii')
        nmv.skeleton.update_arbors_radii(
            morphology=self.morphology, morphology_options=self.options.morphology)

        nmv.logger.info('Updating Branching to Primary / Secondary')
        nmv.builders.skeleton.update_sections_branching(builder=self)

        # Update the style of the arbors
        nmv.skeleton.ops.update_arbors_style(
            morphology=self.morphology, arbor_style=self.options.morphology.arbor_style)

        # Create a static bevel object that you can use to scale the samples along the arbors
        # of the morphology and then hide it
        bevel_object = nmv.mesh.create_bezier_circle(
            radius=1.0, vertices=self.options.morphology.bevel_object_sides, name='bevel')
        nmv.scene.hide_object(bevel_object)

        # Add the bevel object to the morphology objects because if this bevel is lost we will
        # lose the rounded structure of the arbors
        self.morphology_objects.append(bevel_object)

        # Create the skeleton materials
        self.create_single_skeleton_materials_list()

        # Resample the sections of the morphology skeleton
        nmv.builders.skeleton.resample_skeleton_sections(builder=self)

        # Create each arbor as a separate component
        self.create_each_arbor_as_separate_component(bevel_object=bevel_object)

        # Create all the arbors as a single component
        # self.create_all_arbors_as_single_component(bevel_object=bevel_object)

        # Draw the soma
        nmv.builders.skeleton.draw_soma(builder=self)

        # Transforming to global coordinates
        nmv.builders.skeleton.transform_to_global_coordinates(builder=self)

        # Return the list of the drawn morphology objects
        nmv.logger.info('Done')
        return self.morphology_objects

####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
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
from .base import MorphologyBuilderBase
import nmv.analysis
import nmv.bbox
import nmv.mesh
import nmv.enums
import nmv.skeleton
import nmv.consts
import nmv.geometry
import nmv.scene
import nmv.bmeshi
import nmv.shading
import nmv.utilities
import nmv.rendering


####################################################################################################
# @DendrogramBuilder
####################################################################################################
class DendrogramBuilder(MorphologyBuilderBase):
    """Draws the morphology dendrogram."""

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

        nmv.logger.header('Building Dendrogram')

        # Initialize the builder
        self.initialize_builder()

        # Get the maximum radius to make it easy to compute the deltas
        maximum_radius = nmv.analysis.kernel_maximum_sample_radius(
            morphology=self.morphology).morphology_result

        # Compute the dendrogram of the morphology
        if self.options.morphology.dendrogram_type == nmv.enums.Dendrogram.Type.DETAILED:
            nmv.skeleton.compute_morphology_dendrogram(
                morphology=self.morphology, delta=maximum_radius * 8)
        else:
            nmv.skeleton.compute_morphology_dendrogram(
                morphology=self.morphology, delta=8)

        # A list of all the skeleton poly-lines
        skeleton_poly_lines = list()

        if not self.options.morphology.ignore_apical_dendrites:
            if self.morphology.has_apical_dendrites():
                for arbor in self.morphology.apical_dendrites:
                    nmv.skeleton.create_dendrogram_poly_lines_list_of_arbor(
                        section=arbor,
                        poly_lines_data=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.apical_dendrite_branch_order,
                        dendrogram_type=self.options.morphology.dendrogram_type)

        if not self.options.morphology.ignore_axons:
            if self.morphology.has_axons():
                for arbor in self.morphology.axons:
                    nmv.skeleton.create_dendrogram_poly_lines_list_of_arbor(
                        section=arbor,
                        poly_lines_data=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.axon_branch_order,
                        dendrogram_type=self.options.morphology.dendrogram_type)

        if not self.options.morphology.ignore_basal_dendrites:
            if self.morphology.has_basal_dendrites():
                for arbor in self.morphology.basal_dendrites:
                    nmv.skeleton.create_dendrogram_poly_lines_list_of_arbor(
                        section=arbor,
                        poly_lines_data=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.basal_dendrites_branch_order,
                        dendrogram_type=self.options.morphology.dendrogram_type)

        # The soma to stems line
        center = nmv.skeleton.add_soma_to_stems_line(
            morphology=self.morphology, poly_lines_data=skeleton_poly_lines,
            ignore_apical_dendrites=self.options.morphology.ignore_apical_dendrites,
            ignore_basal_dendrites=self.options.morphology.ignore_basal_dendrites,
            ignore_axons=self.options.morphology.ignore_axons)

        # Draw the poly-lines as a single object
        morphology_object = nmv.geometry.draw_poly_lines_in_single_object(
            poly_lines=skeleton_poly_lines, object_name=self.morphology.label,
            edges=self.options.morphology.edges, bevel_object=self.bevel_object,
            materials=self.skeleton_materials)

        # Adjust the center
        nmv.scene.set_object_location(morphology_object, center)

        # Add the created dendrogram to the skeleton
        self.morphology_objects.append(morphology_object)

        # Always switch to the top view to see the dendrogram quite well
        nmv.scene.view_axis(axis='TOP')

        # Add the morphology objects to a collection
        self.collection_morphology_objects_in_collection(name='Dendrogram')

        # Return the list of the drawn morphology objects
        return self.morphology_objects

    ################################################################################################
    # @draw_morphology_skeleton_with_matplotlib
    ################################################################################################
    def draw_morphology_skeleton_with_matplotlib(self):
        """Draws the morphology skeleton dendrogram with matplotlib. The resulting file should be
        included in the analysis fact sheet."""

        # Verify the presence of the plotting packages
        nmv.utilities.verify_plotting_packages()

        # Plotting imports
        import numpy
        import seaborn
        import matplotlib
        matplotlib.use('agg')
        import matplotlib.pyplot as pyplot

        # Create the color palette
        self.morphology.create_morphology_color_palette()

        # Resample the sections of the morphology skeleton
        self.resample_skeleton_sections()

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

        # Adjust seaborn configuration
        seaborn.set_style("white")

        # Adjusting the matplotlib parameters
        pyplot.rcParams['axes.grid'] = 'False'
        pyplot.rcParams['font.family'] = 'NimbusSanL'
        pyplot.rcParams['axes.edgecolor'] = '0.1'
        pyplot.axis('off')

        if not self.options.morphology.ignore_apical_dendrites:
            if self.morphology.has_apical_dendrites():
                for i, arbor in enumerate(self.morphology.apical_dendrites):

                    # A list of all the skeleton poly-lines
                    skeleton_poly_lines = list()

                    # Create the poly-lines
                    nmv.skeleton.create_dendrogram_poly_lines_list_of_arbor(
                        section=arbor,
                        poly_lines_data=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.apical_dendrite_branch_order,
                        stretch_legs=False)

                    for poly_line in skeleton_poly_lines:

                        x_list = list()
                        y_list = list()

                        for sample in poly_line.samples:
                            x_list.append(sample[0][0])
                            y_list.append(sample[0][1])

                        x = numpy.array(x_list)
                        y = numpy.array(y_list)
                        ax = pyplot.plot([x_list[0], x_list[1]], [y_list[0], y_list[1]], lw=1.0,
                                         color=self.morphology.apical_dendrites_colors[i])

        if not self.options.morphology.ignore_axons:
            if self.morphology.has_axons():
                for i, arbor in enumerate(self.morphology.axons):

                    # A list of all the skeleton poly-lines
                    skeleton_poly_lines = list()

                    # Create the polylines
                    nmv.skeleton.create_dendrogram_poly_lines_list_of_arbor(
                        section=arbor,
                        poly_lines_data=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.axon_branch_order,
                        stretch_legs=False)

                    # Plot
                    for poly_line in skeleton_poly_lines:
                        x_list = list()
                        y_list = list()

                        for sample in poly_line.samples:
                            x_list.append(sample[0][0])
                            y_list.append(sample[0][1])

                        x = numpy.array(x_list)
                        y = numpy.array(y_list)
                        ax = pyplot.plot([x_list[0], x_list[1]], [y_list[0], y_list[1]], lw=1.0,
                                         color=self.morphology.axons_colors[i])

        if not self.options.morphology.ignore_basal_dendrites:
            if self.morphology.has_basal_dendrites():
                for i, arbor in enumerate(self.morphology.basal_dendrites):

                    # A list of all the skeleton poly-lines
                    skeleton_poly_lines = list()

                    # Create the polylines
                    nmv.skeleton.create_dendrogram_poly_lines_list_of_arbor(
                        section=arbor,
                        poly_lines_data=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.basal_dendrites_branch_order,
                        stretch_legs=False)

                    # Plot
                    for poly_line in skeleton_poly_lines:
                        x_list = list()
                        y_list = list()

                        for sample in poly_line.samples:
                            x_list.append(sample[0][0])
                            y_list.append(sample[0][1])

                        x = numpy.array(x_list)
                        y = numpy.array(y_list)

                        ax = pyplot.plot([x_list[0], x_list[1]], [y_list[0], y_list[1]], lw=1.0,
                                         color=self.morphology.basal_dendrites_colors[i])

        # The soma to stems line
        skeleton_poly_lines = list()
        center = nmv.skeleton.add_soma_to_stems_line(
            morphology=self.morphology, poly_lines_data=skeleton_poly_lines,
            ignore_apical_dendrites=self.options.morphology.ignore_apical_dendrites,
            ignore_basal_dendrites=self.options.morphology.ignore_basal_dendrites,
            ignore_axons=self.options.morphology.ignore_axons)

        for poly_line in skeleton_poly_lines:
            x_list = list()
            y_list = list()

            for sample in poly_line.samples:
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

    ################################################################################################
    # @draw_highlighted_arbors
    ################################################################################################
    def draw_highlighted_arbors(self,
                                dendrogram_type=nmv.enums.Dendrogram.Type.SIMPLIFIED):
        """Reconstruct and draw the morphological skeleton.

        :return
            A list of all the drawn morphology objects including the soma and arbors.
        """

        nmv.logger.header('Building Dendrogram')

        # Get the maximum radius to make it easy to compute the deltas
        maximum_radius = nmv.analysis.kernel_maximum_sample_radius(
            morphology=self.morphology).morphology_result

        # Compute the dendrogram of the morphology
        if dendrogram_type == nmv.enums.Dendrogram.Type.SIMPLIFIED:
            nmv.skeleton.compute_morphology_dendrogram(
                morphology=self.morphology, delta=8.0)
        else:
            nmv.skeleton.compute_morphology_dendrogram(
                morphology=self.morphology, delta=maximum_radius * 8.0)

        # A list of all the skeleton poly-lines
        skeleton_poly_lines = list()

        material_index = 0
        if not self.options.morphology.ignore_apical_dendrites:
            if self.morphology.has_apical_dendrites():
                for arbor in self.morphology.apical_dendrites:
                    nmv.skeleton.create_dendrogram_poly_lines_list_of_arbor(
                        section=arbor,
                        poly_lines_data=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.apical_dendrite_branch_order,
                        arbor_material_index=material_index,
                        dendrogram_type=dendrogram_type)
                    material_index += 2

        if not self.options.morphology.ignore_basal_dendrites:
            if self.morphology.has_basal_dendrites():
                for arbor in self.morphology.basal_dendrites:
                    nmv.skeleton.create_dendrogram_poly_lines_list_of_arbor(
                        section=arbor,
                        poly_lines_data=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.basal_dendrites_branch_order,
                        arbor_material_index=material_index,
                        dendrogram_type=dendrogram_type)
                    material_index += 2

        if not self.options.morphology.ignore_axons:
            if self.morphology.has_axons():
                for arbor in self.morphology.axons:
                    nmv.skeleton.create_dendrogram_poly_lines_list_of_arbor(
                        section=arbor,
                        poly_lines_data=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.axon_branch_order,
                        arbor_material_index=material_index,
                        dendrogram_type=dendrogram_type)
                    material_index += 2

        # The soma to stems line
        center = nmv.skeleton.add_soma_to_stems_line(
            morphology=self.morphology, poly_lines_data=skeleton_poly_lines,
            ignore_apical_dendrites=self.options.morphology.ignore_apical_dendrites,
            ignore_basal_dendrites=self.options.morphology.ignore_basal_dendrites,
            ignore_axons=self.options.morphology.ignore_axons, soma_material_index=material_index,
            dendrogram_type=dendrogram_type)

        bevel_object = nmv.mesh.create_bezier_circle(
            radius=1.0, resolution=self.options.morphology.bevel_object_sides, name='Cross Section')

        # Draw the poly-lines as a single object
        morphology_object = nmv.geometry.draw_poly_lines_in_single_object(
            poly_lines=skeleton_poly_lines, object_name=self.morphology.label,
            edges=self.options.morphology.edges, bevel_object=bevel_object,
            materials=self.skeleton_materials)

        nmv.scene.set_object_location(morphology_object, center)

        # Return the list of the drawn morphology objects
        return self.morphology_objects

    ################################################################################################
    # @create_per_arbor_material_list
    ################################################################################################
    def create_per_arbor_material_list(self):

        nmv.logger.info('Creating materials')

        # Clear already existing materials list
        self.clear_materials()

        # Apical materials
        if self.morphology.has_apical_dendrites():
            for arbor in self.morphology.apical_dendrites:
                arbor_materials = nmv.skeleton.ops.create_skeleton_materials(
                    name=arbor.tag,
                    material_type=self.options.shading.morphology_material,
                    color=arbor.color)
                self.skeleton_materials.extend(arbor_materials)

        # Basal materials
        if self.morphology.has_basal_dendrites():
            for arbor in self.morphology.basal_dendrites:
                arbor_materials = nmv.skeleton.ops.create_skeleton_materials(
                    name=arbor.tag,
                    material_type=self.options.shading.morphology_material,
                    color=arbor.color)
                self.skeleton_materials.extend(arbor_materials)

        # Axons materials
        if self.morphology.has_axons():
            for arbor in self.morphology.axons:
                arbor_materials = nmv.skeleton.ops.create_skeleton_materials(
                    name=arbor.tag,
                    material_type=self.options.shading.morphology_material,
                    color=arbor.color)
                self.skeleton_materials.extend(arbor_materials)

        # Soma materials
        soma_materials = nmv.skeleton.ops.create_skeleton_materials(
            name='Soma Material',
            material_type=self.options.shading.morphology_material,
            color=self.morphology.soma_color)
        self.skeleton_materials.extend(soma_materials)

    ################################################################################################
    # @render_highlighted_arbors
    ################################################################################################
    def render_highlighted_arbors(self,
                                  dendrogram_type=nmv.enums.Dendrogram.Type.SIMPLIFIED,
                                  resolution=2048):
        """Render the morphology with different colors per arbor for analysis."""

        # NOTE: Readjust the parameters here to plot everything for the whole morphology
        self.options.morphology.adjust_to_analysis_mode()

        # Use flat shading to get the same one we get with matplotlib
        self.options.shading.morphology_material = nmv.enums.Shader.FLAT

        # Create the materials
        self.create_per_arbor_material_list()

        # Draw the dendrogram, all arbors with same radius
        self.draw_highlighted_arbors(dendrogram_type=dendrogram_type)

        # Compute the bounding box of the dendrogram and stretch it
        bounding_box = nmv.bbox.compute_scene_bounding_box_for_curves()
        delta = bounding_box.get_largest_dimension() * 0.025
        bounding_box.extend_bbox(delta_x=1.5 * delta, delta_y=delta)

        if dendrogram_type == nmv.enums.Dendrogram.Type.SIMPLIFIED:
            file_name = 'dendrogram_simplified'
        else:
            file_name = 'dendrogram_detailed'
        nmv.rendering.render(
            bounding_box=bounding_box,
            camera_view=nmv.enums.Camera.View.FRONT,
            image_resolution=resolution,
            image_name=file_name,
            image_directory='%s/%s' % (self.options.io.analysis_directory,
                                       self.options.morphology.label))



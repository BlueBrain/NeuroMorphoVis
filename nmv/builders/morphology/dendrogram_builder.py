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

# System imports
import copy

# Internal imports
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
        self.axons_materials = None

        # A list of the colors/materials of the basal dendrites
        self.basal_dendrites_materials = None

        # A list of the colors/materials of the apical dendrite
        self.apical_dendrites_materials = None

        # A list of the colors/materials of the articulation spheres
        self.articulations_materials = None

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
        nmv.builders.morphology.create_skeleton_materials_and_illumination(builder=self)

        # Index: 0 - 1
        self.skeleton_materials.extend(self.soma_materials)

        # Index: 2 - 3
        self.skeleton_materials.extend(self.apical_dendrites_materials)

        # Index: 4 - 5
        self.skeleton_materials.extend(self.basal_dendrites_materials)

        # Index: 6 - 7
        self.skeleton_materials.extend(self.axons_materials)

    ################################################################################################
    # @create_per_arbor_material_list
    ################################################################################################
    def create_per_arbor_material_list(self):

        nmv.logger.info('Creating materials')

        # Clear all the materials that are already present in the scene
        for material in bpy.data.materials:
            if 'soma_skeleton' in material.name or \
                    'axon_skeleton' in material.name or \
                    'basal_dendrites_skeleton' in material.name or \
                    'apical_dendrite_skeleton' in material.name or \
                    'articulation' in material.name or \
                    'gray' in material.name:
                material.user_clear()
                bpy.data.materials.remove(material)

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
            name='soma_material',
            material_type=self.options.shading.morphology_material,
            color=self.morphology.soma_color)
        self.skeleton_materials.extend(soma_materials)

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
        nmv.builders.morphology.resample_skeleton_sections(builder=self)

        # Get the maximum radius to make it easy to compute the deltas
        maximum_radius = nmv.analysis.kernel_maximum_sample_radius(
            morphology=self.morphology).morphology_result

        # Compute the dendrogram of the morphology
        nmv.skeleton.compute_morphology_dendrogram(
            morphology=self.morphology, delta=maximum_radius * 8)

        # A list of all the skeleton poly-lines
        skeleton_poly_lines = list()

        if not self.options.morphology.ignore_apical_dendrites:
            if self.morphology.has_apical_dendrites():
                for arbor in self.morphology.apical_dendrites:
                    nmv.skeleton.create_dendrogram_poly_lines_list_of_arbor(
                        section=arbor,
                        poly_lines_data=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.apical_dendrite_branch_order)

        if not self.options.morphology.ignore_axons:
            if self.morphology.has_axons():
                for arbor in self.morphology.axons:
                    nmv.skeleton.create_dendrogram_poly_lines_list_of_arbor(
                        section=arbor,
                        poly_lines_data=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.axon_branch_order)

        if not self.options.morphology.ignore_basal_dendrites:
            if self.morphology.has_basal_dendrites():
                for arbor in self.morphology.basal_dendrites:
                    nmv.skeleton.create_dendrogram_poly_lines_list_of_arbor(
                        section=arbor,
                        poly_lines_data=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.basal_dendrites_branch_order)

        # The soma to stems line
        center = nmv.skeleton.add_soma_to_stems_line(
            morphology=self.morphology, poly_lines_data=skeleton_poly_lines,
            ignore_apical_dendrites=self.options.morphology.ignore_apical_dendrites,
            ignore_basal_dendrites=self.options.morphology.ignore_basal_dendrites,
            ignore_axons=self.options.morphology.ignore_axons)

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
        for font_file in font_files:
            font_manager.fontManager.addfont(font_file)

        # Create the color palette
        self.morphology.create_morphology_color_palette()

        # Resample the sections of the morphology skeleton
        nmv.builders.morphology.resample_skeleton_sections(builder=self)

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

                    # Create the polylines
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
    # @draw_morphology_skeleton
    ################################################################################################
    def draw_highlighted_arbors(self):
        """Reconstruct and draw the morphological skeleton.

        :return
            A list of all the drawn morphology objects including the soma and arbors.
        """

        nmv.logger.header('Building skeleton using DendrogamBuilder')

        nmv.skeleton.update_arbors_radii(self.morphology, self.options.morphology)

        # Create the skeleton materials
        # self.create_single_skeleton_materials_list()
        self.create_per_arbor_material_list()

        # Resample the sections of the morphology skeleton
        nmv.builders.morphology.resample_skeleton_sections(builder=self)

        # Get the maximum radius to make it easy to compute the deltas
        maximum_radius = nmv.analysis.kernel_maximum_sample_radius(
            morphology=self.morphology).morphology_result

        # Compute the dendrogram of the morphology
        nmv.skeleton.compute_morphology_dendrogram(
            morphology=self.morphology, delta=maximum_radius * 8)

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
                        arbor_material_index=material_index)
                    material_index += 2

        if not self.options.morphology.ignore_basal_dendrites:
            if self.morphology.has_basal_dendrites():
                for arbor in self.morphology.basal_dendrites:
                    nmv.skeleton.create_dendrogram_poly_lines_list_of_arbor(
                        section=arbor,
                        poly_lines_data=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.basal_dendrites_branch_order,
                        arbor_material_index=material_index)
                    material_index += 2

        if not self.options.morphology.ignore_axons:
            if self.morphology.has_axons():
                for arbor in self.morphology.axons:
                    nmv.skeleton.create_dendrogram_poly_lines_list_of_arbor(
                        section=arbor,
                        poly_lines_data=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.axon_branch_order,
                        arbor_material_index=material_index)
                    material_index += 2

        # The soma to stems line
        center = nmv.skeleton.add_soma_to_stems_line(
            morphology=self.morphology, poly_lines_data=skeleton_poly_lines,
            ignore_apical_dendrites=self.options.morphology.ignore_apical_dendrites,
            ignore_basal_dendrites=self.options.morphology.ignore_basal_dendrites,
            ignore_axons=self.options.morphology.ignore_axons, soma_material_index=material_index)

        bevel_object = nmv.mesh.create_bezier_circle(
            radius=1.0, vertices=self.options.morphology.bevel_object_sides, name='bevel')
        nmv.scene.hide_object(bevel_object)

        # Draw the poly-lines as a single object
        morphology_object = nmv.geometry.draw_poly_lines_in_single_object(
            poly_lines=skeleton_poly_lines, object_name=self.morphology.label,
            edges=self.options.morphology.edges, bevel_object=bevel_object,
            materials=self.skeleton_materials)

        nmv.scene.set_object_location(morphology_object, center)

        # Return the list of the drawn morphology objects
        return self.morphology_objects

    ################################################################################################
    # @render_highlighted_arbors
    ################################################################################################
    def render_highlighted_arbors(self):
        """Render the morphology with different colors per arbor for analysis.
        """

        # NOTE: Readjust the parameters here to plot everything for the whole morphology
        self.options.morphology.adjust_to_analysis_mode()

        # Draw the whole morphology with individual colors, but to-scale
        self.options.shading.morphology_material = nmv.enums.Shader.FLAT
        self.draw_highlighted_arbors()

        # Compute the bounding box of the dendrogram and stretch it
        bounding_box = nmv.bbox.compute_scene_bounding_box_for_curves()
        bounding_box.extend_bbox(delta=20)

        nmv.rendering.render(
            bounding_box=bounding_box,
            camera_view=nmv.enums.Camera.View.FRONT,
            image_resolution=2048,
            image_name='%s_%s' % (self.morphology.label, 'dendrogram'),
            image_directory='%s/%s' % (self.options.io.analysis_directory,
                                       self.options.morphology.label))
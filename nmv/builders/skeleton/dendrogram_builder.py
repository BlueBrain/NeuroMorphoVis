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
from mathutils import Vector

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


####################################################################################################
# @DendrogramBuilder
####################################################################################################
class DendrogramBuilder:
    """Builds and draws the morphology as a series of samples where each sample is represented by
    a sphere.

    NOTE: We use bmeshes to generate the spheres and then link them to the scene all at once.
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
            morphology=self.morphology, delta=maximum_radius * 2)

        # A list of all the skeleton poly-lines
        skeleton_poly_lines = list()

        if self.morphology.apical_dendrite is not None:
            nmv.skeleton.create_dendrogram_poly_lines_list_of_arbor(
                self.morphology.apical_dendrite, skeleton_poly_lines)

        if self.morphology.dendrites is not None:
            for basal_dendrite in self.morphology.dendrites:
                nmv.skeleton.create_dendrogram_poly_lines_list_of_arbor(
                    basal_dendrite, skeleton_poly_lines)

        if self.morphology.axon is not None:
            nmv.skeleton.create_dendrogram_poly_lines_list_of_arbor(
                self.morphology.axon, skeleton_poly_lines)

        # The soma to stems line
        center = nmv.skeleton.add_soma_to_stems_line(
            morphology=self.morphology, poly_lines_data=skeleton_poly_lines)

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


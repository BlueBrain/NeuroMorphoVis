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
    # @construct_tree_poly_lines
    ################################################################################################
    def construct_tree_poly_lines(self,
                                  root,
                                  poly_lines_list=[],
                                  branching_level=0,
                                  max_branching_level=nmv.consts.Math.INFINITY,
                                  prefix=nmv.consts.Arbors.BASAL_DENDRITES_PREFIX,
                                  material_start_index=0):
        """Creates a list of poly-lines corresponding to all the sections in the given tree.

        :param root:
            Arbor root, or children sections.
        :param poly_lines_list:
            A list that will combine all the constructed poly-lines.
        :param branching_level:
            Current branching level of the arbor.
        :param max_branching_level:
            The maximum branching level given by the user.
        :param prefix:
            The prefix that is prepended to the name of the poly-line.
        :param material_start_index:
            An index that indicates which material to be used for which arbor.
        """

        # If the section is None, simply return
        if root is None:
            return
        poly_data = list()

        nmv.skeleton.get_arbor_poly_lines_as_connected_sections(
            root=root, poly_lines_data=poly_lines_list,
            poly_line_data=poly_data, max_branching_level=max_branching_level)

    ################################################################################################
    # @draw_morphology_skeleton
    ################################################################################################
    def draw_morphology_skeleton(self):
        """Reconstruct and draw the morphological skeleton.

        :return
            A list of all the drawn morphology objects including the soma and arbors.
        """

        nmv.logger.header('Building skeleton using ConnectedSectionsBuilder')

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

        # A list of all the skeleton poly-lines
        skeleton_poly_lines = list()

        # Apical dendrite
        nmv.logger.info('Constructing poly-lines')
        if not self.options.morphology.ignore_apical_dendrite:
            if self.morphology.apical_dendrite is not None:
                nmv.logger.detail('Apical dendrite')
                self.construct_tree_poly_lines(
                    root=self.morphology.apical_dendrite,
                    poly_lines_list=skeleton_poly_lines,
                    max_branching_level=self.options.morphology.apical_dendrite_branch_order,
                    prefix=nmv.consts.Arbors.APICAL_DENDRITES_PREFIX,
                    material_start_index=nmv.enums.Color.APICAL_DENDRITE_MATERIAL_START_INDEX)

        # Axon
        if not self.options.morphology.ignore_axon:
            if self.morphology.axon is not None:
                nmv.logger.detail('Axon')
                self.construct_tree_poly_lines(
                    root=self.morphology.axon,
                    poly_lines_list=skeleton_poly_lines,
                    max_branching_level=self.options.morphology.axon_branch_order,
                    prefix=nmv.consts.Arbors.BASAL_DENDRITES_PREFIX,
                    material_start_index=nmv.enums.Color.AXON_MATERIAL_START_INDEX)

        # Basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:
            if self.morphology.dendrites is not None:
                for i, basal_dendrite in enumerate(self.morphology.dendrites):
                    nmv.logger.detail('Basal dendrite [%d]' % i)
                    self.construct_tree_poly_lines(
                        root=basal_dendrite,
                        poly_lines_list=skeleton_poly_lines,
                        max_branching_level=self.options.morphology.basal_dendrites_branch_order,
                        prefix=nmv.consts.Arbors.AXON_PREFIX,
                        material_start_index=nmv.enums.Color.BASAL_DENDRITES_MATERIAL_START_INDEX)

        # Draw the poly-lines as a single object
        morphology_object = nmv.geometry.draw_poly_lines_in_single_object(
            poly_lines=skeleton_poly_lines, object_name=self.morphology.label,
            poly_line_type='POLY', bevel_object=bevel_object, materials=self.skeleton_materials)

        # Append it to the morphology objects
        self.morphology_objects.append(morphology_object)

        # Draw the soma
        nmv.builders.skeleton.draw_soma(builder=self)

        # Transforming to global coordinates
        nmv.builders.skeleton.transform_to_global_coordinates(builder=self)

        # Return the list of the drawn morphology objects
        nmv.logger.info('Done')
        return self.morphology_objects


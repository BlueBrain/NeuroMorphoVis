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

    def get_leaves(self, section, leaves):

        if section.is_leaf():
            leaves.append(section)
        for child in section.children:
            self.get_leaves(child, leaves)

    def count_sub_tree_leaves(self,
                              root):
        leafs = list()
        self.get_leaves(root, leafs)
        print(len(leafs))
        return len(leafs)

    def count_right_leaves(self,
                           root):
        if root.has_children():
            return self.count_sub_tree_leaves(root.children[0])
        else:
            return 0

    def count_left_leaves(self,
                          root):
        if root.has_children():
            return self.count_sub_tree_leaves(root.children[1])
        else:
            return 0

    def draw_sub_tree(self,
                      root,
                      x, y):

        right = self.count_right_leaves(root)
        left = self.count_left_leaves(root)
        total = left + right

        # length
        length = 2 #root.compute_length()

        starting_point = Vector((x, y, 0))

        if self.count_sub_tree_leaves(root) == 1:
            ending_point = Vector((x, length, 0))
        else:
            ending_point = Vector((x, y + length, 0))

        # draw current
        nmv.geometry.draw_line(point1=starting_point, point2=ending_point, thickness=0.1)

        # draw the subtree
        for i, child in enumerate(root.children):
            if i == 0:
                starting_x = x + (right / 2.0)
            else:
                starting_x = x - (left / 2.0)

            self.draw_sub_tree(child, x=starting_x, y=y + length)




    # ratio between the left and the right gets the x distance
    def draw_arbor_dendrogram(self,
                              arbor):

        right = self.count_right_leaves(arbor)
        left = self.count_left_leaves(arbor)
        total = right + left

        print('balance')
        print(right, ' ', left)

        tree_width = total
        x = tree_width / 2.0
        y = 0

        # draw the root as a line starting from 0, 0 and up
        length = 2 # arbor.compute_length()

        # draw the line
        starting_point = Vector((x, y, 0))

        if self.count_sub_tree_leaves(arbor) == 1:
            ending_point = Vector((x, length, 0))
        else:
            ending_point = Vector((x, y + length, 0))

        # draw current
        nmv.geometry.draw_line(point1=starting_point, point2=ending_point, thickness=0.1)




        # children
        for i, child in enumerate(arbor.children):

            if i == 0:
                starting_x = x + (total / 2.0)
            else:
                starting_x = x - (total / 2.0)


            #print(self.count_sub_tree_leaves(child))
            #print('starting: ', starting_x)
            self.draw_sub_tree(child, x=starting_x, y=y + length)











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


        self.draw_arbor_dendrogram(self.morphology.apical_dendrite)

        # Return the list of the drawn morphology objects
        nmv.logger.info('Done')
        return self.morphology_objects


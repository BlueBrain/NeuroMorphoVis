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
import nmv.mesh
import nmv.enums
import nmv.skeleton


####################################################################################################
# @DisconnectedSectionsBuilder
####################################################################################################
class DisconnectedSectionsBuilder:
    """Builds and draws the morphology as a series of disconnected sections.
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
        self.options = options

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

    def get_section_poly_line(self, section, material_index):

        section_poly_line_data = nmv.skeleton.get_section_poly_line(section=section)



        pass



    def draw_arbor(self,
                   arbor,
                   prefix,
                   materials,
                   bevel_object,
                   max_branching_level,
                   single_object):
        """

        :param arbor:
        :param prefix:
        :param materials:
        :param bevel_object:
        :param max_branching_level:
        :param single_object:
        :return:
        """


        pass

    ################################################################################################
    # @draw_morphology_skeleton
    ################################################################################################
    def draw_morphology_skeleton(self):
        """Reconstruct and draw the morphological skeleton.

        :return
            A list of all the drawn morphology objects including the soma and arbors.
        """

        # Create a static bevel object that you can use to scale the samples along the arbors
        # of the morphology
        bevel_object = nmv.mesh.create_bezier_circle(
            radius=1.0, vertices=self.options.morphology.bevel_object_sides, name='bevel')

        # Add the bevel object to the morphology objects because if this bevel is lost we will
        # lose the rounded structure of the arbors
        self.morphology_objects.append(bevel_object)

        # NOTE: Before drawing the skeleton, create the materials, once and for all, to improve the
        # performance since this is way better than creating a new material per section or segment
        # or any individual object
        nmv.builders.skeleton.create_skeleton_materials_and_illumination(builder=self)

        # Resample the sections of the morphology skeleton
        nmv.builders.skeleton.resample_skeleton_sections(builder=self)






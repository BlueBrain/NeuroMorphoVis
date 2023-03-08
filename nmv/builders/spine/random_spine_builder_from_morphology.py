####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of NeuroMorphoVis <https://github.com/BlueBrain/NeuroMorphoVis>
#
# This library is free software; you can redistribute it and/or modify it under the terms of the
# GNU Lesser General Public License version 3.0 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with this library;
# if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA.
####################################################################################################

# System imports
import random
import copy

# Blender imports
import bpy
from mathutils import Vector

import nmv.consts
import nmv.shading
import nmv.skeleton
import nmv.scene
import nmv.utilities
import nmv.geometry
import nmv.mesh


####################################################################################################
# @RandomSpineBuilder
####################################################################################################
class RandomSpineBuilderFromMorphology:
    """This builder creates the skeletons of the spines that will be used in the MetaBuilder to
    integrate spines into neuron meshes.

    NOTE: The spines being built here are random and do not correspond to neither a real or
    simulated circuit.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 morphology,
                 options):
        """Constructor

        :param morphology:
            A given morphology skeleton to create the mesh for.
        :param options:
            Loaded options from NeuroMorphoVis.
        """

        # Neuron morphology
        self.neuron_morphology = morphology

        # Loaded options from NeuroMorphoVis
        self.options = options

        # A list of all the templates that we can use to build the morphology
        self.spine_template_structures = list()

        # Construct a bevel object that will be used to build the spines
        self.bevel_object = nmv.mesh.create_bezier_circle(radius=1.0,
                                                          vertices=8,
                                                          name='spines_bevel')

        # Build the spine template structures
        self.build_spines_template_structures()

    ################################################################################################
    # @build_spine_structure
    ################################################################################################
    def build_spine_structure(self, spine_morphology):

        # A list of poly-lines
        spine_poly_lines = list()

        # Construct the polyline format
        for section in spine_morphology.sections:
            spine_poly_lines.append(nmv.geometry.PolyLine(
                samples=nmv.skeleton.ops.get_section_poly_line(section=section)))

        # Draw the poly-lines
        spine_structure = nmv.geometry.ops.draw_poly_lines_in_single_object(
            poly_lines=spine_poly_lines, bevel_object=self.bevel_object, poly_line_caps=False)

        # Return a reference to the spine template
        return spine_structure

    ################################################################################################
    # @build_spines_template_structures
    ################################################################################################
    def build_spines_template_structures(self):

        # Load the template spines
        template_spines_morphologies = nmv.file.load_spine_morphologies_from_data_files(
            nmv.consts.Paths.SPINES_MORPHOLOGIES_DIRECTORY)

        # Build structures from the template morphologies
        for template_morphology in template_spines_morphologies:
            self.spine_template_structures.append(self.build_spine_structure(
                spine_morphology=template_morphology))

    ################################################################################################
    # @get_spine_morphologies_for_arbor
    ################################################################################################
    def get_spine_morphologies_for_arbor(self,
                                         arbor,
                                         number_spines_per_micron,
                                         max_branching_order):

        spine_morphologies = list()

        # Get the normals along the segments along the arbors
        nmv.skeleton.ops.apply_operation_to_arbor(
            *[arbor,
              nmv.skeleton.ops.get_random_spines_across_section,
              self.spine_template_structures,
              number_spines_per_micron,
              max_branching_order,
              spine_morphologies,
              True])

        # Return a list of spine morphologies (samples and radii) that can be used to draw
        # the spine in the scene at the respective locations
        return spine_morphologies

    ################################################################################################
    # @clean_unwanted_data
    ################################################################################################
    def clean_unwanted_data(self):

        nmv.scene.delete_list_objects(self.spine_template_structures)
        nmv.scene.delete_object_in_scene(self.bevel_object)

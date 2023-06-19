####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
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
import copy

# Blender imports
import bpy

# Internal imports
import nmv.utilities
import nmv.enums
import nmv.consts
import nmv.skeleton
import nmv.mesh
import nmv.shading
import nmv.scene


####################################################################################################
# @MorphologyBuilderBase
####################################################################################################
class MorphologyBuilderBase:
    """Base class for all the morphology builders."""

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 morphology,
                 options):
        """Constructor

        :param morphology:
            A given morphology.
        :param options:
            NeuroMorphoVis options
        """

        # Morphology, and we deepcopy the instance such in case we modify it
        self.morphology = copy.deepcopy(morphology)

        # System options, and we deepcopy them in case a reference is changed by accident
        self.options = copy.deepcopy(options)

        # A reference to the created soma object
        self.soma_mesh = None

        # All the reconstructed objects of the morphology, for example, poly-lines, spheres etc...
        self.morphology_objects = list()

        # A list of the colors/materials of the soma
        self.soma_materials = list()

        # A list of the colors/materials of the axon
        self.axons_materials = list()

        # A list of the colors/materials of the basal dendrites
        self.basal_dendrites_materials = list()

        # A list of the colors/materials of the apical dendrite
        self.apical_dendrites_materials = list()

        # A list of the colors/materials of the articulation spheres
        self.articulations_materials = list()

        # A list of the color/materials of the endfeet patches
        self.endfeet_materials = list()

        # An aggregate list of all the materials of the skeleton
        self.skeleton_materials = list()

        # A gray material to highlight the other arbors in colors
        self.gray_material = None

        # All lights created in the scene
        self.lights = None

        # UI Context
        self.context = None

        # The bevel object used to interpolate the lines
        self.bevel_object = None

    ################################################################################################
    # @initialize_builder
    ################################################################################################
    def initialize_builder(self):
        """Initializes the builder, default for all builders unless specified otherwise."""

        # Creates the bevel object that is used to interpolate the morphology across its centerline
        self.create_bevel_object()

        # Pre-process and update the radii, based on the selected input from the user
        self.update_sections_radii()

        # Pre-process and update the branching, based on the selected input from the user
        self.update_skeleton_branching()

        # Pre-process and update the style of the arbors, based on the selected input from the user
        self.update_skeleton_style()

        # Resample the sections, based on the selected input from the user
        self.resample_skeleton_sections()

        # Create the materials that will be applied to the morphology.
        self.create_morphology_skeleton_materials()

        # Add the illumination
        self.create_illumination()

    ################################################################################################
    # @update_sections_radii
    ################################################################################################
    def update_sections_radii(self):
        """Updates the radii of each section in the morphology."""

        nmv.skeleton.update_arbors_radii(
            morphology=self.morphology, morphology_options=self.options.morphology)

    ################################################################################################
    # @update_skeleton_branching
    ################################################################################################
    def update_skeleton_branching(self):
        """Updates the branching of the morphology, either based on angle or radius."""

        nmv.skeleton.update_skeleton_branching(
            morphology=self.morphology, branching_method=self.options.morphology.branching)

    ################################################################################################
    # @update_skeleton_style
    ################################################################################################
    def update_skeleton_style(self):
        """Updates the style of the skeleton, mainly for artistic designs."""

        nmv.skeleton.ops.update_arbors_style(
            morphology=self.morphology, arbor_style=self.options.morphology.arbor_style)

    ################################################################################################
    # @create_bevel_object
    ################################################################################################
    def create_bevel_object(self):
        """Creates a bevel object that is used to interpolate the polylines."""

        # Create the bevel object
        self.bevel_object = nmv.mesh.create_bezier_circle(
            radius=1.0, resolution=self.options.morphology.bevel_object_sides,
            location=self.morphology.soma.centroid, name='Cross Section')

        # Add it to the base collection
        nmv.utilities.create_collection_with_objects(
            name='Auxiliary %s' % self.morphology.label, objects_list=[self.bevel_object])

    ################################################################################################
    # @clear_materials
    ################################################################################################
    def clear_materials(self):
        """Clears existing morphology materials."""

        for material in bpy.data.materials:
            if self.morphology.code in material.name:
                nmv.scene.delete_material(material=material)

        # Clear the lists (the materials references)
        self.soma_materials.clear()
        self.axons_materials.clear()
        self.basal_dendrites_materials.clear()
        self.apical_dendrites_materials.clear()
        self.articulations_materials.clear()
        self.endfeet_materials.clear()
        self.skeleton_materials.clear()

    ################################################################################################
    # @create_soma_materials
    ################################################################################################
    def create_soma_materials(self):
        """Creates the soma materials and updates the corresponding list.

        :return:
            A list containing the created materials.
        """

        soma_materials = nmv.skeleton.create_multiple_materials_with_same_color(
            name='Soma Morphology [%s]' % self.morphology.code,
            color=self.options.shading.morphology_soma_color,
            material_type=self.options.shading.morphology_material, number_elements=2)
        self.soma_materials.extend(soma_materials)
        return soma_materials

    ################################################################################################
    # @create_axons_materials
    ################################################################################################
    def create_axons_materials(self):
        """Creates the axons materials and updates the corresponding list.

        :return:
           A list containing the created materials.
        """

        axons_materials = nmv.skeleton.create_multiple_materials_with_same_color(
            name='Axons Morphology [%s]' % self.morphology.code,
            color=self.options.shading.morphology_axons_color,
            material_type=self.options.shading.morphology_material, number_elements=2)
        self.axons_materials.extend(axons_materials)
        return axons_materials

    ################################################################################################
    # @create_basal_dendrites_materials
    ################################################################################################
    def create_basal_dendrites_materials(self):
        """Creates the basal dendrites materials and updates the corresponding list.

        :return:
           A list containing the created materials.
        """
        basal_dendrites_materials = nmv.skeleton.create_multiple_materials_with_same_color(
            name='Basal Dendrites Morphology [%s]' % self.morphology.code,
            color=self.options.shading.morphology_basal_dendrites_color,
            material_type=self.options.shading.morphology_material, number_elements=2)
        self.basal_dendrites_materials.extend(basal_dendrites_materials)
        return basal_dendrites_materials

    ################################################################################################
    # @create_apical_dendrites_materials
    ################################################################################################
    def create_apical_dendrites_materials(self):
        """Creates the apical dendrites materials and updates the corresponding list.

        :return:
           A list containing the created materials.
        """
        apical_dendrites_materials = nmv.skeleton.create_multiple_materials_with_same_color(
            name='Apical Dendrites Morphology [%s]' % self.morphology.code,
            color=self.options.shading.morphology_apical_dendrites_color,
            material_type=self.options.shading.morphology_material, number_elements=2)
        self.apical_dendrites_materials.extend(apical_dendrites_materials)
        return apical_dendrites_materials

    ################################################################################################
    # @create_gray_materials
    ################################################################################################
    def create_gray_materials(self):
        """Creates the gray materials and updates the corresponding list.

        :return:
           A list containing the created materials.
        """

        gray_materials = nmv.skeleton.create_multiple_materials_with_same_color(
            name='Gray Morphology [%s]' % self.morphology.code,
            color=nmv.consts.Color.GREYSH,
            material_type=self.options.shading.morphology_material, number_elements=2)
        return gray_materials

    ################################################################################################
    # @create_articulation_materials
    ################################################################################################
    def create_articulation_materials(self):
        """Creates the articulations materials and updates the corresponding list.

        :return:
           A list containing the created materials.
        """
        articulations_materials = nmv.skeleton.create_multiple_materials_with_same_color(
            name='Articulations Morphology [%s]' % self.morphology.code,
            color=self.options.shading.morphology_articulation_color,
            material_type=self.options.shading.morphology_material, number_elements=2)
        self.articulations_materials.extend(articulations_materials)
        return articulations_materials

    ################################################################################################
    # @create_endfeet_materials
    ################################################################################################
    def create_endfeet_materials(self):
        """Creates the endfeet materials and updates the corresponding list.

        :return:
           A list containing the created materials.
        """

        endfeet_materials = nmv.skeleton.create_multiple_materials_with_same_color(
            name='Endfeet Morphology [%s]' % self.morphology.code,
            color=self.options.shading.morphology_endfeet_color,
            material_type=self.options.shading.morphology_material, number_elements=2)
        self.endfeet_materials.extend(endfeet_materials)
        return endfeet_materials

    ################################################################################################
    # @create_default_coloring_scheme_materials
    ################################################################################################
    def create_default_coloring_scheme_materials(self):
        """Creates the materials for the default coloring scheme."""

        # Soma, Indices 0 and 1 in @self.skeleton_materials
        self.skeleton_materials.extend(self.create_soma_materials())

        # Apical dendrites, Indices 2 and 3 in @self.skeleton_materials
        self.skeleton_materials.extend(self.create_apical_dendrites_materials())

        # Basals dendrites, Indices 4 and 5 in @self.skeleton_materials
        self.skeleton_materials.extend(self.create_basal_dendrites_materials())

        # Axons, Indices 6 and 7 in @self.skeleton_materials
        self.skeleton_materials.extend(self.create_axons_materials())

        # Gray material, Indices 8 and 9 in @self.skeleton_materials
        self.skeleton_materials.extend(self.create_gray_materials())

        # Articulations, Indices 10 and 11 in @self.skeleton_materials
        self.skeleton_materials.extend(self.create_articulation_materials())

        # Endfeet, if applicable, Indices 12 and 13 in @self.skeleton_materials
        self.skeleton_materials.extend(self.create_endfeet_materials())

    ################################################################################################
    # @create_alternating_materials
    ################################################################################################
    def create_alternating_materials(self):
        """Creates alternating materials for arbors, and a single material for other components."""

        # Soma material, Indices 0 and 1 in @self.skeleton_materials
        self.skeleton_materials.extend(self.create_soma_materials())

        # Apical dendrite
        self.apical_dendrites_materials.append(nmv.shading.create_material(
            name='Apicals 1 [%s]' % self.morphology.code,
            material_type=self.options.shading.morphology_material,
            color=self.options.shading.morphology_alternating_color_1))
        self.apical_dendrites_materials.append(nmv.shading.create_material(
            name='Apicals 2 [%s]' % self.morphology.code,
            material_type=self.options.shading.morphology_material,
            color=self.options.shading.morphology_alternating_color_2))
        self.skeleton_materials.extend(self.apical_dendrites_materials)

        # Basal dendrites
        self.basal_dendrites_materials.append(nmv.shading.create_material(
            name='Basals 1 [%s]' % self.morphology.code,
            material_type=self.options.shading.morphology_material,
            color=self.options.shading.morphology_alternating_color_1))
        self.basal_dendrites_materials.append(nmv.shading.create_material(
            name='Basals 2 [%s]' % self.morphology.code,
            material_type=self.options.shading.morphology_material,
            color=self.options.shading.morphology_alternating_color_2))
        self.skeleton_materials.extend(self.basal_dendrites_materials)

        # Axon
        self.axons_materials.append(nmv.shading.create_material(
            name='Axons 1 [%s]' % self.morphology.code,
            material_type=self.options.shading.morphology_material,
            color=self.options.shading.morphology_alternating_color_1))
        self.axons_materials.append(nmv.shading.create_material(
            name='Axons 2 [%s]' % self.morphology.code,
            material_type=self.options.shading.morphology_material,
            color=self.options.shading.morphology_alternating_color_2))
        self.skeleton_materials.extend(self.axons_materials)

        # Gray material
        self.skeleton_materials.extend(self.create_gray_materials())

        # Articulations
        self.skeleton_materials.extend(self.create_articulation_materials())

        # Endfeet, if applicable
        self.skeleton_materials.extend(self.create_endfeet_materials())

    ################################################################################################
    # @create_colormap_materials
    ################################################################################################
    def create_colormap_materials(self):
        """Creates the materials associated with the selected colormap."""

        # Soma
        self.skeleton_materials.extend(self.create_soma_materials())

        # Axons
        self.axons_materials = nmv.skeleton.create_multiple_materials(
            name='Axons [%s]' % self.morphology.code,
            material_type=self.options.shading.morphology_material,
            color_list=self.options.shading.morphology_colormap_list)
        self.skeleton_materials.extend(self.axons_materials)

        # Basal dendrites
        self.basal_dendrites_materials = nmv.skeleton.create_multiple_materials(
            name='Basals [%s]' % self.morphology.code,
            material_type=self.options.shading.morphology_material,
            color_list=self.options.shading.morphology_colormap_list)
        self.skeleton_materials.extend(self.basal_dendrites_materials)

        # Apical dendrites
        self.apical_dendrites_materials = nmv.skeleton.create_multiple_materials(
            name='Apicals [%s]' % self.morphology.code,
            material_type=self.options.shading.morphology_material,
            color_list=self.options.shading.morphology_colormap_list)
        self.skeleton_materials.extend(self.apical_dendrites_materials)

        # Gray material, Indices 8 and 9 in @self.skeleton_materials
        self.skeleton_materials.extend(self.create_gray_materials())

        # Articulations, Indices 10 and 11 in @self.skeleton_materials
        self.skeleton_materials.extend(self.create_articulation_materials())

        # Endfeet, if applicable, Indices 12 and 13 in @self.skeleton_materials
        self.skeleton_materials.extend(self.create_endfeet_materials())

    ################################################################################################
    # @create_base_skeleton_materials
    ################################################################################################
    def create_morphology_skeleton_materials(self):
        """Creates the materials of the morphology skeleton."""

        # Clean the already existing materials
        self.clear_materials()

        # Create the new materials
        scheme = self.options.shading.morphology_coloring_scheme

        # Every component (axons, apicals, basals, articulations, endfeet) has a specific color
        if scheme == nmv.enums.ColorCoding.DEFAULT_SCHEME:
            self.create_default_coloring_scheme_materials()

        # All the components have the same color (homogeneous coloring)
        # NOTE: The homogeneous coloring is done during obtaining the values from the interface
        elif scheme == nmv.enums.ColorCoding.HOMOGENEOUS_COLOR:
            self.create_default_coloring_scheme_materials()

        # Alternating colors, for the arbors, but same for the soma, articulations and endfeet
        elif scheme == nmv.enums.ColorCoding.ALTERNATING_COLORS:
            self.create_alternating_materials()

        # Color map(s)
        else:
            self.create_colormap_materials()

    ################################################################################################
    # @create_illumination
    ################################################################################################
    def create_illumination(self):
        """Creates the illumination sources that correspond to the selected shader."""

        # Clear the lights
        if self.lights is not None:
            nmv.scene.delete_list_objects(object_list=self.lights)

        # Create an illumination specific for the given material
        self.lights = nmv.shading.create_material_specific_illumination(
            self.options.shading.mesh_material)

        # Create a new collection from the created lights
        nmv.utilities.create_collection_with_objects(
            name='Illumination %s' % self.morphology.code, objects_list=self.lights)

    ################################################################################################
    # @resample_skeleton_sections
    ################################################################################################
    def resample_skeleton_sections(self):
        """Re-samples the sections of the morphology skeleton before drawing it."""

        nmv.skeleton.resample_skeleton(
            morphology=self.morphology, morphology_options=self.options.morphology)

    ################################################################################################
    # @shade_soma_mesh
    ################################################################################################
    def shade_soma_mesh(self):
        """Shades the soma mesh before displaying it in the scene."""

        # Assign a material to the soma sphere
        nmv.shading.set_material_to_object(self.soma_mesh, self.soma_materials[0])

        # Smooth shade the sphere to look nice
        nmv.mesh.ops.shade_smooth_object(self.soma_mesh)

    ################################################################################################
    # @draw_soma_as_sphere
    ################################################################################################
    def draw_soma_as_sphere(self):
        """Draws the soma as a symbolic sphere."""

        nmv.logger.detail('Symbolic Sphere Soma')
        self.soma_mesh = nmv.mesh.create_uv_sphere(
            radius=self.morphology.soma.mean_radius, location=self.morphology.soma.centroid,
            name='Soma')

        # Add the soma mesh to the morphology objects
        self.morphology_objects.append(self.soma_mesh)

        # Shades the soma mesh
        self.shade_soma_mesh()

    ################################################################################################
    # @create_base_skeleton_materials
    ################################################################################################
    def draw_meta_balls_soma(self):
        """Reconstructs a soma mesh using the SomaMetaBuilder."""

        nmv.logger.detail('Meta-ball Soma')
        builder = nmv.builders.SomaMetaBuilder(morphology=self.morphology, options=self.options)
        self.soma_mesh = builder.reconstruct_soma_mesh(apply_shader=False)

        # Add the soma mesh to the morphology objects
        self.morphology_objects.append(self.soma_mesh)

        # Shades the soma mesh
        self.shade_soma_mesh()

    ################################################################################################
    # @draw_soft_body_soma
    ################################################################################################
    def draw_soft_body_soma(self):
        """Reconstructs a soma mesh using the SomaSoftBodyBuilder."""

        nmv.logger.detail('Soft-body Soma')
        builder = nmv.builders.SomaSoftBodyBuilder(morphology=self.morphology, options=self.options)
        self.soma_mesh = builder.reconstruct_soma_mesh(apply_shader=False)

        # Add the soma mesh to the morphology objects
        self.morphology_objects.append(self.soma_mesh)

        # Shades the soma mesh
        self.shade_soma_mesh()

    ################################################################################################
    # @draw_soma
    ################################################################################################
    def draw_soma(self):
        """Draws the soma."""

        method = self.options.morphology.soma_representation
        if method == nmv.enums.Soma.Representation.SPHERE:
            self.draw_soma_as_sphere()
        elif method == nmv.enums.Soma.Representation.SOFT_BODY:
            self.draw_soft_body_soma()
        elif method == nmv.enums.Soma.Representation.META_BALLS:
            self.draw_meta_balls_soma()
        else:
            nmv.logger.detail('Soma is ignored')

    ################################################################################################
    # @draw_endfeet_if_applicable
    ################################################################################################
    def draw_endfeet_if_applicable(self):
        """Draws the endfeet of the astrocytes if they are present in the skeleton."""

        # Draw every endfoot in the list and append the resulting mesh to the collector
        for endfoot in self.morphology.endfeet:
            self.morphology_objects.append(endfoot.create_surface_patch(
                material=self.endfeet_materials[0]))

    ################################################################################################
    # @collection_morphology_objects_in_collection
    ################################################################################################
    def collection_morphology_objects_in_collection(self,
                                                    name='Morphology'):
        """Collects all the resulting objects of the morphology, or the dendrogram, in a group.

        :param name:
            The name of the collection object.
        """

        nmv.utilities.create_collection_with_objects(
            name='%s %s' % (name, self.morphology.label), objects_list=self.morphology_objects)

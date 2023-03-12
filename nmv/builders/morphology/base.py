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
    """Base class for all the morphology builders.
    Any morphology builder should inherit from this class, otherwise it will raise an error.
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
        :param options:
            System options.
        """

        # Morphology, and we deepcopy the instance such in case we modify it
        self.morphology = copy.deepcopy(morphology)

        # System options, and we deepcopy them in case a reference is changed by accident
        self.options = copy.deepcopy(options)

        # All the reconstructed objects of the morphology, for example, poly-lines, spheres etc...
        self.morphology_objects = list()

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

        # A list of the color/materials of the endfeet patches
        self.endfeet_materials = None

        # An aggregate list of all the materials of the skeleton
        self.skeleton_materials = list()

        # A gray material to highlight the other arbors in colors
        self.gray_material = None

        # UI Context
        self.context = None

    ################################################################################################
    # @clean_skeleton_material
    ################################################################################################
    @classmethod
    def clean_skeleton_material(cls):
        """Cleans all the morphology skeleton materials that exist in the Blender context.

        :return:
        """

        # Clear all the materials that are already present in the scene
        for material in bpy.data.materials:
            if 'soma_skeleton' in material.name or              \
               'axons_skeleton' in material.name or             \
               'basal_dendrites_skeleton' in material.name or   \
               'apical_dendrite_skeleton' in material.name or   \
               'articulations' in material.name or              \
               'endfeet' in material.name or                    \
               'gray' in material.name:

                nmv.utilities.disable_std_output()
                bpy.data.materials.remove(material, do_unlink=True)
                nmv.utilities.enable_std_output()

    ################################################################################################
    # @create_bevel_object
    ################################################################################################
    def create_bevel_object(self):
        """Creates a bevel object that is used to interpolate the polylines.

        :return:
        """
        bevel_object = nmv.mesh.create_bezier_circle(
            radius=1.0, resolution=self.options.morphology.bevel_object_sides,
            location=self.morphology.soma.centroid, name='Cross Section')

        return bevel_object

    ################################################################################################
    # @create_soma_material
    ################################################################################################
    def create_soma_material(self):
        """Creates the material of the soma for all the modes.
        """

        # Soma material
        self.soma_materials = nmv.skeleton.create_multiple_materials_with_same_color(
            name='soma_skeleton', material_type=self.options.shading.morphology_material,
            color=self.options.shading.morphology_soma_color,
            number_elements=1)

    ################################################################################################
    # @create_articulations_material
    ################################################################################################
    def create_articulations_material(self):
        """Creates the material of the articulations
        """

        # Articulations, ONLY, for the articulated reconstruction method
        self.articulations_materials = nmv.skeleton.create_multiple_materials_with_same_color(
            name='articulations', material_type=self.options.shading.morphology_material,
            color=self.options.shading.morphology_articulation_color,
            number_elements=1)

    ################################################################################################
    # @endfeet_materials
    ################################################################################################
    def create_endfeet_material(self):
        self.endfeet_materials = nmv.skeleton.create_multiple_materials_with_same_color(
            name='endfeet', material_type=self.options.shading.morphology_material,
            color=self.options.shading.morphology_endfeet_color,
            number_elements=1)

    ################################################################################################
    # @create_homogeneous_materials
    ################################################################################################
    def create_homogeneous_materials(self,
                                     number_elements=1):
        """

        :param number_elements:
        :return:
        """

        # Soma material
        self.create_soma_material()

        # Axon
        self.axons_materials = nmv.skeleton.create_multiple_materials_with_same_color(
            name='axon_skeleton', material_type=self.options.shading.morphology_material,
            color=self.options.shading.morphology_soma_color,
            number_elements=number_elements)

        # Basal dendrites
        self.basal_dendrites_materials = nmv.skeleton.create_multiple_materials_with_same_color(
            name='basal_dendrites_skeleton',
            material_type=self.options.shading.morphology_material,
            color=self.options.shading.morphology_soma_color,
            number_elements=number_elements)

        # Apical dendrite
        self.apical_dendrites_materials = nmv.skeleton.create_multiple_materials_with_same_color(
            name='apical_dendrite_skeleton',
            material_type=self.options.shading.morphology_material,
            color=self.options.shading.morphology_soma_color,
            number_elements=number_elements)

        # Articulations, ONLY, for the articulated reconstruction method
        self.create_articulations_material()

        # Endfeet, ONLY, for the astrocyte morphologies
        self.create_endfeet_material()

    ################################################################################################
    # @create_arbors_materials
    ################################################################################################
    def create_arbors_materials(self,
                                number_elements=1):
        """

        :param number_elements:
        :return:
        """
        # Soma material
        self.create_soma_material()

        # Axon
        self.axons_materials = nmv.skeleton.create_multiple_materials_with_same_color(
            name='axon_skeleton', material_type=self.options.shading.morphology_material,
            color=self.options.shading.morphology_axons_color,
            number_elements=number_elements)

        # Basal dendrites
        self.basal_dendrites_materials = nmv.skeleton.create_multiple_materials_with_same_color(
            name='basal_dendrites_skeleton',
            material_type=self.options.shading.morphology_material,
            color=self.options.shading.morphology_basal_dendrites_color,
            number_elements=number_elements)

        # Apical dendrite
        self.apical_dendrites_materials = nmv.skeleton.create_multiple_materials_with_same_color(
            name='apical_dendrite_skeleton',
            material_type=self.options.shading.morphology_material,
            color=self.options.shading.morphology_apical_dendrites_color,
            number_elements=number_elements)

        # Articulations, ONLY, for the articulated reconstruction method
        self.create_articulations_material()

        # Endfeet, ONLY, for the astrocyte morphologies
        self.create_endfeet_material()

    ################################################################################################
    # @create_alternating_materials
    ################################################################################################
    def create_alternating_materials(self):
        """

        :return:
        """

        # Soma material
        self.create_soma_material()

        # Axon
        self.axons_materials = list()
        self.axons_materials.append(nmv.skeleton.create_single_material(
            name='axons_skeleton_1',
            material_type=self.options.shading.morphology_material,
            color=self.options.shading.morphology_alternating_color_1))
        self.axons_materials.append(nmv.skeleton.create_single_material(
            name='axons_skeleton_2',
            material_type=self.options.shading.morphology_material,
            color=self.options.shading.morphology_alternating_color_2))

        # Basal dendrites
        self.basal_dendrites_materials = list()
        self.basal_dendrites_materials.append(nmv.skeleton.create_single_material(
            name='basal_dendrites_skeleton_1',
            material_type=self.options.shading.morphology_material,
            color=self.options.shading.morphology_alternating_color_1))
        self.basal_dendrites_materials.append(nmv.skeleton.create_single_material(
            name='basal_dendrites_skeleton_2',
            material_type=self.options.shading.morphology_material,
            color=self.options.shading.morphology_alternating_color_2))

        # Apical dendrite
        self.apical_dendrites_materials = list()
        self.apical_dendrites_materials.append(nmv.skeleton.create_single_material(
            name='apical_dendrites_skeleton_1',
            material_type=self.options.shading.morphology_material,
            color=self.options.shading.morphology_alternating_color_1))
        self.apical_dendrites_materials.append(nmv.skeleton.create_single_material(
            name='apical_dendrites_skeleton_2',
            material_type=self.options.shading.morphology_material,
            color=self.options.shading.morphology_alternating_color_2))

        # Articulations, ONLY, for the articulated reconstruction method
        self.create_articulations_material()

        # Endfeet, ONLY, for the astrocyte morphologies
        self.create_endfeet_material()

    ################################################################################################
    # @create_colormap_materials
    ################################################################################################
    def create_colormap_materials(self):
        """Creates the

        :return:
        """

        self.clean_skeleton_material()

        # Soma material
        self.create_soma_material()

        # Basal dendrites
        self.basal_dendrites_materials = nmv.skeleton.create_multiple_materials(
            name='basal_dendrites_skeleton',
            material_type=self.options.shading.morphology_material,
            color_list=self.options.shading.morphology_colormap_list)

        # Apical dendrites
        self.apical_dendrites_materials = nmv.skeleton.create_multiple_materials(
            name='apical_dendrites_skeleton',
            material_type=self.options.shading.morphology_material,
            color_list=self.options.shading.morphology_colormap_list)

        # Axons
        self.axons_materials = nmv.skeleton.create_multiple_materials(
            name='axons_skeleton',
            material_type=self.options.shading.morphology_material,
            color_list=self.options.shading.morphology_colormap_list)

        # Articulations, ONLY, for the articulated reconstruction method
        self.create_articulations_material()

        # Endfeet, ONLY, for the astrocyte morphologies
        self.create_endfeet_material()

    ################################################################################################
    # @update_sections_branching
    ################################################################################################
    def update_sections_branching(self):
        """Updates the sections at the branching points and label them to primary or secondary based
        on their angles and radii.
        """

        nmv.logger.info('Updating section branching to primary and secondary')

        # Label the primary and secondary sections based on angles
        if self.options.morphology.branching == nmv.enums.Skeleton.Branching.ANGLES:
            nmv.skeleton.ops.apply_operation_to_morphology(
                *[self.morphology,
                  nmv.skeleton.ops.label_primary_and_secondary_sections_based_on_angles])

        # Label the primary and secondary sections based on radii
        else:
            nmv.skeleton.ops.apply_operation_to_morphology(
                *[self.morphology,
                  nmv.skeleton.ops.label_primary_and_secondary_sections_based_on_radii])

    ################################################################################################
    # @resample_skeleton_sections
    ################################################################################################
    def resample_skeleton_sections(self):
        """Re-samples the sections of the morphology skeleton before drawing it.

        NOTE: This resampling process is performed on a per-section basis, so the first and last samples
        of the section are left intact.
            A given skeleton builder.
        """

        nmv.logger.info('Resampling skeleton')

        # The adaptive resampling is quite important to prevent breaking the structure
        if self.options.morphology.resampling_method == \
                nmv.enums.Skeleton.Resampling.ADAPTIVE_RELAXED:
            nmv.logger.detail('Relaxed Adaptive Resampling')
            nmv.skeleton.ops.apply_operation_to_morphology(
                *[self.morphology, nmv.skeleton.ops.resample_section_adaptively_relaxed])
        elif self.options.morphology.resampling_method == \
                nmv.enums.Skeleton.Resampling.ADAPTIVE_PACKED:
            nmv.logger.detail('Packed (or Overlapping) Adaptive Resampling')
            nmv.skeleton.ops.apply_operation_to_morphology(
                *[self.morphology, nmv.skeleton.ops.resample_section_adaptively])
        elif self.options.morphology.resampling_method == \
                nmv.enums.Skeleton.Resampling.FIXED_STEP:
            nmv.logger.detail('Fixed Step Resampling with step of [%f] um' %
                              self.options.morphology.resampling_step)
            nmv.skeleton.ops.apply_operation_to_morphology(
                *[self.morphology, nmv.skeleton.ops.resample_section_at_fixed_step,
                  self.options.morphology.resampling_step])
        else:
            pass

    ################################################################################################
    # @create_base_skeleton_materials
    ################################################################################################
    def create_base_skeleton_materials(self):

        # Clean the skeleton materials
        self.clean_skeleton_material()

        # For simplification and code line limit
        scheme = self.options.shading.morphology_coloring_scheme

        # Homogeneous color
        if scheme == nmv.enums.ColorCoding.HOMOGENEOUS_COLOR:
            self.create_homogeneous_materials()

        # Color arbors by type
        elif scheme == nmv.enums.ColorCoding.DEFAULT_SCHEME:
            self.create_arbors_materials()

        # Alternating colors
        elif scheme == nmv.enums.ColorCoding.ALTERNATING_COLORS:
            self.create_alternating_materials()

        # Colormap
        else:
            self.create_colormap_materials()

    ################################################################################################
    # @create_base_skeleton_materials
    ################################################################################################
    def draw_soma_sphere(self):
        """Draws a sphere that represents the soma.
        """

        # Get a reference to the soma
        soma = self.morphology.soma

        # Draw the soma as a sphere
        soma_sphere = nmv.mesh.create_uv_sphere(
            radius=soma.mean_radius, location=soma.centroid, name='soma')

        # Assign a material to the soma sphere
        nmv.shading.set_material_to_object(soma_sphere, self.soma_materials[0])

        # Return a reference to the object
        return soma_sphere

    ################################################################################################
    # @create_base_skeleton_materials
    ################################################################################################
    def draw_meta_balls_soma(self):
        """Draws the soma.
        """

        # Create the MetaBuilder
        soma_builder_object = nmv.builders.SomaMetaBuilder(self.morphology, self.options)

        # Reconstruct the soma, don't apply the default shader and use the one from the
        # morphology panel
        soma_mesh = soma_builder_object.reconstruct_soma_mesh(apply_shader=False)

        # Apply the shader given in the morphology options, not the one in the soma toolbox
        nmv.shading.set_material_to_object(soma_mesh, self.soma_materials[0])

        # Add the soma mesh to the morphology objects
        self.morphology_objects.append(soma_mesh)

    ################################################################################################
    # @create_base_skeleton_materials
    ################################################################################################
    def draw_soma(self):
        """Draws the soma.
        """

        # Draw the soma as a sphere object
        if self.options.morphology.soma_representation == nmv.enums.Soma.Representation.SPHERE:

            # Draw the soma sphere
            nmv.logger.detail('Symbolic sphere')
            soma_sphere = self.draw_soma_sphere()

            # Smooth shade the sphere to look nice
            nmv.mesh.ops.shade_smooth_object(soma_sphere)

            # Add the soma sphere to the morphology objects to keep track on it
            self.morphology_objects.append(soma_sphere)

        # Or as a reconstructed profile using the soma builder
        elif self.options.morphology.soma_representation == nmv.enums.Soma.Representation.SOFT_BODY:

            # Create a soma builder object
            soma_builder_object = nmv.builders.SomaSoftBodyBuilder(self.morphology,
                                                                   self.options)

            # Reconstruct the three-dimensional profile of the soma mesh without applying the
            # default shader to it,
            # since we need to use the shader specified in the morphology options
            soma_mesh = soma_builder_object.reconstruct_soma_mesh(apply_shader=False)

            # Apply the shader given in the morphology options, not the one in the soma toolbox
            nmv.shading.set_material_to_object(soma_mesh, self.soma_materials[0])

            # Add the soma mesh to the morphology objects
            self.morphology_objects.append(soma_mesh)

        elif self.options.morphology.soma_representation == \
                nmv.enums.Soma.Representation.META_BALLS:
            self.draw_meta_balls_soma()

        # Otherwise, ignore the soma drawing
        else:
            nmv.logger.detail('Ignoring soma')

    ################################################################################################
    # @create_base_skeleton_materials
    ################################################################################################
    def create_skeleton_materials_and_illumination(self):
        """Creates the materials of the entire morphology skeleton and the accompanying
        illumination.

        NOTE: The created materials are stored in member variables of the given builder.
        """

        # Clear all the materials that are already present in the scene
        for material in bpy.data.materials:
            if 'soma_skeleton' in material.name or \
               'axon_skeleton' in material.name or \
               'basal_dendrites_skeleton' in material.name or \
               'apical_dendrite_skeleton' in material.name or \
               'articulation' in material.name or \
               'endfeet' in material.name or \
               'gray' in material.name:

                nmv.utilities.disable_std_output()
                bpy.data.materials.remove(material, do_unlink=True)
                nmv.utilities.enable_std_output()

        # Soma
        self.soma_materials = nmv.skeleton.ops.create_skeleton_materials(
            name='soma_skeleton', material_type=self.options.shading.morphology_material,
            color=self.options.shading.morphology_soma_color)

        # Axon
        self.axons_materials = nmv.skeleton.ops.create_skeleton_materials(
            name='axon_skeleton', material_type=self.options.shading.morphology_material,
            color=self.options.shading.morphology_axons_color)

        # Basal dendrites
        self.basal_dendrites_materials = nmv.skeleton.ops.create_skeleton_materials(
            name='basal_dendrites_skeleton', material_type=self.options.shading.morphology_material,
            color=self.options.shading.morphology_basal_dendrites_color)

        # Apical dendrite
        self.apical_dendrites_materials = nmv.skeleton.ops.create_skeleton_materials(
            name='apical_dendrite_skeleton', material_type=self.options.shading.morphology_material,
            color=self.options.shading.morphology_apical_dendrites_color)

        # Articulations, ONLY, for the articulated reconstruction method
        if self.options.morphology.reconstruction_method == \
                nmv.enums.Skeleton.Method.ARTICULATED_SECTIONS:
            self.articulations_materials = nmv.skeleton.ops.create_skeleton_materials(
                name='articulation', material_type=self.options.shading.morphology_material,
                color=self.options.shading.morphology_articulation_color)

        self.endfeet_materials = nmv.skeleton.ops.create_skeleton_materials(
            name='endfeet', material_type=self.options.shading.morphology_material,
            color=self.options.shading.morphology_endfeet_color)

        # Create an illumination specific for the given material
        nmv.shading.create_material_specific_illumination(
            material_type=self.options.shading.morphology_material,
            location=self.morphology.soma.centroid)

    ################################################################################################
    # @transform_to_global_coordinates
    ################################################################################################
    def transform_to_global_coordinates(self):
        """Transforms the morphology to the global coordinates.
        """

        return
        # Transform the arbors to the global coordinates if required for a circuit
        if self.options.morphology.global_coordinates or not self.options.morphology.center_at_origin:

            # Ignore if no information is given
            if self.options.morphology.gid is None and self.morphology.original_center is None:
                return

            # Make sure that a GID is selected
            if self.options.morphology.gid is not None:
                nmv.logger.log('Transforming morphology to global coordinates ')
                nmv.skeleton.ops.transform_morphology_to_global_coordinates(
                    morphology_objects=self.morphology_objects,
                    blue_config=self.options.morphology.blue_config,
                    gid=self.options.morphology.gid)

                # Don't proceed
                return

            # If the original center is updated
            if self.morphology.original_center is not None:
                nmv.logger.info('Transforming to global coordinates')

                # Do it mesh by mesh
                for i, morphology_object in enumerate(self.morphology_objects):

                    # Progress
                    nmv.utilities.show_progress('* Transforming to global coordinates',
                                                float(i),
                                                float(len(self.morphology_objects)))

                    # Translate the object
                    nmv.scene.translate_object(scene_object=morphology_object,
                                               shift=self.morphology.original_center)


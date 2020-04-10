####################################################################################################
# Copyright (c) 2016 - 2020, EPFL / Blue Brain Project
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

# Internal imports
import nmv.enums
import nmv.shading
import nmv.skeleton
import nmv.mesh


####################################################################################################
# @create_skeleton_materials_and_illumination
####################################################################################################
def create_skeleton_materials_and_illumination(builder):
    """Creates the materials of the entire morphology skeleton and the accompanying illumination.

    NOTE: The created materials are stored in member variables of the given builder.

    :param builder:
        A given skeleton builder.
    """

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

    # Soma
    builder.soma_materials = nmv.skeleton.ops.create_skeleton_materials(
        name='soma_skeleton', material_type=builder.options.shading.morphology_material,
        color=builder.options.shading.soma_color)

    # Axon
    builder.axons_materials = nmv.skeleton.ops.create_skeleton_materials(
        name='axon_skeleton', material_type=builder.options.shading.morphology_material,
        color=builder.options.shading.morphology_axon_color)

    # Basal dendrites
    builder.basal_dendrites_materials = nmv.skeleton.ops.create_skeleton_materials(
        name='basal_dendrites_skeleton', material_type=builder.options.shading.morphology_material,
        color=builder.options.shading.morphology_basal_dendrites_color)

    # Apical dendrite
    builder.apical_dendrites_materials = nmv.skeleton.ops.create_skeleton_materials(
        name='apical_dendrite_skeleton', material_type=builder.options.shading.morphology_material,
        color=builder.options.shading.morphology_apical_dendrites_color)

    # Articulations, ONLY, for the articulated reconstruction method
    if builder.options.morphology.reconstruction_method == \
            nmv.enums.Skeleton.Method.ARTICULATED_SECTIONS:
        builder.articulations_materials = nmv.skeleton.ops.create_skeleton_materials(
            name='articulation', material_type=builder.options.shading.morphology_material,
            color=builder.options.shading.morphology_articulation_color)

    # Create an illumination specific for the given material
    nmv.shading.create_material_specific_illumination(builder.options.shading.morphology_material)


####################################################################################################
# @update_sections_branching
####################################################################################################
def update_sections_branching(builder):
    """Updates the sections at the branching points and label them to primary or secondary based
    on their angles and radii.

    :param builder:
        A given skeleton builder.
    """

    # Label the primary and secondary sections based on angles
    if builder.options.morphology.branching == nmv.enums.Skeleton.Branching.ANGLES:
        nmv.skeleton.ops.apply_operation_to_morphology(
            *[builder.morphology,
              nmv.skeleton.ops.label_primary_and_secondary_sections_based_on_angles])

    # Label the primary and secondary sections based on radii
    else:
        nmv.skeleton.ops.apply_operation_to_morphology(
            *[builder.morphology,
              nmv.skeleton.ops.label_primary_and_secondary_sections_based_on_radii])


####################################################################################################
# @resample_skeleton_sections
####################################################################################################
def resample_skeleton_sections(builder):
    """Re-samples the sections of the morphology skeleton before drawing it.

    NOTE: This resampling process is performed on a per-section basis, so the first and last samples
    of the section are left intact.

    :param builder:
        A given skeleton builder.
    """

    nmv.logger.info('Resampling sections')

    # The adaptive resampling is quite important to prevent breaking the structure
    if builder.options.morphology.resampling_method == \
            nmv.enums.Skeleton.Resampling.ADAPTIVE_RELAXED:
        nmv.logger.detail('Relaxed Adaptive Resampling')
        nmv.skeleton.ops.apply_operation_to_morphology(
            *[builder.morphology, nmv.skeleton.ops.resample_section_adaptively_relaxed])
    elif builder.options.morphology.resampling_method == \
            nmv.enums.Skeleton.Resampling.ADAPTIVE_PACKED:
        nmv.logger.detail('Packed (or Overlapping) Adaptive Resampling')
        nmv.skeleton.ops.apply_operation_to_morphology(
            *[builder.morphology, nmv.skeleton.ops.resample_section_adaptively])
    elif builder.options.morphology.resampling_method == \
            nmv.enums.Skeleton.Resampling.FIXED_STEP:
        nmv.logger.detail('Fixed Step Resampling with step of [%f] um' %
                          builder.options.morphology.resampling_step)
        nmv.skeleton.ops.apply_operation_to_morphology(
            *[builder.morphology, nmv.skeleton.ops.resample_section_at_fixed_step,
              builder.options.morphology.resampling_step])
    else:
        pass


####################################################################################################
# @draw_soma_sphere
####################################################################################################
def draw_soma_sphere(builder):
    """Draws a sphere that represents the soma.
    """

    # Get a reference to the soma
    soma = builder.morphology.soma

    # Draw the soma as a sphere
    soma_sphere = nmv.mesh.create_uv_sphere(
        radius=soma.largest_radius, location=soma.centroid, name='soma')

    # Assign a material to the soma sphere
    nmv.shading.set_material_to_object(soma_sphere, builder.soma_materials[0])

    # Return a reference to the object
    return soma_sphere


####################################################################################################
# @draw_soma
####################################################################################################
def draw_soma(builder):
    """Draws the soma.

    :param builder:
        A given skeleton builder.
    """

    # Draw the soma as a sphere object
    if builder.options.morphology.soma_representation == nmv.enums.Soma.Representation.SPHERE:

        # Draw the soma sphere
        nmv.logger.detail('Symbolic sphere')
        soma_sphere = draw_soma_sphere(builder=builder)

        # Smooth shade the sphere to look nice
        nmv.mesh.ops.shade_smooth_object(soma_sphere)

        # Add the soma sphere to the morphology objects to keep track on it
        builder.morphology_objects.append(soma_sphere)

    # Or as a reconstructed profile using the soma builder
    elif builder.options.morphology.soma_representation == nmv.enums.Soma.Representation.SOFT_BODY:

        # Create a soma builder object
        soma_builder_object = nmv.builders.SomaSoftBodyBuilder(builder.morphology, builder.options)

        # Reconstruct the three-dimensional profile of the soma mesh without applying the
        # default shader to it,
        # since we need to use the shader specified in the morphology options
        soma_mesh = soma_builder_object.reconstruct_soma_mesh(apply_shader=False)

        # Apply the shader given in the morphology options, not the one in the soma toolbox
        nmv.shading.set_material_to_object(soma_mesh, builder.soma_materials[0])

        # Add the soma mesh to the morphology objects
        builder.morphology_objects.append(soma_mesh)

    elif builder.options.morphology.soma_representation == \
            nmv.enums.Soma.Representation.META_BALLS:

        # Create the MetaBuilder
        soma_builder_object = nmv.builders.SomaMetaBuilder(builder.morphology, builder.options)

        # Reconstruct the soma, don't apply the default shader and use the one from the
        # morphology panel
        soma_mesh = soma_builder_object.reconstruct_soma_mesh(apply_shader=False)

        # Apply the shader given in the morphology options, not the one in the soma toolbox
        nmv.shading.set_material_to_object(soma_mesh, builder.soma_materials[0])

        # Add the soma mesh to the morphology objects
        builder.morphology_objects.append(soma_mesh)

    # Otherwise, ignore the soma drawing
    else:
        nmv.logger.detail('Ignoring soma')


####################################################################################################
# @transform_to_global_coordinates
####################################################################################################
def transform_to_global_coordinates(builder):

    # Transform the arbors to the global coordinates if required for a circuit
    if builder.options.morphology.global_coordinates and \
            builder.options.morphology.blue_config is not None and \
            builder.options.morphology.gid is not None:
        # Transforming
        nmv.logger.log('Transforming morphology to global coordinates ')
        nmv.skeleton.ops.transform_morphology_to_global_coordinates(
            morphology_objects=builder.morphology_objects,
            blue_config=builder.options.morphology.blue_config,
            gid=builder.options.morphology.gid)

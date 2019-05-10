####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
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

# System Imports
import sys

# Internal imports
import nmv
import nmv.options


####################################################################################################
# @NeuroMorphoVisOptions
####################################################################################################
class NeuroMorphoVisOptions:
    """Workflow options all combined in a single structure.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        """Constructor
        """

        # Morphology options
        self.morphology = nmv.options.morphology_options.MorphologyOptions()

        # Mesh options
        self.mesh = nmv.options.mesh_options.MeshOptions()

        # Input / output options
        self.io = nmv.options.io_options.IOOptions()

        # Soma options (for the soma)
        self.soma = nmv.options.soma_options.SomaOptions()

    ################################################################################################
    # @consume_arguments
    ################################################################################################
    def consume_arguments(self,
                          arguments):
        """Convert the command line arguments to options.

        :param arguments:
            Input command line arguments.
        """

        # Internal imports
        import nmv.consts
        import nmv.enums
        import nmv.file
        import nmv.utilities

        ############################################################################################
        # Output options
        ############################################################################################
        # Main output directory
        self.io.output_directory = arguments.output_directory

        # Images directory
        self.io.images_directory = '%s/%s' % (arguments.output_directory,
                                              nmv.consts.Paths.IMAGES_FOLDER)

        # Sequences directory
        self.io.sequences_directory = '%s/%s' % (arguments.output_directory,
                                                 nmv.consts.Paths.SEQUENCES_FOLDER)

        # Meshes directory
        self.io.meshes_directory = '%s/%s' % (arguments.output_directory,
                                              nmv.consts.Paths.MESHES_FOLDER)

        # Morphologies directory
        self.io.morphologies_directory = '%s/%s' % (arguments.output_directory,
                                                    nmv.consts.Paths.MORPHOLOGIES_FOLDER)

        # Morphologies directory
        self.io.analysis_directory = '%s/%s' % (arguments.output_directory,
                                                nmv.consts.Paths.ANALYSIS_FOLDER)

        # Statistics directory
        self.io.statistics_directory = '%s/%s' % (arguments.output_directory,
                                                  nmv.consts.Paths.STATS_FOLDER)

        ############################################################################################
        # Morphology options
        ############################################################################################
        # Morphology reconstruction flag
        self.morphology.reconstruct_morphology = arguments.reconstruct_morphology_skeleton

        # Morphology skeleton
        self.morphology.skeleton = nmv.enums.Skeletonization.Skeleton.get_enum(
            arguments.morphology_skeleton)

        # Morphology reconstruction method
        self.morphology.reconstruction_method = nmv.enums.Skeletonization.Method.get_enum(
           argument=arguments.morphology_reconstruction_algorithm)

        # Morphology GID
        if arguments.input == 'gid':

            # Update the GID
            self.morphology.gid = arguments.gid

            # Update the circuit
            self.morphology.blue_config = arguments.blue_config

            # Update the label
            self.morphology.label = 'neuron_' + str(arguments.gid)

        # Morphology file
        if arguments.input == 'file':

            # Set the gid to None
            self.morphology.gid = None

            # Update the file
            self.morphology.morphology_file_path = arguments.morphology_file

            # Update the morphology label
            self.morphology.label = nmv.file.ops.get_file_name_from_path(arguments.morphology_file)

        # Soma reconstruction
        self.morphology.soma_representation = \
            nmv.enums.Soma.Representation.get_enum(arguments.soma_representation)

        # Ignore axon
        self.morphology.ignore_axon = arguments.ignore_axon

        # Ignore apical dendrite, if exists
        self.morphology.ignore_apical = arguments.ignore_apical_dendrites

        # Ignore basal dendrites
        self.morphology.ignore_basal_dendrites = arguments.ignore_basal_dendrites

        # Axon branching level
        self.morphology.axon_branch_order = arguments.axon_branching_order

        # Basal dendrites branching level
        self.morphology.basal_dendrites_branch_order = arguments.basal_dendrites_branching_order

        # Apical dendrite branching level, if exists
        self.morphology.apical_dendrite_branch_order = arguments.apical_dendrites_branching_order

        # Export the reconstructed morphology to the global coordinates of the circuit
        self.morphology.global_coordinates = arguments.global_coordinates

        # Morphology material
        self.morphology.material = nmv.enums.Shading.get_enum(arguments.shader)

        # Soma color
        self.morphology.soma_color = nmv.utilities.parse_color_from_argument(arguments.soma_color)

        # Axon color
        self.morphology.axon_color = nmv.utilities.parse_color_from_argument(arguments.axon_color)

        # Basal dendrites color
        self.morphology.basal_dendrites_color = nmv.utilities.parse_color_from_argument(
            arguments.basal_dendrites_color)

        # Apical dendrite color
        self.morphology.apical_dendrites_color = nmv.utilities.parse_color_from_argument(
            arguments.apical_dendrites_color)

        # Bevel object sides used for the branches reconstruction
        self.morphology.bevel_object_sides = arguments.bevel_sides

        # Sections radii
        # Fixed radius across all the arbors
        if arguments.sections_radii == 'fixed':
            self.morphology.scale_sections_radii = False
            self.morphology.unify_sections_radii = True
            self.morphology.sections_fixed_radii_value = arguments.fixed_section_radius

        # Scaled radii w.r.t the given in the morphology file
        elif arguments.sections_radii == 'scaled':
            self.morphology.scale_sections_radii = True
            self.morphology.unify_sections_radii = False
            self.morphology.sections_radii_scale = arguments.radii_scale_factor

        # Filtered
        elif arguments.sections_radii == 'filtered':
            self.morphology.scale_sections_radii = False
            self.morphology.unify_sections_radii = False
            self.morphology.sections_radii_scale = arguments.radii_scale_factor

        # Default as given in the morphology file
        else:
            self.morphology.scale_sections_radii = False
            self.morphology.unify_sections_radii = False

        # Camera view [FRONT, SIDE or TOP]
        self.morphology.camera_view = nmv.enums.Camera.View.get_enum(arguments.camera_view)

        # Rendering view
        self.morphology.rendering_view = nmv.enums.Skeletonization.Rendering.View.get_enum(
            arguments.rendering_view)

        # Resolution basis
        self.morphology.resolution_basis = nmv.enums.Skeletonization.Rendering.Resolution.TO_SCALE if \
            arguments.render_to_scale else nmv.enums.Skeletonization.Rendering.Resolution.FIXED_RESOLUTION

        # Render a close up view of the morphology
        self.morphology.render = arguments.render_neuron_morphology

        # Render a close up view of the morphology
        self.morphology.render_360 = arguments.render_neuron_morphology_360

        # Render the progressive reconstruction of the morphology
        self.morphology.render_progressive = arguments.render_neuron_morphology_progressive

        # Full view image resolution
        self.morphology.full_view_resolution = arguments.full_view_resolution

        # Resolution scale factor
        self.morphology.resolution_scale_factor = arguments.resolution_scale_factor

        # Close up image resolution
        self.morphology.close_up_resolution = arguments.close_up_resolution

        # Close up view dimensions
        self.morphology.close_up_dimensions = arguments.close_up_dimensions

        # Export the morphology to .h5 file
        self.morphology.export_h5 = arguments.export_morphology_h5

        # Export the morphology to .swc file
        self.morphology.export_swc = arguments.export_morphology_swc

        # Export the morphology skeleton to .blend file for rendering using tubes
        self.morphology.export_blend = arguments.export_morphology_blend

        ############################################################################################
        # Soma soft body options
        ############################################################################################
        # Stiffness
        self.soma.stiffness = arguments.soma_stiffness

        # Subdivision level of the sphere
        self.soma.subdivision_level = arguments.soma_subdivision_level

        # Soma color
        self.soma.soma_color = nmv.utilities.parse_color_from_argument(arguments.soma_color)

        # Soma material
        self.soma.soma_material = nmv.enums.Shading.get_enum(arguments.shader)

        # Reconstruct soma mesh
        self.soma.reconstruct_soma_mesh = arguments.reconstruct_soma_mesh

        # Render soma mesh flag
        self.soma.render_soma_mesh = arguments.render_soma_mesh

        # Render soma mesh 360
        self.soma.render_soma_mesh_360 = arguments.render_soma_mesh_360

        # Render progressive reconstruction of the soma mesh
        self.soma.render_soma_mesh_progressive = arguments.render_soma_mesh_progressive

        # Rendering resolution for the soma frames
        self.soma.rendering_resolution = arguments.full_view_resolution

        # Camera view [FRONT, SIDE or TOP]
        self.soma.camera_view = nmv.enums.Camera.View.get_enum(arguments.camera_view)

        # Export soma mesh in .ply format
        self.soma.export_ply = arguments.export_soma_mesh_ply

        # Export soma mesh in .obj format
        self.soma.export_obj = arguments.export_soma_mesh_obj

        # Export soma mesh in .stl format
        self.soma.export_stl = arguments.export_soma_mesh_stl

        # Export soma mesh in .blend format
        self.soma.export_blend = arguments.export_soma_mesh_blend

        ############################################################################################
        # Mesh options
        ############################################################################################
        # Reconstruct neuron mesh for exporting
        self.mesh.reconstruct_neuron_mesh = arguments.reconstruct_neuron_mesh

        # Skeletonization
        self.mesh.skeletonization = nmv.enums.Meshing.Skeleton.get_enum(
            arguments.morphology_skeleton)

        # Tessellation level (between 0.1 and 1.0)
        self.mesh.tessellation_level = float(arguments.tessellation_level)

        # Tessellate the mesh after the reconstruction if requested
        self.mesh.tessellate_mesh = True if 0.1 < self.mesh.tessellation_level < 1.0 else False

        # Meshing technique
        self.mesh.meshing_technique = nmv.enums.Meshing.Technique.get_enum(
            arguments.meshing_algorithm)

        # Spines (source)
        self.mesh.spines = nmv.enums.Meshing.Spines.Source.get_enum(arguments.spines)

        # Spine quality
        self.mesh.spines_mesh_quality = \
            nmv.enums.Meshing.Spines.Quality.get_enum(arguments.spines_quality)

        # Random spines percentage
        self.mesh.random_spines_percentage = arguments.random_spines_percentage

        # Edges of the meshes, either hard or smooth
        self.mesh.edges = nmv.enums.Meshing.Edges.get_enum(arguments.edges)

        # Surface
        self.mesh.surface = nmv.enums.Meshing.Surface.get_enum(arguments.surface)

        # Render a static image of the mesh
        self.mesh.render = arguments.render_neuron_mesh

        # Render a 360 sequence of the mesh
        self.mesh.render_360 = arguments.render_neuron_mesh_360

        # Camera view [FRONT, SIDE or TOP]
        self.mesh.camera_view = nmv.enums.Camera.View.get_enum(arguments.camera_view)

        # Rendering view
        self.mesh.rendering_view = nmv.enums.Meshing.Rendering.View.get_enum(
            arguments.rendering_view)

        # Resolution basis
        self.mesh.resolution_basis = nmv.enums.Meshing.Rendering.Resolution.TO_SCALE if \
            arguments.render_to_scale else nmv.enums.Meshing.Rendering.Resolution.FIXED_RESOLUTION

        # Resolution scale factor
        self.mesh.resolution_scale_factor = arguments.resolution_scale_factor

        # Full view image resolution
        self.mesh.full_view_resolution = arguments.full_view_resolution

        # Close up image resolution
        self.mesh.close_up_resolution = arguments.close_up_resolution

        # Close up view dimensions
        self.mesh.close_up_dimensions = arguments.close_up_dimensions

        # Mesh material
        self.mesh.material = nmv.enums.Shading.get_enum(arguments.shader)

        # Soma color
        self.mesh.soma_color = nmv.utilities.parse_color_from_argument(arguments.soma_color)

        # Axon color
        self.mesh.axon_color = nmv.utilities.parse_color_from_argument(arguments.axon_color)

        # Basal dendrites color
        self.mesh.basal_dendrites_color = nmv.utilities.parse_color_from_argument(
            arguments.basal_dendrites_color)

        # Apical dendrite color
        self.mesh.apical_dendrites_color = nmv.utilities.parse_color_from_argument(
            arguments.apical_dendrites_color)

        # Spines color
        self.mesh.spines_color = nmv.utilities.parse_color_from_argument(arguments.spines_color)

        # Nucleus color
        self.mesh.nucleus_color = nmv.utilities.parse_color_from_argument(arguments.nucleus_color)

        # Save the reconstructed mesh as a .PLY file to the meshes directory
        self.mesh.export_ply = arguments.export_neuron_mesh_ply

        # Save the reconstructed mesh as a .OBJ file to the meshes directory
        self.mesh.export_obj = arguments.export_neuron_mesh_obj

        # Save the reconstructed mesh as a .STL file to the meshes directory
        self.mesh.export_stl = arguments.export_neuron_mesh_stl

        # Save the reconstructed mesh as a .BLEND file to the meshes directory
        self.mesh.export_blend = arguments.export_neuron_mesh_blend

        # Export each part of the neuron as a separate mesh if possible
        self.mesh.export_individuals = arguments.export_individuals

        # Export the reconstructed mesh to the global coordinates of the circuit
        self.mesh.global_coordinates = arguments.global_coordinates

        # Connect the arbors to the soma to form a single mesh
        self.mesh.soma_connection = nmv.enums.Meshing.SomaConnection.CONNECTED if \
            arguments.connect_soma_arbors else nmv.enums.Meshing.SomaConnection.DISCONNECTED



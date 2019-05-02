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

# Internal imports
import nmv 
import nmv.consts
import nmv.enums


####################################################################################################
# @MeshOptions
####################################################################################################
class MeshOptions:
    """Mesh options
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        """Constructor
        """

        # DATA #####################################################################################
        # This flag must be set to reconstruct a mesh
        self.reconstruct_neuron_mesh = False

        # MESHING OPTIONS ##########################################################################
        # Tessellate the mesh after the reconstruction
        self.tessellate_mesh = False

        # Tessellation level (between 0.1 and 1.0)
        self.tessellation_level = nmv.consts.Meshing.MAX_TESSELLATION_LEVEL

        # Fixing morphology artifacts
        self.fix_morphology_artifacts = True

        # Skeletonization technique
        self.skeletonization = nmv.enums.Meshing.Skeleton.ORIGINAL

        # Meshing technique
        self.meshing_technique = nmv.enums.Meshing.Technique.PIECEWISE_WATERTIGHT

        # Export in circuit coordinates, by default no unless there is a circuit file given
        self.global_coordinates = False

        # Soma connection to the arbors, connected or disconnected
        self.soma_connection = nmv.enums.Meshing.SomaConnection.DISCONNECTED

        # Connecting the different objects of the neuron into a single mesh
        self.neuron_objects_connection = nmv.enums.Meshing.ObjectsConnection.DISCONNECTED

        # Create the mesh to look like a real neuron or more for visualization
        self.surface = nmv.enums.Meshing.Surface.SMOOTH

        # Edges of the meshes, either hard or smooth
        self.edges = nmv.enums.Meshing.Edges.HARD

        # Branching of the meshes, either based on angles or radii
        self.branching = nmv.enums.Meshing.Branching.ANGLES

        # The shape of the skeleton that is used in the union meshing algorithm
        self.skeleton_shape = nmv.enums.Meshing.UnionMeshing.QUAD_SKELETON

        # SPINES OPTIONS ###########################################################################
        # The source where the spines will be loaded from, by default ignore the spines
        self.spines = nmv.enums.Meshing.Spines.Source.IGNORE

        # Spines mesh quality, by default low quality
        self.spines_mesh_quality = nmv.enums.Meshing.Spines.Quality.LQ

        # Percentage of random spines
        self.random_spines_percentage = nmv.consts.Meshing.RANDOM_SPINES_PERCENTAGE

        # NUCLEI OPTIONS ###########################################################################
        # Nucleus, ignore by default
        self.nucleus = nmv.enums.Meshing.Nucleus.IGNORE

        # Nucleus mesh quality, by default low quality
        self.nucleus_mesh_quality = nmv.enums.Meshing.Nucleus.Quality.LQ

        # COLOR & MATERIALS OPTIONS ################################################################
        # Morphology material
        self.material = nmv.enums.Shading.LAMBERT_WARD

        # Soma color
        self.soma_color = nmv.enums.Color.SOMA

        # Axon color
        self.axon_color = nmv.enums.Color.AXONS

        # Basal dendrites color
        self.basal_dendrites_color = nmv.enums.Color.BASAL_DENDRITES

        # Apical dendrites color
        self.apical_dendrites_color = nmv.enums.Color.APICAL_DENDRITES

        # Spines color
        self.spines_color = nmv.enums.Color.SPINES

        # Nucleus color
        self.nucleus_color = nmv.enums.Color.NUCLEI

        # MESH RENDERING ###########################################################################
        # Camera view
        self.camera_view = nmv.enums.Camera.View.FRONT

        # Rendering view
        self.rendering_view = nmv.enums.Meshing.Rendering.View.MID_SHOT_VIEW

        # Image resolution is based on scale or to a fixed resolution
        self.resolution_basis = nmv.enums.Meshing.Rendering.Resolution.FIXED_RESOLUTION

        # Render a static frame of the mesh
        self.render = False

        # Render a 360 sequence of the reconstructed mesh
        self.render_360 = False

        # Full view image resolution
        self.full_view_resolution = nmv.consts.Image.FULL_VIEW_RESOLUTION

        # Close up image resolution
        self.close_up_resolution = nmv.consts.Image.CLOSE_UP_RESOLUTION

        # Close up view dimensions
        self.close_up_dimensions = nmv.consts.Image.CLOSE_UP_DIMENSIONS

        # The scale factor used to scale the morphology rendering frame, default 1.0
        self.resolution_scale_factor = 1.0

        # MESH EXPORT ##############################################################################
        # Save the reconstructed mesh as a .ply file to the output directory
        self.export_ply = False

        # Save the reconstructed mesh as a .obj file to the output directory
        self.export_obj = False

        # Save the reconstructed mesh as a .stl file to the output directory
        self.export_stl = False

        # Save the reconstructed mesh as a .blend file to the output directory
        self.export_blend = False

        # Export individual objects of the neurons to separate meshes
        self.export_individuals = False

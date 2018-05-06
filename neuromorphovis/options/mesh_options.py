####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
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

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2016 - 2018, Blue Brain Project / EPFL"
__credits__     = ["Ahmet Bilgili", "Juan Hernando", "Stefan Eilemann"]
__version__     = "1.0.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"


# Internal imports
import neuromorphovis as nmv 
import neuromorphovis.consts
import neuromorphovis.enums


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

        # This flag must be set to reconstruct a mesh
        self.reconstruct_neuron_mesh = False

        # Tessellate the mesh after the reconstruction
        self.tessellate_mesh = False

        # Tessellation level (between 0.1 and 1.0)
        self.tessellation_level = nmv.consts.Meshing.MAX_TESSELLATION_LEVEL

        # Fixing morphology artifacts
        self.fix_morphology_artifacts = True

        # Meshing technique
        self.meshing_technique = None

        # Attach spines to the neuron
        self.build_spines = False

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

        # Export in circuit coordinates, by default no unless there is a circuit file given
        self.global_coordinates = False

        # Morphology material
        self.material = nmv.enums.Shading.LAMBERT_WARD

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

        # Save the reconstructed mesh as a .ply file to the output directory
        self.export_ply = False

        # Save the reconstructed mesh as a .obj file to the output directory
        self.export_obj = False

        # Save the reconstructed mesh as a .stl file to the output directory
        self.export_stl = False

        # Save the reconstructed mesh as a .blend file to the output directory
        self.export_blend = False

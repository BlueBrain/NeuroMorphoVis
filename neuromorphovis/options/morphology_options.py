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
# @MorphologyOptions
####################################################################################################
class MorphologyOptions:
    """Configuration options for reconstructing a morphology skeleton.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        """Constructor
        """

        # This flag must be set to reconstruct the morphology
        self.reconstruct_morphology = False

        # Skeletonization algorithm, ORIGINAL by default
        self.skeleton = nmv.enums.Skeletonization.Skeleton.ORIGINAL

        # The GID of a given neuron in a given circuit using a blue config
        self.gid = None

        # The circuit
        self.blue_config = None

        # Morphology file path (if read from .H5 or .SWC file)
        self.morphology_file_path = None

        # Morphology file name (if read from .H5 or .SWC file)
        self.morphology_file_name = None

        # Morphology label (based on the GID or the morphology file name)
        self.label = None

        # Soma reconstruction technique (IGNORE, SPHERE, or REALISTIC by default)
        self.soma_representation = nmv.enums.Soma.Representation.REALISTIC

        # Branching of the morphologies in the connected modes, either based on angles or radii
        self.branching = nmv.enums.Skeletonization.Branching.ANGLES

        # Connect to soma
        self.connect_to_soma = False

        # Enable/Disable axon reconstruction
        self.ignore_axon = False

        # Enable/Disable basal dendrites reconstruction
        self.ignore_basal_dendrites = False

        # Enable/Disable apical dendrite reconstruction (if exists)
        self.ignore_apical_dendrite = False

        # Axon branching order
        self.axon_branch_order = nmv.consts.Arbors.MAX_BRANCHING_ORDER

        # Basal dendrites branching order
        self.basal_dendrites_branch_order = nmv.consts.Arbors.MAX_BRANCHING_ORDER

        # Apical dendrites branch order
        self.apical_dendrite_branch_order = nmv.consts.Arbors.MAX_BRANCHING_ORDER

        # Soma color
        self.soma_color = nmv.enums.Color.SOMA

        # Axon color
        self.axon_color = nmv.enums.Color.AXONS

        # Basal dendrites color
        self.basal_dendrites_color = nmv.enums.Color.BASAL_DENDRITES

        # Apical dendrites color
        self.apical_dendrites_color = nmv.enums.Color.APICAL_DENDRITES

        # Articulations color
        self.articulation_color = nmv.enums.Color.ARTICULATION

        # The radii of the sections (as specified in the morphology file, scaled with a given
        # scale factor, or constant at given fixed value)
        self.arbors_radii = nmv.enums.Skeletonization.ArborsRadii.AS_SPECIFIED

        # A scale factor for the radii of the sections
        self.sections_radii_scale = 1.0

        # A fixed and unified value for the radii of all the sections in the morphology
        self.sections_fixed_radii_value = 1.0

        # Number of sides of the bevel object used to scale the sections
        # This parameter controls the quality of the reconstructed morphology
        self.bevel_object_sides = nmv.consts.Meshing.BEVEL_OBJECT_SIDES

        # Selected a method to reconstruct the morphology
        self.reconstruction_method = nmv.enums.Skeletonization.Method.CONNECTED_SECTION_ORIGINAL

        # Morphology material
        self.material = nmv.enums.Shading.LAMBERT_WARD

        # Camera view
        self.camera_view = nmv.enums.Camera.View.FRONT

        # Rendering view
        self.rendering_view = nmv.enums.Skeletonization.Rendering.View.MID_SHOT_VIEW

        # Image resolution is based on scale or to a fixed resolution
        self.rendering_resolution = nmv.enums.Skeletonization.Rendering.Resolution.FIXED_RESOLUTION

        # Render a static frame of the morphology
        self.render = False

        # Render a 360 sequence of the reconstructed morphology
        self.render_360 = False

        # Progressive rendering of the morphology reconstruction (requires breadth first drawing)
        self.render_progressive = False

        # Full view image resolution
        self.full_view_resolution = nmv.consts.Image.FULL_VIEW_RESOLUTION

        # Close up image resolution
        self.close_up_resolution = nmv.consts.Image.CLOSE_UP_RESOLUTION

        # Close up view dimensions
        self.close_up_dimensions = nmv.consts.Image.CLOSE_UP_DIMENSIONS

        # The scale factor used to scale the morphology rendering frame, default 1.0
        self.resolution_scale_factor = 1.0

        # Export the morphology to .H5 file
        self.export_h5 = False

        # Export the morphology to .SWC file
        self.export_swc = False

        # Export the morphology skeleton to .BLEND file for rendering using tubes
        self.export_blend = False

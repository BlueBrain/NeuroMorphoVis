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

        # Arbor style
        self.arbor_style = nmv.enums.Arbors.Style.ORIGINAL

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

        # The arbors connectivity to the soma
        self.arbors_to_soma_connection = nmv.enums.Arbors.Roots.ALL_CONNECTED_TO_ORIGIN

        # Enable/Disable axon reconstruction
        self.ignore_axon = False

        # Enable/Disable basal dendrites reconstruction
        self.ignore_basal_dendrites = False

        # Enable/Disable apical dendrite reconstruction (if exists)
        self.ignore_apical_dendrite = False

        # Axon branching order
        self.axon_branch_order = nmv.consts.Arbors.AXON_DEFAULT_BRANCHING_ORDER

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

        # Threshold radius, where any section with lower radius values will not drawn
        self.threshold_radius = 100000

        # Global coordinates
        self.global_coordinates = False

        # Number of sides of the bevel object used to scale the sections
        # This parameter controls the quality of the reconstructed morphology
        self.bevel_object_sides = nmv.consts.Meshing.BEVEL_OBJECT_SIDES

        # Selected a method to reconstruct the morphology
        self.reconstruction_method = nmv.enums.Skeletonization.Method.DISCONNECTED_SECTIONS

        # Morphology material
        self.material = nmv.enums.Shading.LAMBERT_WARD

        # SKELETON RENDERING #######################################################################
        # Camera view
        self.camera_view = nmv.enums.Camera.View.FRONT

        # Rendering view
        self.rendering_view = nmv.enums.Skeletonization.Rendering.View.MID_SHOT_VIEW

        # Image resolution is based on scale or to a fixed resolution
        self.resolution_basis = nmv.enums.Skeletonization.Rendering.Resolution.FIXED_RESOLUTION

        # Render a static frame of the skeleton
        self.render = False

        # Render a 360 sequence of the reconstructed skeleton
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

    ################################################################################################
    # @set_default
    ################################################################################################
    def set_default(self):
        """Sets the default options for duplicated objects.
        """

        # Skeletonization algorithm, ORIGINAL by default
        self.skeleton = nmv.enums.Skeletonization.Skeleton.ORIGINAL

        # Arbor style
        self.arbor_style = nmv.enums.Arbors.Style.ORIGINAL

        # Soma reconstruction technique (IGNORE, SPHERE, or REALISTIC by default)
        self.soma_representation = nmv.enums.Soma.Representation.SPHERE

        # Branching of the morphologies in the connected modes, either based on angles or radii
        self.branching = nmv.enums.Skeletonization.Branching.RADII

        # The arbors connectivity to the soma
        self.arbors_to_soma_connection = nmv.enums.Arbors.Roots.ALL_CONNECTED_TO_ORIGIN

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

        # Threshold radius, where any section with lower radius values will not drawn
        self.threshold_radius = 100000

        # Global coordinates
        self.global_coordinates = False

        # Number of sides of the bevel object used to scale the sections
        # This parameter controls the quality of the reconstructed morphology
        self.bevel_object_sides = nmv.consts.Meshing.BEVEL_OBJECT_SIDES

        # Selected a method to reconstruct the morphology
        self.reconstruction_method = nmv.enums.Skeletonization.Method.DISCONNECTED_SECTIONS

        # Morphology material
        self.material = nmv.enums.Shading.LAMBERT_WARD
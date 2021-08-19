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

# Internal imports
import nmv.consts
import nmv.enums


####################################################################################################
# @RenderingOptions
####################################################################################################
class RenderingOptions:
    """Rendering options.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        """Constructor
        """

        # Render a static frame of the morphology
        self.render_morphology_static_frame = False

        # Render a 360 sequence of the morphology
        self.render_morphology_360 = False

        # Progressive rendering
        self.render_morphology_progressive = False

        # Render a static frame of the mesh
        self.render_mesh_static_frame = False

        # Render a 360 sequence of the mesh
        self.render_mesh_360 = False

        # Render a static frame of the soma
        self.render_soma_static_frame = False

        # Render a 360 sequence of the soma
        self.render_soma_360 = False

        # Progressive rendering of the soma
        self.render_soma_progressive = False

        # Camera view
        self.camera_view = nmv.enums.Camera.View.FRONT

        # Rendering view
        self.rendering_view = nmv.enums.Rendering.View.MID_SHOT

        # Image resolution is based on scale or to a fixed resolution
        self.resolution_basis = nmv.enums.Rendering.Resolution.FIXED

        # Full view image resolution
        self.frame_resolution = nmv.consts.Image.FULL_VIEW_RESOLUTION

        # Close up image resolution
        self.close_up_resolution = nmv.consts.Image.CLOSE_UP_RESOLUTION

        # Close up view dimensions
        self.close_up_dimensions = nmv.consts.Image.CLOSE_UP_DIMENSIONS

        # The scale factor used to scale the frame, default 1.0
        self.resolution_scale_factor = nmv.consts.Image.DEFAULT_IMAGE_SCALE_FACTOR

        # Image extension
        self.image_format = nmv.enums.Image.Extension.PNG

        # Scale bar
        self.render_scale_bar = False



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
import neuromorphovis.enums
import neuromorphovis.rendering


####################################################################################################
# @NeuronSkeletonRenderer
####################################################################################################
class NeuronSkeletonRenderer:
    """A simple factory for rendering reconstructed neuronal skeletons."""

    ################################################################################################
    # @SomaRenderer
    ################################################################################################
    def __init__(self):
        pass

    ################################################################################################
    # @render
    ################################################################################################
    @staticmethod
    def render(bounding_box,
               camera_view=nmv.enums.Camera.View.FRONT,
               image_resolution=512,
               image_name='SKELETON',
               image_directory=None,
               keep_camera_in_scene=False):
        """Render the morphology skeleton to a .PNG image.

        :param bounding_box:
            The bounding box of the view requested to be rendered.
        :param camera_view:
            The view of the camera, by default FRONT.
        :param image_resolution:
            The resolution of the image, by default 512.
        :param image_name:
            The name of the image, by default 'SKELETON'.
        :param image_directory:
            The directory where the image will be rendered. If the directory is set to None,
            then the prefix is included in @image_name.
        :param keep_camera_in_scene:
            Keep the camera used to do the rendering after the rendering is done.
        """

        # Create a camera
        skeleton_camera = nmv.rendering.Camera('MorphologyCamera_%s' % camera_view)

        # Image path prefix, i.e. w/o extension which will be added later
        image_prefix = \
            '%s/%s' % (image_directory, image_name) if image_directory is not None else image_name

        # Render an image
        skeleton_camera.render_scene(bounding_box=bounding_box, camera_view=camera_view,
            image_resolution=image_resolution, image_name=image_prefix,
            keep_camera_in_scene=keep_camera_in_scene)

    ################################################################################################
    # @render
    ################################################################################################
    @staticmethod
    def render_at_angle(morphology_objects,
                        angle,
                        bounding_box,
                        camera_view=nmv.enums.Camera.View.FRONT,
                        image_resolution=512,
                        image_name='SKELETON',
                        image_directory=None):
        """Render the morphology skeleton to a .PNG image at a specific angle.

        :param morphology_objects:
            A list of all the objects that belong to the reconstructed morphology.
        :param angle:
            The angle the frame will be rendered at.
        :param bounding_box:
            The bounding box of the view requested to be rendered.
        :param camera_view:
            The view of the camera, by default FRONT.
        :param image_resolution:
            The resolution of the image, by default 512.
        :param image_name:
            The name of the image, by default 'SKELETON'.
        :param image_directory:
            The directory where the image will be rendered. If the directory is set to None,
            then the prefix is included in @image_name.
        """

        # Rotate all the objects as if they are a single object
        for morphology_object in morphology_objects:

            # Rotate the soma mesh around the y axis
            morphology_object.rotation_euler[1] = angle * 2 * 3.14 / 360.0

        nmv.rendering.NeuronSkeletonRenderer.render(
            bounding_box=bounding_box, camera_view=camera_view,
            image_resolution=image_resolution, image_name=image_name)

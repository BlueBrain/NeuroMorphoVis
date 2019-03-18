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
import nmv.bbox
import nmv.enums


####################################################################################################
# @SomaRenderer
####################################################################################################
class SomaRenderer:
    """A simple factory for rendering reconstructed somata meshes."""

    ################################################################################################
    # @SomaRenderer
    ################################################################################################
    def __init__(self):
        pass

    ################################################################################################
    # @render
    ################################################################################################
    @staticmethod
    def render(view_extent=25.0,
               camera_view=nmv.enums.Camera.View.FRONT,
               image_resolution=512,
               image_name='SOMA',
               image_directory=None,
               keep_camera_in_scene=False):
        """Render the soma to a .PNG image.

        :param view_extent:
            The extent of the view, by default 25.0 microns.
        :param camera_view:
            The view of the camera, by default FRONT.
        :param image_resolution:
            The resolution of the image, by default 512.
        :param image_name:
            The name of the image, by default 'SOMA'.
        :param image_directory:
            The directory where the image will be rendered. If the directory is set to None,
            then the prefix is included in @image_name.
        :param keep_camera_in_scene:
            Keep the camera used to do the rendering after the rendering is done.
        """

        # Compute the bounding box for the extent
        bounding_box = nmv.bbox.compute_unified_extent_bounding_box(extent=view_extent)

        # Create a camera
        soma_camera = nmv.rendering.Camera('SomaCamera_%s' % camera_view)

        # Image path prefix, i.e. w/o extension which will be added later
        image_prefix = \
            '%s/%s' % (image_directory, image_name) if image_directory is not None else image_name

        # Render an image
        soma_camera.render_scene(
            bounding_box=bounding_box, camera_view=camera_view, image_resolution=image_resolution,
            image_name=image_prefix, keep_camera_in_scene=keep_camera_in_scene)

    ################################################################################################
    # @render_scene_object
    ################################################################################################
    @staticmethod
    def render_at_angle(soma_mesh,
                        angle=0.0,
                        view_extent=25.0,
                        camera_view=nmv.enums.Camera.View.FRONT,
                        image_resolution=512,
                        image_name='SOMA',
                        image_directory=None):
        """Render the soma mesh at a specific angle.

        :param soma_mesh:
            A reference to the reconstructed soma mesh.
        :param angle:
            The orientation of the reconstructed soma mesh.
        :param view_extent:
            The extent of the view, by default 25.0 microns.
        :param camera_view:
            The view of the camera, by default FRONT.
        :param image_resolution:
            The resolution of the image, by default 512.
        :param image_name:
            The name of the image, by default 'SOMA'.
        :param image_directory:
            The directory where the image will be rendered. If the directory is set to None,
            then the prefix is included in @image_name.
        """

        # Rotate the soma mesh around the y axis
        soma_mesh.rotation_euler[1] = angle * 2 * 3.14 / 360.0

        # Render a frame while the soma mesh is at this specific angle
        SomaRenderer.render(view_extent=view_extent,
                            camera_view=camera_view,
                            image_resolution=image_resolution,
                            image_name=image_name,
                            image_directory=image_directory)


####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
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
import nmv.rendering


################################################################################################
# @render
################################################################################################
def render(bounding_box,
           camera_view=nmv.enums.Camera.View.FRONT,
           image_resolution=nmv.consts.Image.DEFAULT_RESOLUTION,
           image_name='image',
           image_format=nmv.enums.Image.Extension.PNG,
           image_directory=None,
           keep_camera_in_scene=False):
    """Render a scene within a given bounding box to an image.

    :param bounding_box:
        The bounding box of the view requested to be rendered.
    :param camera_view:
        The view of the camera, by default FRONT.
    :param image_resolution:
        The resolution of the image, by default 1024.
    :param image_name:
        The name of the image, by default 'image'.
    :param image_format:
        The file format of the image.
    :param image_directory:
        The directory where the image will be rendered. If the directory is set to None,
        then the prefix is included in @image_name.
    :param keep_camera_in_scene:
        Keep the camera used to do the rendering after the rendering is done.
    """

    # Create a camera
    skeleton_camera = nmv.rendering.Camera('nmvCamera_%s' % camera_view)

    # Image path prefix, i.e. w/o extension which will be added later
    image_prefix = \
        '%s/%s' % (image_directory, image_name) if image_directory is not None else image_name

    # Render an image
    skeleton_camera.render_scene(bounding_box=bounding_box,
                                 camera_view=camera_view,
                                 image_resolution=image_resolution,
                                 image_name=image_prefix,
                                 image_format=image_format,
                                 keep_camera_in_scene=keep_camera_in_scene)


################################################################################################
# @render_to_scale
################################################################################################
def render_to_scale(bounding_box,
                    camera_view=nmv.enums.Camera.View.FRONT,
                    image_scale_factor=nmv.consts.Image.DEFAULT_IMAGE_SCALE_FACTOR,
                    image_name='image',
                    image_format=nmv.enums.Image.Extension.PNG,
                    image_directory=None,
                    keep_camera_in_scene=False):
    """Render a scene within a given bounding box to scale.

    :param bounding_box:
        The bounding box of the view requested to be rendered.
    :param camera_view:
        The view of the camera, by default FRONT.
    :param image_scale_factor:
        The factor used to scale the resolution of the image the image, by default 1.
    :param image_name:
        The name of the image, by default 'image'.
    :param image_format:
        The file format of the image.
    :param image_directory:
        The directory where the image will be rendered. If the directory is set to None,
        then the prefix is included in @image_name.
    :param keep_camera_in_scene:
        Keep the camera used to do the rendering after the rendering is done.
    """

    # Create a camera
    skeleton_camera = nmv.rendering.Camera('MeshCamera_%s' % camera_view)

    # Image path prefix, i.e. w/o extension which will be added later
    image_prefix = '%s/%s' % (
        image_directory, image_name) if image_directory is not None else image_name

    # Render an image
    skeleton_camera.render_scene_to_scale(bounding_box=bounding_box,
                                          camera_view=camera_view,
                                          scale_factor=image_scale_factor,
                                          image_name=image_prefix,
                                          image_format=image_format,
                                          keep_camera_in_scene=keep_camera_in_scene)


################################################################################################
# @render_at_angle
################################################################################################
def render_at_angle(scene_objects,
                    angle,
                    bounding_box,
                    camera_view=nmv.enums.Camera.View.FRONT_360,
                    image_resolution=512,
                    image_name='image',
                    image_directory=None):
    """Render the mesh to a .PNG image at a specific angle.
    :param scene_objects:
        A list of all the objects that belong to the reconstructed mesh.
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
    for scene_object in scene_objects:

        # Rotate the mesh object around the y axis
        scene_object.rotation_euler[1] = angle * 2 * 3.14 / 360.0

    # Render the image
    render(bounding_box=bounding_box, camera_view=camera_view, image_resolution=image_resolution,
           image_name=image_name)


################################################################################################
# @render_at_angle_to_scale
################################################################################################
def render_at_angle_to_scale(scene_object,
                             angle,
                             bounding_box,
                             camera_view=nmv.enums.Camera.View.FRONT_360,
                             image_scale_factor=nmv.consts.Image.DEFAULT_IMAGE_SCALE_FACTOR,
                             image_name='image',
                             image_directory=None):
    """Render the mesh to a .PNG image at a specific angle.
    :param mesh_objects:
        A list of all the objects that belong to the reconstructed mesh.
    :param angle:
        The angle the frame will be rendered at.
    :param bounding_box:
        The bounding box of the view requested to be rendered.
    :param camera_view:
        The view of the camera, by default FRONT.
    :param image_scale_factor:
        The factor used to scale the resolution of the image the image, by default 1.
    :param image_name:
        The name of the image, by default 'SKELETON'.
    :param image_directory:
        The directory where the image will be rendered. If the directory is set to None,
        then the prefix is included in @image_name.
    """

    # Rotate all the objects as if they are a single object
    for scene_object in scene_object:

        # Rotate the mesh object around the y axis
        scene_object.rotation_euler[1] = angle * 2 * 3.14 / 360.0

    # Render the image to scale
    render_to_scale(bounding_box=bounding_box,
                    camera_view=camera_view,
                    image_scale_factor=image_scale_factor,
                    image_name=image_name)
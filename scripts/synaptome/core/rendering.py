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

# Blender
from mathutils import Vector

# Internal imports
import nmv.bbox
import nmv.consts
import nmv.enums
import nmv.rendering
import nmv.scene


####################################################################################################
# @render_image
####################################################################################################
def render_image(output_directory,
                 image_name,
                 resolution):
    """Render an image of the synaptome.

    :param image_name:
        The label of the image.
    :param output_directory:
        The output directory where the images will be created.
    :param resolution:
        The base resolution of the image.
    """

    # Images directory
    images_directory = output_directory + '/images'

    # Create the images directory if it does not exist
    if not nmv.file.ops.path_exists(images_directory):
        nmv.file.ops.clean_and_create_directory(images_directory)

    # Get the bounding box
    bounding_box = nmv.bbox.compute_scene_bounding_box_for_meshes()

    # Render the image
    nmv.rendering.render(
        bounding_box=bounding_box,
        image_resolution=resolution,
        image_name=image_name,
        image_directory=images_directory)


####################################################################################################
# @render_360
####################################################################################################
def render_360(output_directory,
               label,
               resolution):
    """Renders a 360 of the synaptome.

    :param label:
        label
    :param output_directory:
        The output directory where the frames and final movie will be generated.
    :param resolution:
        The base resolution of the video frames.
    """

    # The directory where the frames will be rendered
    frames_directory = output_directory + '/%s_synaptome_360_frames' % label

    # Create the images directory if it does not exist
    if not nmv.file.ops.path_exists(frames_directory):
        nmv.file.ops.clean_and_create_directory(frames_directory)

    # Get a list of all the meshes in the scene
    scene_objects = nmv.scene.get_list_of_meshes_in_scene()

    # Compute the bounding box
    rendering_bbox = nmv.bbox.compute_scene_bounding_box_for_meshes()
    bounding_box_360 = nmv.bbox.compute_360_bounding_box(
        rendering_bbox, Vector((0, 0, 0)))

    # Stretch the bounding box by few microns
    bounding_box_360.extend_bbox_uniformly(delta=nmv.consts.Image.GAP_DELTA)

    # Render the image
    for i in range(360):

        # Set the frame name
        image_name = '%s/%s' % (frames_directory, '{0:05d}'.format(i))

        nmv.rendering.renderer.render_at_angle(
            scene_objects=scene_objects,
            angle=i,
            bounding_box=bounding_box_360,
            camera_view=nmv.enums.Camera.View.FRONT_360,
            image_resolution=resolution,
            image_name=image_name)

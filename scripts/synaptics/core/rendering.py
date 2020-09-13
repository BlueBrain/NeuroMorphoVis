####################################################################################################
# Copyright (c) 2020, EPFL / Blue Brain Project
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

# System imports
import os
from PIL import Image

# Blender
from mathutils import Vector

# Internal imports
import nmv.bbox
import nmv.consts
import nmv.enums
import nmv.rendering
import nmv.scene
import nmv.file


####################################################################################################
# @render_image
####################################################################################################
def scale_frame(input_frame,
                desired_base_resolution,
                output_directory=None):
    """Scales or resizes an input frame to a new one with a given base resolution.

    :param input_frame:
        The input frame or image to be resized.
    :param output_directory:
        The output directory where the resized frame will be generated to.
    :param desired_base_resolution:
        The base (largest) resolution of the scaled image.
    :return:
        A reference to the resized frame
    """

    # Open the original frame
    original_frame = Image.open(input_frame)

    # Get the dimensions to compute the scaling factor
    aspect_ratio = (1.0 * original_frame.width) / (1.0 * original_frame.height)

    # Compute the new dimensions of the image
    if aspect_ratio > 1.0:
        new_width = desired_base_resolution
        new_height = int(1.0 * desired_base_resolution / aspect_ratio)
    else:
        new_width = int(desired_base_resolution * aspect_ratio)
        new_height = desired_base_resolution

    # Resize the frame
    resized_frame = original_frame.resize(size=(new_width, new_height))

    # Close the original frame
    original_frame.close()

    # Get the name of the frame
    if output_directory is not None:
        resized_frame.save('%s/%s' % (output_directory, os.path.basename(input_frame)))

    # Return a reference to the resized frame
    return resized_frame


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

    # Create the images directory if it does not exist
    if not nmv.file.ops.path_exists(output_directory):
        nmv.file.ops.clean_and_create_directory(output_directory)

    # Get the bounding box
    bounding_box = nmv.bbox.compute_scene_bounding_box_for_curves_and_meshes()

    # Render the image
    for view in [nmv.enums.Camera.View.FRONT]:
        image_name_with_view = image_name + '_%s' % view
        nmv.rendering.render(
            camera_view=view,
            bounding_box=bounding_box,
            image_resolution=resolution,
            image_name=image_name_with_view,
            image_directory=output_directory)


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
    :return
        A list of all the raw frames that were rendered for the synaptomes.
    """

    # The directory where the original frames will be rendered
    original_frames_directory = output_directory + '/%s_360' % label

    # Create the images directory if it does not exist
    if not nmv.file.ops.path_exists(original_frames_directory):
        nmv.file.ops.clean_and_create_directory(original_frames_directory)

    # The directory where the resized frames will be rendered
    scaled_frames_directory = output_directory + '/%s_360_scaled' % label

    # Create the images directory if it does not exist
    if not nmv.file.ops.path_exists(scaled_frames_directory):
        nmv.file.ops.clean_and_create_directory(scaled_frames_directory)

    # Get a list of all the meshes in the scene
    scene_objects = nmv.scene.get_list_of_meshes_in_scene()

    # Compute the bounding box
    rendering_bbox = nmv.bbox.compute_scene_bounding_box_for_meshes()
    bounding_box_360 = nmv.bbox.compute_360_bounding_box(
        rendering_bbox, Vector((0, 0, 0)))

    # Stretch the bounding box by few microns
    bounding_box_360.extend_bbox_uniformly(delta=nmv.consts.Image.GAP_DELTA)

    # Render the sequence
    frames = list()
    for i in range(360):

        # Set the frame name
        frame_name = '%s/%s' % (original_frames_directory, '{0:05d}'.format(i))

        # Render the frame
        nmv.rendering.renderer.render_at_angle(
            scene_objects=scene_objects,
            angle=i,
            bounding_box=bounding_box_360,
            camera_view=nmv.enums.Camera.View.FRONT_360,
            image_resolution=resolution,
            image_name=frame_name)

        # Add the frame to the list
        frames.append('%s.png' % frame_name)

    # Return a list of frames
    return frames


####################################################################################################
# @add_background_and_360_to_raw_frames
####################################################################################################
def add_background_and_360_to_raw_frames(raw_frames_list,
                                         background_image_file,
                                         rotation_frames_directory):
    """Add the background image and the 360 legend to the frames.

    :param raw_frames_list:
        A list of the raw frames.
    :param background_image_file:
        The background image.
    :param rotation_frames_directory:
        The directory that contains the 360 frames of the legend.
    """

    for i, frame in enumerate(raw_frames_list):
        print(frame)

        # Scale the frame
        synaptome_frame = scale_frame(input_frame=frame, desired_base_resolution=1000)

        # Rotation file
        rotation_image_path = '%s/%s' % (rotation_frames_directory, os.path.basename(frame))

        # Background image
        background_image = Image.open(background_image_file)

        # Rotation image
        rotation_image = Image.open(rotation_image_path)
        rotation_image = rotation_image.resize(size=(250, 250))
        background_image.paste(rotation_image, (10, 560 - 125), rotation_image)

        # Create a new frame that is transparent and add it to the background
        transparent_frame = Image.new('RGBA',
                                      (synaptome_frame.width - 100, synaptome_frame.height - 100),
                                      (255, 255, 255, 10))

        # Overlay the transparent frame
        if transparent_frame.width > transparent_frame.height:
            x = 880 + 50
            y = 40 + int((1000 - transparent_frame.height) / 2.0)
        else:
            x = 880 + 40 + int((1000 - transparent_frame.width) / 2.0)
            y = 40 + 50
        #background_image.paste(transparent_frame, (x, y), transparent_frame)

        # Overlay the original image over the background image
        if synaptome_frame.width > synaptome_frame.height:
            x = 880
            y = 40 + int((1000 - synaptome_frame.height) / 2.0)
        else:
            x = 880 + 40 + int((1000 - synaptome_frame.width) / 2.0)
            y = 40
        background_image.paste(synaptome_frame, (x, y), synaptome_frame)

        # Save the final image
        background_image.save(frame)
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
import ntpath
import copy
from PIL import Image, ImageOps, ImageDraw, ImageFont

# Blender
import bpy
from mathutils import Vector

# Internal imports
import nmv.bbox
import nmv.consts
import nmv.enums
import nmv.rendering
import nmv.scene
import nmv.file
import nmv.utilities


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
    view = nmv.enums.Camera.View.FRONT
    image_name_with_view = image_name + '_%s' % view
    nmv.rendering.render(
        camera_view=view,
        bounding_box=bounding_box,
        image_resolution=resolution,
        image_name=image_name_with_view,
        image_directory=output_directory)

    # Return the image name for compositing
    return '%s/%s.png' % (output_directory, image_name_with_view)


####################################################################################################
# @render_close_up
####################################################################################################
def render_close_up(close_up_mesh,
                    image_name):

    # Use the denoiser
    bpy.context.scene.view_layers[0].cycles.use_denoising = True

    bpy.context.scene.render.resolution_x = 1000
    bpy.context.scene.render.resolution_y = 2000

    # Create the camera
    camera_object = nmv.rendering.Camera('CloseupCamera')
    camera = camera_object.create_base_camera()

    # Select the close-up mesh
    nmv.scene.select_object(close_up_mesh)
    nmv.scene.set_active_object(close_up_mesh)

    # Set the camera to orthographic
    camera.data.type = 'ORTHO'

    # Activate the camera
    bpy.context.scene.camera = bpy.data.objects["CloseupCamera"]

    # Focus the view on the close-up mesh
    bpy.ops.view3d.camera_to_view_selected()

    # Avoid chopping
    camera.location[2] = 0

    # Adjust the ortho scale to get a bigger FOV
    camera.data.ortho_scale = camera.data.ortho_scale * 4

    # Adjust the clipping plane
    camera.data.clip_end = 100000

    # Set the image file name
    bpy.data.scenes['Scene'].render.filepath = '%s.png' % image_name

    # Transparent
    nmv.scene.set_transparent_background()

    # Render the image
    bpy.ops.render.render(write_still=True)

    # Turn off the denoiser for the huge images to avoid crappy rendering times
    bpy.context.scene.view_layers[0].cycles.use_denoising = False

    # Return the image name for the compositing
    return '%s.png' % image_name


####################################################################################################
# @render_synaptome_close_up_on_soma_360
####################################################################################################
def render_synaptome_close_up_on_soma_360(output_directory,
                                          label,
                                          close_up_size,
                                          resolution=2000):

    # Adjust shading
    bpy.context.scene.display.shading.light = 'STUDIO'
    bpy.context.scene.display.shading.studio_light = 'outdoor.sl'

    # The directory where the original frames will be rendered
    frames_directory = output_directory + '/%s_close_up_360' % label

    # Create the images directory if it does not exist
    if not nmv.file.ops.path_exists(frames_directory):
        nmv.file.ops.clean_and_create_directory(frames_directory)

    # Adjust the resolution
    bpy.context.scene.render.resolution_x = int (0.5 * resolution)
    bpy.context.scene.render.resolution_y = resolution

    # Create the camera
    camera_object = nmv.rendering.Camera('CloseupCamera')
    camera = camera_object.create_base_camera()

    # Activate the camera
    bpy.context.scene.camera = bpy.data.objects["CloseupCamera"]

    # Adjust the ortho scale to get a bigger FOV
    camera.data.ortho_scale = close_up_size

    # Adjust the clipping plane
    camera.data.clip_end = 100000

    # Avoid chopping
    camera.location[2] = 500

    # Get a list of all the meshes in the scene
    scene_objects = nmv.scene.get_list_of_meshes_in_scene()

    # Render the sequence
    frames = list()
    for i in range(360):

        # Rotate all the objects as if they are a single object
        for scene_object in scene_objects:
            # Rotate the mesh object around the y axis
            scene_object.rotation_euler[1] = i * 2 * 3.14 / 360.0

        # Set the frame name
        frame_name = '%s/%s' % (frames_directory, '{0:05d}'.format(i))

        # Set the image file name
        bpy.data.scenes['Scene'].render.filepath = '%s.png' % frame_name

        # Render the image
        bpy.ops.render.render(write_still=True)

        # Add the frame to the list
        frames.append('%s.png' % frame_name)

    # Return the list of frames
    return frames


####################################################################################################
# @render_synaptome_full_view_360
####################################################################################################
def render_synaptome_full_view_360(output_directory,
                                   label,
                                   resolution):
    """Renders a 360 of the synaptome full view.

    :param label:
        label
    :param output_directory:
        The output directory where the frames and final movie will be generated.
    :param resolution:
        The base resolution of the video frames.
    :return
        A list of all the raw frames that were rendered for the synaptomes.
    """

    bpy.context.scene.display.shading.light = 'STUDIO'
    bpy.context.scene.display.shading.studio_light = 'outdoor.sl'

    # The directory where the original frames will be rendered
    frames_directory = output_directory + '/%s_full_view_360' % label

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

    # Render the sequence
    frames = list()
    for i in range(360):

        # Set the frame name
        frame_name = '%s/%s' % (frames_directory, '{0:05d}'.format(i))

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
# @compose_frame
####################################################################################################
def compose_frame(full_view_file,
                  close_up_file,
                  background_image_file,
                  output_directory,
                  edge_gap=100,
                  close_up_frame_border_thickness=2,
                  full_view_to_close_up_ratio=0.6,
                  bounding_box=None):
    """Composite the final frame with the full view image and the close-up image on the
    final background.

    :param full_view_file:
        The path to the full view file.
    :param close_up_file:
        The path to the close up file.
    :param background_image_file:
        The path to the background image
    :param output_directory:
        The output directory of the project.
    :param edge_gap:
        The edge gap for the sides of the frame.
    :param close_up_frame_border_thickness:
        The border thickness of the close-up image.
    :param full_view_to_close_up_ratio:
        The ratio between the full-view image to the close-up image in the frame.
    """

    # Open the background image
    background_image = Image.open(background_image_file)

    # Open the full view image
    full_view_image = Image.open(full_view_file)

    # Open the close-up image
    close_up_image = Image.open(close_up_file)

    # Add a frame to the close-up image
    close_up_image = ImageOps.expand(
        close_up_image, border=close_up_frame_border_thickness, fill='white')

    # Get the size of the background image
    background_width, background_height = background_image.size

    # Widths in pixels for the full view area and the close-up one
    full_view_area_width = int(background_width * full_view_to_close_up_ratio)
    close_up_area_width = background_width - full_view_area_width

    # The drawing areas, where the final images are drawn should consider the edge gap
    full_view_drawing_width = int(full_view_area_width - (edge_gap * 2))
    full_view_drawing_height = int(background_height - (edge_gap * 2))

    # Scale the full view image to fit within the drawing area
    full_view_image_width, full_view_image_height = full_view_image.size
    full_view_aspect_ratio = (1.0 * full_view_image_width) / (1.0 * full_view_image_height)
    if full_view_aspect_ratio > 1.0:
        scale = (1.0 * full_view_image_width) / (1.0 * full_view_drawing_width)
        resized_image_width = full_view_drawing_width
        resized_image_height = int(full_view_image_height / scale)
    else:
        scale = (1.0 * full_view_image_height) / (1.0 * full_view_drawing_height)
        resized_image_height = full_view_drawing_height
        resized_image_width = int(full_view_image_width / scale)

    # The final full-view image is ready to be pasted to the background frame
    full_view_resized_image = full_view_image.resize((
            resized_image_width, resized_image_height), Image.BICUBIC)

    # Calculate the starting x and y pixels where the pasting will happen
    full_view_delta_x = int((full_view_drawing_width - full_view_resized_image.size[0]) * 0.5)
    full_view_delta_y = int((full_view_drawing_height - full_view_resized_image.size[1]) * 0.5)
    full_view_starting_x = edge_gap + full_view_delta_x
    full_view_starting_y = edge_gap + full_view_delta_y

    # Paste the full view image to the background image
    background_image.paste(full_view_resized_image, (full_view_starting_x, full_view_starting_y),
                           full_view_resized_image)

    # Compute the scale bar
    if bounding_box is not None:
        full_view_image_width = full_view_resized_image.size[1]
        synaptome_width = bounding_box.bounds[0]
        width_per_pixel = (1.0 * full_view_image_width) / (1.0 * synaptome_width)

        graphic = ImageDraw.Draw(background_image)
        graphic.line((edge_gap, full_view_starting_y + full_view_drawing_height,
                      edge_gap + 83, full_view_starting_y + full_view_drawing_height),
                     fill=(255, 255, 255, 255))

        font = ImageFont.truetype('%s/font.ttf' % os.path.dirname(os.path.realpath(__file__)), 25)
        graphic.text((edge_gap, full_view_starting_y + full_view_drawing_height + 5),
                     "%d µm" % int(width_per_pixel * 83), font=font, fill=(255, 255, 255, 128))

    # The drawing areas, where the final images are drawn should consider the edge gap
    close_up_drawing_width = int(close_up_area_width - (edge_gap * 2))
    close_up_drawing_height = int(background_height - (edge_gap * 2))

    # Scale the close-up image to fit within the drawing area
    close_up_image_width, close_up_image_height = close_up_image.size
    close_up_image_aspect_ratio = (1.0 * close_up_image_width) / (1.0 * close_up_image_height)
    if close_up_image_aspect_ratio < 1.0:
        scale = (1.0 * close_up_image_height) / (1.0 * close_up_drawing_height)
        resized_image_height = close_up_drawing_height
        resized_image_width = int(close_up_image_width / scale)
    else:
        scale = (1.0 * close_up_image_width) / (1.0 * close_up_drawing_width)
        resized_image_width = close_up_drawing_width
        resized_image_height = int(close_up_drawing_height / scale)

    # The final close-up image that will be pasted on the background frame
    close_up_resized_image = close_up_image.resize(
            (resized_image_width, resized_image_height), Image.BICUBIC)

    # Calculate the starting x and y pixels where the pasting will happen
    close_up_image_delta_x = int((close_up_drawing_width - close_up_resized_image.size[0]) * 0.5)
    close_up_image_delta_y = int((close_up_drawing_height - close_up_resized_image.size[1]) * 0.5)
    close_up_starting_x = full_view_area_width + edge_gap + close_up_image_delta_x
    close_up_starting_y = edge_gap + close_up_image_delta_y

    # Paste the close-up image to the background image
    background_image.paste(close_up_resized_image, (close_up_starting_x, close_up_starting_y),
                           close_up_resized_image)

    # Save the background image with the new data
    background_image.save('%s/%s' % (output_directory, ntpath.basename(full_view_file)))

    # Close all the images
    background_image.close()
    full_view_image.close()
    close_up_image.close()


def compose_360_frames(full_view_frames,
                       close_up_frames,
                       background_image_file,
                       output_directory,
                       edge_gap=100,
                       close_up_frame_border_thickness=2,
                       full_view_to_close_up_ratio=0.6,
                       bounding_box=None):

    # The directory where the original frames will be rendered
    original_frames_directory = output_directory + '/composite'

    # Create the images directory if it does not exist
    if not nmv.file.ops.path_exists(original_frames_directory):
        nmv.file.ops.clean_and_create_directory(original_frames_directory)

    for i in range(len(full_view_frames)):

        full_view_frame = full_view_frames[i]
        close_up_frame = close_up_frames[i]

        compose_frame(full_view_file=full_view_frame,
                      close_up_file=close_up_frame,
                      background_image_file=background_image_file,
                      output_directory=original_frames_directory,
                      bounding_box=bounding_box)


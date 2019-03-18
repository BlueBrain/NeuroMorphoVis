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

# Blender imports
import bpy
from mathutils import Vector

# Internal imports
import nmv
import nmv.bbox
import nmv.scene
import nmv.camera


####################################################################################################
# @render_scene_at_resolution
####################################################################################################
def render_scene_at_resolution(file_name='image',
                               film_base_resolution=512,
                               view='FRONT'):
    """Render the current scene to an image at a given resolution.

    :param file_name:
        The output name of the rendered image.
    :param film_base_resolution:
        The 'base' resolution of the image.
    :param view:
        The rendering view.
    """

    # Deselect all the object
    nmv.scene.ops.deselect_all()

    # Set camera location and target based on the selected view to render the images
    scene_bounding_box = nmv.bbox.compute_scene_bounding_box()
    center = scene_bounding_box.center
    camera_x = scene_bounding_box.p_max[0] + scene_bounding_box.bounds[0]
    camera_y = scene_bounding_box.p_max[1] + scene_bounding_box.bounds[1]
    camera_z = scene_bounding_box.p_max[2] + scene_bounding_box.bounds[2]

    camera_location_x = Vector((camera_x, center.y, center.z))
    camera_location_y = Vector((center.x, camera_y, center.z))
    camera_location_z = Vector((center.x, center.y, camera_z))

    # Add a camera object at the camera location
    camera_object = None

    # Front view
    if view == 'FRONT':

        # Add a camera along the z-axis
        camera_object = nmv.rendering.camera.create_default_camera(location=camera_location_z)

        # Rotate the camera
        nmv.camera.ops.rotate_camera_for_front_view(camera_object=camera_object)

    # Side view
    elif view == 'SIDE':

        # Add a camera along the x-axis
        camera_object = nmv.rendering.camera.create_default_camera(location=camera_location_x)

        # Rotate the camera
        nmv.camera.ops.rotate_camera_for_side_view(camera_object=camera_object)

    # Top view
    elif view == 'TOP':

        # Add a camera along the y-axis
        camera_object = nmv.camera.create_default_camera(location=camera_location_y)

        # Rotate the camera
        nmv.camera.ops.rotate_camera_for_top_view(camera_object=camera_object)

    # Update the camera resolution
    nmv.camera.ops.set_camera_resolution_for_specific_view(
        camera_object, film_base_resolution, view)

    # Activate the selected camera for rendering
    nmv.camera.ops.set_active_camera(camera_object)

    # Set the image file name
    bpy.data.scenes['Scene'].render.filepath = '%s.png' % file_name

    # Render the image
    bpy.ops.render.render(write_still=True)


####################################################################################################
# @render_scene_to_scale
####################################################################################################
def render_scene_to_scale(file_name='image',
                          resolution_scale_factor=1,
                          view='FRONT'):
    """Renders the current scene to an image based on the scale of the largest object in the scene.

    :param file_name:
        The output name of the rendered image.
    :param resolution_scale_factor:
        This scale factor scales the 'base' resolution of the image.
    :param view:
        Rendering view.
    """

    # Deselect all the object
    nmv.scene.ops.deselect_all()

    # Set camera location and target based on the selected view to render the images
    scene_bounding_box = nmv.bbox.compute_scene_bounding_box()
    center = scene_bounding_box.center
    camera_x = scene_bounding_box.p_max[0] + scene_bounding_box.bounds[0]
    camera_y = scene_bounding_box.p_max[1] + scene_bounding_box.bounds[1]
    camera_z = scene_bounding_box.p_max[2] + scene_bounding_box.bounds[2]

    camera_location_x = Vector((camera_x, center.y, center.z))
    camera_location_y = Vector((center.x, camera_y, center.z))
    camera_location_z = Vector((center.x, center.y, camera_z))

    # Add a camera at the camera location
    camera_object = None

    # Front view
    if view == 'FRONT':

        # Add a camera along the z-axis
        camera_object = nmv.camera.create_default_camera(location=camera_location_z)

        # Rotate the camera
        nmv.camera.ops.rotate_camera_for_front_view(camera_object=camera_object)

    # Side view
    elif view == 'SIDE':

        # Add a camera along the x-axis
        camera_object = nmv.camera.create_default_camera(location=camera_location_x)

        # Rotate the camera
        nmv.camera.ops.rotate_camera_for_side_view(camera_object=camera_object)

    # Top view
    elif view == 'TOP':

        # Add a camera along the y-axis
        camera_object = nmv.camera.create_default_camera(location=camera_location_y)

        # Rotate the camera
        nmv.camera.ops.rotate_camera_for_top_view(camera_object=camera_object)

    # Update the camera resolution
    nmv.camera.ops.set_camera_resolution_to_scale_for_specific_view(
        camera_object, scale_factor=resolution_scale_factor, view=view)

    # Activate the selected camera for rendering
    nmv.camera.ops.set_active_camera(camera_object)

    # Set the image file name
    bpy.data.scenes['Scene'].render.filepath = '%s.png' % file_name

    # Render the image
    bpy.ops.render.render(write_still=True)
















####################################################################################################
# @render_full_view
####################################################################################################
def render_full_view(view_bounding_box,
                     image_name,
                     image_output_directory,
                     image_base_resolution=512,
                     camera_view='FRONT'):
    """
    Renders an image that shows the full view of the neuron morphology or mesh.

    :param view_bounding_box: The bounding box of the morphology or the mesh.
    :param image_name: The prefix of the generated image.
    :param image_output_directory: The directory where the image will be generated to.
    :param image_base_resolution: The 'base' resolution of the film.
    :param camera_view: The rendering view, can be 'FRONT', 'SIDE' or 'TOP'.
    :return:
    """

    # Deselect all the object in the scene
    nmv.scene.ops.deselect_all()

    # Create scene camera
    camera = camera_ops.create_camera(view_bounding_box=view_bounding_box,
        image_base_resolution=image_base_resolution, camera_view=camera_view)

    # Image path prefix, i.e. w/o extension which will be added later
    image_path_prefix = '%s/%s_%s' % (image_output_directory, image_name, camera_view)

    # Render the image to film
    camera_ops.render_scene_to_image(camera, image_path_prefix)

    # Delete the camera and any accompanying objects such as light
    nmv.scene.ops.delete_list_objects([camera])


####################################################################################################
# @render_full_view
####################################################################################################
def render_full_view_to_scale(view_bounding_box,
                              image_name,
                              image_output_directory,
                              image_scale_factor=1.0,
                              camera_view='FRONT'):
    """
    Renders an image that shows the full view of the neuron morphology or mesh to scale.
    This functionality os required when we need to make a collage of neurons that must respect
    the scale of the neurons.

    :param view_bounding_box: The bounding box of the morphology or the mesh.
    :param image_name: The prefix of the generated image.
    :param image_output_directory: The directory where the image will be generated to.
    :param image_scale_factor: The scale factor of the image for rendering higher resolution images.
    :param camera_view: The rendering view, can be 'FRONT', 'SIDE' or 'TOP'.
    :return:
    """

    # Deselect all the object in the scene
    nmv.scene.ops.deselect_all()

    # Create scene camera
    camera = camera_ops.create_to_scale_camera(view_bounding_box=view_bounding_box,
        image_scale_factor=image_scale_factor, camera_view=camera_view)

    # Image path prefix, i.e. w/o extension which will be added later
    image_path_prefix = '%s/%s_%s' % (image_output_directory, image_name, camera_view)

    # Render the image to film
    camera_ops.render_scene_to_image(camera, image_path_prefix)

    # Delete the camera and any accompanying objects such as light
    nmv.scene.ops.delete_list_objects([camera])


####################################################################################################
# @render_full_view_360
####################################################################################################
def render_full_view_360(objects_list,
                         view_bounding_box,
                         soma_center,
                         sequence_name,
                         sequence_output_directory,
                         image_base_resolution=512):
    """
    Renderes a 360 sequence for a list of objects.

    :param objects_list: A list of scene objects.
    :param view_bounding_box: The bounding box of the view.
    :param soma_center: The center of the soma in the scene.
    :param sequence_name: The name of the sequence.
    :param sequence_output_directory: The output directory of the sequence.
    :param image_base_resolution: The base resolution of the image.
    """

    # Deselect all the object in the scene
    nmv.scene.ops.deselect_all()

    # Compute the 360 bounding box
    bounding_box_360 = bounding_box.compute_360_bounding_box(view_bounding_box, soma_center)

    # Create scene camera
    camera = camera_ops.create_camera(
        view_bounding_box=bounding_box_360, image_base_resolution=image_base_resolution)

    # Create a directory where the sequence frames will be generated
    frames_directory = '%s/%s_360' % (sequence_output_directory, sequence_name)
    file_ops.clean_and_create_directory(frames_directory)

    # 360
    for i in range(0, 360):

        # Rotate each object in the skeleton object around the y axis
        for scene_object in objects_list:

            # Rotate the soma object around the y axis
            scene_object.rotation_euler[1] = i * 2 * 3.14 / 360.0

        # Set the frame name
        frame_name = '%s/%s_%s' % (frames_directory, 'frame', '{0:05d}'.format(i))

        # Render the image to film
        camera_ops.render_scene_to_image(camera, frame_name)

    # Delete the camera and any accompanying objects such as light
    nmv.scene.ops.delete_list_objects([camera])


####################################################################################################
# @render_soma_close_up
####################################################################################################
def render_close_up(image_name,
                    image_output_directory,
                    image_base_resolution=512,
                    camera_view='FRONT',
                    close_up_dimension=20):
    """
    Renders an image that shows a close up mainly on the soma.

    :param image_name: The prefix of the generated image.
    :param image_output_directory: The directory where the image will be generated to.
    :param image_base_resolution: The 'base' resolution of the film.
    :param camera_view: The rendering view, can be 'FRONT', 'SIDE' or 'TOP'.
    :param close_up_dimension: The unified dimension of the close up in microns.
    """

    # Setup a unified scale bounding box based on the close up dimension
    p_min = Vector((-close_up_dimension, -close_up_dimension, -close_up_dimension))
    p_max = Vector((close_up_dimension, close_up_dimension, close_up_dimension))

    # Create a symmetric bounding box that fits certain unified bounds for all the somata.
    unified_scale_bounding_box = bounding_box.BoundingBox(p_min=p_min, p_max=p_max)

    # Deselect all the object in the scene
    nmv.scene.ops.deselect_all()

    # Create scene camera
    camera = camera_ops.create_camera(view_bounding_box=unified_scale_bounding_box,
        image_base_resolution=image_base_resolution, camera_view=camera_view)

    # Image path prefix, i.e. w/o extension which will be added later
    image_path_prefix = '%s/%s_close_up_%s' % (image_output_directory, image_name, camera_view)

    # Render the image to film
    camera_ops.render_scene_to_image(camera, image_path_prefix)

    # Delete the camera and any accompanying objects such as light
    nmv.scene.ops.delete_list_objects([camera])


####################################################################################################
# @render_close_up_360
####################################################################################################
def render_close_up_360(scene_object,
                        sequence_name,
                        sequence_output_directory,
                        frame_base_resolution=512,
                        close_up_dimension=20):
    """
    Renders a 360 movie that shows a close up mainly on the soma.

    :param scene_object: A reference to the given object to be rendered.
    :param sequence_name: Output file prefix for the frames and the sequence.
    :param sequence_output_directory: The output directory where the sequence will be generated.
    :param frame_base_resolution: The 'base' resolution of the film.
    :param close_up_dimension: The unified dimension of the close up in microns.
    """

    # Setup a unified scale bounding box based on the close up dimension
    p_min = Vector((-close_up_dimension, -close_up_dimension, -close_up_dimension))
    p_max = Vector((close_up_dimension, close_up_dimension, close_up_dimension))

    # Create a symmetric bounding box that fits certain unified bounds for all the somas.
    unified_scale_bounding_box = bounding_box.BoundingBox(p_min=p_min, p_max=p_max)

    # Deselect all the object in the scene
    nmv.scene.ops.deselect_all()

    # Create scene camera
    camera = camera_ops.create_camera(view_bounding_box=unified_scale_bounding_box,
        image_base_resolution=frame_base_resolution)

    # Create a directory where the sequence frames will be generated
    frames_directory = '%s/%s_close_up_360' % (sequence_output_directory, sequence_name)
    file_ops.clean_and_create_directory(frames_directory)

    # 360
    for i in range(0, 360):

        # Rotate the soma object around the y axis
        scene_object.rotation_euler[1] = i * 3.14 / 360.0

        # Set the frame name
        frame_name = '%s/%s_%s' % (frames_directory, 'frame', '{0:05d}'.format(i))

        # Render the image to film
        camera_ops.render_scene_to_image(camera, frame_name)

    # Delete the camera and any accompanying objects such as light
    nmv.scene.ops.delete_list_objects([camera])


####################################################################################################
# @render_close_up_progressive
####################################################################################################
def render_close_up_progressive(scene_object,
                                sequence_name,
                                sequence_output_directory,
                                frame_base_resolution=512,
                                close_up_dimension=20):
    """
    Renders a progressive movie that shows a dynamic growing of a scene object mainly the soma.

    :param scene_object: A reference to the given object to be rendered.
    :param sequence_name: Output file prefix for the frames and the sequence.
    :param sequence_output_directory: The output directory where the sequence will be generated.
    :param frame_base_resolution: The 'base' resolution of the film.
    :param close_up_dimension: The unified dimension of the close up in microns.
    """

    # Setup a unified scale bounding box based on the close up dimension
    p_min = Vector((-close_up_dimension, -close_up_dimension, -close_up_dimension))
    p_max = Vector((close_up_dimension, close_up_dimension, close_up_dimension))

    # Create a symmetric bounding box that fits certain unified bounds for all the somata.
    unified_scale_bounding_box = bounding_box.BoundingBox(p_min=p_min, p_max=p_max)

    # Deselect all the object in the scene
    nmv.scene.ops.deselect_all()

    # Create scene camera
    camera = camera_ops.create_camera(view_bounding_box=unified_scale_bounding_box,
        image_base_resolution=frame_base_resolution)

    # Create a directory where the sequence frames will be generated
    frames_directory = '%s/%s_progressive' % (sequence_output_directory, sequence_name)
    file_ops.clean_and_create_directory(frames_directory)

    # Simulation
    for i in range(0, 100):

        # Update the frame based on the soft body simulation
        bpy.context.scene.frame_set(i)

        # Set the frame name
        frame_name = '%s/%s_%s' % (frames_directory, 'frame', '{0:05d}'.format(i))

        # Render the image to film
        camera_ops.render_scene_to_image(camera, frame_name)

    # Delete the camera and any accompanying objects such as light
    nmv.scene.ops.delete_list_objects([camera])


####################################################################################################
# @render_frame_at_angle
####################################################################################################
def render_frame_at_angle(scene_objects,
                          camera,
                          angle,
                          frame_name):
    """
    Renders a frame at a certain angle.

    :param scene_object: An group of objects in the scene to rotate.
    :param camera: A given camera that was created based on the bounding box of the scene object.
    :param angle: Rotation angle.
    :param frame_name: The name of the frame
    """

    # Rotate each object in the skeleton object around the y axis
    for scene_object in scene_objects:

        # Rotate the soma object around the y axis
        scene_object.rotation_euler[1] = angle * 2 * 3.14 / 360.0

    # Render the image to film
    camera_ops.render_scene_to_image(camera, frame_name)














####################################################################################################
# @render_soma_close_up
####################################################################################################
def render_soma_close_up(file_name='image',
                         film_base_resolution=512,
                         view='FRONT',
                         close_up_dimension=20):
    """
    Renders an image that shows a close up mainly on the soma.

    :param file_name: The output file name.
    :param film_base_resolution: The 'base' resolution of the film.
    :param view: The rendering view, can be 'FRONT', 'SIDE' or 'TOP'.
    :param close_up_dimension: The unified dimension of the close up in microns.
    """

    # Setup a unified scale bounding box based on the close up dimension
    p_min = Vector((-close_up_dimension, -close_up_dimension, -close_up_dimension))
    p_max = Vector((close_up_dimension, close_up_dimension, close_up_dimension))

    # Create a symmetric bounding box that fits certain unified bounds for all the somas.
    unified_scale_bounding_box = bounding_box.BoundingBox(p_min=p_min, p_max=p_max)

    # Deselect all the object in the scene
    nmv.scene.ops.deselect_all()

    # Set camera location and target based on the selected view to render the images
    center = unified_scale_bounding_box.center
    camera_x = unified_scale_bounding_box.p_max[0] + unified_scale_bounding_box.bounds[0]
    camera_y = unified_scale_bounding_box.p_max[1] + unified_scale_bounding_box.bounds[1]
    camera_z = unified_scale_bounding_box.p_max[2] + unified_scale_bounding_box.bounds[2]

    camera_location_x = Vector((camera_x, center.y, center.z))
    camera_location_y = Vector((center.x, camera_y, center.z))
    camera_location_z = Vector((center.x, center.y, camera_z))

    # Add a camera at the camera location
    camera = None

    # Front view
    if view == 'FRONT':

        # Add a camera along the z-axis
        camera = camera_ops.add_camera(location=camera_location_z)

        # Rotate the camera
        camera_ops.rotate_camera_for_front_view(camera=camera)

    # Side view
    elif view == 'SIDE':

        # Add a camera along the x-axis
        camera = camera_ops.add_camera(location=camera_location_x)

        # Rotate the camera
        camera_ops.rotate_camera_for_side_view(camera=camera)

    # Top view
    elif view == 'TOP':

        # Add a camera along the y-axis
        camera = camera_ops.add_camera(location=camera_location_y)

        # Rotate the camera
        camera_ops.rotate_camera_for_top_view(camera=camera)

    # Otherwise, use the front view (with a warning)
    else:

        # Add a camera along the z-axis
        camera = camera_ops.add_camera(location=camera_location_z)

        # Rotate the camera
        camera_ops.rotate_camera_for_front_view(camera=camera)

    # Update the camera resolution. This must be the same for all the view, because we have a
    # unified bounding box
    camera_ops.set_camera_resolution(
        camera, film_base_resolution, bounds=unified_scale_bounding_box.bounds)

    # Render the image to film
    camera_ops.render_scene_to_image(camera, file_name)

    # Delete the camera and any accompanying objects such as light
    nmv.scene.ops.delete_list_objects([camera])


####################################################################################################
# @render_soma_close_up_360
####################################################################################################
def render_soma_close_up_360(soma_object,
                             sequence_output_directory,
                             file_name='image',
                             film_base_resolution=512,
                             close_up_dimension=20):
    """
    Renders a 360 movie that shows a close up mainly on the soma.

    :param soma_object: A reference to the soma object.
    :param sequence_output_directory: The output directory where the sequence will be generated.
    :param file_name: Output file prefix for the frames and the sequence.
    :param film_base_resolution: The 'base' resolution of the film.
    :param close_up_dimension: The unified dimension of the close up in microns.
    """

    # Setup a unified scale bounding box based on the close up dimension
    p_min = Vector((-close_up_dimension, -close_up_dimension, -close_up_dimension))
    p_max = Vector((close_up_dimension, close_up_dimension, close_up_dimension))

    # Create a symmetric bounding box that fits certain unified bounds for all the somas.
    unified_scale_bounding_box = bounding_box.BoundingBox(p_min=p_min, p_max=p_max)

    # Deselect all the object in the scene
    nmv.scene.ops.deselect_all()

    # Set camera location and target based on the selected view to render the images
    center = unified_scale_bounding_box.center
    camera_z = unified_scale_bounding_box.p_max[2] + unified_scale_bounding_box.bounds[2]
    camera_location_z = Vector((center.x, center.y, camera_z))

    # Add a camera along the z-axis
    camera = camera_ops.add_camera(location=camera_location_z)

    # Rotate the camera
    camera_ops.rotate_camera_for_front_view(camera=camera)

    # Update the camera resolution. This must be the same for all the view, because we have a
    # unified bounding box
    camera_ops.set_camera_resolution(
        camera, film_base_resolution, bounds=unified_scale_bounding_box.bounds)

    # 360
    for i in range(0, 360):

        # Set the frame name
        frame_name = '%s/%s_%d' % (sequence_output_directory, file_name, i)

        # Rotate the soma object around the y axis
        soma_object.rotation_euler[1] = i * 3.14 / 360.0

        # Render the image to film
        camera_ops.render_scene_to_image(camera, frame_name)

    # Delete the camera and any accompanying objects such as light
    nmv.scene.ops.delete_list_objects([camera])





####################################################################################################
# @render_morphology
####################################################################################################
def render_morphology(morphology_bounding_box,
                      file_name='image',
                      film_base_resolution=512,
                      view='FRONT'):
    """
    Renders an image that shows a close up mainly on the soma.

    :param morphology_bounding_box: The bounding box of the morphology.
    :param file_name: The output file name.
    :param film_base_resolution: The 'base' resolution of the film.
    :param view: The rendering view, can be 'FRONT', 'SIDE' or 'TOP'.
    """

    # Deselect all the object in the scene
    nmv.scene.ops.deselect_all()

    # Set camera location and target based on the selected view to render the images
    center = morphology_bounding_box.center
    camera_x = morphology_bounding_box.p_max[0] + morphology_bounding_box.bounds[0]
    camera_y = morphology_bounding_box.p_max[1] + morphology_bounding_box.bounds[1]
    camera_z = morphology_bounding_box.p_max[2] + morphology_bounding_box.bounds[2]

    camera_location_x = Vector((camera_x, center.y, center.z))
    camera_location_y = Vector((center.x, camera_y, center.z))
    camera_location_z = Vector((center.x, center.y, camera_z))

    # Add a camera at the camera location
    camera = None

    # Front view
    if view == 'FRONT':

        # Add a camera along the z-axis
        camera = camera_ops.add_camera(location=camera_location_z)

        # Rotate the camera
        camera_ops.rotate_camera_for_front_view(camera=camera)

    # Side view
    elif view == 'SIDE':

        # Add a camera along the x-axis
        camera = camera_ops.add_camera(location=camera_location_x)

        # Rotate the camera
        camera_ops.rotate_camera_for_side_view(camera=camera)

    # Top view
    elif view == 'TOP':

        # Add a camera along the y-axis
        camera = camera_ops.add_camera(location=camera_location_y)

        # Rotate the camera
        camera_ops.rotate_camera_for_top_view(camera=camera)

    # Otherwise, use the front view (with a warning)
    else:

        # Add a camera along the z-axis
        camera = camera_ops.add_camera(location=camera_location_z)

        # Rotate the camera
        camera_ops.rotate_camera_for_front_view(camera=camera)

    # Update the camera resolution. This must be the same for all the view, because we have a
    # unified bounding box
    camera_ops.set_camera_resolution(
        camera, film_base_resolution, bounds=morphology_bounding_box.bounds)

    # Render the image to film
    camera_ops.render_scene_to_image(camera, file_name)

    # Delete the camera and any accompanying objects such as light
    nmv.scene.ops.delete_list_objects([camera])

'''
####################################################################################################
# @render_available_data
####################################################################################################
def render_available_data(file_name, film_resolution=512):
    """
    Renders the entire scene. This doesn't require any further magic, just use the render_scene()
    function and it will do it.

    :param film_resolution: The 'base' resolution of the film.
    :param file_name: The image name.
    """

    camera_ops.render_scene(file_name, film_resolution)



####################################################################################################
# @render_scene_to_scale
####################################################################################################
def render_scene_to_scale(file_name, scale_factor=1):
    """
    Renders the entire scene. This doesn't require any further magic, just use the render_scene()
    function and it will do it.

    :param file_name: The output path of the created image.
    :param scale_factor: The resolution scale factor.
    """

    camera_ops.render_scene_to_scale(file_name, scale_factor)
'''




class SomaRenderer():

    def render(self, resolution, extent):
        pass



class NeuronSkeletonRenderer():

    def render_close_up(self, resolution, extent):
        pass

    def render(self, resolution, view):

        # Based on the view compute the bounding box of the morphology skeleton
        pass

    def render_to_scale(self, scale_factor, view):

        # Based on the view, compute the bounding box of the morphology skeleton
        pass

class NeuronMeshRenderer():

    def render(self, resolution, view):

        # Based on the view compute the bounding box of the mesh
        pass

    def render_to_scale(self, scale_factor, view):

        # Based on the view, compute the bounding box of the mesh
        pass

    pass
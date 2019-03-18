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

# System imports
import math

# Blender imports
import bpy
from mathutils import Vector

# Internal modules
import nmv
import nmv.bbox
import nmv.consts
import nmv.enums
import nmv.scene
import nmv.utilities


####################################################################################################
# @Camera
####################################################################################################
class Camera:
    """Camera
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 name='Camera'):
        """Constructor

        :param name:
            The name of the camera, by default 'BaseCamera'.
        """

        # Camera reference
        self.camera = None

        # Camera name
        self.name = name

    ################################################################################################
    # @create_base_camera
    ################################################################################################
    def create_base_camera(self,
                           location=nmv.consts.Math.ORIGIN,
                           rotation=nmv.consts.Math.ORIGIN):
        """Create a new default Blender camera and returns a reference to it.

        :param location:
            The location of the camera, by default the origin.
        :param rotation:
            The rotation axis of the camera, by default zero rotation around the origin.
        :return
            A reference to the created camera.
        """

        # Deselect all the objects in the scene
        nmv.scene.ops.deselect_all()

        # Create a camera object and add it to the scene
        bpy.ops.object.camera_add(location=location, rotation=rotation)

        # Set the camera to be the active object
        camera = bpy.context.scene.objects.active

        # Rename the camera to the specified name
        camera.name = self.name

        # Return a reference to the camera object
        return camera

    ################################################################################################
    # @rotate_camera_for_front_view
    ################################################################################################
    def rotate_camera_for_front_view(self):
        """Rotate the given camera in the direction of the typical front view.
        """

        # Adjust the orientation
        self.camera.rotation_euler[0] = 0.0
        self.camera.rotation_euler[1] = 0.0
        self.camera.rotation_euler[2] = 0.0

    ################################################################################################
    # @rotate_camera_for_side_view
    ################################################################################################
    def rotate_camera_for_side_view(self):
        """Rotate the camera in the direction of the typical side view.
        """

        # Adjust the orientation
        self.camera.rotation_euler[0] = 0
        self.camera.rotation_euler[1] = 1.5708
        self.camera.rotation_euler[2] = 0

    ################################################################################################
    # @rotate_camera_for_top_view
    ################################################################################################
    def rotate_camera_for_top_view(self):
        """Rotate the camera in the direction of the typical top view.
        """

        # Adjust the orientation
        self.camera.rotation_euler[0] = -1.5708
        self.camera.rotation_euler[1] = 3.14
        self.camera.rotation_euler[2] = 0

    ################################################################################################
    # @set_active
    ################################################################################################
    def set_active(self):
        """Set the active camera to this one.
        """

        # Set the active camera to the given one
        bpy.data.scenes['Scene'].camera = self.camera

    ################################################################################################
    # @render_image
    ################################################################################################
    def render_image(self,
                     image_name='IMAGE'):
        """Render an image to a file.

        :param image_name:
            The output name of the rendered image.
        """

        # Activate the camera for rendering
        self.set_active()

        # Switch the rendering engine to cycles to be able to create the material
        if not bpy.context.scene.render.engine == 'CYCLES':
            bpy.context.scene.render.engine = 'CYCLES'

        # Set the image file name
        bpy.data.scenes['Scene'].render.filepath = '%s.png' % image_name

        # Render the image and ignore Blender verbosity
        bpy.ops.render.render(write_still=True)

    ################################################################################################
    # @get_camera_positions
    ################################################################################################
    @staticmethod
    def get_camera_positions(bounding_box):
        """Computes the camera position for an orthographic projection

        :param bounding_box:
            Scene bounding box.
        :return:
            Camera locations for the three different views.
        """

        # Set camera location and target based on the selected view to render the image
        center = bounding_box.center
        camera_x = bounding_box.p_max[0] + bounding_box.bounds[0]
        camera_y = bounding_box.p_max[1] + bounding_box.bounds[1]
        camera_z = bounding_box.p_max[2] + bounding_box.bounds[2]

        # Camera location
        camera_location_x = Vector((camera_x, center.y, center.z))
        camera_location_y = Vector((center.x, camera_y, center.z))
        camera_location_z = Vector((center.x, center.y, camera_z))

        # Return a vector for the camera position for XYZ locations
        return [camera_location_x, camera_location_y, camera_location_z]

    ################################################################################################
    # @get_camera_positions_for_perspective_projection
    ################################################################################################
    @staticmethod
    def get_camera_positions_for_perspective_projection(bounding_box, fov=45):
        """Computes the camera position for a perspective projection

        :param bounding_box:
            Scene bounding box.
        :param fov:
            Camera field of view, by default 45 degrees.
        :return:
            Camera locations for the three different views.
        """

        # Set camera location and target based on the selected view to render the image
        center = bounding_box.center
        bounds = bounding_box.bounds
        r = math.sqrt((0.5 * bounds[0] * 0.5 * bounds[0]) +
                      (0.5 * bounds[1] * 0.5 * bounds[1]) +
                      (0.5 * bounds[2] * 0.5 * bounds[2]))
        camera_x = r / math.tan(math.radians(0.5 * fov)) * 1.25
        camera_y = r / math.tan(math.radians(0.5 * fov)) * 1.25
        camera_z = r / math.tan(math.radians(0.5 * fov)) * 1.25

        # Camera location
        camera_location_x = Vector((camera_x, center.y, center.z))
        camera_location_y = Vector((center.x, camera_y, center.z))
        camera_location_z = Vector((center.x, center.y, camera_z))

        # Return a vector for the camera position for XYZ locations
        return [camera_location_x, camera_location_y, camera_location_z]

    ################################################################################################
    # @update_camera_resolution
    ################################################################################################
    def update_camera_resolution(self,
                                 resolution=512,
                                 camera_view=nmv.enums.Camera.View.FRONT,
                                 bounds=None):
        """Update the resolution of the camera film based on the rendering view.

        :param resolution:
            The 'base' resolution of the camera, by default 512.
        :param camera_view:
            The view of the camera FRONT, FRONT_360, SIDE or TOP, by default FRONT.
        :param bounds:
            An optional bounding box dimensions of the scene or a specific object.
        """

        # Get the scene bounding box to adjust the camera accordingly, if the bounds are not set
        if bounds is None:

            # Recompute the scene bounding box
            nmv.logger.log('WARNING: Scene Bounding Box is Recomputed!')
            bounds = nmv.bbox.compute_scene_bounding_box().bounds

        # Compute the orthographic scale based in the give camera view
        orthographic_scale = 1.0
        x_bounds = 0.0
        y_bounds = 0.0

        # Front view
        if camera_view == nmv.enums.Camera.View.FRONT:

            # 'FRONT' : bounds[0] & bounds[1]
            orthographic_scale = bounds[0]
            if orthographic_scale < bounds[1]:
                orthographic_scale = bounds[1]

            x_bounds = bounds[0]
            y_bounds = bounds[1]

        # Side view
        elif camera_view == nmv.enums.Camera.View.SIDE:

            # 'SIDE' : bounds[1] & bounds[2]
            orthographic_scale = bounds[1]
            if orthographic_scale < bounds[2]:
                orthographic_scale = bounds[2]

            x_bounds = bounds[2]
            y_bounds = bounds[1]

        # Top view
        elif camera_view == nmv.enums.Camera.View.TOP:

            # 'TOP' : bounds[2] & bounds[0]
            orthographic_scale = bounds[2]
            if orthographic_scale < bounds[0]:
                orthographic_scale = bounds[0]

            x_bounds = bounds[0]
            y_bounds = bounds[2]

        # 360 front view
        elif camera_view == nmv.enums.Camera.View.FRONT_360:

            # 360
            x_bounds = bounds[0]
            y_bounds = bounds[1]

            orthographic_scale = x_bounds
            if orthographic_scale < y_bounds:
                orthographic_scale = y_bounds

        # Front view by default
        else:

            # Use FRONT by default
            orthographic_scale = bounds[0]
            if orthographic_scale < bounds[1]:
                orthographic_scale = bounds[1]

            x_bounds = bounds[0]
            y_bounds = bounds[1]

        # Adjust the camera parameters
        self.camera.data.clip_start = 0.0
        self.camera.data.clip_end = 100000
        self.camera.data.type = 'ORTHO'
        self.camera.data.ortho_scale = orthographic_scale

        # Set the image resolution
        bpy.context.scene.render.resolution_x = int(resolution * x_bounds / orthographic_scale) * 2
        bpy.context.scene.render.resolution_y = int(resolution * y_bounds / orthographic_scale) * 2

        # Set the background to be transparent
        bpy.context.scene.cycles.film_transparent = True

    ################################################################################################
    # @update_camera_resolution_to_scale
    ################################################################################################
    def update_camera_resolution_to_scale(self,
                                          scale_factor=1.0,
                                          camera_view=nmv.enums.Camera.View.FRONT,
                                          bounds=None):
        """Update the resolution of the camera film based on the rendering view for certain scale.

        :param scale_factor:
            Scale factor to scale the resolution of the image.
        :param camera_view:
            The view of the camera 'FRONT', 'SIDE' or 'TOP'.
        :param bounds:
            An optional bounding box dimensions of the scene or a specific object.
        """

        # Get the scene bounding box to adjust the camera accordingly, if the bounds are not set
        if bounds is None:
            bounds = nmv.bbox.compute_scene_bounding_box().bounds

        # Compute the orthographic scale based in the give camera view
        orthographic_scale = 1.0
        x_bounds = 0.0
        y_bounds = 0.0

        if camera_view == nmv.enums.Camera.View.FRONT:

            # 'FRONT' : bounds[0] & bounds[1]
            orthographic_scale = bounds[0]
            if orthographic_scale < bounds[1]:
                orthographic_scale = bounds[1]

            x_bounds = bounds[0]
            y_bounds = bounds[1]

        elif camera_view == nmv.enums.Camera.View.SIDE:

            # 'SIDE' : bounds[1] & bounds[2]
            orthographic_scale = bounds[1]
            if orthographic_scale < bounds[2]:
                orthographic_scale = bounds[2]

            x_bounds = bounds[2]
            y_bounds = bounds[1]

        elif camera_view == nmv.enums.Camera.View.TOP:

            # 'TOP' : bounds[2] & bounds[0]
            orthographic_scale = bounds[2]
            if orthographic_scale < bounds[0]:
                orthographic_scale = bounds[0]

            x_bounds = bounds[0]
            y_bounds = bounds[2]

        elif camera_view == nmv.enums.Camera.View.FRONT_360:

            # 360
            x_bounds = bounds[0]
            y_bounds = bounds[1]

            orthographic_scale = x_bounds
            if orthographic_scale < y_bounds:
                orthographic_scale = y_bounds

        else:

            # Use FRONT by default
            orthographic_scale = bounds[0]
            if orthographic_scale < bounds[1]:
                orthographic_scale = bounds[1]

            x_bounds = bounds[0]
            y_bounds = bounds[1]

        # Adjust the camera parameters
        self.camera.data.clip_start = 0.0
        self.camera.data.clip_end = 1000000
        self.camera.data.type = 'ORTHO'
        self.camera.data.ortho_scale = orthographic_scale

        # Set the image resolution
        bpy.context.scene.render.resolution_x = int(scale_factor * x_bounds) * 2
        bpy.context.scene.render.resolution_y = int(scale_factor * y_bounds) * 2

        # Use Cycles renderer
        bpy.context.scene.render.engine = 'CYCLES'

        # Set the background to be transparent
        bpy.context.scene.cycles.film_transparent = True

    ################################################################################################
    # @setup_camera_for_scene
    ################################################################################################
    def setup_camera_for_scene(self,
                               bounding_box,
                               camera_view=nmv.enums.Camera.View.FRONT,
                               camera_projection=nmv.enums.Camera.Projection.ORTHOGRAPHIC):

        # Get the scene bounding box to adjust the camera accordingly, if the bounds are not set
        if bounding_box is None:
            bounding_box = nmv.bbox.compute_scene_bounding_box()

        # Compute the location of the camera based on the bounding box
        if camera_projection == nmv.enums.Camera.Projection.PERSPECTIVE:
            camera_locations = self.get_camera_positions_for_perspective_projection(
                bounding_box=bounding_box)
        else:
            camera_locations = self.get_camera_positions(bounding_box=bounding_box)

        # Front view (or for 360)
        if camera_view == nmv.enums.Camera.View.FRONT or \
           camera_view == nmv.enums.Camera.View.FRONT_360:

            # Add a camera along the z-axis
            self.camera = self.create_base_camera(location=camera_locations[2])

            # Rotate the camera
            self.rotate_camera_for_front_view()

        # Side view
        elif camera_view == nmv.enums.Camera.View.SIDE:

            # Add a camera along the x-axis
            self.camera = self.create_base_camera(location=camera_locations[0])

            # Rotate the camera
            self.rotate_camera_for_side_view()

        # Top view
        elif camera_view == nmv.enums.Camera.View.TOP:

            # Add a camera along the y-axis
            self.camera = self.create_base_camera(location=camera_locations[1])

            # Rotate the camera
            self.rotate_camera_for_top_view()

        # Default is FRONT
        else:

            # Add a camera along the z-axis
            self.camera = self.create_base_camera(location=camera_locations[2])

            # Rotate the camera
            self.rotate_camera_for_front_view()

    ################################################################################################
    # @render_scene
    ################################################################################################
    def render_scene(self,
                     bounding_box,
                     camera_view=nmv.enums.Camera.View.FRONT,
                     image_resolution=512,
                     image_name='IMAGE',
                     camera_projection=nmv.enums.Camera.Projection.ORTHOGRAPHIC,
                     keep_camera_in_scene=True):
        """Render scene using an orthographic camera.

        :param bounding_box:
            The bounding box of all the objects that should be rendered.
        :param camera_view:
            The view of the camera: TOP, FRONT, or SIDE, by default FRONT.
        :param image_resolution:
            The 'base' resolution of the image, by default 512.
        :param image_name:
            The name of the image, by default 'IMAGE'.
        :param camera_projection:
            Camera projection either orthographic or perspective.
        :param keep_camera_in_scene:
            Keep the camera in the scene after rendering.
        """

        # Get the scene bounding box to adjust the camera accordingly, if the bounds are not set
        if bounding_box is None:
            bounding_box = nmv.bbox.compute_scene_bounding_box()

        # Setup the camera
        self.setup_camera_for_scene(bounding_box, camera_view, camera_projection)

        # Update the camera resolution
        self.update_camera_resolution(resolution=image_resolution, camera_view=camera_view,
            bounds=bounding_box.bounds)
        if camera_projection == nmv.enums.Camera.Projection.PERSPECTIVE:
            self.camera.data.type = 'PERSP'
            bpy.context.object.data.angle = math.radians(45.0)
        else:
            self.camera.data.type = 'ORTHO'

        # Deselect all the object in the scene
        nmv.scene.ops.deselect_all()

        # Render the image
        self.render_image(image_name=image_name)

        # Keep the camera in the scene or delete it after the rendering
        if not keep_camera_in_scene:

            # Delete the camera
            nmv.scene.ops.delete_object_in_scene(self.camera)

    ################################################################################################
    # @render_scene_bounding_box
    ################################################################################################
    def render_scene_to_scale(self,
                              bounding_box=None,
                              camera_view=nmv.enums.Camera.View.FRONT,
                              scale_factor=1.0,
                              image_name='IMAGE',
                              keep_camera_in_scene=False):
        """Render a scene to scale using orthographic projection.

        :param bounding_box:
            The bounding box of all the objects that should be rendered.
            If no given bounding box is given, them the whole scene will be rendered.
        :param camera_view:
            The view of the camera: TOP, FRONT, or SIDE, by default FRONT.
        :param scale_factor:
            A factor to scale the resolution of the image.
        :param image_name:
            The name of the image, by default 'IMAGE'.
        :param keep_camera_in_scene:
            Keep the camera in the scene after rendering.
        """

        # Setup the camera
        self.setup_camera_for_scene(bounding_box, camera_view)

        # Update the camera resolution
        self.update_camera_resolution_to_scale(
            scale_factor=scale_factor, camera_view=camera_view, bounds=bounding_box.bounds)

        # Deselect all the object in the scene
        nmv.scene.ops.deselect_all()

        # Render the image
        self.render_image(image_name=image_name)

        # Keep the camera in the scene or delete it after the rendering
        if not keep_camera_in_scene:

            # Delete the camera
            nmv.scene.ops.delete_object_in_scene(self.camera)

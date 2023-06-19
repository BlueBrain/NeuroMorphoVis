####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
# Author: Marwan Abdellah <marwan.abdellah@epfl.ch>
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
import matplotlib
from matplotlib import cm

# Blender imports
from mathutils import Vector

# Internal imports
import nmv.bbox
import nmv.enums
import nmv.rendering
import nmv.shading


####################################################################################################
# SimulationMeshRender
####################################################################################################
class SimulationMeshRender:

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 mesh_object,
                 simulation_data,
                 colormap='hsv',
                 colormap_resolution=16):
        """Constructor

        :param mesh_object:
            A given mesh to visualize the simulation on top.
        :param simulation_data:
            A list of the simulation time series. This list has N entries, each entry has M elements
            where M is the number of faces in the mesh.
        :param colormap:
            A given color-map to map the simulation.
            One of the following 'hsv', 'viridis', 'plasma', 'inferno', 'magma', 'cividis'
        """

        # Input mesh
        self.mesh_object = mesh_object

        # Simulation data
        self.simulation_data = simulation_data

        # The colormap
        self.colormap = colormap

        # Number of elements in the colormap
        self.colormap_resolution = colormap_resolution

        # A list of all the materials
        self.materials = list()

        self.bounding_box = None

    ################################################################################################
    # @get_bounding_box
    ################################################################################################
    def get_bounding_box(self):

        # If the bounding box is computed before, return it and do not compute it again
        if self.bounding_box is not None:
            return self.bounding_box

        # Compute the bounding box for the mesh
        self.bounding_box = nmv.bbox.compute_scene_bounding_box_for_meshes()

        # Return the bounding box
        return self.bounding_box

    ################################################################################################
    # @create_colormap_materials
    ################################################################################################
    def create_colormap_materials(self):

        # Create a list of colors
        cmap = matplotlib.cm.get_cmap(self.colormap, self.colormap_resolution)

        for i in range(self.colormap_resolution):
            self.materials.append(nmv.shading.create_lambert_ward_material(
                name='color_%d' % i, color=Vector((cmap(i)[0], cmap(i)[1], cmap(i)[2]))))

    ################################################################################################
    # @assign_colors_to_faces_based_on_index
    ################################################################################################
    def assign_colors_to_faces_based_on_index(self, offset=0):

        # If the materials list is empty, create it
        if len(self.materials) == 0:
            self.create_colormap_materials()

        # Clear the previous materials assigned to this mesh object
        self.mesh_object.data.materials.clear()

        # Assign the material to the given object
        for material in self.materials:
            self.mesh_object.data.materials.append(material)

        # Get the minimum and maximum values for mapping
        min_index = 0
        max_index = len(self.mesh_object.data.polygons)

        # Number of materials
        number_materials = len(self.materials)

        # Iterate over all the faces and update the indices
        for i, face in enumerate(self.mesh_object.data.polygons):

            # Get the material index based on the index of the face in the mesh
            material_index = int(
                (face.index - min_index) * number_materials / (max_index - min_index))

            # Material offset
            material_index = material_index + offset
            material_index = material_index % number_materials

            # Assign the material index to the face
            face.material_index = material_index

    ################################################################################################
    # @render_frame
    ################################################################################################
    def render_frame(self,
                     image_name,
                     images_directory,
                     image_resolution=1024,
                     camera_view=nmv.enums.Camera.View.FRONT):

        # Compute the bounding box for the mesh
        bounding_box = self.get_bounding_box()

        # Render the image
        nmv.rendering.render(
            bounding_box=bounding_box,
            camera_view=camera_view,
            image_resolution=image_resolution,
            image_name=image_name,
            image_directory=images_directory)

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

# Blender imports
import bpy
from mathutils import Vector

# Internal imports
import nmv.mesh
import nmv.utilities
import nmv.shading
import nmv.scene


####################################################################################################
# @Endfoot
####################################################################################################
class Endfoot:
    """Astrocyte endfoot"""

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 name='Endfoot',
                 points=None,
                 triangles=None):
        """Constructor

        :param name:
            The name of the endfoot.
        :param points:
            A list of all the points of the endfoot in the format of <XYZ,R> per item.
        :param triangles:
            A list of all the triangles of the endfoot in the format of <XYZ> per item.
        """

        # The name of the endfoot
        self.name = name

        # A list of the given points of the endfoot, including the radius [X, Y, Z, R]
        self.points = points

        # A list of triangles <V0, V1, V2>
        self.triangles = triangles

        # A list of the vertices of the endfoot <X, Y, Z> from the points list
        self.vertices = list()
        if self.points is not None:
            self.vertices = [(p[0], p[1], p[2]) for p in self.points]

        # A list of constructed edges from the from_pydata function, EMPTY
        self.edges = list()

    ################################################################################################
    # @create_surface_patch
    ################################################################################################
    def create_surface_patch(self,
                             material=None,
                             collection_name="Endfeet"):
        """Creates a surface patch of the endfoot.

        :param material:
            The material that will be applied to the endfoot.
        :param collection_name:
            The name of the Blender collection.
        :return:
            A reference to the created patch mesh.
        """

        # Create a new mesh object
        mesh = bpy.data.meshes.new(self.name)
        mesh_object = bpy.data.objects.new(mesh.name, mesh)

        # Create the collection and link the mesh object to it
        collection = nmv.utilities.create_new_collection(name=collection_name)
        collection.objects.link(mesh_object)

        # Update the data in the mesh
        bpy.context.view_layer.objects.active = mesh_object
        mesh.from_pydata(self.vertices, self.edges, self.triangles)

        # Assign the material to the endfeet
        if material is not None:
            nmv.shading.set_material_to_object(
                mesh_object=mesh_object, material_reference=material)

        # Smooth the surface for the shading
        nmv.mesh.shade_smooth_object(mesh_object=mesh_object)

        # Return a reference to the constructed patch
        return mesh_object

    ################################################################################################
    # @create_resampled_surface_patch
    ################################################################################################
    def create_resampled_surface_patch(self,
                                       material=None,
                                       subdivision_level=3):
        """Creates a re-sampled patch of the endfoot surface.

        :param material:
            The material that will be applied to the resulting patch.
        :param subdivision_level:
            The subdivision level that will be used to resample the surface.
        :return:
            A reference to the created mesh.
        """

        # Create a basic surface patch
        surface_patch = self.create_surface_patch(material=material)

        # Resample the patch
        bpy.ops.object.modifier_add(type='SUBSURF')
        bpy.context.object.modifiers["Subdivision"].subdivision_type = 'SIMPLE'
        bpy.context.object.modifiers["Subdivision"].levels = subdivision_level
        bpy.context.object.modifiers["Subdivision"].show_only_control_edges = True
        bpy.context.object.modifiers["Subdivision"].uv_smooth = 'PRESERVE_CORNERS'

        if nmv.utilities.is_blender_290():
            bpy.ops.object.modifier_apply(modifier="Subdivision")
        else:
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subdivision")

        # Return a reference to the surface patch
        return surface_patch

    ################################################################################################
    # @compute_average_thickness
    ################################################################################################
    def compute_average_thickness(self):
        """Computes the average thickness of the endfoot.

        :return:
            The average thickness of the endfoot from all the samples.
        """

        thickness = 0.0
        if len(self.points) > 0:
            for p in self.points:
                thickness += p[3]
            thickness /= len(self.points)
        return thickness

    ################################################################################################
    # @compute_centroid
    ################################################################################################
    def compute_centroid(self):
        """Computes the centroid of the endfoot.

        :return:
            The centroid of the endfoot.
        """

        centroid = Vector((0.0, 0.0, 0.0))
        if len(self.points) > 0:
            for p in self.points:
                point = Vector((p[0], p[1], p[2]))
                centroid += point
            centroid /= len(self.points)
        return centroid

    ################################################################################################
    # @create_geometry_with_metaballs
    ################################################################################################
    def create_geometry_with_metaballs(self,
                                       material=None):
        """Creates the endfoot geometry with meta-balls.

        :param material:
            A reference to the material that will be applied to the endfoot mesh.
        :return:
            A reference to the resulting endfoot mesh.
        """

        # Create the resampled surface patch of the endfeet
        patch = self.create_resampled_surface_patch(material)

        # Create a meta-skeleton
        endfoot_geometry_name = 'Patch_' + self.name
        meta_skeleton = bpy.data.metaballs.new(endfoot_geometry_name)

        # Create a new meta-object that reflects the reconstructed mesh at the end of the operation
        meta_mesh = bpy.data.objects.new(endfoot_geometry_name, meta_skeleton)

        # Link the meta-object to the scene
        nmv.scene.link_object_to_scene(meta_mesh)

        # Initial resolution of the meta skeleton, this will get updated later in the finalization
        meta_skeleton.resolution = 1.0

        # Make sure that the endfoot is located at the centroid
        meta_mesh.location = Vector((0.0, 0.0, 0.0))

        # Compiling the vertex list
        vertex_list = list()
        for v in patch.data.vertices:
            vertex_list.append(v.co)

        # Determine the average thickness
        thickness = self.compute_average_thickness()

        # Make sure that you don't go beyond the thickness limit to avoid performance issues
        smallest_radius = 1e5

        # Construct the meta-elements per sample
        for vertex in vertex_list:

            # New meta-element
            meta_element = meta_skeleton.elements.new()

            # Adjusting the radius based on the thickness
            meta_element.radius = thickness

            # Update the smallest radius value and ensure that the thickness is a valid value
            if thickness < smallest_radius:
                if thickness < 0.01:
                    thickness = 0.01
                smallest_radius = thickness

            # Update its coordinates
            meta_element.co = vertex

        # Update the resolution
        meta_skeleton.resolution = smallest_radius
        nmv.logger.detail('Endfeet [%s], Meta Resolution [%f]' % (self.name,
                                                                  meta_skeleton.resolution))
        # Select the mesh
        for scene_object in bpy.context.scene.objects:
            if endfoot_geometry_name in scene_object:
                meta_mesh = bpy.context.scene.objects[endfoot_geometry_name]
                break

        # Set the mesh to be the active one
        nmv.scene.set_active_object(meta_mesh)

        # Convert it to a mesh from meta-balls
        nmv.logger.detail('Converting the Meta-object to a Mesh (Patience Please!)')
        bpy.ops.object.convert(target='MESH')

        # Updating the mesh name, as a workaround to the modifiers
        meta_mesh = bpy.context.scene.objects[endfoot_geometry_name + '.001']
        meta_mesh.name = endfoot_geometry_name

        # Assign the material to the endfeet
        if material is not None:
            nmv.shading.set_material_to_object(mesh_object=meta_mesh, material_reference=material)

        # Smooth the surface for the shading
        nmv.mesh.shade_smooth_object(mesh_object=meta_mesh)

        # Delete the Patch
        nmv.scene.delete_object_in_scene(bpy.context.scene.objects[self.name])

        # Rename the endfoot object
        meta_mesh.name = self.name

        # Return a reference to the endfeet mesh
        return meta_mesh


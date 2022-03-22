####################################################################################################
# Copyright (c) 2020, EPFL / Blue Brain Project
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

# Blender imports
import bpy
import bmesh

# Internal imports
import nmv.scene
import nmv.utilities


####################################################################################################
# @MeshCleaner
####################################################################################################
class MeshCleaner:
    """Cleans a given mesh with problems like holes, non-manifold vertices and inverted normals.

    NOTE: This implementation is based on the code of the 3DPrint add-on that is available in
    Blender under the GPL license.
    """

    def __init__(self,
                 threshold=0.0001,
                 sides=0):
        """Constructor

        :param threshold:
            Minimum distance between elements to merge.
        :param sides:
            Number of sides in hole required to fill (zero fills all holes.
        """

        # Merging threshold
        self.threshold = threshold

        # Number of sides in holes to be filled.
        self.sides = sides

        # Vertex count difference
        self.vertex_count_difference = None

        # Edge count difference
        self.edge_count_difference = None

        # Face count difference
        self.face_count_difference = None

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
        """Execute the operator.

        :param context:
            Blender context.
        """

        # Get the current mode
        current_mode = context.mode

        # Setup the environment
        self.setup_environment()

        # Original bmesh
        bm_key_orig = self.count_mesh_elements(context)

        # Delete loose
        self.delete_loose()

        # Delete interior
        self.delete_interior()

        # Remove doubles
        self.remove_doubles(self.threshold)

        # Dissolve degenerate
        self.dissolve_degenerate(self.threshold)

        # Fix non-manifold
        self.fix_non_manifold(context, self.sides)  # may take a while

        # Make normals consistent
        self.make_normals_consistently_outwards()

        # Get the new mesh
        bm_key = self.count_mesh_elements(context)

        # Switch back to object mode if already on the edit mode
        if current_mode != 'EDIT_MESH':
            bpy.ops.object.mode_set(mode='OBJECT')

        # Compute data for stats.
        self.vertex_count_difference = bm_key[0] - bm_key_orig[0]
        self.edge_count_difference = bm_key[1] - bm_key_orig[1]
        self.face_count_difference = bm_key[2] - bm_key_orig[2]

    ################################################################################################
    # @count_mesh_elements
    ################################################################################################
    @staticmethod
    def count_mesh_elements(context):
        """Count number of elements in the mesh.

        :param context:
            Blender context.
        :return:
            Number of vertices, number of edges, number of faces.
        """
        bm = bmesh.from_edit_mesh(context.edit_object.data)
        return len(bm.verts), len(bm.edges), len(bm.faces)

    ################################################################################################
    # @setup_environment
    ################################################################################################
    @staticmethod
    def setup_environment():
        """Set the mode as edit, select mode as vertices, and reveal hidden vertices.
        """

        # Set to EDIT mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Set to vertex mode
        bpy.ops.mesh.select_mode(type='VERT')

        # Reveal
        bpy.ops.mesh.reveal()

    ################################################################################################
    # @remove_doubles
    ################################################################################################
    @staticmethod
    def remove_doubles(threshold):
        """Remove duplicate vertices.

        :param threshold:
            Distance to merge.
        """

        # Select all vertices in the mesh
        bpy.ops.mesh.select_all(action='SELECT')

        # Remove doubles
        bpy.ops.mesh.remove_doubles(threshold=threshold)

    ################################################################################################
    # @delete_loose
    ################################################################################################
    @staticmethod
    def delete_loose():
        """Delete loose vertices, edges or faces.
        """

        # Select all vertices, edges and faces in the mesh
        bpy.ops.mesh.select_all(action='SELECT')

        # Delete the loose ones
        nmv.utilities.disable_std_output()
        bpy.ops.mesh.delete_loose(use_verts=True, use_edges=True, use_faces=True)
        nmv.utilities.enable_std_output()

    ################################################################################################
    # @delete_interior
    ################################################################################################
    @staticmethod
    def delete_interior():
        """Delete interior faces.
        """

        # Select all faces
        bpy.ops.mesh.select_all(action='DESELECT')

        # Select interior faces
        bpy.ops.mesh.select_interior_faces()

        # Delete the faces
        nmv.utilities.disable_std_output()
        bpy.ops.mesh.delete(type='FACE')
        nmv.utilities.enable_std_output()

    ################################################################################################
    # @dissolve_degenerate
    ################################################################################################
    @staticmethod
    def dissolve_degenerate(threshold):
        """Dissolve zero area faces and zero length edges.
        """

        # Select all faces
        bpy.ops.mesh.select_all(action='SELECT')

        # Dissolve degenerate
        bpy.ops.mesh.dissolve_degenerate(threshold=threshold)

    ################################################################################################
    # @make_normals_consistently_outwards
    ################################################################################################
    @staticmethod
    def make_normals_consistently_outwards():
        """Have all normals face outwards.
        """

        # Select all faces
        bpy.ops.mesh.select_all(action='SELECT')

        # Make normals consistent
        bpy.ops.mesh.normals_make_consistent()

    ################################################################################################
    # @fix_non_manifold
    ################################################################################################
    @classmethod
    def fix_non_manifold(cls,
                         context,
                         sides):
        """Naive iterate-until-no-more approach for fixing manifolds

        :param context:
            Blender context.
        :param sides:
            Number of sides in hole required to fill (zero fills all holes.
        """

        # Count the total number of non-manifold vertices
        total_non_manifold = cls.count_non_manifold_vertices(context)

        # If zero, return
        if not total_non_manifold:
            return

        # Get the states
        bm_states = set()
        bm_key = cls.count_mesh_elements(context)
        bm_states.add(bm_key)

        # Fill all the non-manifold vertices and delete any newly generated ones on-the-fly
        while True:
            cls.fill_non_manifold(sides)
            nmv.utilities.disable_std_output()
            cls.delete_newly_generated_non_manifold_vertices()
            nmv.utilities.enable_std_output()

            bm_key = cls.count_mesh_elements(context)
            if bm_key in bm_states:
                break
            else:
                bm_states.add(bm_key)

    ################################################################################################
    # @setup_environment
    ################################################################################################
    @staticmethod
    def select_non_manifold_vertices(use_wire=False,
                                     use_boundary=False,
                                     use_multi_face=False,
                                     use_non_contiguous=False,
                                     use_verts=False):
        """Selects non-manifold vertices.

        :param use_wire:
            See Blender documentation.
        :param use_boundary:
            See Blender documentation.
        :param use_multi_face:
            See Blender documentation.
        :param use_non_contiguous:
            See Blender documentation.
        :param use_verts:
            See Blender documentation.
        """
        bpy.ops.mesh.select_non_manifold(
            extend=False,
            use_wire=use_wire,
            use_boundary=use_boundary,
            use_multi_face=use_multi_face,
            use_non_contiguous=use_non_contiguous,
            use_verts=use_verts)

    ################################################################################################
    # @count_non_manifold_vertices
    ################################################################################################
    @classmethod
    def count_non_manifold_vertices(cls,
                                    context):
        """Return a set of coordinates of non-manifold vertices.

        :param context:
            Blender context.
        :return:
            A set of coordinates of non-manifold vertices
        """

        # Select the non-manifold vertices
        cls.select_non_manifold_vertices(use_wire=True, use_boundary=True, use_verts=True)

        # Convert the mesh to a bmesh
        bm = bmesh.from_edit_mesh(context.edit_object.data)

        # Count the non-manifold vertices that are selected
        return sum((1 for v in bm.verts if v.select))

    ################################################################################################
    # @fill_non_manifold
    ################################################################################################
    @classmethod
    def fill_non_manifold(cls,
                          sides):
        """Fills in any remnant non-manifolds
        """

        # Select all the vertices
        bpy.ops.mesh.select_all(action='SELECT')

        # Fill the holes in the mesh
        bpy.ops.mesh.fill_holes(sides=sides)

    ################################################################################################
    # @delete_newly_generated_non_manifold_vertices
    ################################################################################################
    @classmethod
    def delete_newly_generated_non_manifold_vertices(cls):
        """Delete any newly generated vertices from the filling repair
        """

        # Select the non-manifold vertices
        cls.select_non_manifold_vertices(use_wire=True, use_verts=True)

        # Delete the vertices
        nmv.utilities.disable_std_output()
        bpy.ops.mesh.delete(type='VERT')
        nmv.utilities.enable_std_output()


####################################################################################################
# @clean_mesh_object
####################################################################################################
def clean_mesh_object(mesh_object,
                      threshold=0.0001,
                      sides=0):
    """Cleans a mesh object and make it two-manifold.

    :param mesh_object:
        A given mesh object to clean.
    :param threshold:
        Distance threshold between the vertices to be merged together.
    :param sides:
        Number of sides of holes to be filled.
    :return
        A tuple with number of vertices/edges/faces removed from the cleaning operation.
    """

    # Select the mesh object
    nmv.scene.select_object(scene_object=mesh_object)

    # Construct a mesh cleaner object
    mesh_cleaner = MeshCleaner(threshold=threshold, sides=sides)

    # Execute the operator
    mesh_cleaner.execute(bpy.context)

    # Return the result
    return (mesh_cleaner.vertex_count_difference,
            mesh_cleaner.edge_count_difference,
            mesh_cleaner.face_count_difference)

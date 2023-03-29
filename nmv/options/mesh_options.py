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


####################################################################################################
# @MeshOptions
####################################################################################################
class MeshOptions:
    """Mesh options"""

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        """Constructor"""

        # MESHING OPTIONS ##########################################################################
        # Tessellate the mesh after the reconstruction
        self.tessellate_mesh = False

        # Tessellation level (between 0.1 and 1.0)
        self.tessellation_level = nmv.consts.Meshing.MAX_TESSELLATION_LEVEL

        # Fixing morphology artifacts
        self.fix_morphology_artifacts = True

        # Meshing technique
        self.meshing_technique = nmv.enums.Meshing.Technique.PIECEWISE_WATERTIGHT

        # Soma reconstruction technique
        self.soma_type = nmv.enums.Soma.Representation.SOFT_BODY

        # Export in circuit coordinates, by default no unless there is a circuit file given
        self.global_coordinates = False

        # Which proxy meshing method will be within the voxelization-based re-meshing
        self.proxy_mesh_method = nmv.enums.Meshing.Proxy.CONNECTED_SECTIONS

        # Soma connection to the arbors, connected or disconnected
        self.soma_connection = nmv.enums.Meshing.SomaConnection.DISCONNECTED

        # Connecting the different objects of the neuron into a single mesh
        self.neuron_objects_connection = nmv.enums.Meshing.ObjectsConnection.DISCONNECTED

        # Create the mesh to look like a real neuron or more for visualization
        self.surface = nmv.enums.Meshing.Surface.SMOOTH

        # Edges of the meshes, either hard or smooth
        self.edges = nmv.enums.Meshing.Edges.HARD

        # The shape of the skeleton that is used in the union meshing algorithm
        self.skeleton_shape = nmv.enums.Meshing.UnionMeshing.QUAD_SKELETON

        # SPINES OPTIONS ###########################################################################
        # The source where the spines will be loaded from, by default ignore the spines
        self.spines = nmv.enums.Meshing.Spines.Source.IGNORE

        # Spines mesh quality, by default low quality
        self.spines_mesh_quality = nmv.enums.Meshing.Spines.Quality.LQ

        # Number of random spines per micron
        self.number_spines_per_micron = nmv.consts.Meshing.NUMBER_SPINES_PER_MICRON

        # NUCLEI OPTIONS ###########################################################################
        # Nucleus, ignore by default
        self.nucleus = nmv.enums.Meshing.Nucleus.IGNORE

        # Nucleus mesh quality, by default low quality
        self.nucleus_mesh_quality = nmv.enums.Meshing.Nucleus.Quality.LQ

        # MESH EXPORT ##############################################################################
        # Save the reconstructed mesh as a .ply file to the output directory
        self.export_ply = False

        # Save the reconstructed mesh as a .obj file to the output directory
        self.export_obj = False

        # Save the reconstructed mesh as a .stl file to the output directory
        self.export_stl = False

        # Save the reconstructed mesh as a .blend file to the output directory
        self.export_blend = False

        # Export individual objects of the neurons to separate meshes
        self.export_individuals = False

####################################################################################################
# Copyright (c) 2016 - 2019, EPFL / Blue Brain Project
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
import copy

# Blender imports
import bpy

# Internal imports
import nmv.enums
import nmv.consts
import nmv.skeleton
import nmv.mesh
import nmv.shading
import nmv.scene
import nmv.utilities


####################################################################################################
# @MeshBuilderBase
####################################################################################################
class MeshBuilderBase:
    """Base class for all the mesh builders.
    Any mesh builder should inherit from this class, otherwise it will raise an error.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 morphology,
                 options,
                 builder_name):
        """Constructor

        :param morphology:
            A given morphology skeleton to create the mesh for.
        :param options:
            NeuroMorphoVis options.
        :param builder_name:
            The name of the mesh builder used to create the mesh.
        """

        # Morphology
        self.morphology = copy.deepcopy(morphology)

        # Loaded options from NeuroMorphoVis
        self.options = copy.deepcopy(options)

        # The name of the builder
        self.builder_name = builder_name

        # This flag is set to True if the resulting neuron, or astrocyte, mesh is entirely
        # represented by a single mesh object.
        self.result_is_single_object_mesh = False

        # A reference to the reconstructed soma mesh
        self.soma_mesh = None

        # A list of the reconstructed meshes of the apical dendrites
        self.apical_dendrites_meshes = list()

        # A list of the reconstructed meshes of the basal dendrites
        self.basal_dendrites_meshes = list()

        # A list of the reconstructed meshes of the axon
        self.axons_meshes = list()

        # A list of the endfeet meshes, if exist
        self.endfeet_meshes = list()

        # A list of the spine meshes, if exist
        self.spines_meshes = list()

        # A list of all the neuron/astrocyte meshes that are reconstructed
        self.neuron_meshes = list()

        # A reference to the neuron mesh after its creation
        self.neuron_mesh = None

        # A list of the colors/materials of the soma, or the entire membrane
        self.soma_materials = None

        # A list of the colors/materials of the axon
        self.axons_materials = None

        # A list of the colors/materials of the basal dendrites
        self.basal_dendrites_materials = None

        # A list of the colors/materials of the apical dendrite
        self.apical_dendrites_materials = None

        # A list of all the materials of the endfeet
        self.endfeet_materials = None

        # A list of the colors/materials of the spines
        self.spines_materials = None

        # All lights created in the scene
        self.lights = None

        # Statistics
        self.profiling_statistics = ''

        # Stats. about the morphology
        self.morphology_statistics = 'Morphology: \n'

        # Stats. about the mesh
        self.mesh_statistics = ''

        # Profiling function object
        self.PROFILE = nmv.utilities.profile_function

    ################################################################################################
    # @clear_meshes_lists
    ################################################################################################
    def clear_meshes_lists(self):
        """Clear all the lists of the meshes. This operation is done after a joint operation."""

        self.axons_meshes.clear()
        self.basal_dendrites_meshes.clear()
        self.apical_dendrites_meshes.clear()
        self.endfeet_meshes.clear()
        self.spines_meshes.clear()
        self.neuron_meshes.clear()

    ################################################################################################
    # @clear_materials
    ################################################################################################
    def clear_materials(self):
        """Clears existing morphology materials."""

        for material in bpy.data.materials:
            if self.morphology.code in material.name:
                nmv.scene.delete_material(material=material)

    ################################################################################################
    # @create_soma_materials
    ################################################################################################
    def create_soma_materials(self):
        """Creates the materials of the soma."""

        self.soma_materials = nmv.shading.create_materials(
            material_type=self.options.shading.mesh_material,
            name='Soma Mesh [%s]' % self.morphology.code,
            color=self.options.shading.mesh_soma_color)

    ################################################################################################
    # @create_axons_materials
    ################################################################################################
    def create_axons_materials(self):
        """Creates the materials of the axons."""

        self.axons_materials = nmv.shading.create_materials(
            material_type=self.options.shading.mesh_material,
            name='Axon Mesh [%s]' % self.morphology.code,
            color=self.options.shading.mesh_axons_color)

    ################################################################################################
    # @create_basal_dendrites_materials
    ################################################################################################
    def create_basal_dendrites_materials(self):
        """Creates the materials of the basal dendrites."""

        self.basal_dendrites_materials = nmv.shading.create_materials(
            material_type=self.options.shading.mesh_material,
            name='Basal Dendrites Mesh [%s]' % self.morphology.code,
            color=self.options.shading.mesh_basal_dendrites_color)

    ################################################################################################
    # @create_apical_dendrites_materials
    ################################################################################################
    def create_apical_dendrites_materials(self):
        """Creates the materials of the apical dendrites."""

        self.apical_dendrites_materials = nmv.shading.create_materials(
            material_type=self.options.shading.mesh_material,
            name='Apical Dendrites Mesh [%s]' % self.morphology.code,
            color=self.options.shading.mesh_apical_dendrites_color)

    ################################################################################################
    # @create_spines_materials
    ################################################################################################
    def create_spines_materials(self):
        """Creates the materials of the spines."""

        self.spines_materials = nmv.shading.create_materials(
            material_type=self.options.shading.mesh_material,
            name='Spines Mesh [%s]' % self.morphology.code,
            color=self.options.shading.mesh_spines_color)

    ################################################################################################
    # @create_endfeet_materials
    ################################################################################################
    def create_endfeet_materials(self):
        """Creates the materials of the astrocytic endfeet."""

        self.endfeet_materials = nmv.skeleton.create_multiple_materials_with_same_color(
            name='Endfeet Mesh [%s]' % self.morphology.code,
            material_type=self.options.shading.mesh_material,
            color=self.options.shading.mesh_endfeet_color,
            number_elements=1)

    ################################################################################################
    # @create_skeleton_materials
    ################################################################################################
    def create_skeleton_materials(self):
        """Create the materials that will be used to shade the mesh objects."""

        # Initially, delete the old materials
        self.clear_materials()

        # Create all the skeleton materials
        self.create_soma_materials()
        self.create_axons_materials()
        self.create_basal_dendrites_materials()
        self.create_apical_dendrites_materials()
        self.create_endfeet_materials()

    ################################################################################################
    # @create_illumination
    ################################################################################################
    def create_illumination(self):
        """Creates the illumination sources that correspond to the selected shader."""

        # Clear the lights
        if self.lights is not None:
            nmv.scene.delete_list_objects(object_list=self.lights)

        # Create an illumination specific for the given material
        self.lights = nmv.shading.create_material_specific_illumination(
            self.options.shading.mesh_material)

        # Create a new collection from the created lights
        nmv.utilities.create_collection_with_objects(name='Illumination', objects_list=self.lights)

    ################################################################################################
    # @resample_skeleton_sections
    ################################################################################################
    def resample_skeleton_sections(self):
        """Resamples the sections of the morphology skeleton before drawing it. Note that the
        resampling process is performed on a per-section basis, therefore the first and last samples
        of the section are left intact.
        """

        nmv.skeleton.resample_skeleton(
            morphology=self.morphology, morphology_options=self.options.morphology)

    ################################################################################################
    # @remove_arbors_samples_inside_soma
    ################################################################################################
    def remove_arbors_samples_inside_soma(self):
        """Removes the internal arbor samples that are considered located inside the soma."""

        nmv.logger.info('Removing Internal Samples')
        nmv.skeleton.ops.apply_operation_to_morphology(
            *[self.morphology, nmv.skeleton.ops.remove_samples_inside_soma,
              self.morphology.soma.centroid])

    ################################################################################################
    # @update_morphology_skeleton
    ################################################################################################
    def update_morphology_skeleton(self):
        """Verifies and repairs the morphology if the contain any artifacts that would potentially
        affect the reconstruction quality of the mesh.

        NOTE: The filters or operations performed in this builder are only specific to it. Other
        builders might apply a different set of filters.
        """

        # Remove internal samples
        self.remove_arbors_samples_inside_soma()

        # Resample the sections of the morphology skeleton
        self.resample_skeleton_sections()

        # Radii
        nmv.skeleton.update_arbors_radii(
            morphology=self.morphology, morphology_options=self.options.morphology)

        # Branching
        nmv.skeleton.update_skeleton_branching(morphology=self.morphology,
                                               branching_method=self.options.morphology.branching)

        # Update the style of the arbors
        nmv.skeleton.ops.update_arbors_style(
            morphology=self.morphology, arbor_style=self.options.morphology.arbor_style)

    ################################################################################################
    # @reconstruct_meta_soma_mesh
    ################################################################################################
    def reconstruct_meta_soma_mesh(self):
        """Reconstructs a soma mesh using the SomaMetaBuilder."""

        # Create a builder object and reconstruct the soma mesh
        builder = nmv.builders.SomaMetaBuilder(morphology=self.morphology, options=self.options)
        self.soma_mesh = builder.reconstruct_soma_mesh(apply_shader=False)

        # Add the soma mesh to the meshes list
        self.neuron_meshes.append(self.soma_mesh)

    ################################################################################################
    # @reconstruct_soft_body_soma_mesh
    ################################################################################################
    def reconstruct_soft_body_soma_mesh(self):
        """Reconstructs a soma mesh using the SomaSoftBodyBuilder."""

        # Create a builder object and reconstruct the soma mesh
        builder = nmv.builders.SomaSoftBodyBuilder(morphology=self.morphology, options=self.options)
        self.soma_mesh = builder.reconstruct_soma_mesh(apply_shader=False)

        # Add to the meshes list
        self.neuron_meshes.append(self.soma_mesh)

    ################################################################################################
    # @reconstruct_soma_mesh
    ################################################################################################
    def reconstruct_soma_mesh(self):
        """Reconstruct the mesh of the soma."""

        if self.options.mesh.soma_type == nmv.enums.Soma.Representation.META_BALLS:
            self.reconstruct_meta_soma_mesh()
        else:
            self.reconstruct_soft_body_soma_mesh()

        # Apply the shader to the reconstructed soma mesh
        nmv.shading.set_material_to_object(self.soma_mesh, self.soma_materials[0])

    ################################################################################################
    # @get_neuron_mesh_objects
    ################################################################################################
    def get_neuron_mesh_objects(self,
                                exclude_spines=False):
        """Gets a list of all the objects that belong to the neuron mesh. If all the objects are all
        connected into a single object, it will be returned as a single item in a list.

        :param exclude_spines:
            Exclude the spine meshes from this selection since they have a very special treatment.
        :return:
            A list of all the mesh objects that belong to the neuron
        """

        # Prepare the list
        neuron_mesh_objects = list()

        # Query the objects in the scene
        for scene_object in bpy.context.scene.objects:

            # Only select meshes
            if scene_object.type == 'MESH':

                # Exclude the spines
                if not exclude_spines:
                    if 'spine' in scene_object.name:
                        neuron_mesh_objects.append(scene_object)

                if 'Apical' in scene_object.name or \
                    'Basal' in scene_object.name or \
                    'Axon' in scene_object.name or \
                    'Soma' in scene_object.name or \
                    'Endfoot' in scene_object.name or \
                        self.morphology.label in scene_object.name:
                    neuron_mesh_objects.append(scene_object)

        # Return the list
        return neuron_mesh_objects

    ################################################################################################
    # @adjust_texture_mapping_of_all_meshes
    ################################################################################################
    def adjust_texture_mapping_of_all_meshes(self,
                                             texspace_size=5.0):
        """Adjusts the UV mapping of the meshes. This operation is recommended to be called after
        any mesh operation.

        :param texspace_size:
            Texture space size, by default 5.0.
        """

        # Get a list of all the neurons in the scene
        mesh_objects = self.get_neuron_mesh_objects(exclude_spines=False)

        # Adjust the mapping of all the meshes
        nmv.shading.adjust_materials_uv(mesh_objects=mesh_objects, texspace_size=texspace_size)

    ################################################################################################
    # @collect_morphology_stats
    ################################################################################################
    def collect_morphology_stats(self):
        """Collects the stats. of the morphology skeleton.
        """

        self.morphology_statistics += '\t* Soma: ' + 'Found \n' \
            if self.morphology.soma is not None else 'Not Found \n'
        if self.morphology.apical_dendrites is not None:
            self.morphology_statistics += '\t* Apical Dendrites: %d \n' \
                                             % len(self.morphology.apical_dendrites)
        else:
            self.morphology_statistics += '\t* Apical Dendrites: 0 \n'

        if self.morphology.basal_dendrites is not None:
            self.morphology_statistics += '\t* Basal Dendrites: %d \n' \
                                             % len(self.morphology.basal_dendrites)
        else:
            self.morphology_statistics += '\t* Basal Dendrites: 0 \n'

        if self.morphology.axons is not None:
            self.morphology_statistics += '\t* Axons: %d \n' \
                                             % len(self.morphology.axons)
        else:
            self.morphology_statistics += '\t* Axons: 0 \n'

    ################################################################################################
    # @create_skeleton_materials
    ################################################################################################
    def collect_mesh_stats(self):
        """Collects the stats. of the reconstructed mesh.
        """

        # Get neuron objects
        neuron_mesh_objects = self.get_neuron_mesh_objects(exclude_spines=False)

        total_vertices = 0
        total_polygons = 0

        # Do it mesh by mesh
        for i, neuron_mesh_object in enumerate(neuron_mesh_objects):
            vertices = len(neuron_mesh_object.data.vertices)
            polygons = len(neuron_mesh_object.data.polygons)

            total_vertices += vertices
            total_polygons += polygons

            self.mesh_statistics += '\t' + neuron_mesh_object.name + \
                                   ': Polygons [%d], ' % polygons + 'Vertices [%d] \n' % vertices

        self.mesh_statistics += \
            '\tTotal : Polygons [%d], ' % total_polygons + 'Vertices [%d] \n' % total_vertices

    ################################################################################################
    # @write_statistics_to_file
    ################################################################################################
    def write_statistics_to_file(self,
                                 tag):
        """Write the profiling stats. and also the mesh stats to file.

        :param tag:
            A label that will be used to tag the stats. file.
        """

        # Collect the morphology stats.
        self.collect_morphology_stats()

        # Write the stats to file
        if self.options.io.statistics_directory is None:
            return
        if not nmv.file.ops.path_exists(self.options.io.statistics_directory):
            nmv.file.ops.clean_and_create_directory(self.options.io.statistics_directory)

        # Open the stats. file
        stats_file = open('%s/%s-%s.stats' % (self.options.io.statistics_directory,
                                              self.morphology.label, tag), 'w')

        # Write the data
        stats_file.write(self.morphology_statistics)
        stats_file.write('\n')
        stats_file.write(self.profiling_statistics)
        stats_file.write('\n')
        stats_file.write(self.mesh_statistics)

        # Close the file
        stats_file.close()

    ################################################################################################
    # @transform_to_global_coordinates
    ################################################################################################
    def transform_to_global_coordinates(self):
        """Transforms the neuron mesh to the global coordinates.

        NOTE: Spine transformation is already implemented by the spine builder, and therefore
        this function applies only to the arbors and the soma.
        """

        return

        # Transform the arbors to the global coordinates if required for a circuit
        if self.options.morphology.global_coordinates or not self.options.morphology.center_at_origin:

            # Ignore if no information is given
            if self.options.morphology.gid is None and self.morphology.original_center is None:
                return

            # Make sure that a GID is selected
            if self.options.morphology.gid is not None:
                nmv.logger.info('Transforming to global coordinates')

                # Get neuron objects
                neuron_mesh_objects = self.get_neuron_mesh_objects(exclude_spines=False)

                # Do it mesh by mesh
                for i, neuron_mesh_object in enumerate(neuron_mesh_objects):
                    # Show the progress
                    nmv.utilities.show_progress(
                        '* Transforming to global coordinates', float(i),
                        float(len(neuron_mesh_objects)))

                    # Transforming to global coordinates
                    nmv.skeleton.ops.transform_to_global_coordinates(
                        mesh_object=neuron_mesh_object,
                        blue_config=self.options.morphology.blue_config,
                        gid=self.options.morphology.gid)

                # Show the progress
                nmv.utilities.show_progress('* Transforming to global coordinates', 0, 0,
                                            done=True)

                # Don't proceed
                return

            # If the original center is updated
            if self.morphology.original_center is not None:
                nmv.logger.info('Transforming to global coordinates')

                # Get neuron objects
                neuron_mesh_objects = self.get_neuron_mesh_objects(exclude_spines=False)

                # Do it mesh by mesh
                for i, mesh_object in enumerate(neuron_mesh_objects):
                    # Progress
                    nmv.utilities.show_progress('* Transforming to global coordinates',
                                                float(i),
                                                float(len(neuron_mesh_objects)))

                    # Translate the object
                    nmv.scene.translate_object(scene_object=mesh_object,
                                               shift=self.morphology.original_center)

    ################################################################################################
    # @decimate_neuron_mesh
    ################################################################################################
    def decimate_neuron_mesh(self):
        """Decimates the reconstructed neuron mesh.
        """

        # Ensure that the tessellation level is within range
        if 0.01 < self.options.mesh.tessellation_level < 1.0:
            nmv.logger.info('Decimating Mesh')

            # Get neuron objects
            neuron_mesh_objects = self.get_neuron_mesh_objects(exclude_spines=True)

            # Do it mesh by mesh
            for i, neuron_mesh_object in enumerate(neuron_mesh_objects):

                # Show the progress
                nmv.utilities.show_progress(
                    '* Decimating the mesh', float(i), float(len(neuron_mesh_objects)))

                # Decimate each mesh object
                nmv.mesh.ops.decimate_mesh_object(
                    mesh_object=neuron_mesh_object,
                    decimation_ratio=self.options.mesh.tessellation_level)

            # Show the progress
            nmv.utilities.show_progress('* Decimating the mesh', 0, 0, done=True)

            # Adjust the texture mapping
            nmv.shading.adjust_materials_uv(neuron_mesh_objects)

    ################################################################################################
    # @add_surface_noise_to_arbor
    ################################################################################################
    def add_surface_noise_to_arbor(self):
        """Adds noise to the surface of the arbors of the reconstructed mesh(es).
        """

        meshing_technique = self.options.mesh.meshing_technique

        if self.options.mesh.surface == nmv.enums.Meshing.Surface.ROUGH:
            nmv.logger.info('Adding surface roughness to arbors')

            # Get a list of all the meshes of the reconstructed arbors
            mesh_objects = self.get_neuron_mesh_objects()

            # The soma is already reconstructed with high number of subdivisions for accuracy,
            # and the arbors are reconstructed with minimal number of samples that is sufficient to
            # make them smooth. Therefore, we must add the noise around the soma and its connections
            # to the arbors (the stable extent) with a different amplitude.
            stable_extent_center, stable_extent_radius = \
                nmv.skeleton.ops.get_stable_soma_extent_for_morphology(self.morphology)

            # The subdivision parameters are based on the mesh builder

            if meshing_technique == nmv.enums.Meshing.Technique.PIECEWISE_WATERTIGHT:
                for mesh_object in mesh_objects:
                    nmv.mesh.smooth_object(mesh_object=mesh_object, level=1)
                    nmv.mesh.add_surface_noise_to_mesh(
                        mesh_object=mesh_object, subdivision_level=0, noise_strength=1.0)

            elif meshing_technique == nmv.enums.Meshing.Technique.SKINNING:
                for mesh_object in mesh_objects:
                    nmv.mesh.add_surface_noise_to_mesh(
                        mesh_object=mesh_object, subdivision_level=0, noise_strength=1.0)

            elif meshing_technique == nmv.enums.Meshing.Technique.UNION:
                for mesh_object in mesh_objects:
                    nmv.mesh.add_surface_noise_to_mesh(
                        mesh_object=mesh_object, subdivision_level=0, noise_strength=1.0)
                    nmv.mesh.decimate_mesh_object(mesh_object=mesh_object, decimation_ratio=0.25)
                    nmv.mesh.decimate_mesh_object(mesh_object=mesh_object, decimation_ratio=0.25)
                    nmv.mesh.decimate_mesh_object(mesh_object=mesh_object, decimation_ratio=0.5)
                    # Smooth using Catmull-Clark subdivision
                    nmv.mesh.smooth_object(mesh_object=mesh_object, level=1)
            else:
                return
        else:

            # Get a list of all the meshes of the reconstructed arbors
            mesh_objects = self.get_neuron_mesh_objects()

            #if meshing_technique == nmv.enums.Meshing.Technique.UNION:
            #    for mesh_object in mesh_objects:
            #        clean_union_operator_reconstructed_surface(mesh_object=mesh_object)

    ################################################################################################
    # @adjust_origins_to_soma_center
    ################################################################################################
    def adjust_origins_to_soma_center(self):

        for i_mesh in self.apical_dendrites_meshes:
            nmv.mesh.set_mesh_origin(
                mesh_object=i_mesh, coordinate=self.morphology.soma.centroid)

        for i_mesh in self.basal_dendrites_meshes:
            nmv.mesh.set_mesh_origin(
                mesh_object=i_mesh, coordinate=self.morphology.soma.centroid)

        for i_mesh in self.axons_meshes:
            nmv.mesh.set_mesh_origin(
                mesh_object=i_mesh, coordinate=self.morphology.soma.centroid)

    ################################################################################################
    # @join_objects_and_adjust_origin
    ################################################################################################
    def join_objects_and_adjust_origin(self):
        """Join all the mesh objects in the scene into a single mesh.

        :return:
            A reference to the joint mesh.
        """

        # Are the objects connected or not
        connection = self.options.mesh.neuron_objects_connection
        if connection == nmv.enums.Meshing.ObjectsConnection.CONNECTED:

            # Join all the mesh objects into a single one
            self.neuron_mesh = nmv.mesh.join_mesh_objects(self.neuron_meshes, self.morphology.label)

            # Clear all the lists that contain references to the meshes, they are not valid anymore
            self.axons_meshes.clear()
            self.basal_dendrites_meshes.clear()
            self.apical_dendrites_meshes.clear()
            self.endfeet_meshes.clear()
            self.spines_meshes.clear()
            self.neuron_meshes.clear()

            # Adjust the origin of the resulting mesh
            nmv.mesh.set_mesh_origin(
                mesh_object=self.neuron_mesh, coordinate=self.morphology.soma.centroid)

            nmv.utilities.create_collection_with_objects(
                name='Mesh %s' % self.morphology.label, objects_list=[self.neuron_mesh])

            # Return a reference to the joint mesh object
            return self.neuron_mesh

        # If they are not connected, then adjust the origins only
        else:

            # Adjust the origin of the soma mesh
            nmv.mesh.set_mesh_origin(
                mesh_object=self.soma_mesh, coordinate=self.morphology.soma.centroid)

            # Adjust the origin of the apical dendrites meshes
            for i_mesh in self.apical_dendrites_meshes:
                nmv.mesh.set_mesh_origin(
                    mesh_object=i_mesh, coordinate=self.morphology.soma.centroid)

            # Adjust the origin of the basal dendrites meshes
            for i_mesh in self.basal_dendrites_meshes:
                nmv.mesh.set_mesh_origin(
                    mesh_object=i_mesh, coordinate=self.morphology.soma.centroid)

            # Adjust the origin of the axons meshes
            for i_mesh in self.axons_meshes:
                nmv.mesh.set_mesh_origin(
                    mesh_object=i_mesh, coordinate=self.morphology.soma.centroid)

            # Create a new collection from the created objects of the mesh
            nmv.utilities.create_collection_with_objects(
                name='Mesh %s' % self.morphology.label, objects_list=self.neuron_meshes)

    ################################################################################################
    # @add_spines_to_surface
    ################################################################################################
    def add_spines_to_surface(self,
                              join_spine_meshes=False):
        """Adds spines meshes to the surface mesh of the neuron.

        NOTE: The spines will just be added to the surface, but they will not get merged to the surface
        with any union operator.

        :param builder:
            An object of the builder that is used to reconstruct the neuron mesh.
        :param join_spine_meshes:
            Join all the spines meshes into a single mesh object for simplicity.
        """

        # Build spines from a BBP circuit
        if self.options.mesh.spines == nmv.enums.Meshing.Spines.Source.CIRCUIT:
            nmv.logger.info('Adding Spines from a BBP Circuit')
            spines_objects = nmv.builders.build_circuit_spines(
                morphology=self.morphology, blue_config=self.options.morphology.blue_config,
                gid=self.options.morphology.gid, material=self.spines_materials[0])

        # Just add some random spines for the look only
        elif self.options.mesh.spines == nmv.enums.Meshing.Spines.Source.RANDOM:
            nmv.logger.info('Adding Random Spines')
            spines_builder = nmv.builders.RandomSpineBuilder(
                morphology=self.morphology, options=self.options)
            spines_objects = spines_builder.add_spines_to_morphology()

        # Otherwise ignore spines
        else:
            return

        # Join the spine objects into a single mesh, if required
        if join_spine_meshes:
            spine_mesh_name = 'Spines [%s]' % self.options.morphology.label
            nmv.mesh.join_mesh_objects(spines_objects, spine_mesh_name)

    ################################################################################################
    # @modify_morphology_skeleton
    ################################################################################################
    def modify_morphology_skeleton(self):
        """Modifies the morphology skeleton, if required. These modifications are generic and not
        specific to any builder. Specific modifications can be implemented as a function in the
        corresponding builder.
        """

        # Taper the sections if requested
        if self.options.morphology.arbor_style == nmv.enums.Skeleton.Style.TAPERED or \
           self.options.morphology.arbor_style == nmv.enums.Skeleton.Style.TAPERED_ZIGZAG:
            nmv.skeleton.ops.apply_operation_to_morphology(
                *[self.morphology, nmv.skeleton.ops.taper_section])

        # Zigzag the sections if required
        if self.options.morphology.arbor_style == nmv.enums.Skeleton.Style.ZIGZAG or \
           self.options.morphology.arbor_style == nmv.enums.Skeleton.Style.TAPERED_ZIGZAG:
            nmv.skeleton.ops.apply_operation_to_morphology(
                *[self.morphology, nmv.skeleton.ops.zigzag_section])

    ################################################################################################
    # @select_arbor_to_soma_vertices
    ################################################################################################
    @staticmethod
    def select_arbor_to_soma_vertices(soma_mesh,
                                      arbor):
        """Selects a set of vertices to smooth an arbor that is connected to the soma.

        :param soma_mesh:
            A reference to the mesh object of the soma.
        :param arbor:
            A reference to the mesh object of the arbor.
        """

        # Get the arbor starting point at its initial segment
        branch_starting_point = arbor.samples[0].point

        # Get its direction
        branch_direction = arbor.samples[0].point.normalized()

        # The bridging point is computed
        bridging_point = branch_starting_point - 0.75 * branch_direction

        # The smoothing extent (radius) is assumed to be double that radius of the initial sample
        smoothing_extent = arbor.samples[0].radius * 2.0

        # Select the vertices that need to be smoothed
        nmv.mesh.ops.select_vertices_within_extent(
            mesh_object=soma_mesh, point=bridging_point, radius=smoothing_extent)

    ################################################################################################
    # @smooth_arbors_to_soma_connections
    ################################################################################################
    def smooth_arbors_to_soma_connections(self):
        """Smooths the connectivity between the arbors and the soma.

        :param builder:
            An object of the builder that is used to reconstruct the neuron mesh.
        """

        # Deselect all the objects in the scene
        nmv.scene.ops.deselect_all()

        # Select the soma object
        nmv.scene.ops.select_object(self.soma_mesh)

        # Deselect all the vertices of the section mesh, for safety !
        nmv.mesh.ops.deselect_all_vertices(self.soma_mesh)

        if self.options.mesh.soma_connection == nmv.enums.Meshing.SomaConnection.CONNECTED:

            # Connecting apical dendrites
            if not self.options.morphology.ignore_apical_dendrites:
                if self.morphology.has_apical_dendrites():
                    for arbor in self.morphology.apical_dendrites:
                        self.select_arbor_to_soma_vertices(soma_mesh=self.soma_mesh, arbor=arbor)

            # Connecting basal dendrites
            if not self.options.morphology.ignore_basal_dendrites:
                if self.morphology.has_basal_dendrites():
                    for arbor in self.morphology.basal_dendrites:
                        self.select_arbor_to_soma_vertices(soma_mesh=self.soma_mesh, arbor=arbor)

            # Connecting axons
            if not self.options.morphology.ignore_axons:
                if self.morphology.has_axons():
                    for arbor in self.morphology.axons:
                        self.select_arbor_to_soma_vertices(soma_mesh=self.soma_mesh, arbor=arbor)

        if self.options.mesh.soma_type == \
                nmv.enums.Soma.Representation.META_BALLS:
            # Apply the smoothing filter on the selected vertices
            nmv.mesh.ops.smooth_selected_vertices(mesh_object=self.soma_mesh, iterations=5)

        # Deselect all the vertices of the final mesh at the end
        nmv.mesh.ops.deselect_all_vertices(mesh_object=self.soma_mesh)

    ################################################################################################
    # @connect_arbors_to_soma
    ################################################################################################
    def connect_arbors_to_soma(self):
        """Connects the root section of a given arbor to the soma at its initial segment.

        This function checks if the arbor mesh is 'logically' connected to the soma or not,
        following to the initial validation steps that determines if the arbor has a valid
        connection point to the soma or not.
        If the arbor is 'logically' connected to the soma, this function returns immediately.
        The arbor is a Section object, see Section() @section.py.

        :param builder:
            An object of the builder that is used to reconstruct the neuron mesh.
        """

        # Determine the connection function
        if self.options.mesh.soma_type == \
                nmv.enums.Soma.Representation.SOFT_BODY:
            connection_function = nmv.skeleton.ops.connect_arbor_to_soft_body_soma
        elif self.options.mesh.soma_type == \
                nmv.enums.Soma.Representation.META_BALLS:
            connection_function = nmv.skeleton.ops.connect_arbor_to_meta_ball_soma
        else:
            nmv.logger.warning('No soma-to-arbor connection function is used')
            return

        if self.options.mesh.soma_connection == nmv.enums.Meshing.SomaConnection.CONNECTED:
            nmv.logger.info('Connecting arbors to soma')

            # Connecting axons
            if not self.options.morphology.ignore_axons:
                if self.morphology.has_axons():
                    for arbor in self.morphology.axons:
                        nmv.logger.detail(arbor.label)
                        self.soma_mesh = connection_function(self.soma_mesh, arbor)

            # Connecting apical dendrites
            if not self.options.morphology.ignore_apical_dendrites:
                if self.morphology.has_apical_dendrites():
                    for arbor in self.morphology.apical_dendrites:
                        nmv.logger.detail(arbor.label)
                        self.soma_mesh = connection_function(self.soma_mesh, arbor)

            # Connecting basal dendrites
            if not self.options.morphology.ignore_basal_dendrites:
                if self.morphology.has_basal_dendrites():
                    for arbor in self.morphology.basal_dendrites:
                        nmv.logger.detail(arbor.label)
                        self.soma_mesh = connection_function(self.soma_mesh, arbor)

            # Adjust the normals
            nmv.mesh.adjust_normals(mesh_object=self.soma_mesh)

        # Smooth the connections between the soma and the connected curves
        self.smooth_arbors_to_soma_connections()

        # Adjust the texture mapping after connecting the meshes together
        self.adjust_texture_mapping_of_all_meshes()

    ################################################################################################
    # @reconstruct_endfeet
    ################################################################################################
    def build_endfeet(self):
        """Reconstructs the endfeet geometry"""

        # Header
        nmv.logger.header('Reconstructing endfeet')

        # Build the endfoot mesh
        for endfoot in self.morphology.endfeet:

            # Append the resulting mesh to the resulting meshes
            if self.endfeet_meshes:
                endfoot_mesh = endfoot.create_geometry_with_metaballs(
                    material=self.endfeet_materials[0])
            else:
                endfoot_mesh = endfoot.create_geometry_with_metaballs()

            self.endfeet_meshes.append(endfoot_mesh)
            self.neuron_meshes.append(endfoot_mesh)

    ################################################################################################
    # @assign_material_to_single_object_mesh
    ################################################################################################
    def assign_material_to_single_object_mesh(self):
        """Assigns the soma material, as an entire membrane material, to the meshes reconstructed
        in a single mesh object."""

        # Deselect all objects
        nmv.scene.ops.deselect_all()

        # Activate the mesh object
        nmv.scene.set_active_object(self.neuron_mesh)

        # Assign the material to the selected mesh
        nmv.shading.set_material_to_object(self.neuron_mesh, self.soma_materials[0])

        # Update the UV mapping
        nmv.shading.adjust_material_uv(self.neuron_mesh)

        # Activate the mesh object
        nmv.scene.set_active_object(self.neuron_mesh)

    ################################################################################################
    # @report_builder_statistics
    ################################################################################################
    def report_builder_statistics(self):
        """Reports the relevant performance statistics about the used mesh builder."""

        # Collect the statistics of the mesh building process
        self.collect_mesh_stats()

        # Add the statistics to the logger and display them
        nmv.logger.statistics(self.profiling_statistics)

        # Write the statistics to a file
        self.write_statistics_to_file(tag=self.builder_name)

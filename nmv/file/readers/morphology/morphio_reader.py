####################################################################################################
# Copyright (c) 2016 - 2024, EPFL / Blue Brain Project
# Author(s): Marwan Abdellah <marwan.abdellah@epfl.ch>
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
import numpy

# Blender imports
from mathutils import Vector

# Internal imports
import nmv
import nmv.bbox
import nmv.enums
import nmv.consts
import nmv.file
import nmv.skeleton
import nmv.utilities
import nmv.geometry
import nmv.mesh
import nmv.scene


####################################################################################################
# @MorphIOLoader
####################################################################################################
class MorphIOLoader:
    """A powerful morphology reader that uses the MorphIO library to load the neuronal morphologies.
    MorphIO is an open source project developed by the Blue Brain Project at EPFL. The code is
    available on GitHub: https://github.com/BlueBrain/MorphIO.
    Note that we use MorphIO to load morphologies in .ASC, .SWC and .H5 formats. The structure is
    then mapped to the NMV one.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 morphology_file,
                 morphology_format,
                 center_morphology=True):
        """Constructor

        :param morphology_file:
            A given path to the morphology file.
        :param center_morphology:
            If this flag is set to True, the morphology will be centered at the origin, i.e. the
            soma will be located at the origin.
        """

        # Set the path to the given morphology file irrespective to its extension
        self.morphology_file = morphology_file

        # The file format of the morphology
        self.morphology_format = morphology_format

        # If this flag is set, the soma of the neuron must be located at the origin
        self.center_morphology = center_morphology

        # A list of all the points in the morphology file, for bounding box computations
        self.points_list = list()

        # A list of sections that are extracted from the file for processing
        self.sections_list = list()

        # The radius of the soma as reported in the original morphology
        self.reported_soma_radius = None

        # The centroid of the soma as reported in the original morphology
        self.reported_soma_centroid = None

        # The final or actual radius of the soma after implementing the NMV logic
        self.soma_radius = None

        # The final centroid of the soma that is given to NMV.
        self.soma_centroid = None

        # A list of the soma profile points computed based on the initial segments of the arbors
        self.soma_profile_points = list()
        
        # The morphology label of the neuron 
        self.morphology_label = None
        
        # The morphology file format, this is used to determine the file format of the morphology
        self.morpholog_file_format = None
    
    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self, 
                 center_morphology=True):
        
        # If this flag is set, the soma of the neuron must be located at the origin
        self.center_morphology = center_morphology
        
        # A list of all the points in the morphology file, for bounding box computations
        self.points_list = list()

        # A list of sections that are extracted from the file for processing
        self.sections_list = list()

        # The radius of the soma as reported in the original morphology
        self.reported_soma_radius = None

        # The centroid of the soma as reported in the original morphology
        self.reported_soma_centroid = None

        # The final or actual radius of the soma after implementing the NMV logic
        self.soma_radius = None

        # The final centroid of the soma that is given to NMV.
        self.soma_centroid = None

        # A list of the soma profile points computed based on the initial segments of the arbors
        self.soma_profile_points = list()
        
    ################################################################################################
    # @build_soma
    ################################################################################################
    def build_soma(self,
                   axons_trees=None,
                   basal_dendrites_trees=None,
                   apical_dendrite_tree=None):
        """Builds the soma object and returns a reference to it.

        :param axons_trees:
            The reconstructed trees of the axons.
        :param basal_dendrites_trees:
            The reconstructed trees of the basal dendrites.
        :param apical_dendrite_tree:
            The reconstructed tree of the apical dendrite.
        :return:
            A reference to the soma object.
        """

        # Collect the profile points from all the arbors
        arbors_profile_points = list()

        # Axons profile points
        if axons_trees is not None:
            arbors_profile_points.extend(
                nmv.file.readers.morphology.common.get_arbors_profile_points(axons_trees))

        # Basal dendrites points
        if basal_dendrites_trees is not None:
            arbors_profile_points.extend(
                nmv.file.readers.morphology.common.get_arbors_profile_points(basal_dendrites_trees))

        # Apical dendrite profile point
        if apical_dendrite_tree is not None:
            arbors_profile_points.extend(
                nmv.file.readers.morphology.common.get_arbors_profile_points(apical_dendrite_tree))

        nmv_soma = nmv.skeleton.Soma(
            centroid=self.soma_centroid,
            mean_radius=self.soma_radius,
            reported_centroid=self.reported_soma_centroid,
            reported_mean_radius=self.reported_soma_radius,
            profile_points=self.soma_profile_points,
            arbors_profile_points=arbors_profile_points)

        # Return a reference to the NMV soma object
        return nmv_soma

    ################################################################################################
    # @read_single_point_soma
    ################################################################################################
    def read_single_point_soma(self,
                               morphio_soma):
        """Reads and gets the data for a single point soma.

        @param morphio_soma:
            The soma object of MorphIO
        """

        # Get the centroid
        center = morphio_soma.center
        self.reported_soma_centroid = Vector((center[0], center[1], center[2]))
        self.reported_soma_radius = morphio_soma.diameters[0] * 0.5

    ################################################################################################
    # @read_neuromorpho_three_point_cylinders_soma
    ################################################################################################
    def read_neuromorpho_three_point_cylinders_soma(self,
                                                    morphio_soma):
        """Reads and gets the data for a 3-point cylinder soma.

        @param morphio_soma:
            The soma object of MorphIO
        """

        self.read_soma_cylinders(morphio_soma=morphio_soma)

    ################################################################################################
    # @read_soma_cylinders
    ################################################################################################
    def read_soma_cylinders(self,
                            morphio_soma):
        """Reads and gets the data for a cylinders-based soma.

        @param morphio_soma:
            The soma object of MorphIO
        """

        # Get the centroid
        center = morphio_soma.center
        self.reported_soma_centroid = Vector((center[0], center[1], center[2]))

        # Detect the soma radius
        proxy_soma = list()
        for i, _point in enumerate(morphio_soma.points):

            # Construct a point vector and get the radius of the point
            _point = _point.tolist()
            x = float(_point[0])
            y = float(_point[1])
            z = float(_point[2])
            point = Vector((x, y, z))
            r = float(morphio_soma.diameters[i] * 0.5)

            # Create an ico sphere and add it to a proxy object
            proxy_soma.append(nmv.geometry.create_ico_sphere(radius=r, location=point, subdivisions=2))

        # Construct an outer shell of the proxy soma
        proxy_soma = nmv.mesh.join_mesh_objects(proxy_soma, name='proxy')
        nmv.mesh.apply_voxelization_remeshing_modifier(
            mesh_object=proxy_soma, voxel_size=1.0, adaptivity=False)

        # Gather the points of the proxy soma that make the profile points
        for _point in proxy_soma.data.vertices:
            self.soma_profile_points.append(proxy_soma.matrix_world @ _point.co)

        # Delete the proxy soma, not needed any further
        nmv.scene.delete_object_in_scene(scene_object=proxy_soma)

        # Compute the average soma radius from the profile points
        if len(self.soma_profile_points) > 0:
            self.reported_soma_radius = 0
            for _point in self.soma_profile_points:
                self.reported_soma_radius += (_point - self.reported_soma_centroid).length
            self.reported_soma_radius /= len(self.soma_profile_points)

    ################################################################################################
    # @read_simple_contour_soma
    ################################################################################################
    def read_simple_contour_soma(self,
                                 morphio_soma):
        """Reads and gets the data for contour-based soma.

        @param morphio_soma:
            The soma object of MorphIO
        """

        # Get the centroid
        center = morphio_soma.center
        self.reported_soma_centroid = Vector((center[0], center[1], center[2]))

        # Detect the soma radius
        for _point in morphio_soma.points:
            _point = _point.tolist()
            x = float(_point[0])
            y = float(_point[1])
            z = float(_point[2])
            self.soma_profile_points.append(Vector((x, y, z)))

        # Compute the average soma radius from the profile points
        if len(self.soma_profile_points) > 0:
            self.reported_soma_radius = 0
            for _point in self.soma_profile_points:
                self.reported_soma_radius += (_point - self.reported_soma_centroid).length
            self.reported_soma_radius /= len(self.soma_profile_points)

    ################################################################################################
    # @read_soma_data
    ################################################################################################
    def read_soma_data(self,
                       morphio_soma):
        """Reads the soma data.

        @param morphio_soma:
            The soma object of MorphIO
        @note https://neuromorpho.org/SomaFormat.html
        """

        import morphio

        # Just a single point
        if morphio_soma.type == morphio.SomaType.SOMA_SINGLE_POINT:
            self.read_single_point_soma(morphio_soma=morphio_soma)

        # NeuroMorpho.Org format
        elif morphio_soma.type == morphio.SomaType.SOMA_NEUROMORPHO_THREE_POINT_CYLINDERS:
            self.read_neuromorpho_three_point_cylinders_soma(morphio_soma=morphio_soma)

        # The cylinders description
        elif morphio_soma.type == morphio.SomaType.SOMA_CYLINDERS:
            self.read_soma_cylinders(morphio_soma=morphio_soma)

        # The contour used in H5 and ASCII
        elif morphio_soma.type == morphio.SomaType.SOMA_SIMPLE_CONTOUR:
            self.read_simple_contour_soma(morphio_soma=morphio_soma)


        else:
            self.reported_soma_radius = 3


        return
        # Detect the soma radius
        for i_point in morphio_soma.points:
            i_point = i_point.tolist()
            x = float(i_point[0])
            y = float(i_point[1])
            z = float(i_point[2])
            self.soma_profile_points.append(Vector((x, y, z)))

        # Compute the average soma radius from the profile points
        if len(self.soma_profile_points) > 0:
            self.reported_soma_radius = 0
            for i_point in self.soma_profile_points:
                nmv.geometry.create_uv_sphere(radius=0.5, location=i_point)
                nmv.geometry.draw_line(i_point,  self.reported_soma_centroid)
                self.reported_soma_radius += (i_point - self.reported_soma_centroid).length
            self.reported_soma_radius /= len(self.soma_profile_points)

    ################################################################################################
    # @read_data_from_morphio_morphology
    ################################################################################################
    def read_data_from_morphio_morphology_object(self, morphio_morphology):
        
        import morphio
        import numpy as np
        from mathutils import Vector
        import nmv.consts
        import nmv.skeleton
        import nmv.file.readers.morphology.common
        
        # Read soma data
        self.read_soma_data(morphio_soma=morphio_morphology.soma)
        self.soma_radius = self.reported_soma_radius

        # Determine translation vector for centering
        translation_vector = self.reported_soma_centroid if self.center_morphology else nmv.consts.Math.ORIGIN
        self.soma_centroid = nmv.consts.Math.ORIGIN if self.center_morphology else self.reported_soma_centroid

        # Initialize lists
        points_list = []
        nmv_sections = []
        axons_sections = []
        basal_dendrites_sections = []
        apical_dendrites_sections = []

        # Map morphio section types to NMV section types
        section_type_map = {
            morphio.SectionType.axon: nmv.consts.Skeleton.NMV_AXON_SECTION_TYPE,
            morphio.SectionType.basal_dendrite: nmv.consts.Skeleton.NMV_BASAL_DENDRITE_SECTION_TYPE,
            morphio.SectionType.apical_dendrite: nmv.consts.Skeleton.NMV_APICAL_SECTION_TYPE
        }

        # Process sections in a single pass
        for section in morphio_morphology.sections:
            # Get section properties
            section_id = section.id
            section_parent_id = None if section.is_root else section.parent.id
            section_children_ids = [child.id for child in section.children]

            # Determine section type (default to basal dendrite for unknown types)
            section_type = section_type_map.get(section.type, nmv.consts.Skeleton.NMV_BASAL_DENDRITE_SECTION_TYPE)

            # Vectorize point translation
            points = np.array(section.points) - np.array(translation_vector)
            points_list.extend([Vector((p[0], p[1], p[2])) for p in points])

            # Create section samples
            section_samples = [
                nmv.skeleton.Sample(
                    point=Vector((points[i][0], points[i][1], points[i][2])),
                    radius=section.diameters[i] * 0.5,
                    index=i,
                    morphology_id=0,
                    type=section_type,
                    parent_index=i + 1
                ) for i in range(len(points))
            ]

            # Create NMV section
            nmv_section = nmv.skeleton.Section(
                index=section_id,
                parent_index=section_parent_id,
                children_ids=section_children_ids,
                samples=section_samples,
                type=section_type
            )
            nmv_sections.append(nmv_section)

            # Filter sections by type
            if section_type == nmv.consts.Skeleton.NMV_AXON_SECTION_TYPE:
                axons_sections.append(nmv_section)
            elif section_type == nmv.consts.Skeleton.NMV_APICAL_SECTION_TYPE:
                apical_dendrites_sections.append(nmv_section)
            else:
                basal_dendrites_sections.append(nmv_section)

        # Update instance points_list
        self.points_list = points_list
        self.sections_list = nmv_sections

        # Build arbor trees
        nmv.file.readers.morphology.common.build_tree(axons_sections)
        nmv.file.readers.morphology.common.build_tree(basal_dendrites_sections)
        nmv.file.readers.morphology.common.build_tree(apical_dendrites_sections)

        # Build arbors
        axons = nmv.skeleton.ops.build_arbors_from_sections(axons_sections)
        basal_dendrites = nmv.skeleton.ops.build_arbors_from_sections(basal_dendrites_sections)
        apical_dendrites = nmv.skeleton.ops.build_arbors_from_sections(apical_dendrites_sections)

        # Helper function for labeling and tagging
        def label_arbors(arbors, base_label, base_tag):
            if arbors:
                if len(arbors) == 1:
                    arbors[0].label = base_label
                    arbors[0].tag = base_tag
                else:
                    for i, arbor in enumerate(arbors, 1):
                        arbor.label = f"{base_label} {i}"
                        arbor.tag = f"{base_tag}{i}"

        # Label arbors
        label_arbors(apical_dendrites, "Apical Dendrite", "ApicalDendrite")
        label_arbors(basal_dendrites, "Basal Dendrite", "BasalDendrite")
        label_arbors(axons, "Axon", "Axon")

        # Build soma
        soma = self.build_soma(
            axons_trees=axons,
            basal_dendrites_trees=basal_dendrites,
            apical_dendrite_tree=apical_dendrites
        )

        # Construct NMV morphology
        nmv_morphology = nmv.skeleton.Morphology(
            soma=soma,
            axons=axons,
            basal_dendrites=basal_dendrites,
            apical_dendrites=apical_dendrites,
            label=self.morphology_label,
            file_format=self.morpholog_file_format
        )
        nmv_morphology.original_center = self.reported_soma_centroid

        return nmv_morphology
    '''
    def read_data_from_morphio_morphology_object(self,
                                                 morphio_morphology):
        
        # Import the required module
        import morphio
        
        # Get the soma parameters reported in the morphology file
        self.read_soma_data(morphio_soma=morphio_morphology.soma)

        # Determine the translation vector if it is required to center the morphology
        if self.center_morphology:
            translation_vector = self.reported_soma_centroid
            self.soma_centroid = nmv.consts.Math.ORIGIN
        else:
            translation_vector = nmv.consts.Math.ORIGIN
            self.soma_centroid = self.reported_soma_centroid

        self.soma_radius = self.reported_soma_radius

        # Build the points list
        for i_section in morphio_morphology.sections:
            for i_point in i_section.points:
                self.points_list.append(
                    Vector((i_point[0], i_point[1], i_point[2])) - translation_vector)

        # Linear lists of the sections for the axons, basal dendrites and apical dendrites
        axons_sections = list()
        basal_dendrites_sections = list()
        apical_dendrites_sections = list()

        # A linear list of all the sections, in NeuroMorphoVis format
        nmv_sections = list()
        for i_section in morphio_morphology.sections:

            # Get the section index and its parent section index
            section_id = i_section.id
            section_parent_id = None if i_section.is_root else i_section.parent.id

            # Get the children sections
            section_children_ids = list()
            if len(i_section.children) > 0:
                for child in i_section.children:
                    section_children_ids.append(child.id)

            # Get the section type
            if i_section.type == morphio.SectionType.axon:
                section_type = nmv.consts.Skeleton.NMV_AXON_SECTION_TYPE
            elif i_section.type == morphio.SectionType.basal_dendrite:
                section_type = nmv.consts.Skeleton.NMV_BASAL_DENDRITE_SECTION_TYPE
            elif i_section.type == morphio.SectionType.apical_dendrite:
                section_type = nmv.consts.Skeleton.NMV_APICAL_SECTION_TYPE
            else:
                # If this is not a standard section, draw it as a basal dendrite
                section_type = nmv.consts.Skeleton.NMV_BASAL_DENDRITE_SECTION_TYPE

            # Section samples
            section_samples = list()
            for i in range(len(i_section.points)):

                # Sample point
                sample_point = Vector((i_section.points[i][0] - translation_vector[0],
                                       i_section.points[i][1] - translation_vector[1],
                                       i_section.points[i][2] - translation_vector[2]))

                # Sample radius
                sample_radius = i_section.diameters[i] * 0.5

                # Sample type, is the same as the section type
                sample_type = section_type

                # Sample index, simply the index in the list
                sample_index = i

                # Parent ID, simply let it the current -1
                parent_sample_index = i + 1

                # Construct a NMV sample object and append it to the samples list of the section
                nmv_sample = nmv.skeleton.Sample(point=sample_point,
                                                 radius=sample_radius,
                                                 index=sample_index,
                                                 morphology_id=0,
                                                 type=sample_type,
                                                 parent_index=parent_sample_index)
                section_samples.append(nmv_sample)

            # Construct a NMV section object and append it to the sections list of the morphology
            nmv_section = nmv.skeleton.Section(index=section_id,
                                               parent_index=section_parent_id,
                                               children_ids=section_children_ids,
                                               samples=section_samples,
                                               type=section_type)
            self.sections_list.append(nmv_sections)

            # Filter the sections based on their type
            if i_section.type == morphio.SectionType.axon:
                axons_sections.append(nmv_section)
            elif i_section.type == morphio.SectionType.basal_dendrite:
                basal_dendrites_sections.append(nmv_section)
            elif i_section.type == morphio.SectionType.apical_dendrite:
                apical_dendrites_sections.append(nmv_section)
            else:
                # Add this UNKNOWN section type to the basal dendrites list
                basal_dendrites_sections.append(nmv_section)

        # Build the axons, basal dendrites and apical dendrites trees, i.e. assert parents-children
        nmv.file.readers.morphology.common.build_tree(axons_sections)
        nmv.file.readers.morphology.common.build_tree(basal_dendrites_sections)
        nmv.file.readers.morphology.common.build_tree(apical_dendrites_sections)

        # Get the root sections of axons, basal dendrites and apical dendrites
        axons = nmv.skeleton.ops.build_arbors_from_sections(axons_sections)
        basal_dendrites = nmv.skeleton.ops.build_arbors_from_sections(basal_dendrites_sections)
        apical_dendrites = nmv.skeleton.ops.build_arbors_from_sections(apical_dendrites_sections)

        # Labeling and tagging the apical dendrites
        if apical_dendrites is not None:
            if len(apical_dendrites) == 1:
                apical_dendrites[0].label = 'Apical Dendrite'
                apical_dendrites[0].tag = 'ApicalDendrite'
            else:
                for i in range(len(apical_dendrites)):
                    apical_dendrites[i].label = 'Apical Dendrite %d' % (i + 1)
                    apical_dendrites[i].tag = 'ApicalDendrite%d' % (i + 1)

        # Labeling the basal dendrites
        if basal_dendrites is not None:
            if len(basal_dendrites) == 1:
                basal_dendrites[0].label = 'Basal Dendrite'
                basal_dendrites[0].tag = 'BasalDendrite'
            else:
                for i in range(len(basal_dendrites)):
                    basal_dendrites[i].label = 'Basal Dendrite %d' % (i + 1)
                    basal_dendrites[i].tag = 'BasalDendrite%d' % (i + 1)

        # Labeling and tagging the axons
        if axons is not None:
            if len(axons) == 1:
                axons[0].label = 'Axon'
                axons[0].tag = 'Axon'
            else:
                for i in range(len(axons)):
                    axons[i].label = 'Axon %d' % (i + 1)
                    axons[i].tag = 'Axon%d' % (i + 1)

        # Build the soma, taking into consideration the arbors
        soma = self.build_soma(axons_trees=axons,
                               basal_dendrites_trees=basal_dendrites,
                               apical_dendrite_tree=apical_dendrites)

        # Construct the NMV morphology object
        nmv_morphology = nmv.skeleton.Morphology(
            soma=soma,
            axons=axons,
            basal_dendrites=basal_dendrites,
            apical_dendrites=apical_dendrites,
            label=self.morphology_label,
            file_format=self.morpholog_file_format)

        # Update the centroid
        nmv_morphology.original_center = self.reported_soma_centroid

        # Return a reference to the NMV morphology object
        return nmv_morphology
    '''
    
    ################################################################################################
    # @read_data_from_file
    ################################################################################################
    def read_data_from_file(self):
        """Loads the data from the given file in the constructor.

        This function returns None if the reading operation was unsuccessful.
        """

        # Import the required module
        from morphio import Morphology

        # Load the morphology data using MorphIO
        try:
            morphio_morphology = Morphology(self.morphology_file)
            
            # Updating the morphology label 
            self.morphology_label = nmv.file.ops.get_file_name_from_path(self.morphology_file)
            
            # Updating the file format 
            self.morpholog_file_format = nmv.file.ops.get_file_format_from_path(self.morphology_file)
            
            nmv.logger.log("The morphology file [%s] is loaded successfully" % self.morphology_file)
            return self.read_data_from_morphio_morphology_object(morphio_morphology=morphio_morphology)
        except IOError:
            nmv.logger.error("Cannot load morphology file! [%s]" % self.morphology_file)
            return None
        
    ################################################################################################
    # @read_data_from_morphio_morphology
    ################################################################################################
    def read_data_from_morphio_morphology(self, morphio_morphology, morphology_label):
        """Reads the data from a MorphIO morphology object.

        :param morphio_morphology:
            The MorphIO morphology object.
        :return:
            An NMV morphology object.
        """
        
        # Updating the morphology label 
        self.morphology_label = morphology_label
        
        # Set the file format tp Container 
        self.morpholog_file_format = "Container"
        
        return self.read_data_from_morphio_morphology_object(morphio_morphology=morphio_morphology)
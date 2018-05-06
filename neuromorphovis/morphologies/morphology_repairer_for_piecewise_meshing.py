####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
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

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2016 - 2018, Blue Brain Project / EPFL"
__credits__     = ["Ahmet Bilgili", "Juan Hernando", "Stefan Eilemann"]
__version__     = "1.0.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"


# System imports
import os, sys

# Blender imports
import bpy
from mathutils import Vector, Matrix

# Append the internal modules into the system paths
sys.path.append("%s/../modules" % os.path.dirname(os.path.realpath(__file__)))

# Internal imports
import enumerators
import morphology_ops
import morphology_repair_ops
import morphology_intersection_ops
import morphology_connection_ops
import morphology_analysis_ops


####################################################################################################
# @MorphologyRepairerForPiecewiseMeshing
####################################################################################################
class MorphologyRepairerForPiecewiseMeshing:

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 morphology,
                 branching_method=enumerators.__branching_angles__):
        """
        Constructor.

        :param morphology:
            Input morphology to be fixed.
        :param branching_method:
            The method that is used to label the primary and secondary branches.
        """

        # Morphology
        self.morphology = morphology

        # Branching method
        self.branching_method = branching_method

    ################################################################################################
    # @repair_arbor
    ################################################################################################
    def repair_arbor(self,
                     arbor):
        """
        Repair the arbor and make it suitable for meshing using the piecewise meshing tool.

        :param arbor: The root section of a given arbor.
        """

        # Analyze the arbor to label its primary and secondary branches
        morphology_connection_ops.label_primary_and_secondary_sections_of_arbor(
            section=arbor, branching_method=self.branching_method)

        # Remove 'internal' samples that are located within the soma extent
        self.remove_samples_inside_soma(arbor)

        # Re-sample the arbor
        self.resample_section(arbor)

        # Removing the doubles (or the samples that are so close)
        self.remove_doubles(arbor)

    ################################################################################################
    # @repair_apical_dendrite
    ################################################################################################
    def repair_apical_dendrite(self):
        """
        Repair the apical dendrite of the morphology, if exists.
        """

        # Check if the morphology has an apical dendrite or not
        if self.morphology.apical_dendrite is not None:

            # If yes, then repair it
            nmv.logger.log('\t* Apical dendrite')
            self.repair_arbor(self.morphology.apical_dendrite)

        # Otherwise, just give a note
        else:
            nmv.logger.log('\t\t* NOTE: This morphology does not have an apical dendrite')

    ################################################################################################
    # @analyze_basal_dendrites
    ################################################################################################
    def repair_basal_dendrites(self):
        """
        Repair the basal dendritic tree of the morphology, and report the issues.
        """

        # Check if the morphology has basal dendrites or not
        if self.morphology.dendrites is not None:

            # Do the analysis arbor by arbor
            for i, basal_dendrite in enumerate(self.morphology.dendrites):

                # If yes, then analyze each basal dendrite separately
                nmv.logger.log('\t* Basal dendrite [%d]' % i)
                self.repair_arbor(basal_dendrite)

        # Otherwise, give an error since the morphology must have at leat a single basal dendrite
        else:
            nmv.logger.log('\t\t* ERROR: This morphology does not have any basal dendrites')

    ################################################################################################
    # @repair_axon
    ################################################################################################
    def repair_axon(self):
        """
        Repair the axon of the morphology.
        """

        # Check if the morphology has an axon or not
        if self.morphology.axon is not None:

            # If yes, then repair it
            nmv.logger.log('\t* Axon')
            self.repair_arbor(self.morphology.axon)

        # Otherwise, give an error since the morphology must have an axon
        else:
            nmv.logger.log('\t\t* ERROR: This morphology does not have an axon')

    ################################################################################################
    # @repair
    ################################################################################################
    def repair(self):
        """
        Repair the morphology if required, and report all the repairs.
        """

        nmv.logger.log('**************************************************************************')
        nmv.logger.log('Repairing morphology')
        nmv.logger.log('**************************************************************************')

        # Repair the apical dendrite
        self.repair_apical_dendrite()

        # Repair the basal dendrites
        self.repair_basal_dendrites()

        # Repair the axon
        self.repair_axon()

        # The apical dendrite is always connected to the soma, if exists
        if self.morphology.apical_dendrite is not None:
            self.morphology.apical_dendrite.connected_to_soma = True

        # Verify that the axon is connected to the soma
        self.verify_axon_connection_to_soma()

        # Verify that the basal dendrites are connected to the soma
        self.verify_basal_dendrites_connection_to_soma()

    ################################################################################################
    # @remove_doubles
    ################################################################################################
    def remove_doubles(self,
                       section,
                       threshold=1.0):
        """
        If the section contains doubles (or samples that are very close), then remove them from the
        skeleton and report the issue.

        :param section: A root section, of a given arbor.
        :param threshold: A threshold distance.
        """

        # Compute the number of samples along the section BEFORE removing the duplicate samples
        initial_number_of_samples = len(section.samples)

        # Remove the duplicate samples
        morphology_repair_ops.remove_duplicate_samples_of_section(section, threshold)

        # Compute the number of samples along the section AFTER removing the duplicate samples
        final_number_of_samples = len(section.samples)

        # If some samples are removed, report the section number and the number of removed samples
        if final_number_of_samples < initial_number_of_samples:

            # Number of removed samples
            number_of_removed_samples = initial_number_of_samples - final_number_of_samples

            # Report the issue
            nmv.logger.log('\t\t* REPAIRING: Removing duplicate samples section [%s]: [%d] sample(s)' %
                  (str(section.id), number_of_removed_samples))

        # Iterate over the children
        for child in section.children:

            # Validate the rest of the skeleton of the arbor
            self.remove_doubles(child)

    ################################################################################################
    # @resample_section
    ################################################################################################
    def resample_section(self,
                         section):

        # Re-sample this section
        morphology_repair_ops.resample_section(section)

        # Iterate over the children
        for child in section.children:

            # Validate the rest of the skeleton of the arbor
            self.resample_section(child)

    ################################################################################################
    # @verify_axon_connection_to_soma
    ################################################################################################
    def verify_axon_connection_to_soma(self):
        """
        Verifies if the axon is connected to the soma or not.
        If the initial segment of the axon is located far-away from the soma, the axon is connected
        to the closest dendrite.
        The intersection between the axon and the dendrites is checked, the axon is connected to the
        closest dendrite that is intersecting with it.
        """

        # Report the verification process
        nmv.logger.log('\t* Axon connectivity to soma')

        # Ensure that presence of the axon in the morphology
        if self.morphology.axon is None:

            # Report the issue
            nmv.logger.log('\t\t* WARNING: This morphology does NOT have an axon')

            # Skip
            return

        # Is the axon disconnected from the soma !
        if morphology_connection_ops.is_arbor_disconnected_from_soma(self.morphology.axon):

            # Report the issue
            nmv.logger.log('\t\t* WARNING: The axon @ section [%d] is disconnected from the soma'
                  % self.morphology.axon.id)

            # Get the nearest arbor and sample to the axon initial segment
            nearest_sample = \
                morphology_connection_ops.find_nearest_dendritic_sample_to_axon(self.morphology)

            # Report the repair
            nmv.logger.log('\t\t* REPAIRING: The axon is re-connected to section [%d, %s] @ sample [%d]'
                  % (nearest_sample.section.id, nearest_sample.section.get_type_string(),
                     nearest_sample.id))

            # Mark the axon disconnected from the soma
            self.morphology.axon.connected_to_soma = False

            # Update the axon initial sample based on the nearest dendritic sample
            # The sample should have the same location
            self.morphology.axon.samples[0].point = nearest_sample.point

            # The sample should have a smaller radius to avoid the extrusion artifacts
            self.morphology.axon.samples[0].radius = nearest_sample.radius * 0.5

            # The axon is found not connected to the soma
            return

        # Is the axon intersecting with the apical dendrite, if exists !
        if self.morphology.apical_dendrite is not None:

            # Verify if the axon intersects with the apical dendrite
            if morphology_intersection_ops.axon_intersects_apical_dendrite(
                    axon=self.morphology.axon, apical_dendrite=self.morphology.apical_dendrite,
                    soma_radius=self.morphology.soma.mean_radius):

                # Report the issue
                nmv.logger.log('\t\t* WARNING: The axon @ section [%d] is intersecting with apical dendrite'
                      % self.morphology.axon.id)

                # Find the intersection sample
                nearest_sample = \
                    morphology_connection_ops.find_nearest_apical_dendritic_sample_to_axon(
                        self.morphology)

                # Report the repair
                nmv.logger.log('\t\t* REPAIRING: The axon @ section [%d] is re-connected to section '
                      '[%d, %s] @ sample [%d]' % (self.morphology.axon.id,
                                                  nearest_sample.section.id,
                                                  nearest_sample.section.get_type_string(),
                                                  nearest_sample.id))

                # Mark the axon disconnected from the soma
                self.morphology.axon.connected_to_soma = False

                # Update the axon initial sample based on the nearest dendritic sample
                # The sample should have the same location
                self.morphology.axon.samples[0].point = nearest_sample.point

                # The sample should have a smaller radius to avoid the extrusion artifacts
                self.morphology.axon.samples[0].radius = nearest_sample.radius * 0.5

                # The axon is found to be intersecting with the apical dendrite
                return

        # Is the axon intersecting with any basal dendrite !
        if morphology_intersection_ops.axon_intersects_dendrites(
                axon=self.morphology.axon, dendrites=self.morphology.dendrites,
                soma_radius=self.morphology.soma.mean_radius):

            # Report the issue
            nmv.logger.log('\t\t* WARNING: The axon @ section [%d] is intersecting with a basal dendrite'
                  % self.morphology.axon.id)

            # Find the intersection sample
            nearest_sample = morphology_connection_ops.find_nearest_basal_dendritic_sample_to_axon(
                    self.morphology)

            # Report the repair
            nmv.logger.log('\t\t* REPAIRING: The axon is re-connected to section [%d, %s] @ sample [%d]'
                  % (nearest_sample.section.id, nearest_sample.section.get_type_string(),
                     nearest_sample.id))

            # Mark the axon disconnected from the soma
            self.morphology.axon.connected_to_soma = False

            # Update the axon initial sample based on the nearest dendritic sample
            # The sample should have the same location
            self.morphology.axon.samples[0].point = nearest_sample.point

            # The sample should have a smaller radius to avoid the extrusion artifacts
            self.morphology.axon.samples[0].radius = nearest_sample.radius * 0.5

            # The axon is found to be intersecting with the apical dendrite
            return

        # Mark the axon connected to the soma
        self.morphology.axon.connected_to_soma = True

        nmv.logger.log('\t\t* NOTE: The axon @ section [%d] is connected to the soma' %
              self.morphology.axon.id)

    ################################################################################################
    # @verify_basal_dendrites_connection_to_soma
    ################################################################################################
    def verify_basal_dendrites_connection_to_soma(self):
        """
        Verifies if any basal dendrite is connected to the soma or not.
        The apical dendrite is always assumed to be connected to the soma since its large.
        """

        # Verify dendrite by dendrite
        for i_basal_dendrite, basal_dendrite in enumerate(self.morphology.dendrites):

            nmv.logger.log('\t* Basal dendrite [%d] connectivity to soma' % i_basal_dendrite)

            # Is the basal dendrite disconnected from the soma !
            if morphology_connection_ops.is_arbor_disconnected_from_soma(basal_dendrite):

                # Report the issue
                nmv.logger.log('\t\t* WARNING: The basal dendrite [%d] @ section [%d] is intersecting '
                      'with apical dendrite' % (i_basal_dendrite, basal_dendrite.id))

                # Get the nearest arbor and sample to the dendrite initial segment
                nearest_sample = \
                    morphology_connection_ops.find_nearest_dendritic_sample_to_axon(self.morphology)

                # Report the repair
                nmv.logger.log('\t\t* REPAIRING: The basal dendrite [%d] @ section [%d] is re-connected to '
                      'section [%d, %s] @ sample [%d]' %
                      (i_basal_dendrite,
                       basal_dendrite.id,
                       nearest_sample.section.id,
                       nearest_sample.section.get_type_string(),
                       nearest_sample.id))

                # Mark the basal dendrite disconnected from the soma
                basal_dendrite.connected_to_soma = False

                # Update the basal dendrite initial sample based on the nearest dendritic sample
                # The sample should have the same location
                basal_dendrite.samples[0].point = nearest_sample.point

                # The sample should have a smaller radius to avoid the extrusion artifacts
                basal_dendrite.samples[0].radius = nearest_sample.radius * 0.5

                # Done, next basal dendrite
                continue

            # Is the basal dendrite intersecting with the apical dendrite, if exists !
            if self.morphology.apical_dendrite is not None:

                # Verify if the axon intersects with the apical dendrite
                if morphology_intersection_ops.dendrite_intersects_apical_dendrite(
                        dendrite=basal_dendrite,
                        apical_dendrite=self.morphology.apical_dendrite,
                        soma_radius=self.morphology.soma.mean_radius):

                    # Find the intersection sample
                    nearest_sample = morphology_connection_ops.\
                        find_nearest_apical_dendritic_sample_to_basal_dendrite(
                        morphology=self.morphology, basal_dendrite=basal_dendrite)

                    # Report the issue
                    nmv.logger.log('\t\t* REPAIRING: The basal dendrite [%d] @ section [%d] is re-connected '
                          'to section [%d, %s] @ sample [%d]'
                          % (i_basal_dendrite,
                             basal_dendrite.id,
                             nearest_sample.section.id,
                             nearest_sample.section.get_type_string(),
                             nearest_sample.id))

                    # Mark the basal dendrite disconnected from the soma
                    basal_dendrite.connected_to_soma = False

                    # Update the axon initial sample based on the nearest dendritic sample
                    # The sample should have the same location
                    basal_dendrite.samples[0].point = nearest_sample.point

                    # The sample should have a smaller radius to avoid the extrusion artifacts
                    basal_dendrite.samples[0].radius = nearest_sample.radius * 0.5

                    # Done, next basal dendrite
                    continue

            # Is the basal dendrite intersecting with another basal dendrite !
            # NOTE: The intersection function returns a positive result if this input basal
            # dendrite is intersecting with another basal dendrite with largest radius
            if morphology_intersection_ops.basal_dendrite_intersects_basal_dendrite(
                dendrite=basal_dendrite, dendrites=self.morphology.dendrites,
                soma_radius=self.morphology.soma.mean_radius):

                    # Find the intersection sample
                    nearest_sample = morphology_connection_ops. \
                        find_nearest_basal_dendritic_sample_to_basal_dendrite(
                            morphology=self.morphology, basal_dendrite=basal_dendrite)

                    # Report the issue
                    nmv.logger.log('\t\t* REPAIRING: The basal dendrite [%d] @ section [%d] is re-connected '
                          'to section [%s, %d] @ sample [%d]' %
                          (i_basal_dendrite, basal_dendrite.id, nearest_sample.section.id,
                           nearest_sample.section.get_type_string(), nearest_sample.id))

                    # Mark the basal dendrite disconnected from the soma
                    basal_dendrite.connected_to_soma = False

                    # Update the axon initial sample based on the nearest dendritic sample
                    # The sample should have the same location
                    basal_dendrite.samples[0].point = nearest_sample.point

                    # The sample should have a smaller radius to avoid the extrusion artifacts
                    basal_dendrite.samples[0].radius = nearest_sample.radius * 0.5

                    # Done, next basal dendrite
                    continue

            # Mark the basal dendrite connected to the soma
            basal_dendrite.connected_to_soma = True

            nmv.logger.log('\t\t* NOTE: The basal dendrite [%d] @ section [%d] is connected to the soma' %
                  (i_basal_dendrite, basal_dendrite.id))

    ################################################################################################
    # @remove_samples_inside_soma
    ################################################################################################
    @staticmethod
    def remove_samples_inside_soma(section):
        """
        Removes the samples that are considered 'internal', or located withing the soma extent and
        cause branch intersection with the soma after its reconstruction.

        :param section: A root section, of a given arbor.
        """

        # If the section is only a root, then handle it. Otherwise, ignore this filter
        if section.has_parent():

            # Skip this filter
            return

        # Apply the filter on the initial section of the arbor
        morphology_repair_ops.remove_samples_inside_soma(section)





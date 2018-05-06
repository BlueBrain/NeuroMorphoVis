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
import sample
import morphology_ops
import morphology_analysis_ops
import morphology_repair_ops


####################################################################################################
# @MorphologyAnalyzer
####################################################################################################
class MorphologyAnalyzer:

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 morphology):
        """
        Constructor.

        :param morphology: Input morphology to be analyzed.
        """

        # Morphology
        self.morphology = morphology

    ################################################################################################
    # @analyze_arbor
    ################################################################################################
    def analyze_arbor(self,
                      arbor):
        """
        This function runs various analysis and validation tests to check the quality of the
        morphology.

        :param arbor: The root section of a given arbor.
        """

        # Validate the number of samples (and therefore the number of segments) per section
        self.validate_number_of_samples_per_section(arbor)

        # Validate the ratio between the section length and its radii
        self.validate_section_length_with_respect_to_radii(arbor)

        # Validate the number of children in the section
        self.validate_number_of_children(arbor)

        # Validate the radii of the sections
        self.validate_radii_at_branches(arbor)

        # Validate the presence of doubles (or samples that are too close)
        self.validate_doubles(arbor)

    ################################################################################################
    # @repair_arbor
    ################################################################################################
    def repair_arbor(self,
                     arbor):
        """
        Repair the arbor if it contains any detected artifacts.

        :param arbor: The root section of a given arbor.
        """

        # Repair the sections that have a 'SINGLE' child only
        #self.repair_sections_with_single_children(arbor)

        # Repair the short sections
        #self.repair_short_sections(arbor)

        # Remove the duplicate points
        #self.remove_duplicates(arbor)

        # Update the radii of the children sections with respect to the parents
        #self.repair_sections_with_radii_issues(arbor)

        # Select the primary branches
        #self.select_primary_sections(arbor)

        #self.repair_branches_with_small_bifurcation_angles(arbor)

        # After selecting the primary sections from the secondary ones, rescale the radii to avoid
        # any branching artifacts
        # self.rescale_sections_radii_at_branching_points(arbor)

        # Remove doubles (or duplicate samples that are extremely close to each other)
        # self.remove_doubles(arbor)

        # Re-sample the sections
        #self.resample_sections(arbor)

        # Repair the sections that have two samples only
        # self.repair_sections_with_two_samples(arbor)

        # self.resample_arbor(arbor)

        # Repair the sections that have initial samples with large radii at the front
        # self.repair_sections_with_radii_issues_at_front(arbor)

        # Repair the sections that have initial samples with large radii at the back
        # self.repair_sections_with_radii_issues_at_back(arbor)

        # self.repair_sampling_issues(arbor)

        self.remove_doubles(arbor)

    ################################################################################################
    # @resample_section_ending
    ################################################################################################
    def repair_arbor_for_piecewise_meshing(self,
                                           arbor):
        """
        This method repairs the arbor for the piecewise meshing algorithm.
        * Removing the internal samples that are intersecting within the extent of the soma
        * Removing the doubles (samples that are too close along the arbor) to avoid polyline
        artifacts
        * Connecting the intersecting branches at their roots rather than connecting them to the
        soma
        * Resampling the arbors to avoid smoothing artifacts
        * Vertex smoothing of the morphology

        :param arbor: The root section of a given arbor.
        """

        # Remove the duplicate points
        self.remove_doubles(arbor)






    def repair_branches_with_small_bifurcation_angles(self,
                                                      section):


        if not section.has_children():
            return

        if len(section.children) == 2:
            primary_child = None
            for child in section.children:
                if child.is_primary:
                    primary_child = child
            secondary_child = None
            for child in section.children:
                if not child.is_primary:
                    secondary_child = child

            # Get the angle between the primary and the secondary
            primary_vector_direction = \
                (primary_child.samples[1].point - primary_child.samples[0].point).normalized()
            secondary_vector_direction = \
                (secondary_child.samples[1].point - secondary_child.samples[0].point).normalized()

            # Compute the angles between the primary and the secondary vectors
            angle = primary_vector_direction.angle(secondary_vector_direction) * 180.0 / 3.14

            if angle < 15.0 or angle > 165:
                nmv.logger.log('section [%s] : angle: %f' % (str(section.id), angle))

                #print('section [%s] : angle: %f' % (str(section.id), angle))
                secondary_point = secondary_child.samples[1].point
                secondary_point_distance = \
                    (secondary_child.samples[1].point - secondary_child.samples[0].point).length
                primary_point = primary_child.samples[0].point + (secondary_point_distance * primary_vector_direction)

                primary_to_secondary_point_direction = (secondary_point - primary_point).normalized()
                secondary_child.samples[0].point += primary_to_secondary_point_direction * \
                                                    primary_child.samples[0].radius * 3

                secondary_child.samples[1].point += \
                    primary_to_secondary_point_direction * primary_child.samples[0].radius * 3

        if len(section.children) == 3:
            nmv.logger.log('section has three children')

        # Iterate over the children
        for child in section.children:

            # Validate the rest of the skeleton of the arbor
            self.repair_branches_with_small_bifurcation_angles(child)

    ################################################################################################
    # @analyze_apical_dendrite
    ################################################################################################
    def analyze_apical_dendrite(self):
        """
        Analyze the apical dendrite of the morphology, and report the issues.
        """

        # Check if the morphology has an apical dendrite or not
        if self.morphology.apical_dendrite is not None:

            # If yes, then analyze it
            nmv.logger.log('\t* Apical dendrite')
            self.analyze_arbor(self.morphology.apical_dendrite)

        # Otherwise, just give a note
        else:
            nmv.logger.log('\t\t* NOTE: This morphology does not have an apical dendrite')

    ################################################################################################
    # @analyze_basal_dendrites
    ################################################################################################
    def analyze_basal_dendrites(self):
        """
        Analyze the basal dendritic tree of the morphology, and report the issues.
        """

        # Check if the morphology has basal dendrites or not
        if self.morphology.dendrites is not None:

            # Do the analysis arbor by arbor
            for i, basal_dendrite in enumerate(self.morphology.dendrites):

                # If yes, then analyze each basal dendrite separately
                nmv.logger.log('\t* Basal dendrite [%d]' % i)
                self.analyze_arbor(basal_dendrite)

        # Otherwise, give an error since the morphology must have at leat a single basal dendrite
        else:
            nmv.logger.log('\t\t* ERROR: This morphology does not have any basal dendrites')

    ################################################################################################
    # @analyze_axon
    ################################################################################################
    def analyze_axon(self):
        """
        Analyze the axon of the morphology, and report the morphology.
        """

        # Check if the morphology has an axon or not
        if self.morphology.axon is not None:

            # If yes, then analyze it
            nmv.logger.log('\t* Axon')
            self.analyze_arbor(self.morphology.axon)

        # Otherwise, give an error since the morphology must have an axon
        else:
            nmv.logger.log('\t\t* ERROR: This morphology does not have an axon')

    ################################################################################################
    # @repair_apical_dendrite
    ################################################################################################
    def repair_apical_dendrite(self):
        """
        Repair the apical dendrite of the morphology, if exists.
        """

        # Check if the morphology has an apical dendrite or not
        if self.morphology.apical_dendrite is not None:

            # If yes, then analyze it
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
    # @analyze
    ################################################################################################
    def analyze(self):
        """
        Analyze the given morphology, and report all the issues.
        """

        nmv.logger.log('**************************************************************************')
        nmv.logger.log('Analyzing morphology')
        nmv.logger.log('**************************************************************************')

        # Analyze the apical dendrite
        self.analyze_apical_dendrite()

        # Analyze the basal dendrites
        self.analyze_basal_dendrites()

        # Analyze the axon
        self.analyze_axon()

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

    ################################################################################################
    # @validate_number_of_samples_per_section
    ################################################################################################
    def validate_number_of_samples_per_section(self,
                                               section):
        """
        Validate the number of samples per section.

        :param section: A root section, of a given arbor.
        """

        # Compute the number of samples per section
        number_samples_per_section = \
            morphology_analysis_ops.compute_number_of_samples_per_section(section)

        # If the section has only two samples, then report it as a warning
        if number_samples_per_section == 1:
            nmv.logger.log('\t\t* ERROR: The section [%s] has only 1 sample' % section.id)

        # If the section has only two samples, then report it as a warning
        if number_samples_per_section == 2:
            nmv.logger.log('\t\t* WARNING: The section [%s] has only 2 samples' % section.id)

        # Iterate over the children
        for child in section.children:

            # Validate the rest of the skeleton of the arbor
            self.validate_number_of_samples_per_section(child)

    ################################################################################################
    # @validate_section_length_with_respect_to_radii
    ################################################################################################
    def validate_section_length_with_respect_to_radii(self,
                                                      section):
        """
        Validate the section length with respect to its radii.
        This test verifies if the section is long enough compared to its radii.

        :param: A root section, of a given arbor.
        """

        # Ensure that the section has at least two samples, otherwise give an error
        if len(section.samples) < 2:

            # Report the issue
            nmv.logger.log('ERROR: The section [%d] has less than two samples!' % section.id)

        # Compute the section length
        section_length = morphology_analysis_ops.compute_section_length(section)

        # Get the radii of the first and last samples along the section
        first_sample_radius = section.samples[0].radius
        last_sample_radius = section.samples[-1].radius

        # Compute the minimal section length
        minimal_section_length = 2 * (first_sample_radius + last_sample_radius)

        # If the section length is shorter than the sum of both diameters, report that issue
        if section_length < minimal_section_length:

            # Report the issue
            nmv.logger.log('\t\t* WARNING: The section [%s] is \'SHORT\' [%f < %f]!' %
                  (section.id, section_length, minimal_section_length))

        # Iterate over the children
        for child in section.children:

            # Validate the rest of the skeleton of the arbor
            self.validate_section_length_with_respect_to_radii(child)



    ################################################################################################
    # @validate_doubles
    ################################################################################################
    def validate_doubles(self,
                         section,
                         threshold=1.0):
        """
        Validate if the section has doubles (or samples that are too close or not).

        :param: section: A root section, of a given arbor.
        """

        # Check the distance between every two successive samples and compare it with the threshold
        for i in range(len(section.samples) - 2):

            # Compute the distance between the two samples
            distance = (section.samples[i + 1].point - section.samples[i].point).length

            # Compare the distance with the threshold
            if distance < threshold:

                # Report the issue
                nmv.logger.log('\t\t* WARNING: Section [%s] has doubles, sample [%d], distance [%f]'
                      % (section.id, i + 1, distance))

        # Iterate over the children
        for child in section.children:

            # Validate the rest of the skeleton of the arbor
            self.validate_doubles(child)

    ################################################################################################
    # @repair_sections_with_single_children
    ################################################################################################
    def repair_sections_with_single_children(self,
                                             section):
        """
        If a single has a single child, then consider this child as a continuation to the original
        section and update the morphology.

        :param section: A root section, of a given arbor.
        """

        # Get the number of children of the section
        number_children = len(section.children)

        # The section has only one child
        if number_children == 1:

            # Report the repair
            nmv.logger.log('\t\t* REPAIRING: Section [%s] has been connected to parent' % section.id)

            # Apply the filter
            morphology_analysis_ops.connect_single_child(section)

        # Iterate over the children
        for child in section.children:

            # Validate the rest of the skeleton of the arbor
            self.repair_sections_with_single_children(child)



    ################################################################################################
    # @repair_sections_with_two_samples
    ################################################################################################
    def repair_sections_with_two_samples(self,
                                         section):
        """
        If a section has only two samples, we must re-sample this section and add a further sample
        at the middle of the section.

        :param section: A root section, of a given arbor.
        """

        # Compute the number of samples per section
        number_samples_per_section = \
            morphology_analysis_ops.compute_number_of_samples_per_section(section)

        # Verify that the sectiojn has only two samples
        if number_samples_per_section == 2:

            # Report the repair
            nmv.logger.log('\t\t* REPAIRING: Adding an extra samples to Section [%s]' % str(section.id))

            # Insert an auxiliary sample in the middle (interpolation)
            morphology_analysis_ops.add_extra_sample_at_the_center(section)

        # Iterate over the children
        for child in section.children:

            # Validate the rest of the skeleton of the arbor
            self.repair_sections_with_two_samples(child)

    ################################################################################################
    # @repair_sections_with_radii_issues_at_front
    ################################################################################################
    def repair_sections_with_radii_issues_at_front(self,
                                                   section):
        """
        If the initial sample of the section (at the branching point) has larger radius than that
        of the last sample of the parent section, then, fix this radius by making it equivalent to
        that of the parent sample.

        :param section: A root section, of a given arbor.
        """

        # Skip the root sections
        if section.has_parent():

            # Compare the radius of the first sample of the section with that of the last sample of
            # the parent one, if this child is greater, then report an issue
            if section.samples[0].radius > section.parent.samples[-1].radius:

                # Repair the radius, by setting it at 95% of the parent sample
                section.samples[0].radius = section.parent.samples[-1].radius * 0.95

                # Report the issue
                nmv.logger.log('\t\t* Repairing: Section [%s] radius: Parent=[%f], Child=[%f]' %
                      (str(section.id), section.parent.samples[-1].radius,
                       section.samples[0].radius))

        # Iterate over the children
        for child in section.children:

            # Validate the rest of the skeleton of the arbor
            self.repair_sections_with_radii_issues_at_front(child)

    ################################################################################################
    # @repair_sections_with_radii_issues_at_back
    ################################################################################################
    def repair_sections_with_radii_issues_at_back(self,
                                                  section):
        """
        This function repairs the connections between the different sections.
        It gets the radius of the last sample on a section and compares it with the radii of the
        first samples along its children.
        The radii of the children are compared to each other. The greater radius wins, and the
        radius of the last sample of the section is set to that 'greater' one.
        Then the radius of the other section (or sections if we have more than two children are set
        to a convenient value to allow smooth branching at the branching points.)

        :param section: A root section, of a given arbor.
        """

        # Ensure that this section has children
        if not section.has_children():

            # Break
            return

        # A list that would keep the radii of the children samples
        children_samples_radii = []

        # Iterate over all the children and get the radii of their first samples
        for child in section.children:

            # Add the radius of the first sample to the list
            children_samples_radii.append(child.samples[0].radius)

        if len(children_samples_radii) == 0: return

        # Set the radius of the last sample on the section to the greatest radius
        largest_radius = max(children_samples_radii)
        section.samples[-1].radius = largest_radius

        # For the other children, verify if the radii of their first samples are not less
        # than HALF OF THE LARGEST RADIUS
        for child in section.children:

            # Compare the section radius with the largest radius
            if child.samples[0].radius < 0.5 * largest_radius:

                # Set the radius to that value
                child.samples[0].radius = 0.5 * largest_radius

        # Iterate over the children
        for child in section.children:

            # Validate the rest of the skeleton of the arbor
            self.repair_sections_with_radii_issues_at_back(child)

    ################################################################################################
    # @repair_short_sections
    ################################################################################################
    def repair_short_sections(self,
                              section):
        """
        Repairs the short section along the arbor.
        This function computes the section length and compares it with a minimalistic value to
        verify if this section can be considered short or not.
        If the section is reported to be short, then, we change the radii of the entire section to
        a certain value that corresponds to its length.

        :param section: A root section, of a given arbor.
        """

        # Get the section length
        section_length = morphology_analysis_ops.compute_section_length(section)

        # Get the minimal section length that can be used to re-sample the section
        # This distance can be computed from the first and last samples of the section
        # The section must have at least two samples, otherwise this function will give an error
        minimal_section_length = (section.samples[0].radius + section.samples[-1].radius) * 2

        # If section length is less than the minimal section length, then fix the radii
        if section_length < minimal_section_length:

            # Report it
            nmv.logger.log('\t\t* REPAIRING: Short section [%s]' % str(section.id))

            # Get the average radius of the section can therefore be computed based on the
            # minimal section length value
            average_section_radius = section_length / 4.0

            # Iterate over all the samples along the section and set their radii to this value
            for sample in section.samples:

                # Update the radius value
                sample.radius = average_section_radius

            # Since we have change the radii of the short section, therefore, we must accordingly
            # update the radius of the last sample of the parent section and set the radii of the
            # first samples of the children at the same level to the @average_section_radius to
            # avoid any branching artifacts

            if section.has_parent():

                # Set the radius of the last sample of the parent to @average_section_radius
                section.parent.samples[-1].radius = average_section_radius

                # Set the radii of the first samples of the children sections at the same level to the
                # @average_section_radius
                for child in section.parent.children:
                    child.samples[0].radius = average_section_radius

        # Iterate over the children
        for child in section.children:

            # Validate the rest of the skeleton of the arbor
            self.repair_short_sections(child)

    ################################################################################################
    # @rescale_sections_radii_at_branching_points
    ################################################################################################
    def rescale_sections_radii_at_branching_points(self,
                                                   section):
        """
        This function is called to re-scale the radii of the sections at the branching points to
        avoid the branching artifacts. It must be called after setting the primary and secondary
        sections.
        The radius of the branching point is obtained from the sample with the least radius amongst
        the last sample of the parent and the first samples of the children.
        The radius of the last sample of the parent section is set to this branching point radius,
        as well as that of the primary child.
        The radii of the secondary sections are set to half of this radius.
        :param section: A root section, of a given arbor.
        """

        # Ensure that this section has children
        if not section.has_children():

            # Break
            return

        # Set the initial value of the branching radius to that of the last sample of the section
        branching_radius = section.samples[-1].radius

        # Update the branching radius after inspecting those of the children first samples
        for child in section.children:

            # Compare
            if child.samples[0].radius < branching_radius:

                # Update the branching radius
                branching_radius = child.samples[0].radius

        # Update the radius of the parent
        section.samples[-1].radius = branching_radius

        # Update the radii of the children
        for child in section.children:

            # Update the primary child
            if child.is_primary:

                # Set it to the branching radius
                child.samples[0].radius = branching_radius

            # Update the other secondary children
            else:

                # Set it to 0.5 the value of the branching radius
                child.samples[0].radius = 0.5 * branching_radius

        # Iterate over the children
        for child in section.children:

            # Validate the rest of the skeleton of the arbor
            self.rescale_sections_radii_at_branching_points(child)

    ################################################################################################
    # @repair_sections_with_radii_issues
    ################################################################################################
    def repair_sections_with_radii_issues(self,
                                          section):
        """
        This function verifies the radii along the morphology skeleton. Then it repairs the
        skeleton to avoid the artifacts at the bifurcation points.
        If the section has children, we obtain the radius of the last sample of the section
        itself and compare it with the radii of the children sections. Since there is a
        continuation along the largest children, then the radius of the last sample of the
        section must be equivalent to the first sample of the largest child.
        The radius of the first sample of the other child(ren) must be set to half of the value
        of the radius of the last sample of the parent section.

        :param section: A root section, of a given arbor.
        """

        # Skip the terminal sections
        if section.has_children():

            # Get the radius of the first sample of the largest child
            largest_radius, largest_child = \
                morphology_analysis_ops.get_largest_radius_of_children(section)

            # If the radius of the last sample of the parent is smaller than that of the first
            # sample of the largest child, then set the child radius to that of the parent
            if section.samples[-1].radius < largest_child.samples[0].radius:

                # Set the child radius to that of the parent
                largest_child.samples[0].radius = section.samples[-1].radius

            # Otherwise, set the parent radius to that of the largest child
            else:

                # Set the parent radius to that of the largest child
                section.samples[-1].radius = largest_child.samples[0].radius

            # Update the secondary children
            for child in section.children:

                # Skip the primary child
                if child.id == largest_child.id:

                    # Skip
                    continue

                # Set it to 0.5 the value
                child.samples[0].radius = largest_child.samples[0].radius * 0.5

        # Iterate over the children
        for child in section.children:

            # Validate the rest of the skeleton of the arbor
            self.repair_sections_with_radii_issues(child)

    ################################################################################################
    # @select_primary_sections
    ################################################################################################
    def select_primary_sections(self,
                                section):
        """
        Sets the primary sections of a given arbor.

        :param section: A root section, of a given arbor.
        """

        # If the section is root, then it is primary by default
        if not section.has_parent():

            # Set the root section to be primary
            section.is_primary = True

        if section.has_children():

            # Select the primary sections of this arbor
            morphology_analysis_ops.update_primary_and_secondary_branching_info(section)

        # Iterate over the children
        for child in section.children:

            # Validate the rest of the skeleton of the arbor
            self.select_primary_sections(child)

    ################################################################################################
    # @resample_sections
    ################################################################################################
    def resample_sections(self,
                          section):
        """
        Re-sample the sections at their front and rear terminals.

        :param section: A root section, of a given arbor.
        """

        # Handle a primary section
        if section.is_primary:
            self.resample_primary_section(section)

        # Handle a secondary section
        else:
            self.resample_secondary_section(section)

        # Iterate over the children
        for child in section.children:

            # Validate the rest of the skeleton of the arbor
            self.resample_sections(child)

    ################################################################################################
    # @resample_primary_section
    ################################################################################################
    def resample_primary_section(self,
                                 section):
        """
        Re-sample a primary section.

        :param section: A root section, of a given arbor.
        """

        # Re-sample the front of the primary section
        self.resample_primary_section_front(section)

        # Re-sample the rear end of the primary section
        self.resample_section_ending(section)

    ################################################################################################
    # @resample_secondary_section
    ################################################################################################
    def resample_secondary_section(self,
                                   section):
        """
        Re-sample a secondary section.

        :param section: A root section, of a given arbor.
        """

        # Re-sample the front of the secondary section
        self.resample_secondary_section_front(section)

        # Re-sample the rear end of the secondary section
        self.resample_section_ending(section)

    ################################################################################################
    # @resample_primary_section_front
    ################################################################################################
    def resample_primary_section_front(self,
                                       section):
        """
        Re-sample the front side of a primary section.

        :param section: A root section, of a given arbor.
        """

        # The re-sampling distance of the primary section is computed based on the section radius
        resampling_distance = section.samples[0].radius * 2

        # Remove the samples that are located within the resampling distance
        # The extent center is the first sample point and the extent radius is the
        # resampling distance
        number_removed_sampled = morphology_repair_ops.remove_samples_within_extent(section=section,
              extent_center=section.samples[0].point, extent_radius=resampling_distance,
              ignore_first_sample=True)

        # Compute the section direction after the removal of the close samples
        section_direction = (section.samples[1].point - section.samples[0].point).normalized()

        # Auxiliary sample position
        sample_position = section.samples[0].point + (section_direction * resampling_distance)

        # The auxiliary sample radius is the same as that of the first sample
        sample_radius = section.samples[0].radius

        # Build the extra samples, and use -1 for the ID to indicate that it is an auxiliary sample
        auxiliary_sample = sample.Sample(point=sample_position,
                                         radius=sample_radius,
                                         id=-1,
                                         section=section)

        if number_removed_sampled > 0:
            nmv.logger.log('\t\t* REPAIRING: Removing samples primary section [%s]' % (str(section.id)))

        # Insert the auxiliary sample just
        section.samples.insert(1, auxiliary_sample)

        # Reorder the samples and their IDs along the section
        section.reorder_samples()

    ################################################################################################
    # @resample_secondary_section_front
    ################################################################################################
    def resample_secondary_section_front(self,
                                         section):
        """
        Re-sample the front side of a secondary section.

        :param section: A root section, of a given arbor.
        """

        # If the section doesn't have a parent, return
        if not section.has_parent():

            # Return, a secondary branch with no parent does not exist !
            return

        # Get the resampling distance of the secondary section
        resampling_distance = \
            morphology_analysis_ops.get_resampling_distance_of_secondary_section(section)

        # Filter all the samples that are located within this sampling distance along the branch
        number_removed_sampled = morphology_repair_ops.remove_samples_within_extent(section=section,
             extent_center=section.samples[0].point, extent_radius=resampling_distance,
             ignore_first_sample=True)

        if number_removed_sampled > 0:
            nmv.logger.log('\t\t* REPAIRING: Removing samples secondary section [%s]' % (str(section.id)))

        # Compute the section direction after the removal of the close samples
        section_direction = (section.samples[1].point - section.samples[0].point).normalized()

        # Auxiliary sample position
        sample_position = section.samples[0].point + (section_direction * resampling_distance)

        # The auxiliary sample radius is the same as that of the first sample
        sample_radius = section.samples[0].radius

        # Build the extra samples, and use -1 for the ID to indicate that it is an auxiliary sample
        auxiliary_sample = sample.Sample(point=sample_position,
                                         radius=sample_radius,
                                         id=-1,
                                         section=section)

        # Insert the auxiliary sample just
        section.samples.insert(1, auxiliary_sample)

        # Reorder the samples and their IDs along the section
        section.reorder_samples()

    ################################################################################################
    # @resample_section_ending
    ################################################################################################
    def resample_section_ending(self,
                                section):
        """
        Re-sample section ending.

        :param section: A root section, of a given arbor.
        """

        # Reverse the sample list
        section.samples = list(reversed(section.samples))

        # Re-sample it
        self.resample_primary_section_front(section)

        # Reverse the sample list
        section.samples = list(reversed(section.samples))

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





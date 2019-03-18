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


####################################################################################################
# @apply_operation_to_arbor
####################################################################################################
def apply_operation_to_arbor(*args):
    """Apply a given function/filter/operation to a given arbor recursively.

    :param args:
        Arguments list, where the first argument is always the root section of the arbor and the
        second argument is the function of the operation/filter that will be applied
        and the rest of the arguments are those that will be passed to the function itself.
    """

    # The section is the first argument
    section = args[0]

    # If the section is None
    if section is None:

        # Simply return
        return

    # The operation is the second argument
    operation = args[1]

    # Construct the root section arguments list, add the section and ignore the operation
    section_args = [section]
    for i in range(2, len(args)):
        section_args.append(args[i])

    # Apply the operation/filter to the first section of the arbor
    operation(*section_args)

    # Ensure that the section has valid children
    if section.children is not None:

        # Apply the operation/filter to the children of the arbors
        for child in section.children:

            # Construct the child section arguments list, add the child and add the operation
            section_args = [child]
            for i in range(1, len(args)):
                section_args.append(args[i])

            # Validate the rest of the skeleton of the arbor
            apply_operation_to_arbor(*section_args)


####################################################################################################
# @apply_operation_to_arbor_conditionally
####################################################################################################
def apply_operation_to_arbor_conditionally(*args):
    """Apply a given function/filter/operation to a given arbor recursively if the branching order
    of this arbor is less than the max order requested by the user.

    :param args:
        Arguments list, where the first argument is always the root section of the arbor and the
        second argument is the function of the operation/filter that will be applied
        and the rest of the arguments are those that will be passed to the function itself.
    """

    # The current branching level is the first argument
    current_branching_level = args[0]

    # The max branching level is the second argument
    max_branching_level = args[1]

    # The section is the third argument
    section = args[2]

    # The operation is the fourth argument
    operation = args[3]

    # Construct the root section arguments list, add the section and ignore the operation
    section_args = list()

    # Add the branching levels
    section_args.append(current_branching_level)
    section_args.append(max_branching_level)

    # Add the section root
    section_args.append(section)

    # Add the rest of the arguments
    for i in range(4, len(args)):
        section_args.append(args[i])

    # Apply the operation/filter to the first section of the arbor
    operation(*section_args)

    # Ensure that the section has valid children
    if section.children is not None:

        # Apply the operation/filter to the children of the arbors
        for child in section.children:

            # Construct the child section arguments list, add the child and add the operation
            section_args = list()

            # Add the branching levels
            section_args.append(current_branching_level)
            section_args.append(max_branching_level)

            # Add the child
            section_args.append(child)

            # Add the operation
            section_args.append(operation)

            for i in range(4, len(args)):
                section_args.append(args[i])

            # Validate the rest of the skeleton of the arbor
            apply_operation_to_arbor_conditionally(*section_args)


####################################################################################################
# @apply_operation_to_morphology
####################################################################################################
def apply_operation_to_morphology(*args):
    """Apply a given function/filter/operation to a given morphology object including all of its
    arbors recursively.

    :param args:
        Arguments list, where the first argument is always the morphology and the second argument
        is the function of the operation/filter that will be applied and the rest of the arguments
        are those that will be passed to the function.
    """

    # The morphology is the first argument
    morphology = args[0]

    # Apical dendrite
    if morphology.apical_dendrite is not None:

        # Construct arbor arguments list
        arbor_args = [morphology.apical_dendrite]
        for i in range(1, len(args)):
            arbor_args.append(args[i])

        # Apply the operation/filter to the arbor
        apply_operation_to_arbor(*arbor_args)

    # Basal dendrites
    if morphology.dendrites is not None:

        # Dendrite by dendrite
        for dendrite in morphology.dendrites:

            # Construct arbor arguments list
            arbor_args = [dendrite]
            for i in range(1, len(args)):
                arbor_args.append(args[i])

            # Apply the operation/filter to the arbor
            apply_operation_to_arbor(*arbor_args)

    # Axon
    if morphology.axon is not None:

        # Construct arbor arguments list
        arbor_args = [morphology.axon]
        for i in range(1, len(args)):
            arbor_args.append(args[i])

        # Apply the operation/filter to the arbor
        apply_operation_to_arbor(*arbor_args)


####################################################################################################
# @apply_operation_to_morphology_partially
####################################################################################################
def apply_operation_to_morphology_partially(*args):
    """Apply a given function/filter/operation to a given morphology object including ONLY the
    arbors that are below certain branching level recursively.

    :param args:
        Arguments list, where the first argument is always the morphology and the second argument
        is the function of the operation/filter that will be applied and the rest of the arguments
        are those that will be passed to the function.
    """

    # The morphology is the first argument
    morphology = args[0]

    # Axon maximum branching order
    axon_branch_level = args[1]

    # Basal dendrites maximum branching order
    basal_dendrites_branch_level = args[2]

    # Apical dendrites maximum branching order
    apical_dendrite_branch_level = args[3]

    # Apical dendrite
    if morphology.apical_dendrite is not None:

        # Construct arbor arguments list
        arbor_args = list()

        # Add the branching levels to the arguments
        current_branching_level = [0]
        arbor_args.append(current_branching_level)
        arbor_args.append(apical_dendrite_branch_level)

        # Add the section root
        arbor_args.append(morphology.apical_dendrite)

        # Add the other arguments
        for i in range(4, len(args)):
            arbor_args.append(args[i])

        # Apply the operation/filter to the arbor
        apply_operation_to_arbor_conditionally(*arbor_args)

    # Basal dendrites
    if morphology.dendrites is not None:

        # Dendrite by dendrite
        for dendrite in morphology.dendrites:

            # Construct arbor arguments list
            arbor_args = list()

            # Add the branching levels to the arguments
            current_branching_level = [0]
            arbor_args.append(current_branching_level)
            arbor_args.append(basal_dendrites_branch_level)

            # Add the section root
            arbor_args.append(dendrite)

            # Add the other arguments
            for i in range(4, len(args)):
                arbor_args.append(args[i])

            # Apply the operation/filter to the arbor
            apply_operation_to_arbor_conditionally(*arbor_args)

    # Axon
    if morphology.axon is not None:

        # Construct arbor arguments list
        arbor_args = list()

        # Add the branching levels to the arguments
        current_branching_level = [0]
        arbor_args.append(current_branching_level)
        arbor_args.append(axon_branch_level)

        # Add the section root
        arbor_args.append(morphology.axon)

        # Add the other arguments
        for i in range(4, len(args)):
            arbor_args.append(args[i])

        # Apply the operation/filter to the arbor
        apply_operation_to_arbor_conditionally(*arbor_args)

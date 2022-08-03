####################################################################################################
# Copyright (c) 2016 - 2020, EPFL / Blue Brain Project
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

    # The max branching level is the second argument
    max_branching_order = args[0]

    # The section is the third argument
    section = args[1]

    # The operation is the fourth argument
    operation = args[2]

    # Construct the root section arguments list, add the section and ignore the operation
    section_args = list()

    # Add the branching levels
    section_args.append(max_branching_order)

    # Add the section root
    section_args.append(section)

    # Add the rest of the arguments
    for i in range(3, len(args)):
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
            section_args.append(max_branching_order)

            # Add the child
            section_args.append(child)

            # Add the operation
            section_args.append(operation)

            for i in range(3, len(args)):
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
    if morphology.has_apical_dendrites():

        # Dendrite by dendrite
        for arbor in morphology.apical_dendrites:

            # Construct arbor arguments list
            arbor_args = [arbor]
            for i in range(1, len(args)):
                arbor_args.append(args[i])

            # Apply the operation/filter to the arbor
            apply_operation_to_arbor(*arbor_args)

    # Basal dendrites
    if morphology.has_basal_dendrites():

        # Dendrite by dendrite
        for arbor in morphology.basal_dendrites:

            # Construct arbor arguments list
            arbor_args = [arbor]
            for i in range(1, len(args)):
                arbor_args.append(args[i])

            # Apply the operation/filter to the arbor
            apply_operation_to_arbor(*arbor_args)

    # Axon
    if morphology.has_axons():

        # Dendrite by dendrite
        for arbor in morphology.axons:

            # Construct arbor arguments list
            arbor_args = [arbor]
            for i in range(1, len(args)):
                arbor_args.append(args[i])

            # Apply the operation/filter to the arbor
            apply_operation_to_arbor(*arbor_args)


####################################################################################################
# @apply_operation_to_trimmed_morphology
####################################################################################################
def apply_operation_to_trimmed_morphology(*args):
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
    axons_branching_order = args[1]

    # Basal dendrites maximum branching order
    basal_dendrites_branching_order = args[2]

    # Apical dendrites maximum branching order
    apical_dendrites_branching_order = args[3]

    # Apical dendrite
    if morphology.has_apical_dendrites():
        for arbor in morphology.apical_dendrites:

            # Construct arbor arguments list
            arbor_args = list()

            # Add the branching levels to the arguments
            arbor_args.append(apical_dendrites_branching_order)

            # Add the section root
            arbor_args.append(arbor)

            # Add the other arguments
            for i in range(4, len(args)):
                arbor_args.append(args[i])

            # Apply the operation/filter to the arbor
            apply_operation_to_arbor_conditionally(*arbor_args)

    # Basal dendrites
    if morphology.has_basal_dendrites():
        for arbor in morphology.basal_dendrites:

            # Construct arbor arguments list
            arbor_args = list()

            # Add the branching levels to the arguments
            arbor_args.append(basal_dendrites_branching_order)

            # Add the section root
            arbor_args.append(arbor)

            # Add the other arguments
            for i in range(4, len(args)):
                arbor_args.append(args[i])

            # Apply the operation/filter to the arbor
            apply_operation_to_arbor_conditionally(*arbor_args)

    # Axon
    if morphology.has_axons():
        for arbor in morphology.basal_dendrites:

            # Construct arbor arguments list
            arbor_args = list()

            # Add the branching levels to the arguments
            arbor_args.append(axons_branching_order)

            # Add the section root
            arbor_args.append(arbor)

            # Add the other arguments
            for i in range(4, len(args)):
                arbor_args.append(args[i])

            # Apply the operation/filter to the arbor
            apply_operation_to_arbor_conditionally(*arbor_args)

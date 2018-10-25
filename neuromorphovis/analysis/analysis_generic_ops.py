

import neuromorphovis as nmv
import neuromorphovis.analysis


####################################################################################################
# @apply_analysis_operation_to_arbor
####################################################################################################
def apply_analysis_operation_to_arbor(*args):
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
            apply_analysis_operation_to_arbor(*section_args)


####################################################################################################
# @apply_analysis_operation_to_morphology
####################################################################################################
def apply_analysis_operation_to_morphology(*args):
    """Apply a given function/filter/operation to a given morphology object including all of its
    arbors recursively.

    :param args:
        Arguments list, where the first argument is always the morphology and the second argument
        is the function of the operation/filter that will be applied and the rest of the arguments
        are those that will be passed to the function.
    """

    # A structure to contain the analysis results of the entire morphology
    analysis_result = nmv.analysis.MorphologyAnalysisResult()


    # The morphology is the first argument
    morphology = args[0]

    analysis_function = args[1]

    # Apical dendrite
    if morphology.apical_dendrite is not None:

        # Construct arbor arguments list
        arbor_args = [morphology.apical_dendrite]
        for i in range(2, len(args)):
            arbor_args.append(args[i])

        # Apply the operation/filter to the arbor
        analysis_result.apical_dendrite_result = analysis_function(*arbor_args)

    # Basal dendrites
    if morphology.dendrites is not None:

        # Create an empty list to collect the resulting data
        analysis_result.basal_dendrites_result = list()

        # Dendrite by dendrite
        for dendrite in morphology.dendrites:

            # Construct arbor arguments list
            arbor_args = [dendrite]
            for i in range(2, len(args)):
                arbor_args.append(args[i])

            # Apply the operation/filter to the arbor
            analysis_result.basal_dendrites_result.append(analysis_function(*arbor_args))

    # Axon
    if morphology.axon is not None:

        # Construct arbor arguments list
        arbor_args = [morphology.axon]
        for i in range(2, len(args)):
            arbor_args.append(args[i])

        # Apply the operation/filter to the arbor
        analysis_result.axon_result = analysis_function(*arbor_args)

    # Return the structure that contains the analysis result
    return analysis_result

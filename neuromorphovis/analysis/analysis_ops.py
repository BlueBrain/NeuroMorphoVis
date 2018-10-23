

# minimum segments length
# average segments length
# maximum segments length

# of a specific neurite
# of the entire morphology skeleton

def compute_segments_length(section,
                            segments_length_list):

    for i in range(len(section.samples) - 1):

        # Retrieve the points along each segment on the section
        point_0 = section.samples[i].point
        point_1 = section.samples[i + 1].point

        # Compute the segment length
        segment_length = (point_1 - point_0).length

        # Append to the list
        segments_length_list.append(segment_length)


def compute_section_length(section,
                           sections_length_list):
    # Section length
    section_length = 0.0

    # If the section has less than two samples, then report the error
    if len(section.samples) < 2:

        # Zero
        sections_length_list.append(section_length)

        # Return
        return

    # Integrate the distance between each two successive samples
    for i in range(len(section.samples) - 1):
        # Retrieve the points along each segment on the section
        point_0 = section.samples[i].point
        point_1 = section.samples[i + 1].point

        # Update the section length
        section_length += (point_1 - point_0).length

    sections_length_list.append(section_length)


####################################################################################################
# @compute_section_length
####################################################################################################
def compute_section_length(section):
    """
    Computes the length of a given section.
    NOTE: This function returns a meaningful value for the roots sections, ONLY when the negative
    samples are removed from the branch, otherwise, the contribution of the negative samples
    will be integrated. The negative samples are those located closer to the origin of the soma
    than the first samples of the section.

    :param section:
        A given section to compute its length.
    :return:
        Section total length in microns.
    """

    # Section length
    section_length = 0.0

    # If the section has less than two samples, then report the error
    if len(section.samples) < 2:

        # Return 0
        return section_length

    # Integrate the distance between each two successive samples
    for i in range(len(section.samples) - 1):

        # Retrieve the points along each segment on the section
        point_0 = section.samples[i].point
        point_1 = section.samples[i + 1].point

        # Update the section length
        section_length += (point_1 - point_0).length

    # Return the section length
    return section_length
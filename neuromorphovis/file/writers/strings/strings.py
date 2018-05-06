"""
exporters.py:
    Mesh exporters into different file formats and types.
"""

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2017, Blue Brain Project / EPFL"
__version__     = "0.1.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"


####################################################################################################
# @write_string_to_file
####################################################################################################
def write_string_to_file(string,
                         file_path):
    """Write a string to a file

    :param string:
        A string to be written to the file.
    :param file_path:
        The output path of the file.
    """

    # Open the file
    file_handle = open(file_path, 'w')

    # Write the string
    file_handle.write(string)

    # Close the file
    file_handle.close()


####################################################################################################
# @write_list_string_to_file
####################################################################################################
def write_list_string_to_file(list_strings,
                              file_path):
    """Write a string to a file

    :param list_strings:
        A string list to be written to the file.
    :param file_path:
        The output path of the file.
    """

    # Open the file
    file_handle = open(file_path, 'w')

    # Write the strings
    for string in list_strings:
        file_handle.write(string + '\n')

    # Close the file
    file_handle.close()
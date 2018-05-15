"""
writer.py:
    A set of utilities for writing target files in different formats.
"""

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2017, Blue Brain Project / EPFL"
__version__     = "0.1.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"

import os
import shutil

################################################################################
# @clean_and_create_directory
################################################################################
def clean_and_create_directory(path):
    """
    Creates a new directory and removes the old one if exists.

    :param path : The path of the directory to be created.
    """

    # if the path exists, remove it and create another one.
    if os.path.exists(path):
        shutil.rmtree(path)
    try:
        os.mkdir(path)
    except:
        print ('ERROR: cannot create directory %s' % path)


###############################################################################
# @create_target_string
###############################################################################
def create_target_string(gid_list, target_name):
    """
    Creates a target string and returns it.
    :param gid_list: Input list of gids.
    :param target_name: The name of the target.
    :return: A string representing a target.
    """
    target_string = ''
    # write header
    target_string += 'Target Cell %s\n' % (target_name)

    # write the '{' before the gids
    target_string += '{\n'

    # write the gids
    for gid in gid_list:
        target_string += "a%d " % gid

    # write the '}' after the gids
    target_string += "\n}\n"


###############################################################################
# @create_target_string_from_data_list
###############################################################################
def create_target_string_from_data_list(data_list, target_name):
    """
    Creates a target string and returns it.
    :param data_list: Input list of data.
    :param target_name: The name of the target.
    :return: A string representing a target.
    """
    target_string = ''

    # write header
    target_string += 'Target Cell %s\n' % (target_name)

    # write the '{' before the gids
    target_string += '{\n'

    # write the gids
    for item in data_list:
        data = item.split(' ')
        target_string += "a%d " % data[0]

    # write the '}' after the gids
    target_string += "\n}\n"


###############################################################################
# @write_target_file
###############################################################################
def write_target_file(gid_list, target_name, file_name, output_path):
    """
    Writes a default target file for a given list of gids.

    :param gid_list: Input list of gids.
    :param target_name: The name of the target.
    :param file_name: The name of the output file.
    :param output_path: The output path of the target file.
    :return:
    """
    # output file
    output_file = '%s/%s.target' % (output_path, file_name)

    # create the target file and open it for writing
    target_file = open(output_file, 'w')

    # write header
    target_file.write('Target Cell %s\n' % (target_name))

    # write the '{' before the gids
    target_file.write('{\n')

    # write the gids
    gids_string = ''
    for gid in gid_list: gids_string += "a%d " % gid
    target_file.write(gids_string)

    # write the '}' after the gids
    target_file.write("\n}\n")

    # close the file
    target_file.close()


###############################################################################
# @write_target_file_from_data_list
###############################################################################
def write_target_file_from_data_list(data_list, target_name, file_name,
                                     output_path):
    """
    Writes a default target file for a given list of gids.

    :param gid_list: Input list of gids.
    :param target_name: The name of the target.
    :param file_name: The name of the output file.
    :param output_path: The output path of the target file.
    :return:
    """
    # output file
    output_file = '%s/%s.target' % (output_path, file_name)

    # create the target file and open it for writing
    target_file = open(output_file, 'w')

    # write header
    target_file.write('Target Cell %s\n' % (target_name))

    # write the '{' before the gids
    target_file.write('{\n')

    # write the gids
    gids_string = ''
    for item in data_list:
        data = item.split(' ')
        gids_string += "a%d " % data[0]
    target_file.write(gids_string)

    # write the '}' after the gids
    target_file.write("\n}\n")

    # close the file
    target_file.close()


###############################################################################
# @write_voxelization_target_file
###############################################################################
def write_voxelization_target_file(data_list, file_name, output_path):
    """
    Writes a voxelization target file for a given list of gids.
    The format of each entity is as follows:
    [1][2][3][4][5][6][7][8][9][10]
        1 Neuron gid
        2 Tag
        3 X position
        4 Y position
        5 Z position
        6 Minimum radius
        7 Mean radius
        8 Max radius
        9 Morphology type
        10 Morphology name

    :param data_list: Input list of data.
    :param file_name: The name of the output file.
    :param output_path: The output path of the target file.
    :return:
    """
    # output file
    output_file = '%s/%s.list' % (output_path, file_name)

    # create the target file and open it for writing
    target_file = open(output_file, 'w')

    # write data to file
    data_string = ''
    for item in data_list: data_string += item
    target_file.write(data_string)

    # close the file
    target_file.close()



###############################################################################
# @write_neurorender_config
###############################################################################
def write_neurorender_config(target,
                             config_file_name,
                             output_path):
    """Writes a configuration file for NeuroRender.

    :param target:
        Created target.
    :param config_file_name:
        Configuration file name.
    :param output_path:
        The path where the configuration file will be written.
    """

    # The path to the output configuration file
    output_file = '%s/%s.list' % (output_path, config_file_name)

    # Create the configuration file and open it for writing
    neurorender_config_file = open(output_file, 'w')

    # New line
    nl = '\n'

    # Tab as spaces to make it clear to read the file manually just in case if we need it
    tab = '    '

    # Write data to file
    data_string = ''
    for neuron in target:

        # Add the neuron data to the output string
        # Header
        data_string += 'NEURON' + nl

        # Neuron GID
        data_string += tab + 'GID: ' + str(neuron.gid) + nl

        # Neuron morphology type
        data_string += tab + 'MTYPE: '+ str(neuron.mtype) + nl

        # Neuron morphology label
        data_string += tab + 'MLABEL: ' + str(neuron.mlabel) + nl

        # Neuron X position
        data_string += tab + 'POSITION: ' + str(neuron.position[0]) + nl


        # We are all set for this neuron, add a new line to start a new neuron
        data_string += nl

    # Write the string
    neurorender_config_file.write(data_string)

    # Close the file
    neurorender_config_file.close()


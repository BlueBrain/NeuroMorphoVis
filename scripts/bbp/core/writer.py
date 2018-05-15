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
# @create_directory
################################################################################
def create_directory(path):
    """Create a directory if it doesn't exist.

    :param path:
        Path where the folder will be created.
    :return:
    """

    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except:
            print('ERROR: cannot create directory %s' % path)


################################################################################
# @clean_and_create_directory
################################################################################
def clean_and_create_directory(path):
    """Create a new directory and removes the old one if exists.

    :param path :
        The path of the directory to be created.
    """

    # if the path exists, remove it and create another one.
    if os.path.exists(path):
        shutil.rmtree(path)
    try:
        os.mkdir(path)
    except:
        print('ERROR: cannot create directory %s' % path)


###############################################################################
# @create_target_string
###############################################################################
def create_target_string(target,
                         target_name):
    """Create a target string and returns it.

    :param target:
        Created target from the filtering process.
    :param target_name:
        The name of the target.
    :return:
        A string representing a target.
    """

    # A string that contains the target
    target_string = ''

    # Write header
    target_string += 'Target Cell %s\n' % (target_name)

    # Write the '{' before the gids
    target_string += '{\n'

    # Write the gids
    for neuron in target:
        target_string += "a%d " % neuron.gid

    # Write the '}' after the gids
    target_string += "\n}\n"


###############################################################################
# @write_target_file
###############################################################################
def write_target_file(target,
                      target_name,
                      target_file_name,
                      output_path):
    """
    Writes a default target file for a given list of gids.

    :param target:
        Created target from the filtering process.
    :param target_name:
        The name of the target.
    :param target_file_name:
        The name of the output file.
    :param output_path:
        The output path of the target file.
    """

    # Output file
    output_file = '%s/%s.target' % (output_path, target_file_name)

    # Create the target file and open it for writing
    target_file = open(output_file, 'w')

    # Write header
    target_file.write('Target Cell %s\n' % (target_name))

    # Write the '{' before the gids
    target_file.write('{\n')

    # Write the gids
    gids_string = ''
    for neuron in target:
        gids_string += "a%d " % neuron.gid
    target_file.write(gids_string)

    # Write the '}' after the gids
    target_file.write("\n}\n")

    # Close the file
    target_file.close()


###############################################################################
# @write_neurorender_config
###############################################################################
def write_neurorender_config(target,
                             config_file_name,
                             output_path):
    """Writes a configuration file for NeuroRender.

    :param target:
        Created target from the filtering process.
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

        # Tag
        data_string += tab + 'TAG: ' + str(neuron.tag) + nl

        # Neuron morphology type
        data_string += tab + 'MORPHOLOGY_TYPE: ' + str(neuron.morphology_type) + nl

        # Neuron morphology label
        data_string += tab + 'MORPHOLOGY_LABEL: ' + str(neuron.morphology_label) + nl

        # Neuron position
        data_string += tab + 'POSITION: ' + str(neuron.position) + nl

        # Neuron position
        data_string += tab + 'ORIENTATION: ' + str(neuron.orientation) + nl

        # Neuron transform
        data_string += tab + 'TRANSFORM: ' + str(neuron.transform) + nl

        # Column
        data_string += tab + 'COLUMN: ' + str(neuron.column) + nl

        # Column
        data_string += tab + 'LAYER: ' + str(neuron.layer) + nl

        # We are all set for this neuron, add a new line to start a new neuron
        data_string += nl

    # Write the string
    neurorender_config_file.write(data_string)

    # Close the file
    neurorender_config_file.close()


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

# System imports
import sys, os

import nmv
import nmv.file


####################################################################################################
# @read_h5_morphology
####################################################################################################
def read_h5_morphology(h5_file):
    """Verifies if the given path is valid or not and then loads a .h5 morphology file.

    If the path is not valid, this function returns None.

    :param h5_file: Path to the H5 morphology file.
    :return: A morphology object or None if the path is not valid.
    """

    # If the path is valid
    if os.path.isfile(h5_file):

        # Load the .h5 morphology
        reader = nmv.file.readers.H5Reader(h5_file=h5_file)
        morphology_object = reader.read_file()

        # Return a reference to this morphology object
        return morphology_object

    # Issue an error
    nmv.logger.log('ERROR: The morphology path [%s] is invalid' % h5_file)

    # Otherwise, return None
    return None


####################################################################################################
# @read_swc_morphology
####################################################################################################
def read_swc_morphology(swc_file):
    """Verifies if the given path is valid or not and then loads a .swc morphology file.

    If the path is not valid, this function returns None.

    :param swc_file:
        Path to the SWC morphology file.
    :return:
        Morphology object and True (if the morphology is loaded) or False (if the something is
        wrong).
    """

    # If the path is valid
    if os.path.isfile(swc_file):

        # Load the .h5 morphology
        reader = nmv.file.readers.SWCReader(swc_file=swc_file)
        morphology_object = reader.read_file()

        # Return a reference to this morphology object
        return morphology_object

    # Issue an error
    nmv.logger.log('ERROR: The morphology path [%s] is invalid' % swc_file)

    # Otherwise, return None
    return None


####################################################################################################
# @read_morphology_from_file
####################################################################################################
def read_morphology_from_file(options):
    """Loads a morphology object from file. This loader mainly supports .h5 or .swc file formats.

    :param options:
        A reference to the system options.
    :return:
        Morphology object and True (if the morphology is loaded) or False (if the something is
        wrong).
    """

    # The morphology file path is available from the system options
    morphology_file_path = options.morphology.morphology_file_path

    # Get the extension from the file path
    morphology_prefix, morphology_extension = os.path.splitext(morphology_file_path)

    # If it is a .h5 file, use the h5 loader
    if '.h5' in morphology_extension:

        # Load the .h5 file
        morphology_object = read_h5_morphology(morphology_file_path)

    elif '.swc' in morphology_extension:

        # Load the .swc file
        morphology_object = read_swc_morphology(morphology_file_path)

    else:

        # Issue an error
        nmv.logger.log('ERROR: The morphology extension [%s] is NOT SUPPORTED' %
                       morphology_extension)
        return False, None

    # If the morphology object is None, return False
    if morphology_object is None:
        return False, None

    # The morphology file was loaded successfully
    return True, morphology_object


####################################################################################################
# @read_morphology_from_file_naively
####################################################################################################
def read_morphology_from_file_naively(morphology_file_path):
    """Loads a morphology object from file. This loader mainly supports .h5 or .swc file formats.

    :param morphology_file_path:
        The path where the morphology is.
    :return:
        Morphology object and True (if the morphology is loaded) or False (if the something is
        wrong).
    """

    # Get the extension from the file path
    morphology_prefix, morphology_extension = os.path.splitext(morphology_file_path)

    # If it is a .h5 file, use the h5 loader
    if '.h5' in morphology_extension:

        # Load the .h5 file
        morphology_object = read_h5_morphology(morphology_file_path)

    elif '.swc' in morphology_extension:

        # Load the .swc file
        morphology_object = read_swc_morphology(morphology_file_path)

    else:

        # Issue an error
        nmv.logger.log('ERROR: The morphology extension [%s] is NOT SUPPORTED' %
                       morphology_extension)
        return False, None

    # If the morphology object is None, return False
    if morphology_object is None:
        return False, None

    # The morphology file was loaded successfully
    return True, morphology_object


####################################################################################################
# @load_from_circuit
####################################################################################################
def load_from_circuit(options):
    """
    Loads a morphology object with a given GID from a given circuit.

    :param options: A reference to the system options.
    :return: Morphology object and True (if the morphology is loaded) or False (if the something is
    wrong)
    """

    morphology_object = None

    morphology_object = nmv.file.BBPReader.load_morphology_from_circuit(
        blue_config=options.morphology.blue_config, gid=options.morphology.gid)

    # If the morphology object is None, return False
    if morphology_object is None:
        return False, None

    # The morphology file was loaded successfully
    return True, morphology_object
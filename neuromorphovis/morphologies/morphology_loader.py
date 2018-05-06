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

# Append the internal modules into the system paths
sys.path.append("%s/../modules" % os.path.dirname(os.path.realpath(__file__)))

# Internal imports
import h5_parser
import bbp_morphology


####################################################################################################
# @load_h5_morphology
####################################################################################################
def load_h5_morphology(morphology_file_path):
    """
    Verifies if the given path is valid or not and then loads a .h5 morphology file.
    If the path is not valid, this function returns None.

    :param morphology_file_path: Path to the morphology file.
    :return: A morphology object or None if the path is not valid.
    """

    # If the path is valid
    if os.path.isfile(morphology_file_path):

        # Load the .h5 morphology
        morphology_object = h5_parser.parse_h5_morphology(morphology_file_path)

        # Return a reference to this morphology object
        return morphology_object

    # Issue an error
    nmv.logger.log('ERROR: The morphology path [%s] is invalid' % morphology_file_path)

    # Otherwise, return None
    return None


####################################################################################################
# @load_swc_morphology
####################################################################################################
def load_swc_morphology(morphology_file_path):
    """
    Verifies if the given path is valid or not and then loads a .swc morphology file.
    If the path is not valid, this function returns None.

    :param morphology_file_path: Path to the morphology file.
    :return: A morphology object or None if the path is not valid.
    """

    # TODO: Update loading swc morphologies

    # Issue an error
    nmv.logger.log('ERROR: The morphology path [%s] is invalid' % morphology_file_path)

    # Otherwise, return None
    return None


####################################################################################################
# @load_from_file
####################################################################################################
def load_from_file(options):
    """
    Loads a morphology object from file. This loader mainly supports .h5 or .swc file formats.

    :param options: A reference to the system options.
    :return: Morphology object and True (if the morphology is loaded) or False (if the something is
    wrong)
    """


    # The morphology file path is available from the system options
    morphology_file_path = options.morphology.morphology_file_path

    # Get the extension from the file path
    morphology_prefix, morphology_extension = os.path.splitext(morphology_file_path)

    # If it is a .h5 file, use the h5 loader
    if 'h5' in morphology_extension:

        # Load the .h5 file
        morphology_object = load_h5_morphology(morphology_file_path)
    elif 'swc' in morphology_extension:

        # Load the .swc file
        morphology_object = load_swc_morphology(morphology_file_path)

    else:

        # Issue an error
        nmv.logger.log('ERROR: The morphology extension [%s] is NOT SUPPORTED' % morphology_extension)
        return False

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

    morphology_object = bbp_morphology.load_morphology_from_gid(
        blue_config=options.morphology.blue_config, gid=options.morphology.gid)

    # If the morphology object is None, return False
    if morphology_object is None:
        return False, None

    # The morphology file was loaded successfully
    return True, morphology_object

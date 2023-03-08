####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
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
import os

# Internal imports
import nmv.bbp
import nmv.consts
import nmv.file
import nmv.interface


####################################################################################################
# @read_swc_morphology_natively
####################################################################################################
def read_swc_morphology_natively(swc_file,
                                 center_at_origin=True):
    """Verifies if the given path is valid or not and then loads a .swc morphology file.
    NOTE: If the path is not valid, this function returns None.

    :param swc_file:
        Path to the SWC morphology file.
    :param center_at_origin:
        Center the loaded morphology skeleton at the origin.
    :return:
        Morphology object (if the morphology is loaded) or False (if the something is wrong).
    """

    # Ensure that the given file is valid and then load the file
    if os.path.isfile(swc_file):
        reader = nmv.file.readers.SWCReader(swc_file=swc_file, center_at_origin=center_at_origin)
        morphology_object = reader.read_file()

        # Return a reference to the loaded morphology object
        return morphology_object

    # Issue an error and return None for panel processing
    nmv.logger.log('ERROR: The morphology path [%s] is invalid' % swc_file)
    return None


####################################################################################################
# @read_h5_morphology_natively
####################################################################################################
def read_h5_morphology_natively(h5_file,
                                center_at_origin=True):
    """Verifies if the given path is valid or not and then loads a .h5 morphology file.
    NOTE: If the path is not valid, this function returns None.

    :param h5_file:
        Path to the H5 morphology file.
     :param center_at_origin:
        Center the loaded morphology skeleton at the origin.
    :return:
        Morphology object (if the morphology is loaded) or False (if the something is wrong).
    """

    # Ensure that the given file is valid and then load the file
    if os.path.isfile(h5_file):
        reader = nmv.file.readers.H5Reader(h5_file=h5_file, center_at_origin=center_at_origin)
        morphology_object = reader.read_file()

        # Return a reference to the loaded morphology object
        return morphology_object

    # Issue an error and return None for panel processing
    nmv.logger.log('ERROR: The morphology path [%s] is invalid' % h5_file)
    return None


####################################################################################################
# @read_morphology_with_morphio
####################################################################################################
def read_morphology_with_morphio(morphology_file_path,
                                 center_at_origin=True):
    import morphio

    # Ensure that the given file is valid and then load the file
    if os.path.isfile(morphology_file_path):
        # Load the .h5 morphology
        try:
            reader = nmv.file.readers.MorphIOLoader(morphology_file_path,
                                                    center_morphology=center_at_origin)
            morphology_object = reader.read_data_from_file()

            # Return a reference to this morphology object
            return morphology_object

        # Throw exception
        except morphio.RawDataError as e:
            nmv.logger.log('ERROR: The morphology [%s] could NOT be loaded with MorphIO: %s' %
                           (morphology_file_path, e))

        # Otherwise, return None
        return None


####################################################################################################
# @read_morphology_from_file
####################################################################################################
def read_morphology_from_file(options,
                              panel=None):
    """Loads a morphology object from file. This loader supports .asc, .h5 or .swc file formats.

    :param options:
        A reference to the system options.
    :param panel:
        A reference to the GUI panel used to load the morphology file.
    :return:
        Morphology object if the morphology is loaded or False (if the something is wrong).
    """

    # The morphology file path is available from the system options
    morphology_file_path = options.morphology.morphology_file_path

    # Get the extension from the file path
    morphology_prefix, morphology_extension = os.path.splitext(morphology_file_path)

    # If it is a .h5 file, use the H5Reader to be able to load astrocytes with endfeet
    # TODO: This option is made until further notice, when we are able to load endfeet from circuits
    if '.h5' in morphology_extension.lower():
        try:
            morphology_object = read_h5_morphology_natively(
                h5_file=morphology_file_path, center_at_origin=options.morphology.center_at_origin)
        except:
            if panel is not None:
                panel.report({'ERROR'}, 'Cannot load this H5 file, please verify its structure')
                return None

            nmv.logger.log('Cannot load this H5 file, please verify its structure')
            return None

    # NOTE: We load the SWC files with MorphIO for performance reasons. If this fails, for whatever
    # reason, we drop the native SWCReader
    elif '.swc' in morphology_extension.lower():
        try:
            morphology_object = read_morphology_with_morphio(
                morphology_file_path=morphology_file_path,
                center_at_origin=options.morphology.center_at_origin)
        except:
            try:
                morphology_object = read_swc_morphology_natively(
                    swc_file=morphology_file_path,
                    center_at_origin=options.morphology.center_at_origin)
            except:
                if panel is not None:
                    panel.report({'ERROR'}, 'Cannot load this SWC file, please verify its structure')
                    return None

                nmv.logger.log('Cannot load this SWC file, please verify its structure')
                return None

    # NOTE: We will always use MorphIO to load .acc morphology files
    elif '.asc' in morphology_extension.lower():
        try:
            morphology_object = read_morphology_with_morphio(
                morphology_file_path, options.morphology.center_at_origin)
        except:
            if panel is not None:
                panel.report({'ERROR'}, 'Cannot load this ASC file, please verify its structure')
                return None

            nmv.logger.log('Cannot load this ASC file, please verify its structure')
            return None

    # Report the error for the users and return None to terminate the loading operation
    else:
        if panel is not None:
            panel.report(
                {'ERROR'}, 'Cannot load files with the [%s] extension.' % morphology_extension)
            return None

        # Report the error for the GUI users and return None to terminate the loading operation
        nmv.logger.log('Cannot load files with the [%s] extension.' % morphology_extension)
        return None

    # The morphology file was loaded successfully
    return morphology_object


####################################################################################################
# @read_morphology_from_circuit
####################################################################################################
def read_morphology_from_circuit(options):
    """Reads a morphology file from a given circuit using the circuit configuration file and a GID
    of the neuron and construct a morphology object.
    NOTE: All the input parameters are part of the given @options argument, which is a type of
    NeuroMorphoVisOption.

    :param options:
        System options.
    :type options:
        NeuroMorphoVisOption
    :return:
        The loaded morphology object.
    """

    # TODO: Handle libSonata circuits
    # Load the circuit from the circuit config, and get the path to the morphology
    circuit = nmv.bbp.BBPCircuit(circuit_config=options.morphology.blue_config)
    morphology_file_path = circuit.get_neuron_morphology_path(options.morphology.gid)

    # Get the data from the circuit and update the necessary fields in NMV
    nmv.consts.Circuit.MTYPES = circuit.get_mtype_strings_list()
    print(nmv.consts.Circuit.MTYPES)
    nmv.consts.Circuit.ETYPES = circuit.get_etype_strings_list()
    nmv.interface.ui_circuit = circuit

    # Load the morphology file into a NMV morphology object using MorphIO
    nmv_morphology_object = nmv.file.read_morphology_with_morphio(
        morphology_file_path=morphology_file_path,
        center_at_origin=options.morphology.center_at_origin)

    # To identify the neuron in the scene, label the morphology object with the GID of the neuron
    nmv_morphology_object.label = str(options.morphology.gid)

    # Return the morphology object
    return nmv_morphology_object











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
import sys
import os
import shutil

# Internal imports
sys.path.append('%s/../../consts' % os.path.dirname(os.path.realpath(__file__)))
from paths_consts import *
import nmv.enums


####################################################################################################
# @clean_and_create_directory
####################################################################################################
def clean_and_create_directory(path):
    """Creates a new directory and removes the old one if exists.

    :param path :
        The path of the directory to be created.
    """

    # if the path exists, remove it and create another one.
    if os.path.exists(path):
        shutil.rmtree(path)
    try:
        os.mkdir(path)
    except ValueError:
        print('ERROR: cannot create directory %s' % path)


####################################################################################################
# @delete_directory
####################################################################################################
def delete_directory(path):
    """Cleans a directory tree.

    :param path:
        A given directory to delete.
    """
    # if the path exists, remove it and create another one.
    if os.path.exists(path):
        shutil.rmtree(path)


####################################################################################################
# @create_directory
####################################################################################################
def create_directory(path):
    """Creates a new directory of it doesn't exist.

    :param path :
        The path of the directory to be created.
    """

    # if the path exists, remove it and create another one.
    if os.path.exists(path):
        return
    try:
        os.mkdir(path)
    except ValueError:
        print('ERROR: cannot create directory %s' % path)


####################################################################################################
# @get_files_in_directory
####################################################################################################
def get_files_in_directory(directory,
                           file_extension=None):
    """Gets all the files in a directory, similar to ls command in linux. If the file extension
    is not specified, it returns a list of all the files.

    :param directory:
        Given directory.
    :param file_extension:
        The extension of requested file.
    :return:
        A list of the requested files.
    """

    # A list of all the files that exist in a directory
    files = list()

    # If the extension is not specified
    if file_extension is None:
        for i_file in os.listdir(directory):
            files.append(i_file)

    # Otherwise, return files that have specific extensions
    else:
        for i_file in os.listdir(directory):
            if i_file.endswith(file_extension):
                files.append(i_file)

    # Return the list
    return files


####################################################################################################
# @write_batch_job_string_to_file
####################################################################################################
def write_batch_job_string_to_file(output_directory,
                                   file_name,
                                   batch_job_string):
    """Writes a string to a file.

    :param output_directory:
        The path where the slurm jobs will be written.
    :param file_name:
        SLURM file prefix.
    :param batch_job_string:
        The batch job string that will be written to the file.
    """

    # Set the absolute file path
    file_path = '%s/%s.sh' % (output_directory, file_name)

    # Open the file
    file_handle = open(file_path, 'w')

    # Write the string
    file_handle.write(batch_job_string)

    # Close the file
    file_handle.close()


####################################################################################################
# @create_output_tree
####################################################################################################
def create_output_tree(output_directory):
    """Creates the output directories tree.

    :param output_directory:
        The path where the project tree will be created.
    """

    # Output directory
    create_directory(output_directory)

    # SLURM directory
    slurm_directory = '%s/%s' % (output_directory, Paths.SLURM_FOLDER)
    create_directory(slurm_directory)

    # SLURM jobs directory
    slurm_jobs_directory = '%s/%s' % (output_directory, Paths.SLURM_JOBS_FOLDER)
    create_directory(slurm_jobs_directory)

    # SLURM logs directory
    slurm_logs_directory = '%s/%s' % (output_directory, Paths.SLURM_LOGS_FOLDER)
    create_directory(slurm_logs_directory)

    # Analysis directory
    analysis_directory = '%s/%s' % (output_directory, Paths.ANALYSIS_FOLDER)
    create_directory(analysis_directory)

    # Morphologies directory
    meshes_directory = '%s/%s' % (output_directory, Paths.MORPHOLOGIES_FOLDER)
    create_directory(meshes_directory)

    # Meshes directory
    meshes_directory = '%s/%s' % (output_directory, Paths.MESHES_FOLDER)
    create_directory(meshes_directory)

    # Images directory
    images_directory = '%s/%s' % (output_directory, Paths.IMAGES_FOLDER)
    create_directory(images_directory)

    # Sequences directory
    sequences_directory = '%s/%s' % (output_directory, Paths.SEQUENCES_FOLDER)
    create_directory(sequences_directory)

    # Stats directory
    stats_directory = '%s/%s' % (output_directory, Paths.STATS_FOLDER)
    create_directory(stats_directory)


####################################################################################################
# @path_exists
####################################################################################################
def path_exists(path):
    """Verifies if the given path exists or not.

    :param path:
        A given path to check its existence.
    :return:
        True or False
    """
    if path is None:
        return False

    return os.path.exists(path)


####################################################################################################
# @get_file_name_from_path
####################################################################################################
def get_file_name_from_path(path):
    """Gets the name of the file from a given path.

    :param path:
        A given path to a certain file.
    :return:
        The file name.
    """

    # Get the file name
    file_name = os.path.basename(path)

    # If the file contains '.', then get the first part only
    if '.' in file_name:
        return os.path.splitext(file_name)[0]

    # Otherwise, return the file name
    return file_name


####################################################################################################
# @get_file_format_from_path
####################################################################################################
def get_file_format_from_path(path):
    """Gets the file format from a given path.

    :param path:
        A given path to a certain file.
    :return:
        The file format.
    """

    # Get the file name
    file_name = os.path.basename(path)

    # If the file contains '.', then get the first part only
    if '.' in file_name:
        return os.path.splitext(file_name)[1]


####################################################################################################
# @get_morphology_file_format
####################################################################################################
def get_morphology_file_format(morphology_file_path):
    """Returns the file format of the morphology from its absolute path.

    :param morphology_file_path:
        The absolute path of the morphology.
    :return:
        The file format enumerator of the morphology, or None.
    """
    morphology_prefix, morphology_extension = os.path.splitext(morphology_file_path)
    if 'asc' in morphology_extension.lower():
        return nmv.enums.Morphology.Format.ASCII
    elif 'swc' in morphology_extension.lower():
        return nmv.enums.Morphology.Format.SWC
    elif 'h5' in morphology_extension.lower():
        return nmv.enums.Morphology.Format.H5
    else:
        return None

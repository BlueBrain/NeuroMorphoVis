#!/usr/bin/python

import subprocess
import os
import re

# The directory where the final results will be print to
#portal_directory = '/gpfs/bbp.cscs.ch/project/proj83/visualization-SSCXDIS-178/portal'
portal_directory = '/gpfs/bbp.cscs.ch/project/proj3/sscx_portal'

# The synaptic pathways directory
root_synaptic_pathways_directory = '/gpfs/bbp.cscs.ch/project/proj83/visualization-SSCXDIS-178/synaptic-pathways/trial-11-12.03.2021'

# The synaptomes directory
root_synaptomes_directory = '/gpfs/bbp.cscs.ch/project/proj83/visualization-SSCXDIS-178/synaptome/trial-8-09.03.2021-mtype'

# All the regsions
regions = [
    'S1DZO',
    'S1DZ',
    'S1FL_Column',
    'S1HL_Column',
    'S1J_Column',
    'S1Sh',
    'S1Tr',
    'S1ULp']


####################################################################################################
# @ Synaptic Pair region
####################################################################################################
class SynapticPair:
    def __init__(self):
        self.pre_gid = ''
        self.post_gid = ''
        self.pre_synaptome = ''
        self.post_synaptome = ''
        self.pre_mtype = ''
        self.post_mtype = ''
        self.synaptic_pathway = ''

# A list of all the shell commands to be executed
all_shell_command = list()

# Do it per region
for region in regions:

    # Get to the actual directories
    synaptic_pathways_directory = root_synaptic_pathways_directory + '/' + region + '_pairs' + '/results'
    synaptomes_directory = root_synaptomes_directory + '/' + region

    # Get all pairs in the synaptic pathways directory
    synaptic_pathways_pairs = os.listdir(synaptic_pathways_directory)

    # Synaptomes files
    synaptome_files = os.listdir(synaptomes_directory)

    # Create an output directory for the region if it doesn't exist
    output_region_directory = '%s/%s' % (portal_directory, region)
    if not os.path.exists(output_region_directory):
        os.mkdir(output_region_directory)

    # A list of all the synaptic pais and their data
    synaptic_pairs_list = list()

    # A list that will collect any missing pairs and report them to be regenerated
    missing_pairs = list()

    # For evey pair in the synaptic pathways
    for i_pair, pair in enumerate(synaptic_pathways_pairs):
        print('[%d / %d]' % (i_pair, len(synaptic_pathways_pairs)))

        # Create a new pair
        synaptic_pair = SynapticPair()

        # Get the pre-synaptic and post-synaptic gids
        result = pair.split('_')
        synaptic_pair.pre_gid = result[0]
        synaptic_pair.post_gid = result[1]

        # Get the png inside the composite directory
        synaptic_pair.synaptic_pathway = pair

        # Keep track on errors
        missing_pair = False

        # Search the synaptomes using the GIDs
        try:
            pre_synaptic_synaptome = [x for x in synaptome_files if re.search(synaptic_pair.pre_gid, x)][0]
            post_synaptic_synaptome = [x for x in synaptome_files if re.search(synaptic_pair.post_gid, x)][0]

        except IndexError:
            lost_pair = 'Synaptome [%s, %s] cannot be found' % (pre_synaptic_synaptome,
                                                                post_synaptic_synaptome)
            print(lost_pair)
            missing_pairs.append(lost_pair)
            missing_pair = True

        # If not missing any pair, proceed
        if not missing_pair:

            # Update the pre-synaptome
            synaptic_pair.pre_synaptome = pre_synaptic_synaptome

            # Remove the GID from the string
            mtype = pre_synaptic_synaptome.replace(synaptic_pair.pre_gid, '')

            # Remove the keyword synaptome
            mtype = mtype.replace('synaptome_', '')

            # Remove the image extension
            mtype = mtype.replace('.png', '')

            # Remove the last underscore
            synaptic_pair.pre_mtype = mtype[:-1]

            # Update the post-synaptome
            synaptic_pair.post_synaptome = post_synaptic_synaptome

            # Remove the GID from the string
            mtype = post_synaptic_synaptome.replace(synaptic_pair.post_gid, '')

            # Remove the keyword synaptome
            mtype = mtype.replace('synaptome_', '')

            # Remove the image extension
            mtype = mtype.replace('.png', '')

            # Remove the last underscore
            synaptic_pair.post_mtype = mtype[:-1]

            # Make a directory in the specific region folder
            directory_name = '[%s][%s]' % (synaptic_pair.pre_mtype, synaptic_pair.post_mtype)
            directory_path = '%s/%s/' % (portal_directory, region)
            # shell_cmd = 'mkdir %s' % directory_path
            # subprocess.call(shell_cmd, shell=True)

            # Copy the pre-synaptic synaptome
            shell_cmd = 'cp %s/%s %s/%s_[%s].png' % (synaptomes_directory,
                                                     synaptic_pair.pre_synaptome,
                                                     directory_path, directory_name,
                                                     synaptic_pair.pre_mtype)
            all_shell_command.append(shell_cmd)

            # Copy the post-synaptic synaptome
            shell_cmd = 'cp %s/%s %s/%s_[%s].png' % (synaptomes_directory,
                                                     synaptic_pair.post_synaptome,
                                                     directory_path, directory_name,
                                                     synaptic_pair.post_mtype)
            all_shell_command.append(shell_cmd)

            # Copy the synaptic pathways
            shell_cmd = 'cp %s/%s/composite/*.png %s/%s_[%s].png' % (synaptic_pathways_directory,
                                                                     synaptic_pair.synaptic_pathway,
                                                                     directory_path,
                                                                     synaptic_pair.pre_mtype,
                                                                     synaptic_pair.post_mtype)
            all_shell_command.append(shell_cmd)

    # Print the missing pairs
    print(missing_pairs)
    f = open('%s/%s.missing' % (portal_directory, region), 'w')
    for ms_pair in missing_pairs:
        f.write(ms_pair)
    f.close()

    for cmd in all_shell_command:
        print(cmd)
        subprocess.call(cmd, shell=True)


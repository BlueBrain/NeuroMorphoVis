#!/usr/bin/python

import subprocess
import os
import re

# The directory where the final results will be print to
portal_directory = '/gpfs/bbp.cscs.ch/project/proj83/visualization-SSCXDIS-178/portal/trial-3-06.03.2021'

# The synaptic pathways directory
root_synaptic_pathways_directory = '/gpfs/bbp.cscs.ch/project/proj83/visualization-SSCXDIS-178/synaptic-pathways/trial-13-06.03.2021'

# The synaptomes directory
root_synaptomes_directory = '/gpfs/bbp.cscs.ch/project/proj83/visualization-SSCXDIS-178/synaptome/trial-10-06.04.2021-mtype'

# All the regsions
'''
regions = [
    'S1DZO',
    'S1DZ',
    'S1FL_Column',
    'S1HL_Column',
    'S1J_Column',
    'S1Sh',
    'S1Tr',
    'S1ULp']
'''

regions = [
    'S1DZ_Column',
    'S1DZO_Column',
    'S1FL_Column',
    'S1HL_Column',
    'S1J_Column',
    'S1Sh_Column',
    'S1Tr_Column',
    'S1ULp_Column'
]

regions = [
    'S1DZ_Column'
]

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
copy_commands = list()

# Do it per region
for region in regions:

    # Get to the actual directories
    synaptic_pathways_directory = root_synaptic_pathways_directory \
                                  + '/' + region + '/results'
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

    # Missing images
    missing_images = list()

    # For evey pair in the synaptic pathways
    for i_pair, pair in enumerate(synaptic_pathways_pairs):
        print('[%d / %d]' % (i_pair, len(synaptic_pathways_pairs)))

        # Create a new pair
        synaptic_pair = SynapticPair()

        # Get the pre-synaptic and post-synaptic gids
        result = pair.split('_')
        synaptic_pair.pre_gid = result[0].replace(' ', '')
        synaptic_pair.post_gid = result[1].replace(' ', '')

        # Get the png inside the composite directory
        synaptic_pair.synaptic_pathway = pair

        # Keep track on errors
        missing_pair = False
        # Search the synaptomes using the GIDs
        try:
            pre_synaptic_synaptome = [x for x in synaptome_files
                                      if re.search('_%s.png' % synaptic_pair.pre_gid, x)][0]

        except IndexError:
            lost_pair = 'Pre-Synaptome [%s] cannot be found \n' % synaptic_pair.pre_gid
            print(lost_pair)
            missing_pairs.append(lost_pair)
            missing_pair = True

        try:
            post_synaptic_synaptome = [y for y in synaptome_files
                                       if re.search('_%s.png' % synaptic_pair.post_gid, y)][0]

        except IndexError:
            lost_pair = 'Post-Synaptome [%s] cannot be found \n' % synaptic_pair.post_gid
            print(lost_pair)
            missing_pairs.append(lost_pair)
            missing_pair = True

        # If not missing any pair, proceed
        if not missing_pair:
            # continue

            # Update the pre-synaptome
            synaptic_pair.pre_synaptome = pre_synaptic_synaptome

            # Remove the GID from the string
            pre_mtype = pre_synaptic_synaptome.replace(str(synaptic_pair.pre_gid), '')

            # Remove the keyword synaptome
            pre_mtype = pre_mtype.replace('synaptome_', '')

            # Remove the image extension
            pre_mtype = pre_mtype.replace('.png', '')

            # Remove the last underscore
            synaptic_pair.pre_mtype = pre_mtype[:-1]

            # Update the post-synaptome
            synaptic_pair.post_synaptome = post_synaptic_synaptome

            # Remove the GID from the string
            post_mtype = post_synaptic_synaptome.replace(synaptic_pair.post_gid, '')

            # Remove the keyword synaptome
            post_mtype = post_mtype.replace('synaptome_', '')

            # Remove the image extension
            post_mtype = post_mtype.replace('.png', '')

            # Remove the last underscore
            synaptic_pair.post_mtype = post_mtype[:-1]

            # Make a directory in the specific region folder
            # NOTE: All the directories were made, so we don't need them
            directory_name = '%s___%s' % (synaptic_pair.pre_mtype, synaptic_pair.post_mtype)
            directory_path = '%s/%s/%s' % (portal_directory, region, directory_name)

            if not os.path.exists(directory_path):
                # print('Missing: %s' % directory_path)
                shell_cmd = 'mkdir %s' % directory_path
                subprocess.call(shell_cmd, shell=True)

            # Copy the pre-synaptic synaptome
            src_image = '%s/%s' % (synaptomes_directory, synaptic_pair.pre_synaptome)
            dst_image = '%s/%s.png' % (directory_path, synaptic_pair.pre_mtype)
            shell_cmd = 'cp %s %s ' % (src_image, dst_image)

            if not os.path.exists(dst_image):
                subprocess.call(shell_cmd, shell=True)

            # Copy the post-synaptic synaptome
            src_image = '%s/%s' % (synaptomes_directory, synaptic_pair.post_synaptome)
            dst_image = '%s/%s.png' % (directory_path, synaptic_pair.post_mtype)
            shell_cmd = 'cp %s %s ' % (src_image, dst_image)

            if not os.path.exists(dst_image):
                subprocess.call(shell_cmd, shell=True)

            # Copy the synaptic pathways
            src_image = '%s/%s/composite/full_view_%s_%s_pathways_FRONT.png' % (
                synaptic_pathways_directory, synaptic_pair.synaptic_pathway,
                synaptic_pair.pre_gid, synaptic_pair.post_gid)
            dst_image = '%s/%s_%s.png' % (directory_path,
                                          synaptic_pair.pre_mtype,
                                          synaptic_pair.post_mtype)
            shell_cmd = 'cp %s %s ' % (src_image, dst_image)

            if not os.path.exists(dst_image):
                subprocess.call(shell_cmd, shell=True)

    # Print the missing pairs
    f = open('%s/%s.missing' % (portal_directory, region), 'w')
    for ms_pair in missing_pairs:
        f.write(ms_pair)

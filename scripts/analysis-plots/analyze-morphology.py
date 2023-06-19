####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
# Author: Marwan Abdellah <marwan.abdellah@epfl.ch>
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
import sys, os, bpy

sys.path.append(('%s/../../' % (os.path.dirname(os.path.realpath(__file__)))))
sys.path.append(('%s/core' % (os.path.dirname(os.path.realpath(__file__)))))

# System imports
import argparse

# NeuroMorphoVis imports
import nmv.analysis
import nmv.skeleton


####################################################################################################
# @parse_command_line_arguments
####################################################################################################
def parse_command_line_arguments(arguments=None):
    """Parses the input arguments.

    :param arguments:
        Command line arguments.
    :return:
        Arguments list.
    """

    # add all the options
    description = 'Resampling neurons to make them lighter while preserving skeletons'
    parser = argparse.ArgumentParser(description=description)

    arg_help = 'An input morphology'
    parser.add_argument('--morphology',
                        action='store', dest='morphology', help=arg_help)

    arg_help = 'Output directory where the resampled morphology will be written'
    parser.add_argument('--output-directory',
                        action='store', dest='output_directory', help=arg_help)

    # Parse the arguments
    return parser.parse_args()


####################################################################################################
# @ Main
####################################################################################################
if __name__ == "__main__":

    # Get all arguments after the '--'
    args = sys.argv
    sys.argv = args[args.index("--") + 0:]

    # Parse the command line arguments
    args = parse_command_line_arguments()

    # Load the morphology file
    morphology_object = nmv.file.readers.read_morphology_from_file(args.morphology)

    # Verify the loading operation
    if morphology_object is None:
        print({'ERROR'}, 'Invalid Morphology File')
        exit(0)

    #analysis_result = nmv.analysis.compute_distribution_number_of_samples_of_morphology(
    #    morphology=morphology_object)

    #for itm in analysis_result.basal_dendrites_result:
    #    print(itm.section_index, itm.branching_order, itm.value, itm.distribution)







    '''
    print('********************************************************')
    analysis_result = nmv.analysis.compute_distribution_segments_length_of_morphology(
        morphology=morphology_object)

    branching_orders = list()
    values = list()
    for i in analysis_result.morphology_result:
        branching_orders.append(i.branching_order)
        values.append(i.value)

    import pandas as pd
    import seaborn as sns

    sns.set_theme(style="darkgrid")

    # Define a dictionary containing Students data
    data = {'Segment Length': values,
            'Order': branching_orders}

    # Convert the dictionary into DataFrame
    df = pd.DataFrame(data)

    print(df)

    import matplotlib.pyplot as plt

    g = sns.barplot(x="Order", y="Segment Length", data=df, palette="Blues_d")
    # g.set(xlim=(1, maximum_branching_order), ylim=(min(average_values) - 2, max(average_values) + 2))

    # setting the title using Matplotlib
    plt.title('Title using Matplotlib Function')
      
    plt.savefig('x.png')
    '''

    analysis_result = nmv.analysis.compute_distribution_samples_radii_of_morphology(
        morphology=morphology_object)

    branching_orders = list()
    values = list()
    for i in analysis_result.morphology_result:
        branching_orders.append(i.branching_order)
        values.append(i.value)

    import pandas as pd
    import seaborn as sns

    sns.set_theme(style="darkgrid")

    # Define a dictionary containing Students data
    data = {'Samples Radii': values,
            'Order': branching_orders}

    # Convert the dictionary into DataFrame
    df2 = pd.DataFrame(data)

    print(df2)

    import matplotlib.pyplot as plt

    g = sns.barplot(x="Order", y="Samples Radii", data=df2, palette="Blues_d")
    # g.set(xlim=(1, maximum_branching_order), ylim=(min(average_values) - 2, max(average_values) + 2))

    # setting the title using Matplotlib
    plt.title('Title using Matplotlib Function')

    plt.savefig('y.png')





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

import os
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

import nmv.consts


def plot_distribution(distribution,
                      tilte,
                      normalized=False,
                      color='b'):
    from matplotlib import font_manager as fm, rcParams
    fpath = '%s/%s' % (nmv.consts.Paths.FONTS_DIRECTORY, 'helvetica-light.ttf')

    prop = fm.FontProperties(fname=fpath)

    sns.set(color_codes=True)

    sns.set_style("whitegrid")
    plt.rcParams['axes.grid'] = 'False'
    plt.rcParams['font.family'] = prop.get_name()
    plt.rcParams['font.monospace'] = 'Regular'
    plt.rcParams['font.style'] = 'normal'

    plt.rcParams['axes.linewidth'] = 0.0
    plt.rcParams['axes.labelsize'] = 10
    plt.rcParams['axes.labelweight'] = 'bold'
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 10
    plt.rcParams['figure.titlesize'] = 10
    plt.rcParams['axes.titlesize'] = 10

    # Convert the distribution list to a numpy array
    np_distribution = np.array(distribution)

    # Adjust the Y-axis format
    # plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=xmax, symbol=' %'))

    # Set the title
    plt.title('Samples')

    # Plot the histogram
    sns.distplot(np_distribution, color='r',kde=False, hist=True, norm_hist=normalized,
                 hist_kws={"color": color, "lw": 0.5},
                 kde_kws={"color": color, "lw": 0.5})

    # plt.savefig('result.png', dpi=150)
    plt.savefig('%s/neuromorphovis-output/%s-plot.pdf' % (os.path.expanduser('~'), tilte), dpi=150)

    # Close figure to reset
    plt.close()

def plot_analysis_results(analysis_results):

    if analysis_results.apical_dendrite_result is not None:
        plot_distribution(analysis_results.apical_dendrite_result, 'apical')

    if analysis_results.basal_dendrites_result is not None:
        for i, basal_dendrite_result in enumerate(analysis_results.basal_dendrites_result):
            plot_distribution(basal_dendrite_result, 'basal_%d' % i)

    if analysis_results.axon_result is not None:
        plot_distribution(analysis_results.axon, 'axon')

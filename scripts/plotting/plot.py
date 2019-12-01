#!/computer/bbp-blender-development/nmv-blender-2.80/Blender-2.80.app/Contents/Resources/2.80/python/bin/python3.7m

import os
import numpy as np
import seaborn as sns
import pandas as pd

import matplotlib.pyplot as plt

from matplotlib import font_manager, rcParams




sns.set(color_codes=True)

# Loading fonts
font_dirs = ['/computer/bbp-blender-development/nmv-blender-2.80/Blender-2.80.app/Contents/Resources/2.80/scripts/addons/NeuroMorphoVis/data/fonts']
font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
font_list = font_manager.createFontList(font_files)
font_manager.fontManager.ttflist.extend(font_list)

# Adjust configuration
sns.set_style("whitegrid")
plt.rcParams['axes.grid'] = 'False'
plt.rcParams['font.family'] = 'Arial'

plt.rcParams['axes.linewidth'] = 0.0
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['axes.labelweight'] = 'regular'

plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['axes.titlesize'] = 15


x_data = ['Axon', 'Basal Dendrite 0', 'Basal Dendrite 1', 'Basal Dendrite 2', 'Basal Dendrite 3', 'Basal Dendrite 4', 'Apical Dendrite']
y_data = [159, 161, 96, 219, 107, 61, 672]

total_number_neurites = 7


print(x_data)
print(y_data)

x = np.asarray(x_data)
y = np.asarray(y_data)

plt.figure(figsize=(5, 7* 0.5))


ax = sns.barplot(x=y, y=x)

'''
width = 0.75
for bar in ax.patches:

    # Current Y center
    y = bar.get_y()

    # Current bar height
    height = bar.get_height()

    # Current center
    centre = y + height / 2.0

    # Set the new center
    bar.set_y(centre - width / 2.0)

    # Set the new height
    bar.set_height(width)
'''

# create a list to collect the plt.patches data
totals = []

# find the values and append to list
for i in ax.patches:
    totals.append(i.get_width())

# set individual bar lables using above list
total = sum(totals)


# set individual bar lables using above list
for i in ax.patches:
    # get_width pulls left or right; get_y pushes up or down
    ax.text(i.get_width() + 10, i.get_y() + .5,
            str(round((i.get_width()/total)*100, 2))+'%', fontsize=10,
            color='dimgrey')


ax.set(xlabel='Number of Samples', title='Number of Samples / Neurite')


plt.savefig('/Users/abdellah/Desktop/nmv-release/figures/dist-1.pdf', bbox_inches='tight')
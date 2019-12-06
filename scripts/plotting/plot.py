#!/bbp/bbp-blender-packages/nmv-blender-2.80-linux-glibc217-x86_64/2.80/python/bin/python3.7m
# ###abdellah-1/bbp/blender-2.80-linux-glibc217-x86_64/2.80/python/bin/python3.7m
#
# import os
# import numpy as np
# import seaborn as seabron
# import pandas
#
# import matplotlib.pyplot as plt
#
# from matplotlib import font_manager, rcParams
#
#
#
# #
# # seabron.set(color_codes=True)
# #
# # # Loading fonts
# # #font_dirs = ['/computer/bbp-blender-development/nmv-blender-2.80/Blender-2.80.app/Contents/Resources/2.80/scripts/addons/NeuroMorphoVis/data/fonts']
# # #font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
# # #font_list = font_manager.createFontList(font_files)
# # #font_manager.fontManager.ttflist.extend(font_list)
# #
# # # Adjust configuration
# # seabron.set_style("whitegrid")
# # plt.rcParams['axes.grid'] = 'False'
# # plt.rcParams['font.family'] = 'Arial'
# #
# # plt.rcParams['axes.linewidth'] = 0.0
# # plt.rcParams['axes.labelsize'] = 10
# # plt.rcParams['axes.labelweight'] = 'regular'
# #
# # plt.rcParams['xtick.labelsize'] = 10
# # plt.rcParams['ytick.labelsize'] = 10
# # plt.rcParams['legend.fontsize'] = 10
# # plt.rcParams['axes.titlesize'] = 15
# #
# # '''
# # x_data = ['Axon', 'Basal Dendrite 0', 'Basal Dendrite 1', 'Basal Dendrite 2', 'Basal Dendrite 3', 'Basal Dendrite 4', 'Apical Dendrite']
# # y_data = [159, 161, 96, 219, 107, 61, 672]
# #
# # total_number_neurites = 7
# #
# #
# # print(x_data)
# # print(y_data)
# #
# # x = np.asarray(x_data)
# # y = np.asarray(y_data)
# #
# # plt.figure(figsize=(5, 7* 0.5))
# #
# #
# # ax = seabron.barplot(x=y, y=x)
# #
# #
# # width = 0.75
# # for bar in ax.patches:
# #
# #     # Current Y center
# #     y = bar.get_y()
# #
# #     # Current bar height
# #     height = bar.get_height()
# #
# #     # Current center
# #     centre = y + height / 2.0
# #
# #     # Set the new center
# #     bar.set_y(centre - width / 2.0)
# #
# #     # Set the new height
# #     bar.set_height(width)
# #
# #
# # # create a list to collect the plt.patches data
# # totals = []
# #
# # # find the values and append to list
# # for i in ax.patches:
# #     totals.append(i.get_width())
# #
# # # set individual bar lables using above list
# # total = sum(totals)
# #
# #
# # # set individual bar lables using above list
# # for i in ax.patches:
# #     # get_width pulls left or right; get_y pushes up or down
# #     ax.text(i.get_width() + 10, i.get_y() + .5,
# #             str(round((i.get_width()/total)*100, 2))+'%', fontsize=10,
# #             color='dimgrey')
# #
# #
# # ax.set(xlabel='Number of Samples', title='Number of Samples / Neurite')
# #
# #
# # plt.savefig('/Users/abdellah/Desktop/nmv-release/figures/dist-1.pdf', bbox_inches='tight')
# #
# # '''
# #
# #
# # x_axis = ['Basal Dendrite 0', 'Basal Dendrite 1', 'Basal Dendrite 2', 'Apical Dendrite']
# # min_data = [4.469760959142065, 7.429318189136655, 21.034047220450837, 0.3162306578714944]
# # avg_data = [86.87139467061229, 73.46274246569858, 81.64371511318917, 60.81749461580289]
# # max_data = [196.56449098822156, 203.49834721120786, 124.24572760742443, 211.88618914987208]
# # data = [y, z, k]
# # X = np.arange(4)
# # plt.bar(X + 0.00, data[0], color = 'b', width = 0.25)
# # plt.bar(X + 0.25, data[1], color = 'g', width = 0.25)
# # plt.bar(X + 0.50, data[2], color = 'r', width = 0.25)
# #
# # plt.savefig('%s/dist-1.pdf' % os.getcwd(), bbox_inches='tight')
# #
# #
# # df = pandas.DataFrame({
# #     'Factor': x,
# #     'Min': y,
# #     'Avg': z,
# #     'Max': k})
# #
# # fig, ax1 = plt.subplots(figsize=(10, 10))
# # tidy = df.melt(id_vars='Factor').rename(columns=str.title)
# # seabron.barplot(x='Factor', y='Value', hue='Variable', data=tidy, ax=ax1)
#
# # needed imports
# from matplotlib import pyplot as plt
# from scipy.cluster.hierarchy import dendrogram, linkage
# import numpy as np
#
# matrix = np.array([
#     [3., 2., 1.], [2., 1., 1.], [1., 0., 1.],
#     [4., 2., 1.], [2., 1., 1.], [1., 0., 1.],
#     [5., 1., 1.], [0., 1., 1.]
# ])
# from scipy.cluster.hierarchy import dendrogram
# import matplotlib.pyplot as plt
#
# import numpy as np
# from scipy.cluster.hierarchy import linkage
# import matplotlib.pyplot as plt
#
# def augmented_dendrogram(*args, **kwargs):
#
#     ddata = dendrogram(*args, **kwargs)
#
#     if not kwargs.get('no_plot', False):
#         for i, d in zip(ddata['icoord'], ddata['dcoord']):
#             x = 0.5 * sum(i[1:3])
#             y = d[1]
#             plt.plot(x, y, 'ro')
#             plt.annotate("%.3g" % y, (x, y), xytext=(0, -8),
#                          textcoords='offset points',
#                          va='top', ha='center')
#
#     return ddata
#
# # Generate a random sample of `n` points in 2-d.
# np.random.seed(12312)
# n = 10
# x = np.random.multivariate_normal([0, 0], np.array([[4.0, 2.5], [2.5, 1.4]]),
#                                   size=(n,))
#
#
# print(x)
#
# linkage_matrix = linkage(x, "single")
# print(linkage_matrix)
#
# plt.figure(figsize=(10, 4))
# plt.clf()
#
# show_leaf_counts = False
# ddata = augmented_dendrogram(linkage_matrix,
#                color_threshold=1,
#                p=6,
#                truncate_mode='lastp',
#                show_leaf_counts=show_leaf_counts,
#                )
# plt.title("show_leaf_counts = %s" % show_leaf_counts)
# plt.savefig('dendrogram_01b.pdf')


import numpy as np
import seaborn as seabron
import matplotlib as mpl
import matplotlib.pyplot as plt

from matplotlib.colors import ListedColormap, LinearSegmentedColormap

seabron.set_style('ticks')
seabron.set_context('paper')

mpl.rcParams['axes.linewidth']=0.5
FIGW = 183  # max width (mm), for nature neuroscience
FIGH = 247  # max height (mm), for nature neuroscience
labelsize=6  # label (font) size
linewidth=0.75

# Custom colormaps
mygreen = (0.313, 0.768, 0.458)
myblue = (0.274, 0.533, 0.925)
myred = (0.996, 0.223, 0.352)
mygrey = (0.42, 0.42, 0.42)


# In[3]:


def mm_2_inches(mm):
    mm_per_inch = 25.4
    if type(mm) is tuple:
        return tuple([e*(1/mm_per_inch) for e in mm])
    else:
        return (1/mm_per_inch) * mm


# In[4]:


y_axis = [0, 1, 2, 3]
y_labels = ['Basal Dendrite 0', 'Basal Dendrite 1', 'Basal Dendrite 2', 'Apical Dendrite']
min_data = np.array([4.469760959142065, 7.429318189136655, 21.034047220450837, 0.3162306578714944])
avg_data = np.array([86.87139467061229, 73.46274246569858, 81.64371511318917, 60.81749461580289])
max_data = np.array([196.56449098822156, 203.49834721120786, 124.24572760742443, 211.88618914987208])


# In[7]:


fig, ax = plt.subplots(figsize=mm_2_inches((FIGW/2.5,FIGW/3.75)))

xerr = np.array([avg_data - min_data, max_data - avg_data])
ax.barh(y_labels, avg_data, color=[myred, myblue, mygreen, mygrey], xerr=xerr, tick_label=y_labels, error_kw={'elinewidth':0.75}, linewidth=0, capsize=2.25)
seabron.despine(bottom=True, top=False)
ax.invert_yaxis()
ax.xaxis.set_ticks_position('top')
ax.tick_params(labelsize=labelsize, **{'length': 3.0, 'pad': 3.0})

plt.savefig('bar_chart_marwan.pdf', transparent=True)




import os
import numpy as np
import seaborn
import pandas

import matplotlib.pyplot as plt

from matplotlib import font_manager, rcParams


# Clear the figure
plt.clf()

# Loading fonts
# font_dirs = ['/computer/bbp-blender-development/nmv-blender-2.80/Blender-2.80.app/Contents/Resources/2.80/scripts/addons/NeuroMorphoVis/data/fonts']
font_dirs = ['/bbp/bbp-blender-packages/nmv-blender-2.80-linux-glibc217-x86_64/2.80/scripts/addons/neuromorphovis/data/fonts']
font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
font_list = font_manager.createFontList(font_files)
font_manager.fontManager.ttflist.extend(font_list)

####################################################################################################
# Example data
x_data = ['Axon',
          'Basal Dendrite 0',
          'Basal Dendrite 1',
          'Basal Dendrite 2',
          'Basal Dendrite 3',
          'Basal Dendrite 4',
          'Apical Dendrite']
y_data = [159, 161, 96, 219, 107, 61, 672]

# Total number of bars, similar to arbors
total_number_of_bars = len(x_data)

# The width of each bar
bar_width = 0.55

# Adjust seaborn configuration
seabron.set_style("white")

# The color palette
# palette = seabron.cubehelix_palette(2 * total_number_of_bars)
palette = seabron.color_palette("pastel", total_number_of_bars)
seabron.set_palette(palette=palette)

# Adjusting the matplotlib parameters
plt.rcParams['axes.grid'] = 'False'
plt.rcParams['font.family'] = 'NimbusSanL'
plt.rcParams['axes.linewidth'] = 0.0
plt.rcParams['axes.labelsize'] = bar_width * 10
plt.rcParams['axes.labelweight'] = 'regular'
plt.rcParams['xtick.labelsize'] = bar_width * 10
plt.rcParams['ytick.labelsize'] = bar_width * 10
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['axes.titlesize'] = bar_width * 1.25 * 10
plt.rcParams['axes.axisbelow'] = True
plt.rcParams['axes.edgecolor'] = '0.1'

# numpay array from the lists
x = np.asarray(x_data)
y = np.asarray(y_data)

# Adjusting the figure size
plt.figure(figsize=(bar_width * 4, total_number_of_bars * 0.5 * bar_width))

# Plot the bar plot
ax = seabron.barplot(x=y, y=x, edgecolor='none')

# Title
ax.set(xlabel='Number of Samples', title='Number of Samples / Neurite')
ax.spines['left'].set_linewidth(0.5)
ax.spines['left'].set_color('black')

# Add percentage on the right side of the bar
for bar in ax.patches:

    # Current Y center
    y = bar.get_y()

    # Current bar height
    height = bar.get_height()

    # Current center
    centre = y + height / 2.0

    # Set the new center
    bar.set_y(centre - bar_width / 2.0)

    # Set the new height
    bar.set_height(bar_width)


# Create a list to collect the plt.patches data
totals = []

# Find the values and append to list
for i in ax.patches:
    totals.append(i.get_width())

# Set individual bar labels using above list
total = sum(totals)

# Set individual bar lables using above list
for i, patch in enumerate(ax.patches):
    # get_width pulls left or right; get_y pushes up or down

    # Get the width of the bar and then add a little increment
    increment = 15
    x = patch.get_width() + increment
    y = patch.get_y() + (bar_width / 2.0) + (bar_width / 8.0)

    # Compute the percentage
    percentage = round((patch.get_width() / total) * 100, 2)
    value = '%d (%2.1f%%)' % (y_data[i], percentage)
    ax.text(x, y, value, fontsize=bar_width * 10, color='dimgrey')

# Save the figure
plt.savefig('example-per-arbor-distribution.pdf', bbox_inches='tight')

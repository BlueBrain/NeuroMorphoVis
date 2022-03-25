#!/usr/bin/python

# -*- coding: iso-8859-15 -*-


# System imports
import sys, os, re, math
import subprocess
import argparse
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager
from matplotlib.ticker import PercentFormatter
from matplotlib.ticker import FormatStrFormatter
	
FILE_TYPES = ['.png']
FILE_TYPE = '.png'
sns.set(color_codes=True)
'''
sns.set_style("whitegrid", 
    {'axes.axisbelow': True,
  'axes.edgecolor': '.8',
  'axes.facecolor': 'white',
  'axes.grid': False,
  'axes.labelcolor': '.6',
  'axes.linewidth': 0.0,
  'font.family': 'Arimo',
  'grid.color': '.8',
  'grid.linestyle': u'-',
  'image.cmap': u'Greys',
  'legend.frameon': True,
  'legend.numpoints': 1,
  'legend.scatterpoints': 1,
  'lines.solid_capstyle': u'round',
  'text.color': '.15',
  'xtick.color': '.15',
  'xtick.direction': u'out',
  'xtick.major.size': 0.0,
  'xtick.minor.size': 0.0,
  'ytick.color': '.15',
  'ytick.direction': u'out',
  'ytick.major.size': 0.0,
  'ytick.minor.size': 0.0
    }
)
'''

# Colors
# b: blue
# g: green
# r: red
# c: cyan
# m: magenta
# y: yellow
# k: black
# w: white

####################################################################################################
# @verify_plotting_packages
####################################################################################################
def verify_plotting_packages():
    """Verifies that all the plotting packages are installed. Otherwise, install the missing one.
    """
    
    import matplotlib
    from matplotlib import font_manager

    # Import the fonts
    font_dirs = [os.path.dirname(os.path.realpath(__file__)) + '/fonts/']
    font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
    font_list = font_manager.createFontList(font_files)
    font_manager.fontManager.ttflist.extend(font_list)

sns.set_style("whitegrid")
plt.rcParams['axes.grid'] = 'True'
plt.rcParams['font.family'] = 'NimbusSanL'
plt.rcParams['font.monospace'] = 'Regular'
plt.rcParams['font.style'] = 'normal'

plt.rcParams['axes.linewidth'] = 0.0
plt.rcParams['axes.labelsize'] = 30
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['xtick.labelsize'] = 30
plt.rcParams['ytick.labelsize'] = 30
plt.rcParams['legend.fontsize'] = 40
plt.rcParams['figure.titlesize'] = 40
plt.rcParams['axes.titlesize'] = 40
plt.rcParams['axes.edgecolor'] = '0.1'




# plt.rcParams['xtick.major.size'] = 1
# plt.rcParams['xtick.minor.size'] = 0.50
# plt.rcParams['xtick.direction'] = u'out'


####################################################################################################
# @parse_command_line_arguments
####################################################################################################
def parse_command_line_arguments(arguments=None):

    # Add all the options
    description = 'Plotting'
    parser = argparse.ArgumentParser(description=description)

    arg_help = 'Input file'
    parser.add_argument('--input', action='store', dest='input', help=arg_help)

    arg_help = 'Output directory where output written'
    parser.add_argument('--output', action='store', dest='output', help=arg_help)
                        
    # Parse the arguments
    return parser.parse_args()


####################################################################################################
# @read_dist_file
####################################################################################################
def read_dist_file(file_path, invert=False):

    data = list()
    file = open(file_path, 'r')
    for line in file:
        content = line.strip(' ').split(' ')
        value = float(content[1])
        if invert:
            value = 1.0 / value
        data.append(value)
    file.close()
    return data


####################################################################################################
# @ plot_dist_file
####################################################################################################
def plot_dist_file(input_directory,
                   dist_file,
                   output_directory,
                   title,
                   plot_titles=True,
                   xmax=100,
                   decimals=1,
                   kde=False,
                   color='b', 
                   invert=False):

    print('\t* ' + title)                   

    # Clear figure 
    plt.clf()
    
    # Get the data list 
    data = read_dist_file('%s/%s' % (input_directory, dist_file), invert=invert)

    # Convert the data to numpy array 
    np_data = np.array(data)

    # Adjusting the figure size
    plt.figure(figsize=(10, 10))

    # Set the title
    if plot_titles:
        plt.title(title, y=0.9)

    # Plot the histogram 
    sns.distplot(np_data, color='r', hist=True, kde=kde, norm_hist=True, bins=40,
                 hist_kws={"color": color, "lw": 0.5},
                 kde_kws={"color": color, "lw": 0.5})

    # Adjust the Y-axis format
    plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=xmax, decimals=decimals, symbol=' %'))

    # Save the figure
    for file_type in FILE_TYPES:
        plt.savefig('%s/%s' % (output_directory,
                               dist_file.replace('.dist', file_type)), dpi=300, bbox_inches='tight')

    # Close figure to reset
    plt.close()


####################################################################################################
# @get_image
####################################################################################################
def get_image(images, search_keyword, measure):
    for file in images:
        if 'stats' in file:
            continue    
        
        keyword = '%s-%s.' % (search_keyword, measure)
        if keyword in file:
            if '.png' in file:
                return file
    return None                


####################################################################################################
# @get_stats_image
####################################################################################################
def get_stats_image(images, search_keyword, measure):
    for file in images:
        
        keyword = '%s-%s.' % (search_keyword, measure)

        if keyword in file:
            return file
    return None  

    
####################################################################################################
# @stack_images
####################################################################################################
def stack_images(directory, search_keyword):

    all_files = os.listdir(directory)
    
    image_files = list()
    image_files.append(get_image(all_files, search_keyword, 'condition-number'))
    image_files.append(get_image(all_files, search_keyword, 'aspect-forbenius'))
    image_files.append(get_image(all_files, search_keyword, 'radius-ratio'))
    image_files.append(get_image(all_files, search_keyword, 'edge-ratio'))
    image_files.append(get_image(all_files, search_keyword, 'radius-to-edge-ratio'))
    image_files.append(get_image(all_files, search_keyword, 'min-angle'))
    image_files.append(get_image(all_files, search_keyword, 'max-angle'))
    image_files.append(get_image(all_files, search_keyword, 'relative-size'))
    image_files.append(get_image(all_files, search_keyword, 'triangle-shape'))
    image_files.append(get_image(all_files, search_keyword, 'triangle-shape-size'))
    image_files.append(get_image(all_files, search_keyword, 'scaled-jacobian'))
    
    shell_command_images = ''
    for image in image_files:
        if image is None:
            continue
        shell_command_images += ' %s/%s ' % (directory, image)
    
    subprocess.call('convert ' + shell_command_images + ' -append %s/summary-%s-stats%s' %
        (directory, search_keyword, FILE_TYPE), shell=True)

    shell_command = 'montage ' + shell_command_images + \
        ' -tile 5x2 -geometry +0+0 %s/hotizontal-%s-stats%s' % (directory, search_keyword, FILE_TYPE)
    print(shell_command)
    subprocess.call(shell_command, shell=True)
    

####################################################################################################
# @stack_groups
####################################################################################################
def stack_groups(directory):

    all_files = os.listdir(directory)

    summary_files = list()
    for file in all_files:
        if 'summary' in file:
            summary_files.append(file)
                
    image_files = list()
    image_files.append(get_stats_image(summary_files, 'summary', 'input-stats'))
    image_files.append(get_stats_image(summary_files, 'summary', 'dmc-stats'))
    image_files.append(get_stats_image(summary_files, 'summary', 'optimized-stats'))
    image_files.append(get_stats_image(summary_files, 'summary', 'watertight-stats'))

    shell_command_images = 'convert '
    for image in image_files:
        if image is None:
            continue
        shell_command_images += ' %s/%s ' % (directory, image)

    shell_command = 'montage ' + shell_command_images + \
        ' -tile 4x1 -geometry +0+0 %s/vertical-%s-stats%s' % (directory, 'all', FILE_TYPE)
    print(shell_command)
    subprocess.call(shell_command, shell=True)

    
####################################################################################################
# @plot_group
####################################################################################################
def plot_group(keyword, dist_files, plot_titles=False, use_kde=False):
    #cmap = plt.cm.get_cmap('jet')
    #colors = cmap(np.arange(10))
    #print(colors)

    colors = sns.color_palette("icefire", 10)
    print(colors)

    i = 0
    for file in dist_files:
        if keyword in file:

            if 'condition-number' in file:
                plot_dist_file(args.input, file, args.output,
                    title='Condition Number', color=colors[0], kde=use_kde, plot_titles=plot_titles)

            if 'radius-ratio' in file:
                plot_dist_file(args.input, file, args.output,
                    title='Radius Ratio', color=colors[1], kde=use_kde, plot_titles=plot_titles, invert=True)

            if 'edge-ratio' in file:
                plot_dist_file(args.input, file, args.output,
                    title='Edge Ratio', color=colors[2], kde=use_kde, plot_titles=plot_titles, invert=True)

            if 'radius-to-edge-ratio' in file:
                plot_dist_file(args.input, file, args.output,
                    title='Radius to Edge Ratio', color=colors[3], kde=use_kde, plot_titles=plot_titles, invert=True)

            if 'min-angle' in file:
                plot_dist_file(args.input, file, args.output,
                    title='Min. Dihedral Angle (deg)', xmax=1, color=colors[4],
                    kde=use_kde, plot_titles=plot_titles)

            if 'max-angle' in file:
                plot_dist_file(args.input, file, args.output,
                    title='Max. Dihedral Angle (deg)', xmax=1, color=colors[5],
                    kde=use_kde, plot_titles=plot_titles)

            if 'relative-size' in file:
                plot_dist_file(args.input, file, args.output,
                    title='Relative Size', color=colors[6], kde=use_kde, plot_titles=plot_titles)

            if 'triangle-shape' in file:
                plot_dist_file(args.input, file, args.output,
                    title='Shape', color=colors[7], kde=use_kde, plot_titles=plot_titles)

            if 'triangle-shape-size' in file:
                plot_dist_file(args.input, file, args.output,
                    title='Shape & Size', color=colors[8], kde=use_kde, plot_titles=plot_titles)

            if 'scaled-jacobian' in file:
                plot_dist_file(args.input, file, args.output,
                    title='Scaled Jacobian', color=colors[9], kde=use_kde, plot_titles=plot_titles)


    stack_images(args.output, keyword)



####################################################################################################
# @read_dist_file
####################################################################################################
def read_sample_file(file_path):

    data = list()
    file = open(file_path, 'r')
    for line in file:
        content = line.strip(' ').split(' ')
        index = int(content[0])
        value = float(content[1])
    file.close()
    return data


####################################################################################################
# @ Main
####################################################################################################
if __name__ == "__main__":

    # Parse the command line arguments
    args = parse_command_line_arguments()
    
    all_files = os.listdir(args.input)
    dist_files = list()

    for file in all_files:
        if '.dist' in file:
            dist_files.append(file)

    plot_titles = True
    use_kde = False
    
    verify_plotting_packages()
    
    try:
        print('input')
        plot_group('input', dist_files, plot_titles=plot_titles, use_kde=use_kde)
    except ValueError:
        pass 

    try:
        print('dmc')
        plot_group('dmc', dist_files, plot_titles=plot_titles, use_kde=use_kde)
    except ValueError:
        pass 
        
    try:
        print('optimized')
        plot_group('optimized', dist_files, plot_titles=plot_titles, use_kde=use_kde)
    except ValueError:
        pass 

    try:
        print('watertight')
        plot_group('watertight', dist_files, plot_titles=plot_titles, use_kde=use_kde)
    except ValueError:
        pass
    
    
          

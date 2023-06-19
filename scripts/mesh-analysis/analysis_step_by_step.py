####################################################################################################
# Copyright (c) 2020, EPFL / Blue Brain Project
# Author(s): Marwan Abdellah <marwan.abdellah@epfl.ch>
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

# Internal imports
import nmv.scene
import nmv.interface
import nmv.bbox
import nmv.enums

# System imports
import os
import sys
import subprocess
import numpy
import seaborn
import matplotlib.pyplot as pyplot

# Internal
sys.path.append(('%s/.' % (os.path.dirname(os.path.realpath(__file__)))))
sys.path.append(('%s/utilities/' % (os.path.dirname(os.path.realpath(__file__)))))

import data_utilities as dutils
import file_utilities as futils
import image_utilities as imutils
import mesh_analysis
import fact_sheet


####################################################################################################
# Per-adjust all the plotting configuration
####################################################################################################
font_size = 30
seaborn.set_style("whitegrid")
pyplot.rcParams['axes.grid'] = 'True'
pyplot.rcParams['grid.linestyle'] = '--'
pyplot.rcParams['grid.linewidth'] = 1.0
pyplot.rcParams['grid.color'] = 'gray'
pyplot.rcParams['grid.alpha'] = 0.25
pyplot.rcParams['font.family'] = 'Helvetica LT Std'
# pyplot.rcParams['font.family'] = 'NimbusSanL'
pyplot.rcParams['font.monospace'] = 'Regular'
pyplot.rcParams['font.style'] = 'normal'
pyplot.rcParams['axes.labelweight'] = 'bold'
pyplot.rcParams['axes.linewidth'] = 1.0
pyplot.rcParams['axes.labelsize'] = font_size
pyplot.rcParams['xtick.labelsize'] = font_size
pyplot.rcParams['ytick.labelsize'] = font_size
pyplot.rcParams['legend.fontsize'] = font_size
pyplot.rcParams['figure.titlesize'] = font_size
pyplot.rcParams['axes.titlesize'] = font_size
pyplot.rcParams['xtick.major.pad'] = '10'
pyplot.rcParams['ytick.major.pad'] = '0'
pyplot.rcParams['axes.edgecolor'] = '1'


####################################################################################################
# @plot_back2back_histograms_normalized
####################################################################################################
def plot_histograms_normalized(dists_directory,
                               output_directory,
                               hist_data,
                               hist_watertight,
                               output_prefix,
                               title=None,
                               invert=False,
                               figure_width=3,
                               figure_height=10,
                               bins=40,
                               color='red',
                               axvline_color='black',
                               bin_width=0.9,
                               save_pdf=False,
                               save_svg=False,
                               dpi=150):
    # Title
    if title is not None:
        print('\t* Plotting [%s]' % title)

    # Read the distributions
    data = futils.read_dist_file('%s/%s' % (dists_directory, hist_data), invert=invert)

    # Clear figure, getting ready for a new figure
    pyplot.clf()

    # A new figure with the given dimensions size
    pyplot.figure(figsize=(figure_width, figure_height))
    pyplot.tight_layout()

    # Create a new frame for the plot to combine both
    frame = pyplot.gca()

    y, x = numpy.histogram(data, bins=bins)
    y = y / max(y)

    x_min = min(x)
    x_max = max(x)
    delta = x_max - x_min
    step = delta / bins
    bins = numpy.arange(x_min, x_max, step)

    # Right histogram
    pyplot.barh(bins, y, color=color, height=step * bin_width)

    # Only plot the Y-axis
    frame.axes.get_xaxis().set_visible(False)
    frame.axes.get_yaxis().set_visible(True)

    # Remove any labels
    pyplot.xlabel('')
    pyplot.ylabel(title)

    pyplot.gca().yaxis.set_major_locator(pyplot.MaxNLocator(5))

    # Add the title if not None
    if title is not None:
        pyplot.title(title, y=1.05)

    # The central line
    pyplot.axvline(0.0)
    pyplot.axvline(linewidth=1, color=axvline_color)

    # Save PNG by default
    pyplot.savefig('%s/%s.png' % (output_directory, output_prefix),
                   dpi=dpi, bbox_inches='tight')

    # Save PDF
    pyplot.savefig('%s/%s.pdf' % (output_directory, output_prefix),
                   dpi=dpi, bbox_inches='tight') if save_pdf else None

    # Save SVG
    pyplot.savefig('%s/%s.svg' % (output_directory, output_prefix),
                   dpi=dpi, bbox_inches='tight') if save_svg else None

    # Close figure to reset
    pyplot.clf()
    pyplot.cla()
    pyplot.close()

    # Return a reference to the PNG image
    return output_prefix + '.png'


####################################################################################################
# @plot_back2back_histograms_normalized
####################################################################################################
def plot_back2back_histograms_normalized(dists_directory,
                                         output_directory,
                                         hist_left,
                                         hist_right,
                                         output_prefix,
                                         title=None,
                                         invert=False,
                                         figure_width=5,
                                         figure_height=10,
                                         bins=40,
                                         color_1='red',
                                         color_2='blue',
                                         axvline_color='black',
                                         bin_width=0.9,
                                         save_pdf=False,
                                         save_svg=False,
                                         dpi=150,
                                         edge_gap=0.05):
    # Title
    if title is not None:
        print('\t* Plotting [%s]' % title)

    # Read the distributions
    data_left = futils.read_dist_file('%s/%s' % (dists_directory, hist_left), invert=invert)
    data_right = futils.read_dist_file('%s/%s' % (dists_directory, hist_right), invert=invert)

    # Clear figure, getting ready for a new figure
    pyplot.clf()

    # A new figure with the given dimensions size
    pyplot.figure(figsize=(figure_width, figure_height))
    pyplot.tight_layout()

    # Create a new frame for the plot to combine both
    frame = pyplot.gca()

    ry, rx = numpy.histogram(data_right, bins=bins)
    ly, lx = numpy.histogram(data_left, bins=bins)

    ry = ry / max(ry)
    ly = ly / max(ly)

    x_min = min(min(rx), min(lx))
    x_max = max(max(rx), max(lx))
    delta = x_max - x_min
    step = delta / bins
    bins = numpy.arange(x_min, x_max, step)

    # Right histogram
    pyplot.barh(bins, ry, color=color_1, height=step * bin_width)

    # Left histogram
    pyplot.barh(bins, -ly, color=color_2, height=step * bin_width)

    # Only plot the Y-axis
    frame.axes.get_xaxis().set_visible(False)
    frame.axes.get_yaxis().set_visible(True)

    # Remove any labels
    pyplot.xlabel('')
    pyplot.ylabel('')

    pyplot.gca().yaxis.set_major_locator(pyplot.MaxNLocator(5))

    # Add the title if not None
    if title is not None:
        pyplot.title(title, y=1.05)

    # The central line
    pyplot.axvline(0.0)
    pyplot.axvline(linewidth=1, color=axvline_color)

    # Save PNG by default
    pyplot.savefig('%s/%s.png' % (output_directory, output_prefix),
                   dpi=dpi, bbox_inches='tight')

    # Save PDF
    pyplot.savefig('%s/%s.pdf' % (output_directory, output_prefix),
                   dpi=dpi, bbox_inches='tight') if save_pdf else None

    # Save SVG
    pyplot.savefig('%s/%s.svg' % (output_directory, output_prefix),
                   dpi=dpi, bbox_inches='tight') if save_svg else None

    # Close figure to reset
    pyplot.clf()
    pyplot.cla()
    pyplot.close()

    # Return a reference to the PNG image
    return output_prefix + '.png'


####################################################################################################
# @create_distributions_image
####################################################################################################
def create_distributions_image(mesh_name,
                               suffix,
                               dists_directory,
                               intermediate_directory,
                               palette=seaborn.color_palette("flare", n_colors=10)):

    # Verify packages
    dutils.verify_plotting_packages()

    # Loading the fonts
    nmv.interface.load_fonts()

    # List all the distributions in the file
    files = os.listdir(dists_directory)
    dists = list()
    for f in files:
        if '.dist' in f and mesh_name in f:
            dists.append(f)

    # Search strings
    strings = [['min-angle', 'Min. Dihedral Angle$^\circ$', False],
               ['max-angle', 'Max. Dihedral Angle$^\circ$', False],
               ['triangle-shape', 'Shape', False],
               ['radius-ratio', 'Radius Ratio', True],
               ['edge-ratio', 'Edge Ratio', True],
               ['radius-to-edge-ratio', 'Radius to Edge Ratio', True]]

    # Plot the distributions and store the images
    dists_pngs = list()
    for i, string in enumerate(strings):
        dists_pngs.append(plot_back2back_histograms_normalized(
            dists_directory=dists_directory,
            output_directory=intermediate_directory,
            hist_left=futils.search_for_dist(dists, suffix, string[0]),
            hist_right=futils.search_for_dist(dists, 'watertight', string[0]),
            output_prefix='%s-%s-%s' % (mesh_name, suffix, string[0]),
            invert=string[2],
            title=string[1],
            color_1=palette[0], color_2=palette[5], axvline_color=palette[9]))

    # Statistic image with all the distributions
    distributions_image = imutils.montage_distributions_horizontally(
        montage_name='%s-%s' % (mesh_name, suffix), input_directory=intermediate_directory,
        distribution_images=dists_pngs, output_directory=intermediate_directory)

    # Return a reference to the image
    return distributions_image


####################################################################################################
# @create_fact_sheet_image
####################################################################################################
def create_fact_sheet_image(mesh_path,
                            output_directory,
                            scenes_directory,
                            reference_name,
                            color,
                            render_meshes=False,
                            mesh_resolution=1500,
                            fact_sheet_resolution=1500,
                            palette=seaborn.color_palette("flare", n_colors=10)):

    # Clear the scene
    nmv.scene.clear_scene()

    # Load the input mesh
    mesh_object = nmv.file.import_mesh(mesh_path)

    # Rotate the mesh object to adjust the orientation in front of the camera
    nmv.scene.rotate_object(mesh_object, 0, 0, 0)

    # Compute the mesh stats
    stats, aabb, wtc = mesh_analysis.compute_mesh_stats(mesh_object)

    # Export it to a blender file
    nmv.file.export_scene_to_blend_file(
        output_directory=scenes_directory, output_file_name=reference_name)

    # Create the fact sheets
    fact_sheet_image = fact_sheet.create_step_by_step_fact_sheet(
        stats=stats, aabb=aabb, wtc=wtc, color=color,
        output_image_path=output_directory, fact_sheet_name=reference_name,
        resolution=fact_sheet_resolution)

    # Return a reference to the image
    return fact_sheet_image


####################################################################################################
# @create_watertight_mesh
####################################################################################################
def create_watertight_mesh(arguments,
                           input_mesh,
                           output_directory):

    # Create the shell command
    shell_command = '%s ' % arguments.ultraMesh2Mesh
    shell_command += '--mesh %s ' % input_mesh
    shell_command += '--output-directory %s ' % output_directory
    shell_command += '--auto-resolution --voxels-per-micron %s ' % str(arguments.voxels_per_micron)
    shell_command += '--solid '
    shell_command += '--optimize-mesh --adaptive-optimization '
    shell_command += '--export-obj-mesh '
    shell_command += '--stats --dists '

    # Execute the shell command
    print(shell_command)
    subprocess.call(shell_command, shell=True)

    # Return a reference to the watertight mesh
    return '%s/meshes/%s-watertight.obj' % (output_directory,
                                            os.path.splitext(os.path.basename(input_mesh))[0])


####################################################################################################
# @create_comparative_mesh_analysis
####################################################################################################
def create_comparative_mesh_analysis(arguments,
                                     mesh_file,
                                     intermediate_directory,
                                     images_directory,
                                     scenes_directory):

    # Full path
    input_mesh_path = '%s/%s' % (arguments.input_directory, mesh_file)

    # Mesh name
    mesh_name = os.path.splitext(os.path.basename(input_mesh_path))[0]

    # Create the watertight mesh, and the stats.
    watertight_mesh_path = create_watertight_mesh(
        arguments=arguments, input_mesh=input_mesh_path,
        output_directory=arguments.output_directory)

    # Create the color palette
    palette = seaborn.color_palette("flare", n_colors=10)

    # Create the distribution image
    distributions_image = create_distributions_image(
        mesh_name=mesh_name, suffix='input',
        dists_directory='%s/distributions' % arguments.output_directory,
        intermediate_directory=intermediate_directory, palette=palette)

    # Create the fact sheet image and the combined rendering image
    fact_sheet_image = create_fact_sheet_image(
        mesh_path=input_mesh_path,
        output_directory=intermediate_directory, scenes_directory=scenes_directory,
        color=dutils.convert_color(palette[5]),
        reference_name=mesh_name, fact_sheet_resolution=1500, render_meshes=True)

    # Combines the stats. image with the fact sheet image to create the final image
    distribution_with_fact_sheet_image = imutils.combine_distributions_with_fact_sheet(
        distributions_image=distributions_image, fact_sheet_image=fact_sheet_image,
        output_directory=images_directory, image_name=mesh_name)

    steps = ['dmc', 'optimized', 'watertight']
    for step in steps:
        reference = '%s-%s' % (mesh_name, step)
        mesh_path = '%s/meshes/%s-%s.obj' % (arguments.output_directory,
                                             mesh_name, step)

        # Create the distribution image
        distributions_image = create_distributions_image(
            mesh_name=mesh_name, suffix=step,
            dists_directory='%s/distributions' % arguments.output_directory,
            intermediate_directory=intermediate_directory, palette=palette)

        fact_sheet_image = create_fact_sheet_image(
            mesh_path=mesh_path,
            output_directory=intermediate_directory, scenes_directory=scenes_directory,
            color=dutils.convert_color(palette[5]), reference_name=reference,
            fact_sheet_resolution=1500)

        # Combines the stats. image with the fact sheet image to create the final image
        distribution_with_fact_sheet_image = imutils.combine_distributions_with_fact_sheet(
            distributions_image=distributions_image, fact_sheet_image=fact_sheet_image,
            output_directory=images_directory, image_name=reference)
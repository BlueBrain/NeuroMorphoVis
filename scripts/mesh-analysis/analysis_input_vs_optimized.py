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
import matplotlib.font_manager as font_manager

# Internal
sys.path.append(('%s/.' % (os.path.dirname(os.path.realpath(__file__)))))
sys.path.append(('%s/utilities/' % (os.path.dirname(os.path.realpath(__file__)))))
import data_utilities as dutils
import file_utilities as futils
import image_utilities as imutils
import rendering_utilities as rutils
import mesh_analysis
import fact_sheet

font_path = os.path.dirname(os.path.realpath(__file__)) + '/fonts/' + 'HelveticaLtObl.ttf'
font_manager.fontManager.addfont(font_path)
prop = font_manager.FontProperties(fname=font_path)


####################################################################################################
# Per-adjust all the plotting configuration
####################################################################################################
font_size = 40
seaborn.set_style("whitegrid")
pyplot.rcParams['axes.grid'] = 'True'
pyplot.rcParams['grid.linestyle'] = '--'
pyplot.rcParams['grid.linewidth'] = 1.0
pyplot.rcParams['grid.color'] = 'gray'
pyplot.rcParams['grid.alpha'] = 0.25
# pyplot.rcParams['font.family'] = 'Helvetica LT Std'
pyplot.rcParams['font.family'] = 'NimbusSanL'
# pyplot.rcParams['font.family'] = prop.get_family()
pyplot.rcParams['font.monospace'] = 'Regular'
pyplot.rcParams['font.style'] = 'normal'
pyplot.rcParams['axes.labelweight'] = 'light'
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
# @plot_distribution
####################################################################################################
def plot_distribution(input_directory,
                      dist_file,
                      output_directory,
                      title,
                      plot_titles=True,
                      color='b',
                      invert=False,
                      save_pdf=False,
                      save_svg=False,
                      dpi=150):

    # Clear figure
    pyplot.clf()

    # Get the data list
    data = futils.read_dist_file('%s/%s' % (input_directory, dist_file), invert=invert)

    # Convert the data to numpy array
    np_data = numpy.array(data)

    # Create a new frame for the plot to combine both
    frame = pyplot.gca()

    # Adjusting the figure size
    pyplot.figure(figsize=(10, 5))
    pyplot.tight_layout()

    # Set the title inside the figure to save some space
    if plot_titles:
        pyplot.title(title, y=1.05)

    # Plot the histogram
    ax = seaborn.histplot(np_data, color=color, bins=50, alpha=0.95)

    # No label
    pyplot.ylabel('')

    # Only plot the Y-axis
    ax.axes.get_xaxis().set_visible(True)
    ax.axes.get_yaxis().set_visible(True)
    ax.spines['bottom'].set_color('black')
    ax.grid(zorder=0)

    # Image prefix
    image_prefix = '%s/%s' % (output_directory, dist_file.replace('.dist', ''))

    # By default, save the figure into a PNG image
    pyplot.savefig(image_prefix + '-p.png', dpi=dpi, bbox_inches='tight')

    # Save PDF
    if save_pdf:
        pyplot.savefig(image_prefix + '-p.pdf', dpi=dpi, bbox_inches='tight')

    # Save SVG
    if save_svg:
        pyplot.savefig(image_prefix + '-p.svg', dpi=dpi, bbox_inches='tight')

    # Close figure to reset
    pyplot.clf()
    pyplot.cla()
    pyplot.close()

    # Return a reference to the png image
    return dist_file.replace('.dist', '-p.png')


####################################################################################################
# @plot_back2back_histograms
####################################################################################################
def plot_back2back_histograms(dists_directory,
                              output_directory,
                              hist_left,
                              hist_right,
                              output_prefix,
                              title=None,
                              invert=False,
                              figure_width=5,
                              figure_height=10,
                              bins=50,
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

    plot_distribution(input_directory=dists_directory,
                      dist_file=hist_left, output_directory=output_directory,
                      title=title, plot_titles=True, color=color_2, invert=invert)

    plot_distribution(input_directory=dists_directory,
                      dist_file=hist_right, output_directory=output_directory,
                      title=title, plot_titles=True, color=color_1, invert=invert)

    # Compute the ranges
    min_value = 0 # min(min(data_left), min(data_right))
    max_value = max(max(data_left), max(data_right))

    # Clear figure, getting ready for a new figure
    pyplot.clf()

    # A new figure with the given dimensions size
    pyplot.figure(figsize=(figure_width, figure_height))
    pyplot.tight_layout()

    # Create a new frame for the plot to combine both
    frame = pyplot.gca()

    # Draw the histograms
    h1 = pyplot.hist(data_right, density=True, range=(min_value, max_value),
                     bins=bins, orientation='horizontal', color=color_1, rwidth=bin_width)
    h2 = pyplot.hist(data_left, density=True, range=(min_value, max_value),
                     bins=bins, orientation='horizontal', color=color_2, rwidth=bin_width)

    # Only plot the Y-axis
    frame.axes.get_xaxis().set_visible(True)
    frame.axes.get_yaxis().set_visible(True)

    # Remove any labels
    pyplot.xlabel('')
    pyplot.ylabel('')

    # Add the title if not None
    if title is not None:
        pyplot.title(title, y=1.05)

    # Adjust the patches
    for patch in h2[2]:
        patch.set_width(-patch.get_width())

    # Get the min and maximum values along the x-axis
    x_min = min([min(w.get_width() for w in h2[2]), min([w.get_width() for w in h1[2]])])
    x_max = max([max(w.get_width() for w in h2[2]), max([w.get_width() for w in h1[2]])])

    # Set the limits based on a given edge gap
    delta = edge_gap * (x_max - x_min)
    pyplot.xlim([x_min - delta, x_max + delta])

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
                                         edge_gap=0.05,
                                         plot_individual=False,
                                         plot_lines=False):
    # Title
    if title is not None:
        print('\t* Plotting [%s]' % title)

    # Read the distributions
    data_left = futils.read_dist_file('%s/%s' % (dists_directory, hist_left), invert=invert)
    data_right = futils.read_dist_file('%s/%s' % (dists_directory, hist_right), invert=invert)

    # Plot individuals
    if plot_individual:
        plot_distribution(input_directory=dists_directory,
                          dist_file=hist_left, output_directory=output_directory,
                          title=title, plot_titles=True, color=color_2, invert=invert)

        plot_distribution(input_directory=dists_directory,
                          dist_file=hist_right, output_directory=output_directory,
                          title=title, plot_titles=True, color=color_1, invert=invert)

    # Compute the ranges
    min_value = 0 # min(min(data_left), min(data_right))
    max_value = max(max(data_left), max(data_right))

    # Clear figure, getting ready for a new figure
    pyplot.clf()

    # A new figure with the given dimensions size
    pyplot.figure(figsize=(figure_width, figure_height))
    pyplot.tight_layout()

    # Create a new frame for the plot to combine both
    frame = pyplot.gca()

    ry, rx = numpy.histogram(data_right, bins=bins, range=(min_value, max_value))
    ly, lx = numpy.histogram(data_left, bins=bins, range=(min_value, max_value))

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

    # Plotting lines
    if plot_lines:

        # Line relative distance
        rvalue = 0.75

        # Right line
        x_values = [rvalue, rvalue]
        y_values = [min(data_right), max(data_right)]
        pyplot.plot(x_values, y_values, color=color_1, alpha=0.25)

        # Left line
        x_values = [-rvalue, -rvalue]
        y_values = [min(data_left), max(data_left)]
        pyplot.plot(x_values, y_values, color=color_2, alpha=0.25)

    # Right box plot
    rvalue = 1.25
    bpr = pyplot.boxplot(data_right, positions=[rvalue], showfliers=True,
                         flierprops=dict(marker='o', markersize=5, alpha=0.5,
                                         markerfacecolor=color_1, markeredgecolor=color_1))
    for box in bpr['boxes']:
        box.set(color=color_1, linewidth=1)
    for whisker in bpr['whiskers']:
        whisker.set(color=color_1, linewidth=1)
    for cap in bpr['caps']:
        cap.set(color=color_1, linewidth=1, xdata=cap.get_xdata() + (-0.025, 0.025))
    for median in bpr['medians']:
        median.set(color=axvline_color, linewidth=1)

    # Left box plot
    bpl = pyplot.boxplot(data_left, positions=[-rvalue], showfliers=True,
                         flierprops=dict(marker='o', markersize=5, alpha=0.5,
                                         markerfacecolor=color_2, markeredgecolor=color_2))
    for box in bpl['boxes']:
        box.set(color=color_2, linewidth=1)
    for whisker in bpl['whiskers']:
        whisker.set(color=color_2, linewidth=1)
    for cap in bpl['caps']:
        cap.set(color=color_2, linewidth=1, xdata=cap.get_xdata() + (-0.025, 0.025))
    for median in bpl['medians']:
        median.set(color=axvline_color, linewidth=1)

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
    strings = [['radius-ratio', 'Radius Ratio', True],
               ['edge-ratio', 'Edge Ratio', True],
               ['radius-to-edge-ratio', 'Radius to Edge Ratio', True],
               ['min-angle', 'Min. Dihedral Angle$^\circ$', False],
               ['max-angle', 'Max. Dihedral Angle$^\circ$', False]]

    # Plot the distributions and store the images
    dists_pngs = list()
    for string in strings:
        dists_pngs.append(plot_back2back_histograms_normalized(
            dists_directory=dists_directory,
            output_directory=intermediate_directory,
            hist_left=futils.search_for_dist(dists, 'original', string[0]),
            hist_right=futils.search_for_dist(dists, 'optimized', string[0]),
            output_prefix='%s-%s' % (mesh_name, string[0]),
            invert=string[2],
            title=string[1],
            color_1=palette[5], color_2=palette[0], axvline_color=palette[9]))

    # Statistic image with all the distributions
    distributions_image = imutils.montage_distributions_horizontally(
        montage_name=mesh_name, input_directory=intermediate_directory,
        distribution_images=dists_pngs, output_directory=intermediate_directory)

    # Return a reference to the image
    return distributions_image


####################################################################################################
# @create_fact_sheet_image
####################################################################################################
def create_fact_sheet_image(input_mesh_path,
                            optimized_mesh_path,
                            output_directory,
                            scenes_directory,
                            reference_name,
                            render_meshes=True,
                            mesh_resolution=1500,
                            fact_sheet_resolution=1500,
                            palette=seaborn.color_palette("flare", n_colors=10)):

    # Clear the scene
    nmv.scene.clear_scene()

    # Load the input mesh
    input_mesh_object = nmv.file.import_mesh(input_mesh_path)

    # Rotate the mesh object to adjust the orientation in front of the camera
    nmv.scene.rotate_object(input_mesh_object, 0, 0, 0)

    # Compute the mesh stats
    i_stats, i_aabb, i_wtc = mesh_analysis.compute_mesh_stats(input_mesh_object)

    # Draws the scale bar
    nmv.interface.draw_scale_bar(
        bounding_box=nmv.bbox.compute_scene_bounding_box_for_meshes(),
        view=nmv.enums.Camera.View.FRONT, material_type=nmv.enums.Shader.LAMBERT_WARD)

    # Export it to a blender file
    nmv.file.export_scene_to_blend_file(
        output_directory=scenes_directory, output_file_name='%s-input' % reference_name)

    # Render the meshes
    input_mesh_image = None
    if render_meshes:
        input_mesh_image = '%s/%s.png' % (output_directory, reference_name)
        rutils.render_mesh_object(
            mesh_object=input_mesh_object, mesh_name='%s' % reference_name,
            output_directory=output_directory, mesh_color=palette[5])

    # Clear the scene
    nmv.scene.clear_scene()

    # Load the watertight mesh
    optimized_mesh_object = nmv.file.import_mesh(optimized_mesh_path)

    # Rotate the mesh object to adjust the orientation in front of the camera
    nmv.scene.rotate_object(optimized_mesh_object, 0, 0, 0)

    # Compute the mesh stats
    wt_stats, wt_aabb, wt_wtc = mesh_analysis.compute_mesh_stats(optimized_mesh_object)

    # Draws the scale bar
    nmv.interface.draw_scale_bar(
        bounding_box=nmv.bbox.compute_scene_bounding_box_for_meshes(),
        view=nmv.enums.Camera.View.FRONT, material_type=nmv.enums.Shader.LAMBERT_WARD)

    # Render the meshes
    optimized_mesh_image = None
    if render_meshes:
        optimized_mesh_image = '%s/%s-optimized.png' % (output_directory, reference_name)
        rutils.render_mesh_object(
            mesh_object=optimized_mesh_object, mesh_name='%s-optimized' % reference_name,
            output_directory=output_directory, mesh_color=palette[0])

    # Export it to a blender file
    nmv.file.export_scene_to_blend_file(
        output_directory=scenes_directory, output_file_name='%s-optimized' % reference_name)

    # Combine the mesh images if they are not None
    combined_renderings_image = None
    if input_mesh_image is not None and optimized_mesh_image is not None:

        # Switch direction based on resolution s
        width, height = imutils.get_image_dimensions(input_mesh_image)
        if width > 1.5 * height:
            combined_renderings_image = imutils.montage_list_images_with_same_dimensions_vertically(
                list_images=[input_mesh_image, optimized_mesh_image],
                output_directory=output_directory, montage_name='%s-renderings' % reference_name)
        else:
            combined_renderings_image = \
                imutils.montage_list_images_with_same_dimensions_horizontally(
                    list_images=[input_mesh_image, optimized_mesh_image],
                    output_directory=output_directory,
                    montage_name='%s-renderings' % reference_name)

    # Create the fact sheets
    fact_sheet_image = fact_sheet.create_input_vs_watertight_fact_sheet(
        i_stats=i_stats, i_aabb=i_aabb, i_wtc=i_wtc,
        wt_stats=wt_stats, wt_aabb=wt_aabb, wt_wtc=wt_wtc,
        i_color=dutils.convert_color(palette[0]), wt_color=dutils.convert_color(palette[5]),
        output_image_path=output_directory, fact_sheet_name=reference_name,
        resolution=fact_sheet_resolution)

    # Return a reference to the image
    return fact_sheet_image, combined_renderings_image


####################################################################################################
# @run_quality_checker
####################################################################################################
def run_quality_checker(mesh_path,
                        quality_checker_executable,
                        output_directory,
                        prefix):
    """Runs the quality checker to create stats. about the mesh.

    :param mesh_path:
        The path to the mesh file.
    :param quality_checker_executable:
        The executable of Ultraliser checker.
    :param output_directory:
        The root output directory
    """

    # Make sure that this directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Construct the command
    command = '%s --mesh %s --output-directory %s --prefix %s' % \
              (quality_checker_executable, mesh_path, output_directory, prefix)
    subprocess.call(command, shell=True)

####################################################################################################
# @create_comparative_mesh_analysis
####################################################################################################
def create_comparative_mesh_analysis(arguments,
                                     mesh_file,
                                     intermediate_directory,
                                     images_directory,
                                     scenes_directory):

    # Verify the packages
    dutils.verify_plotting_packages()

    # Full path
    input_mesh_path = '%s/original/%s' % (arguments.input_directory, mesh_file)

    # Mesh name
    mesh_name = os.path.splitext(os.path.basename(input_mesh_path))[0]

    run_quality_checker(mesh_path=input_mesh_path, quality_checker_executable=arguments.quality_checker_executable, output_directory=arguments.output_directory, prefix='%s_original' % mesh_name)

    # Create the watertight mesh, and the stats if the stats are not created
    optimized_mesh_path = '%s/optimized/%s' % (arguments.input_directory, mesh_file)

    run_quality_checker(mesh_path=optimized_mesh_path, quality_checker_executable=arguments.quality_checker_executable, output_directory=arguments.output_directory, prefix='%s_optimized' % mesh_name)

    # Create the color palette
    palette = seaborn.color_palette("flare", n_colors=10)

    # Create the distribution image
    distributions_image = create_distributions_image(
        mesh_name=mesh_name, dists_directory='%s/distributions' % arguments.output_directory,
        intermediate_directory=intermediate_directory, palette=palette)

    # Create the fact sheet image and the combined rendering image
    fact_sheet_image, combined_renderings_image = create_fact_sheet_image(
        input_mesh_path=input_mesh_path, optimized_mesh_path=optimized_mesh_path,
        output_directory=intermediate_directory, scenes_directory=scenes_directory,
        reference_name=mesh_name, fact_sheet_resolution=1500, render_meshes=True)

    # Combines the stats. image with the fact sheet image to create the final image
    distribution_with_fact_sheet_image = imutils.combine_distributions_with_fact_sheet(
        distributions_image=distributions_image, fact_sheet_image=fact_sheet_image,
        output_directory=images_directory, image_name=mesh_name)

####################################################################################################
# Copyright (c) 2020 - 2021, EPFL / Blue Brain Project
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
import nmv.mesh


####################################################################################################
#
####################################################################################################
def plot_data_in_ascending_order(data, output_directory, file_name,
                                 xlabel, ylabel, title,
                                 log_scale=False):

    data.sort()
    x_axis = [x for x in range(len(data))]

    # Plot histogram
    import matplotlib.pyplot as plt
    plt.plot(x_axis, data, color='red', linestyle='--', marker='.')

    # Log scale
    plt.yscale('log') if log_scale else None

    # Add labels and title
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Histogram Example')

    # Add labels and title
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    file_path = '%s/%s.png' % (output_directory, file_name)
    plt.savefig(file_path)
    plt.close()


####################################################################################################
#
####################################################################################################
def plot_histogram(data, output_directory, file_name, xlabel, ylabel, title, nbins=10):

    # Plot histogram
    import matplotlib.pyplot as plt
    plt.hist(data, bins=nbins, log=True, color='skyblue', edgecolor='black')

    # Add labels and title
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    file_path = '%s/%s.png' % (output_directory, file_name)
    plt.savefig(file_path)
    plt.close()


####################################################################################################
#
####################################################################################################
def write_number_of_partitions(output_directory,
                               file_name,
                               partitions):

    file_path = '%s/%s' % (output_directory, file_name)
    with open(file_path, "w") as file:
        file.write(str(len(partitions)))

####################################################################################################
#
####################################################################################################
def write_number_of_vertices_per_partitions(output_directory,
                                            file_name,
                                            partitions):

    file_path = '%s/%s' % (output_directory, file_name)

    data = list()
    with open(file_path, "w") as file:
        for i, partition in enumerate(partitions):
            value = nmv.mesh.compute_number_of_vertices_of_mesh(partition)
            data.append(value)
            line = '%d %d\n' % (i, value)
            file.write(line)

    plot_histogram(data=data, output_directory=output_directory, file_name=file_name + "_hist",
                   xlabel='Number of Vertices', ylabel='Count', title='Partitions # Vertices',
                   nbins=50)

    # Plot the data
    plot_data_in_ascending_order(data=data, output_directory=output_directory, file_name=file_name,
                   xlabel='Partition', ylabel='# Vertices', title='Partitions # Vertices',)

####################################################################################################
#
####################################################################################################
def write_surface_area_per_partition(output_directory,
                                     file_name,
                                     partitions):

    # Write the result to a text file
    file_path = '%s/%s' % (output_directory, file_name)
    data = list()
    with open(file_path, "w") as file:
        for i, partition in enumerate(partitions):
            value = nmv.mesh.compute_surface_area_of_mesh(partition)
            data.append(value)
            line = '%d %f\n' % (i, value)
            file.write(line)

    # Plot the histogram
    plot_histogram(data=data, output_directory=output_directory, file_name=file_name + "_hist",
                   xlabel='Surface Area', ylabel='Count', title='Partitions Surface Area',
                   nbins=50)

    # Plot the data
    plot_data_in_ascending_order(data=data, output_directory=output_directory, file_name=file_name,
                   xlabel='Partition', ylabel='Surface Area', title='Partitions Surface Area')


####################################################################################################
#
####################################################################################################
def write_bounding_box_diagonal_per_partition(output_directory,
                                              file_name,
                                              partitions):
    # Write the result to a text file
    file_path = '%s/%s' % (output_directory, file_name)
    data = list()
    with open(file_path, "w") as file:
        for i, partition in enumerate(partitions):
            value = nmv.mesh.compute_bounding_box_diagonal_of_mesh(partition)
            data.append(value)
            line = '%d %f\n' % (i, value)
            file.write(line)

    # Plot the histogram
    plot_histogram(data=data, output_directory=output_directory, file_name=file_name + "_hist",
                   xlabel='Size (Bounds Diagonal)', ylabel='Count', title='Partitions Size',
                   nbins=50)

    # Plot the data
    plot_data_in_ascending_order(data=data, output_directory=output_directory, file_name=file_name,
                                 xlabel='Partition', ylabel='Size',
                                 title='Partitions Size')


####################################################################################################
#
####################################################################################################
def write_mesh_analysis_results(output_directory,
                                partitions):

    # Write the number of partitions
    write_number_of_partitions(output_directory=output_directory,
                               file_name='number_partitions',
                               partitions=partitions)

    # Write the number of vertices per partition
    write_number_of_vertices_per_partitions(output_directory=output_directory,
                                            file_name='number_vertices_per_partition',
                                            partitions=partitions)

    # Write the surface area per partition
    write_surface_area_per_partition(output_directory=output_directory,
                                     file_name='surface_area_per_partition',
                                     partitions=partitions)

    write_bounding_box_diagonal_per_partition(output_directory=output_directory,
                                              file_name='size_per_partition',
                                              partitions=partitions)

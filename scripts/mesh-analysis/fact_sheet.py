# -*- coding: utf-8 -*-

####################################################################################################
# Copyright (c) 2020 - 2024, EPFL / Blue Brain Project
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

from __future__ import unicode_literals

# Blender imports
import bpy
import nmv.scene

# System imports

import os
import matplotlib.font_manager as font_manager
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from textwrap import TextWrapper

# Internal
import data_utilities as dutils


####################################################################################################
# @create_input_vs_watertight_fact_sheet
####################################################################################################
def create_input_vs_watertight_fact_sheet(i_stats, i_aabb, i_wtc,
                                          wt_stats, wt_aabb, wt_wtc,
                                          output_image_path,
                                          fact_sheet_name,
                                          i_color=(0, 0, 0),
                                          wt_color=(0, 0, 0),
                                          resolution=1500):

    print('  * Computing Mesh Fact Sheet')

    # We have 12 entries in the image and 4 for adjusting size 
    number_entries = 16

    # Image dimensions
    image_width = int(resolution * 1.15)
    image_height = resolution

    # Calculate the spacing between items
    spacing = int(image_height / (number_entries * 1.2))

    # Create stats. image
    fact_sheet_image = Image.new("RGB", (image_width, image_height),
                                 (255, 255, 255))

    # Create a drawing area
    drawing_area = ImageDraw.Draw(fact_sheet_image)

    # Select a font
    font_path = os.path.dirname(os.path.realpath(__file__)) + '/fonts/NimbusSanL-Regu.otf'
    symbol_font_path = os.path.dirname(os.path.realpath(__file__)) + '/fonts/1H.otf'

    font = ImageFont.truetype(font_path, int(spacing * 0.8), encoding="utf-32")
    fact_sheet_font = ImageFont.truetype(font_path, int(spacing * 1.1), encoding="utf-32")

    # Compute the offsets
    starting_x = int(0.04 * image_width)
    delta_x = starting_x + int(image_width * 0.4)
    epsilon_x = starting_x + int(image_width * 0.7)
    bar_width = (epsilon_x - delta_x) * 0.75

    i = 0.4
    delta_y = i * spacing
    bar_y = delta_y + spacing
    drawing_area.text((starting_x, delta_y), 'Fact Sheet', font=fact_sheet_font, fill=(0, 0, 0))

    # Bars
    drawing_area.line([delta_x, bar_y, delta_x + bar_width, bar_y],
                      fill=i_color, width=int(0.01 * resolution))
    drawing_area.line([epsilon_x, bar_y, epsilon_x + bar_width, bar_y],
                      fill=wt_color, width=int(0.01 * resolution))

    i = 2.0
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Polygons', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), f'{i_stats.polygons:,d}', font=font, fill=(0, 0, 0))
    drawing_area.text((epsilon_x, delta_y), f'{wt_stats.polygons:,d}', font=font, fill=(0, 0, 0))

    i += 1
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Vertices', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), f'{i_stats.vertices:,d}', font=font, fill=(0, 0, 0))
    drawing_area.text((epsilon_x, delta_y), f'{wt_stats.vertices:,d}', font=font, fill=(0, 0, 0))

    i += 1.5
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'AABB Width', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), '%s µm' % dutils.format_number_to_power_string(
        i_aabb.x), font=font, fill=(0, 0, 0))
    drawing_area.text((epsilon_x, delta_y), '%s µm' % dutils.format_number_to_power_string(
        wt_aabb.x), font=font, fill=(0, 0, 0))

    i += 1
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'AABB Height', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), '%s µm' % dutils.format_number_to_power_string(
        i_aabb.y), font=font, fill=(0, 0, 0))
    drawing_area.text((epsilon_x, delta_y), '%s µm' % dutils.format_number_to_power_string(
        wt_aabb.y), font=font, fill=(0, 0, 0))

    i += 1
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'AABB Depth', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), '%s µm' % dutils.format_number_to_power_string(
        i_aabb.z), font=font, fill=(0, 0, 0))
    drawing_area.text((epsilon_x, delta_y), '%s µm' % dutils.format_number_to_power_string(
        wt_aabb.z), font=font, fill=(0, 0, 0))

    i += 1.0
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'AABB Diagonal', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), '%s µm' % dutils.format_number_to_power_string(
        i_aabb.diagonal), font=font, fill=(0, 0, 0))
    drawing_area.text((epsilon_x, delta_y), '%s µm' % dutils.format_number_to_power_string(
        wt_aabb.diagonal), font=font, fill=(0, 0, 0))

    i += 1.5
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Surface Area', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), '%s µm²' % dutils.format_number_to_power_string(
        i_stats.surface_area), font=font, fill=(0, 0, 0))
    drawing_area.text((epsilon_x, delta_y), '%s μm²' % dutils.format_number_to_power_string(
        wt_stats.surface_area), font=font, fill=(0, 0, 0))

    i += 1
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Volume*', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), '%s µm³' % dutils.format_number_to_power_string(
        i_stats.volume), font=font, fill=(0, 0, 0))
    drawing_area.text((epsilon_x, delta_y), '%s µm³' % dutils.format_number_to_power_string(
        wt_stats.volume), font=font, fill=(0, 0, 0))

    i += 1.5
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Mesh Partitions',
                      font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), f'{i_stats.partitions:,d}',
                      font=font, fill=(0, 0, 0))
    drawing_area.text((epsilon_x, delta_y), f'{wt_stats.partitions:,d}',
                      font=font, fill=(0, 0, 0))

    i += 1.5
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Non Manifold Edges',
                      font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), f'{i_wtc.non_manifold_edges:,d}',
                      font=font, fill=(0, 0, 0))
    drawing_area.text((epsilon_x, delta_y), f'{wt_wtc.non_manifold_edges:,d}',
                      font=font, fill=(0, 0, 0))

    i += 1
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Non Manifold Vertices',
                      font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), f'{i_wtc.non_manifold_vertices:,d}',
                      font=font, fill=(0, 0, 0))
    drawing_area.text((epsilon_x, delta_y), f'{wt_wtc.non_manifold_vertices:,d}',
                      font=font, fill=(0, 0, 0))

    i += 1
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Non Continuous Edges',
                      font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), f'{i_wtc.non_contiguous_edge:,d}',
                      font=font, fill=(0, 0, 0))
    drawing_area.text((epsilon_x, delta_y), f'{wt_wtc.non_contiguous_edge:,d}',
                      font=font, fill=(0, 0, 0))

    i += 1
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Self Intersections',
                      font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), f'{i_wtc.self_intersections:,d}',
                      font=font, fill=(0, 0, 0))
    drawing_area.text((epsilon_x, delta_y), f'{wt_wtc.self_intersections:,d}',
                      font=font, fill=(0, 0, 0))

    i += 1.5
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Watertight', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), 'Yes' if i_wtc.watertight else 'No',
                      font=font, fill=(0, 0, 0))
    drawing_area.text((epsilon_x, delta_y), 'Yes' if wt_wtc.watertight else 'No',
                      font=font, fill=(0, 0, 0))

    # Save the image and return a reference to its path
    fact_sheet_image_path = '%s/%s-fact-sheet.png' % (output_image_path, fact_sheet_name)
    fact_sheet_image.save(fact_sheet_image_path)
    fact_sheet_image.close()
    return fact_sheet_image_path


####################################################################################################
# @create_mesh_fact_sheet
####################################################################################################
def create_step_by_step_fact_sheet(stats, aabb, wtc,
                                   fact_sheet_name,
                                   output_image_path,
                                   color=(0, 0, 0),
                                   resolution=1500,
                                   mesh_scale=1):

    print('  * Computing Mesh Fact Sheet')

    # We have 12 entries in the image
    number_entries = 16

    # Image dimensions
    image_width = int(resolution * 0.8)
    image_height = resolution

    # Calculate the spacing between items
    spacing = int(image_height / (number_entries * 1.2))

    # Create stats. image
    fact_sheet_image = Image.new("RGB", (image_width, image_height),
                                 (255, 255, 255))

    # Create a drawing area
    drawing_area = ImageDraw.Draw(fact_sheet_image)

    # Select a font
    font_path = os.path.dirname(os.path.realpath(__file__)) + '/fonts/1H.otf'
    font = ImageFont.truetype(font_path, int(spacing * 0.8))
    fact_sheet_font = ImageFont.truetype(font_path, int(spacing * 1.1))

    # Compute the offsets
    starting_x = int(0.04 * image_width)
    delta_x = starting_x + int(image_width * 0.575)

    i = 0.4
    delta_y = i * spacing
    bar_y = int(delta_y + spacing)
    drawing_area.text((starting_x, delta_y), 'Fact Sheet', font=fact_sheet_font, fill=(0, 0, 0))

    bar_width = int(resolution * 0.25)

    # Bars
    drawing_area.line([delta_x, bar_y, delta_x + bar_width, bar_y],
                      fill=color, width=int(0.01 * resolution))

    i = 2.0
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Polygons', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), f'{stats.polygons:,d}', font=font, fill=(0, 0, 0))

    i += 1
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Vertices', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), f'{stats.vertices:,d}', font=font, fill=(0, 0, 0))

    i += 1.5
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'AABB Width', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), '%s μm' % dutils.format_number_to_power_string(
        aabb.x * mesh_scale), font=font, fill=(0, 0, 0))

    i += 1
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'AABB Height', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), '%s μm' % dutils.format_number_to_power_string(
        aabb.y * mesh_scale), font=font, fill=(0, 0, 0))
    i += 1
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'AABB Depth', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), '%s μm' % dutils.format_number_to_power_string(
        aabb.z * mesh_scale), font=font, fill=(0, 0, 0))

    i += 1.0
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'AABB Diagonal', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), '%s μm' % dutils.format_number_to_power_string(
        aabb.diagonal * mesh_scale), font=font, fill=(0, 0, 0))

    i += 1.5
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Surface Area', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), '%s μm²' % dutils.format_number_to_power_string(
        stats.surface_area * mesh_scale * mesh_scale), font=font, fill=(0, 0, 0))

    i += 1
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Volume*', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), '%s μm³' % dutils.format_number_to_power_string(
        stats.volume * mesh_scale * mesh_scale * mesh_scale), font=font, fill=(0, 0, 0))

    i += 1.5
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Mesh Partitions',
                      font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), f'{stats.partitions:,d}',
                      font=font, fill=(0, 0, 0))

    i += 1.5
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Non Manifold Edges',
                      font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), f'{wtc.non_manifold_edges:,d}',
                      font=font, fill=(0, 0, 0))

    i += 1
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Non Manifold Vertices',
                      font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), f'{wtc.non_manifold_vertices:,d}',
                      font=font, fill=(0, 0, 0))

    i += 1
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Non Continuous Edges',
                      font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), f'{wtc.non_contiguous_edge:,d}',
                      font=font, fill=(0, 0, 0))

    i += 1
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Self Intersections',
                      font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), f'{wtc.self_intersections:,d}',
                      font=font, fill=(0, 0, 0))

    i += 1.5
    delta_y = i * spacing
    drawing_area.text((starting_x, delta_y), 'Watertight', font=font, fill=(0, 0, 0))
    drawing_area.text((delta_x, delta_y), 'Yes' if wtc.watertight else 'No',
                      font=font, fill=(0, 0, 0))

    fact_sheet_image_path = '%s/%s-fact-sheet.png' % (output_image_path, fact_sheet_name)
    fact_sheet_image.save(fact_sheet_image_path)
    fact_sheet_image.close()
    return fact_sheet_image_path

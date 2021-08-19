
# import stand alone modules
import blf
import bpy

# Internal imports
import nmv.bbox
from .line_ops import *
from mathutils import Vector

import nmv.skeleton
import nmv.consts
import os
import nmv.shading
import nmv.scene
import nmv.enums
import nmv.utilities


def add_text(text_string):

    # Create the font curve
    font_curve = bpy.data.curves.new(type="FONT", name="Font Curve")

    # Set the body of the font curve to the scale bar value
    font_curve.body = text_string

    # Update the font
    font_curve.font = bpy.data.fonts['ArialMT']

    # Align the font below the scale bar
    font_curve.align_x = 'CENTER'
    font_curve.align_y = 'CENTER'

    # Create the font object and link it to the scene at the origin
    font_object = bpy.data.objects.new(name="Font Object", object_data=font_curve)
    bpy.context.scene.collection.objects.link(font_object)

    # Return a reference to the font object
    return font_object


def draw_colormap(position,
                  length,
                  radius,
                  material,
                  color_list,
                  resolution,
                  options):

    # Add the maximum value string
    maximum_value_string = add_text(text_string=bpy.context.scene.NMV_MaximumValue)

    # Scale it
    nmv.scene.scale_object_uniformly(
        scene_object=maximum_value_string,
        scale_factor=3 * radius / maximum_value_string.dimensions.x)

    # Adjust its location
    nmv.scene.set_object_location(
        scene_object=maximum_value_string, location=position + Vector((0, 2 * radius, 0)))

    # Add the maximum value string
    minimum_value_string = add_text(text_string=bpy.context.scene.NMV_MinimumValue)

    # Scale it
    nmv.scene.scale_object_uniformly(
        scene_object=minimum_value_string,
        scale_factor=3 * radius / maximum_value_string.dimensions.x)

    # Adjust its location
    nmv.scene.set_object_location(
        scene_object=minimum_value_string,
        location=position - Vector((0, length + (2 * radius), 0)))

    text_objects = [nmv.scene.convert_object_to_mesh(maximum_value_string),
                    nmv.scene.convert_object_to_mesh(minimum_value_string)]
    text_objects = nmv.mesh.join_mesh_objects(mesh_list=text_objects, name='colormap_range')

    text_material = nmv.skeleton.create_single_material(
        name='values_material', material_type=options.shading.morphology_material,
        color=nmv.consts.Color.BLACK)

    nmv.shading.set_material_to_object(mesh_object=text_objects, material_reference=text_material)

    # Step
    delta = 1.0 * length / resolution

    # Create a final list from the given color list
    if resolution == len(color_list):
        interpolated_color_list = color_list
    else:
        interpolated_color_list = nmv.utilities.create_colormap_from_color_list(
            color_list, resolution)

    # A list of all the materials
    materials = nmv.skeleton.create_multiple_materials(
        name='colormap',
        material_type=material,
        color_list=interpolated_color_list)

    # Draw the segments of the colormap
    segments = list()
    bevel_object = nmv.mesh.create_bezier_circle(radius=1.0, vertices=16, name='color_bevel')
    for i in range(resolution):

        # Construct the segment
        segment = draw_cone_line(
            point1=Vector((0, -i * delta, 0)), point2=Vector((0, -1 * (i + 1) * delta, 0)),
            point1_radius=radius, point2_radius=radius, bevel_object=bevel_object)

        # Add shading to the segment
        nmv.shading.set_material_to_object(mesh_object=segment, material_reference=materials[i])

        # Convert the segment to a mesh and append it to a list
        segments.append(nmv.scene.convert_object_to_mesh(scene_object=segment))

    # Delete the bevel
    nmv.scene.delete_object_in_scene(bevel_object)

    # Join all the segments into a single object
    colormap_bar = nmv.mesh.join_mesh_objects(segments, name='Color Map Legend')

    # Adjust the location of the colormap legend
    nmv.scene.set_object_location(scene_object=colormap_bar, location=position)

    # Join everything into the colormap legend
    colormap_legend = nmv.mesh.join_mesh_objects(mesh_list=[text_objects, colormap_bar],
                                                 name='Color Map Legend')

    # Return a reference in case the colormap needs to be changed
    return colormap_legend


####################################################################################################
# @get_scale_bar_length
####################################################################################################
def get_scale_bar_length(view_length):

    if view_length < 100:
        return 10
    elif view_length < 200:
        return 20
    elif view_length < 500:
        return 25
    elif view_length < 1000:
        return 50
    elif view_length < 1500:
        return 100
    else:
        return 150


def draw_scale_bar_text(scale_bar_length,
                        location):

    # Load the Arial font
    bpy.data.fonts.load(nmv.consts.Paths.ARIAL_FONT)

    # Create the font curve
    font_curve = bpy.data.curves.new(type="FONT", name="Font Curve")

    # Set the body of the font curve to the scale bar value
    font_curve.body = "%d \u03BCm" % int(scale_bar_length)

    # Update the font
    font_curve.font = bpy.data.fonts['ArialMT']

    # Align the font below the scale bar
    font_curve.align_x = 'CENTER'
    font_curve.align_y = 'TOP'

    # Create the font object and link it to the scene
    font_object = bpy.data.objects.new(name="Font Object", object_data=font_curve)
    bpy.context.scene.collection.objects.link(font_object)

    # Get the dimensions of the font object to scale the it according to the size of the scale bar
    font_object_width = font_object.dimensions.x

    scale_factor = 0.85 * scale_bar_length / font_object_width
    nmv.scene.scale_object_uniformly(scene_object=font_object, scale_factor=scale_factor)

    font_object_location = location
    nmv.scene.set_object_location(scene_object=font_object, location=font_object_location)

    return font_object



def draw_morphology_scale_bar(morphology,
                              options,
                              view=nmv.enums.Camera.View.FRONT):
    # Get the bounding box of the morphology, and the meshes to account for the soma
    scene_bounding_box = nmv.bbox.compute_scene_bounding_box_for_curves_and_meshes()

    # The scale bar height will be around 10% of the image height
    scale_bar_height = get_scale_bar_length(view_length=scene_bounding_box.bounds[1])

    # The vertical scale bar will be drawn on the left side of the image 5% of its width
    x1 = scene_bounding_box.p_min[0] + 0.05 * scene_bounding_box.bounds[0]
    y1 = scene_bounding_box.p_min[1] + 0.20 * scene_bounding_box.bounds[0]
    z1 = scene_bounding_box.center[2]
    p1 = Vector((x1, y1, z1))
    p2 = p1 + Vector((0, scale_bar_height, 0))
    center = 0.5 * (p1 + p2)

    # The radius of the line depends on the width of the morphology
    line_radius = 0.0015 * scene_bounding_box.bounds[0]

    bevel_object = nmv.mesh.create_bezier_circle(radius=1.0, vertices=16, name='color_bevel')

    # Draw the scale bar as a line
    scale_bar_object = list()
    scale_bar_object.append(nmv.scene.convert_object_to_mesh(
        scene_object=draw_cone_line(
            point1=p1, point2=p2, point1_radius=line_radius, point2_radius=line_radius,
            bevel_object=bevel_object)))
    scale_bar_object.append(nmv.scene.convert_object_to_mesh(
        scene_object=draw_cone_line(
            point1=p1 - Vector((0.2, 0, 0)), point2=p1 + Vector((2, 0, 0)),
            point1_radius=line_radius, point2_radius=line_radius, bevel_object=bevel_object)))
    scale_bar_object.append(nmv.scene.convert_object_to_mesh(
        scene_object=draw_cone_line(
            point1=p2 - Vector((0.2, 0, 0)), point2=p2 + Vector((2, 0, 0)),
            point1_radius=line_radius, point2_radius=line_radius, bevel_object=bevel_object)))
    scale_bar_object.append(nmv.scene.convert_object_to_mesh(
        scene_object=draw_cone_line(
            point1=center - Vector((0.2, 0, 0)), point2=center + Vector((1, 0, 0)),
            point1_radius=line_radius, point2_radius=line_radius, bevel_object=bevel_object)))

    # Delete the bevel
    nmv.scene.delete_object_in_scene(bevel_object)

    # Convert into a mesh
    scale_bar_object = nmv.mesh.join_mesh_objects(mesh_list=scale_bar_object, name='Scale Bar')

    # Assign the materials to the scale bar and the font object
    material = nmv.skeleton.create_single_material(
        name='scale_bar', material_type=options.shading.morphology_material,
        color=nmv.consts.Color.BLACK)
    nmv.shading.set_material_to_object(mesh_object=scale_bar_object, material_reference=material)

    scale_bar_text = draw_scale_bar_text(scale_bar_height, center)

    scale_bar_text.rotation_euler[2] = 1.56381
    scale_bar_text.location[0] += 1
    nmv.shading.set_material_to_object(mesh_object=scale_bar_text, material_reference=material)

    x1 = scene_bounding_box.p_max[0] - 0.1 * scene_bounding_box.bounds[0]
    y1 = scene_bounding_box.p_max[1] - 0.05 * scene_bounding_box.bounds[0]
    z1 = scene_bounding_box.p_max[2]
    p1 = Vector((x1, y1, z1))
    p2 = p1 - Vector((0, scale_bar_height, 0))
    center = 0.5 * (p1 + p2)

    colormap_width = scene_bounding_box.bounds[0] * 0.01
    colormap_height = scene_bounding_box.bounds[1] * 0.2

    # TODO: Draw the colormap
    # draw_colormap(position=p1, color_list=options.shading.morphology_colormap_list,
    #               material=options.shading.morphology_material, length=colormap_height,
    #               radius=colormap_width, resolution=32, options=options)


def draw_morphology_scale_bar2(morphology,
                              options,
                              view=nmv.enums.Camera.View.FRONT):

    # Get the bounding box of the morphology, and the meshes to account for the soma
    scene_bounding_box = nmv.bbox.compute_scene_bounding_box_for_curves_and_meshes()

    # Top view
    if view == nmv.enums.Camera.View.TOP:
        bbox_width = scene_bounding_box.bounds[1]
        scale_bar_area_width = 0.08 * bbox_width

        p1 = Vector((scene_bounding_box.p_min[0] + (bbox_width * 0.08),
                     scene_bounding_box.p_min[1],
                     scene_bounding_box.p_min[2] + (bbox_width * 0.08)))
        p2 = Vector((p1[0] - scale_bar_area_width, p1[1], p1[2]))

    # Side view
    elif view == nmv.enums.Camera.View.SIDE:
        bbox_width = scene_bounding_box.bounds[2]
        scale_bar_area_width = 0.08 * bbox_width

        p1 = Vector((scene_bounding_box.p_min[0],
                     scene_bounding_box.p_min[1] + (bbox_width * 0.08),
                     scene_bounding_box.p_max[2] - (bbox_width * 0.08)))
        p2 = Vector((p1[0], p1[1], p1[2] - scale_bar_area_width))

    # Front view
    else:
        bbox_width = scene_bounding_box.bounds[0]
        scale_bar_area_width = 0.08 * bbox_width

        p1 = Vector((scene_bounding_box.p_min[0] + (bbox_width * 0.08),
                     scene_bounding_box.p_min[1] + (bbox_width * 0.08),
                     scene_bounding_box.p_min[2]))
        p2 = Vector((p1[0] + scale_bar_area_width, p1[1], p1[2]))

    # Adjust the height of the scale bar line based on the height of the image
    line_height = 0.015 * scale_bar_area_width

    # Draw the scale bar as a line
    scale_bar_object = draw_cone_line(
        point1=p1, point2=p2, point1_radius=line_height, point2_radius=line_height)

    # Load the Arial font
    bpy.data.fonts.load(nmv.consts.Paths.ARIAL_FONT)

    # Create the font curve
    font_curve = bpy.data.curves.new(type="FONT", name="Font Curve")

    # Set the body of the font curve to the scale bar value
    font_curve.body = "%d \u03BCm" % scale_bar_area_width

    # Update the font
    font_curve.font = bpy.data.fonts['ArialMT']

    # Align the font below the scale bar
    font_curve.align_y = 'TOP'

    # Create the font object and link it to the scene
    font_object = bpy.data.objects.new(name="Font Object", object_data=font_curve)
    bpy.context.scene.collection.objects.link(font_object)

    if view == nmv.enums.Camera.View.TOP:
        # Get the dimensions of the font object to scale the it according to the size of the scale bar
        font_object_width = font_object.dimensions.x
    elif view == nmv.enums.Camera.View.SIDE:

        # Get the dimensions of the font object to scale the it according to the size of the scale bar
        font_object_width = font_object.dimensions.x
    else:
        # Get the dimensions of the font object to scale the it according to the size of the scale bar
        font_object_width = font_object.dimensions.x

    scale_factor = scale_bar_area_width / font_object_width
    nmv.scene.scale_object_uniformly(scene_object=font_object, scale_factor=scale_factor)

    # Set the location of the font object to the left side of the scale bar
    if view == nmv.enums.Camera.View.TOP:
        font_object_location = Vector((p1[0], p1[1], p1[2] - 5))
        font_object.rotation_euler[0] = 1.56381
        font_object.rotation_euler[2] = 3.14159
    elif view == nmv.enums.Camera.View.SIDE:
        font_object_location = Vector((p1[0], p1[1] - 5, p1[2]))
        font_object.rotation_euler[1] = 1.56381
    else:
        font_object_location = Vector((p1[0], p1[1] - 5, p1[2]))
    nmv.scene.set_object_location(scene_object=font_object, location=font_object_location)

    # Assign the materials to the scale bar and the font object
    material = nmv.skeleton.create_single_material(
        name='scale_bar', material_type=options.shading.morphology_material,
        color=nmv.consts.Color.BLACK)
    nmv.shading.set_material_to_object(mesh_object=scale_bar_object, material_reference=material)
    nmv.shading.set_material_to_object(mesh_object=font_object, material_reference=material)




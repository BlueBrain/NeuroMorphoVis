






def draw_colormap(position,
                  length,
                  radius,
                  material,
                  color_list,
                  resolution,
                  options):

    # Add the maximum value string
    maximum_value_string = create_text_object(text_string=bpy.context.scene.NMV_MaximumValue)

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
        segment = nmv.geometry.draw_cone_line(
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

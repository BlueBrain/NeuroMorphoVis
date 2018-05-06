"""sphere_ops.py: A set of geometric operations required for sphere handling"""

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2017, Blue Brain Project / EPFL"
__version__     = "0.1.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"

# System imports
import math, random

# Blender imports
import bpy
from mathutils import Vector, Matrix

import scene_ops
import materials


####################################################################################################
# @create_uv_sphere
####################################################################################################
def create_uv_sphere(radius=1, 
                     location=(0, 0, 0), 
                     subdivisions=32, 
                     name='uv_sphere',
                     color=None):
    """
    Creates a UV sphere and returns a reference to it.

    :param radius: Sphere radius.
    :param location: Sphere location.
    :param subdivisions: Number of sphere subdivisions, 32 by default.
    :param name: Sphere name.
    :param color: Sphere color.
    :return: A reference to the created uv-sphere object.
    """

    # Deselect all objects
    nmv.scene.ops.deselect_all()
    
    # Add the sphere
    bpy.ops.mesh.primitive_uv_sphere_add(segments=subdivisions, size=radius, location=location)
    
    # Select the sphere to set its name and returns a reference to it
    sphere = bpy.context.scene.objects.active
    sphere.name = name

    # Smoothing the soma via shade smoothing
    nmv.scene.ops.deselect_all()
    nmv.scene.ops.select_object_by_name(sphere)
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.faces_shade_smooth()
    bpy.ops.object.editmode_toggle()

    # Create a material and assign it to the sphere
    if color is not None:
        sphere_material = materials.create_default_material(name='sphere_color', color=color)
        materials.set_material_to_object(sphere, sphere_material)

    # Return a reference to the created sphere object
    return sphere


####################################################################################################
# @create_ico_sphere
####################################################################################################
def create_ico_sphere(radius=1, 
                      location=(0, 0, 0), 
                      subdivisions=3, 
                      name='ico_sphere'):
    """
    Creates a default ico-sphere and returns a reference to it.

    :param radius: Sphere radius.
    :param location: Sphere location.
    :param subdivisions: Number of sphere subdivisions, 3 by default.
    :param name: Sphere name.
    :return: A reference to the created ico-sphere object.
    """

    # Deselect all objects
    nmv.scene.ops.deselect_all()
    
    # Add the sphere
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=subdivisions, size=radius, location=location)
    
    # Select the sphere to set its name and returns a reference to it
    sphere = bpy.context.scene.objects.active
    sphere.name = name

    # Smoothing the soma via shade smoothing
    nmv.scene.ops.deselect_all()
    nmv.scene.ops.select_object_by_name(sphere)
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.faces_shade_smooth()
    bpy.ops.object.editmode_toggle()

    # Return a reference to the sphere
    return sphere


####################################################################################################
# @get_random_point_on_a_sphere
####################################################################################################
def get_random_point_on_a_sphere(radius,
                                 location):
    """
    Returns a random point on a sphere defined by a location and radius.

    :param radius: Sphere radius.
    :param location: Sphere center.
    :return: A random point on the surface of the sphere.
    """

    # Get a random point on the surface of the sphere using the polar coordinates.
    theta = 2 * math.pi * random.uniform(0, 1)
    phi = math.pi * random.uniform(0, 1)
    x = radius * math.cos(theta) * math.sin(phi)
    y = radius * math.sin(theta) * math.sin(phi)
    z = radius * math.cos(phi)
    point = Vector((x, y, z)) + location
    return point 


####################################################################################################
# @get_random_points_on_sphere
####################################################################################################
def get_random_points_on_sphere(radius,
                                location,
                                number_points):
    """
    Returns a list of random points on a sphere defined by a location and radius.

    :param radius: Sphere radius.
    :param location: Sphere center.
    :param number_points: Number of requested points on the surface of the sphere.
    :return:
    """

    # Create a list to encapsulate the obtained points.
    points_list = []

    # Get the points
    for i_point in range(number_points):
        points_list.append(get_random_point_on_a_sphere(radius=radius, location=location))

    # Return a reference to the list
    return points_list


####################################################################################################
# @get_random_point_on_sphere
####################################################################################################
def get_random_point_on_sphere(sphere_object):
    """
    Returns a random point on a given sphere object.

    :param sphere_object: A given sphere object that already exists in the scene.
    :return: A random point on the surface of this sphere object.
    """

    # Get all the vertices on the sphere
    vertices = sphere_object.data.vertices

    # Fill those vertices in a vertices list where you use to sample a point randomly
    vertices_list = []
    for vertex in vertices:
        vertices_list.append(vertex.co)

    # Return a random point from this list
    return random.choice(vertices_list)


####################################################################################################
# @get_random_points_on_sphere
####################################################################################################
def get_random_points_on_sphere(sphere_object,
                                number_points):
    """
    Returns a random set of points on a given sphere object.

    :param sphere_object: A given sphere object that already exists in the scene.
    :param number_points: Requested number of points.
    :return: A list of random points on the surface of the given sphere object.
    """

    # Get all the vertices on the sphere
    vertices = sphere_object.data.vertices

    # Fill those vertices in a vertices list where you use to sample some points randomly
    vertices_list = [] 
    for vertex in vertices:
        vertices_list.append(vertex.co)

    # Return a set of random points from this list
    return random.sample(vertices_list, number_points)


####################################################################################################
# @get_index_of_random_point_on_sphere
####################################################################################################
def get_index_of_random_point_on_sphere(sphere_object):
    """
    Returns an index of a random point on a sphere.

    :param sphere_object: A given sphere object that already exists in the scene.
    :return: The index of a randomly selected point on the given sphere object.
    """

    # Get all the vertices on the sphere
    vertices = sphere_object.data.vertices

    # Fill those vertices in a vertices list where you use to sample some points randomly
    vertices_list = [] 
    for vertex in vertices:
        vertices_list.append([vertex.co, vertex.index])

    # Returns the index of a randomly selected point on the surface of the given sphere object
    return random.choice(vertices_list)[1]


####################################################################################################
# @get_indices_of_random_points_on_sphere
####################################################################################################
def get_indices_of_random_points_on_sphere(sphere_object,
                                           number_points):
    """

    :param sphere_object: A given sphere object that already exists in the scene.
    :param number_points: Requested number of points.
    :return: Returns a list of the indices of a random points on a sphere.
    """

    # Get all the vertices on the sphere
    vertices = sphere_object.data.vertices

    # Fill those vertices in a vertices list where you use to sample some points randomly
    vertices_list = [] 
    for vertex in vertices:
        vertices_list.append([vertex.co, vertex.index])

    # Sample the list
    sampled_list = random.sample(vertices_list, number_points)

    # Return a list of indices
    indices_list = []
    for i in sampled_list:
        indices_list.append(i[1])
    return indices_list


####################################################################################################
# @get_indices_of_points_inside_volume
####################################################################################################
def get_indices_of_points_inside_volume(sphere_object, 
                                        selection_location, 
                                        selection_radius):
    """
    Returns a list of the indices of the selected points within another sphere.

    :param sphere_object:
    :param selection_location:
    :param selection_radius:
    :return:
    """

    vertices = sphere_object.data.vertices
    vertices_list = []
    for vertex in vertices:
        distance = geometry.compute_distance_between_points(
            selection_location, vertex.co)
        if distance < selection_radius:
            vertices_list.append([vertex.co, vertex.index])
    indices_list = []
    for i in vertices_list:
        indices_list.append(i[1])
    return indices_list

####################################################################################################
# @get_index_of_nearest_point_on_sphere
####################################################################################################
def get_index_of_nearest_point_on_sphere(sphere_object, point):
    """
    Returns the index of the nearest point on the sphere.
    """
    vertices = sphere_object.data.vertices
    nearest_vertex_index = -1
    nearest_point_distance = 100000000
    for vertex in vertices:
        distance = geometry.compute_distance_between_points(
            point, vertex.co)
        if distance < nearest_point_distance:
            nearest_point_distance = distance
            nearest_vertex_index = vertex.index
    return [nearest_vertex_index]

####################################################################################################
# @get_indices_of_faces_intersecting_volume
####################################################################################################
def get_indices_of_faces_intersecting_volume(sphere_object, 
                                             selection_location, 
                                             selection_radius):
    """
    Returns a list of all the faces that intersetcs the volume.
    """
    polygons = sphere_object.data.polygons
    vertices = sphere_object.data.vertices
    faces_list = []
    for polygon in polygons:
        distance = geometry.compute_distance_between_points(
                selection_location, polygon.center)
        if distance < selection_radius: 
            faces_list.append(polygon.index)
            
        for vertex in polygon.vertices[:]:
            distance = geometry.compute_distance_between_points(
                selection_location, vertices[vertex].co)
            if distance < selection_radius:
                faces_list.append(polygon.index)
                break
    
    # remove the duplicate faces
    faces_list = list(set(faces_list))
    return faces_list


####################################################################################################
# @get_indices_of_points_of_faces_intersecting_volume
####################################################################################################
def get_indices_of_points_of_faces_intersecting_volume(sphere_object, 
                                                       selection_location, 
                                                       selection_radius):
    """
    Returns a list of points of the faces that are either inside or 
    intersect another sphere specified by its location and radius.
    """
    vertices = sphere_object.data.vertices
    polygons = sphere_object.data.polygons
    faces_list = []
    for polygon in polygons:
        for vertex in polygon.vertices[:]:
            distance = geometry.compute_distance_between_points(
                selection_location, vertices[vertex].co)
            if distance < selection_radius:
                faces_list.append(polygon)
                break

    # add all the vertices of selected faces
    indices_list = []
    for face in faces_list:
        for vertex in face.vertices[:]:
            indices_list.append(vertex)

    # remove duplicated vertices
    indices_list = list(set(indices_list))
    return indices_list 


####################################################################################################
# @get_indices_of_points_of_faces_inside_volume
####################################################################################################
def get_indices_of_points_of_faces_inside_volume(sphere_object,
                                                 selection_location,
                                                 selection_radius):
    """
    Returns a list of points of the faces that are either inside or intersect another sphere
    specified by its location and radius.

    :param sphere_object: A given sphere object that exists in the scene.
    :param selection_location:
    :param selection_radius:
    :return:
    """

    vertices = sphere_object.data.vertices
    polygons = sphere_object.data.polygons
    faces_list = []
    for polygon in polygons:
        distance = geometry.compute_distance_between_points(
                selection_location, polygon.center)
        if distance < selection_radius: 
            faces_list.append(polygon)
            
    # add all the vertices of selected faces
    indices_list = []
    for face in faces_list:
        for vertex in face.vertices[:]:
            indices_list.append(vertex)

    # remove duplicated vertices
    indices_list = list(set(indices_list))
    return indices_list


####################################################################################################
# @add_random_spheres_to_scene
####################################################################################################
def add_random_spheres_to_scene(number_spheres=1):
    """
    Add a set of random spheres to the scene.

    :param number_spheres: Number of spheres to be created in the scene.
    :return A list of all the created spheres in the scene.
    """

    # A list of all the created spheres.
    spheres_list = []

    # Create the spheres and append their reference to the list
    for i in range(number_spheres):
        x = random.uniform(-10, 10)
        y = random.uniform(-10, 10)
        z = random.uniform(-10, 10)

        # Sphere location
        location = Vector((x, y, z))
        sphere = create_uv_sphere(location=location)
        spheres_list.append(sphere)

    # Return the list of all the created spheres.
    return spheres_list


####################################################################################################
# @is_point_inside_sphere
####################################################################################################
def is_point_inside_sphere(sphere_center, 
                           sphere_radius, 
                           point):
    """
    Checks if a given point is located inside a given sphere or not.

    :param sphere_center: Sphere center or location.
    :param sphere_radius: Sphere radius.
    :param point: A given point in the three-dimensional space.
    :return: True or False.
    """

    # Compute the distance between the point and center of the sphere and compare it with the radius
    distance = (sphere_center - point).length
    return True if distance < sphere_radius else False

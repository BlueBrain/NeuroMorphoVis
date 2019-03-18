####################################################################################################
#  Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of NeuroMorphoVis <https://github.com/BlueBrain/NeuroMorphoVis>
#
# This library is free software; you can redistribute it and/or modify it under the terms of the
# GNU Lesser General Public License version 3.0 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with this library;
# if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA.
####################################################################################################

# System imports
import math, random

# Blender imports
from mathutils import Vector, Matrix

import nmv
import nmv.geometry
import nmv.mesh


####################################################################################################
# @get_random_point_on_a_sphere
####################################################################################################
def get_random_point_on_a_sphere(radius,
                                 location):
    """Return a random point on a sphere defined by a location and radius.

    :param radius:
        Sphere radius.
    :param location:
        Sphere center.
    :return:
        A random point on the surface of the sphere.
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
    """Return a list of random points on a sphere defined by a location and radius.

    :param radius:
        Sphere radius.
    :param location:
        Sphere center.
    :param number_points:
        Number of requested points on the surface of the sphere.
    :return:
        A list of random points on the sphere.
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
    """Return a random point on a given sphere object.

    :param sphere_object:
        A given sphere object that already exists in the scene.
    :return:
        A random point on the surface of this sphere object.
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
# @get_random_points_on_sphere_object
####################################################################################################
def get_random_points_on_sphere_object(sphere_object,
                                       number_points):
    """Return a random set of points on a given sphere object.

    :param sphere_object:
        A given sphere object that already exists in the scene.
    :param number_points:
        Requested number of points.
    :return:
        A list of random points on the surface of the given sphere object.
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
    """Return an index of a random point on a sphere.

    :param sphere_object:
        A given sphere object that already exists in the scene.
    :return:
        The index of a randomly selected point on the given sphere object.
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
    """Return a list of indices of random vertices on a given sphere
    :param sphere_object:
        A given sphere object that already exists in the scene.
    :param number_points:
        Requested number of points.
    :return:
        Returns a list of the indices of a random points on a sphere.
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
    """Return a list of the indices of the selected points within another sphere.

    :param sphere_object:
        A given sphere object that already exists in the scene.
    :param selection_location:
        The center of the volume sphere.
    :param selection_radius:
        The radius of the volume sphere.
    :return:
        A list of the indices of the selected points within another sphere.
    """

    vertices = sphere_object.data.vertices
    vertices_list = []
    for vertex in vertices:
        distance = (selection_location - vertex.co).length
        if distance < selection_radius:
            vertices_list.append([vertex.co, vertex.index])
    indices_list = []
    for i in vertices_list:
        indices_list.append(i[1])
    return indices_list


####################################################################################################
# @get_index_of_nearest_point_on_sphere
####################################################################################################
def get_index_of_nearest_point_on_sphere(sphere_object,
                                         point):
    """Return the index of the nearest point on the sphere.

    :param sphere_object:
        A given sphere object.
    :param point:
        A given point in the space.
    :return:
        Index of the nearest vertex on the sphere to the given point.
    """

    vertices = sphere_object.data.vertices
    nearest_vertex_index = -1
    nearest_point_distance = 100000000
    for vertex in vertices:
        distance = (point - vertex.co).length
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

    :param sphere_object:
    :param selection_location:
    :param selection_radius:
    :return:
    """
    """
    Returns a list of all the faces that intersetcs the volume.
    """
    polygons = sphere_object.data.polygons
    vertices = sphere_object.data.vertices
    faces_list = []
    for polygon in polygons:
        distance = (selection_location, polygon.center).lengths
        if distance < selection_radius: 
            faces_list.append(polygon.index)
            
        for vertex in polygon.vertices[:]:
            distance = (selection_location, vertices[vertex].co).length
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
    """Return a list of points of the faces that are either inside or intersect another sphere
    specified by its location and radius.

    :param sphere_object:
        A given sphere object.
    :param selection_location:
        Volume location or center.
    :param selection_radius:
        Volume radius.
    :return:
        A list of indices of the points that correspond to the intersecting faces.
    """

    # Get a list of vertices of the sphere object
    vertices = sphere_object.data.vertices

    # Get a list of polygons of the sphere object
    polygons = sphere_object.data.polygons

    # A list that will keep the intersecting faces
    faces_list = list()

    # Iterate over all the polygons of the sphere objects
    for polygon in polygons:
        for vertex in polygon.vertices[:]:
            distance = (selection_location, vertices[vertex].co).length
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
    """Return a list of points of the faces that are either inside or intersect another sphere
    specified by its location and radius.

    :param sphere_object:
        A given sphere object that exists in the scene.
    :param selection_location:
        Volume location.
    :param selection_radius:
        Volume radius.
    :return:
        A list of indices that reflect the points of the faces that intersect the volume.
    """

    # Get a list of polygons of the sphere object
    polygons = sphere_object.data.polygons

    # A list that will keep the intersecting faces
    faces_list = list()

    # Iterate over all the polygons of the sphere objects
    for polygon in polygons:

        # Compute the distance
        distance = (selection_location - polygon.center).length

        # Check if the polygon within the intersection range
        if distance < selection_radius:

            # Append the polygon to the list
            faces_list.append(polygon)
            
    # Add all the vertices of selected faces
    indices_list = list()

    # Iterate over all the faces of the selected faces
    for face in faces_list:

        # Iterate over the vertices of each face
        for vertex in face.vertices[:]:

            # Append the vertex
            indices_list.append(vertex)

    # Remove duplicated vertices
    indices_list = list(set(indices_list))

    # Return a reference to the indices of the vertices
    return indices_list


####################################################################################################
# @add_random_spheres_to_scene
####################################################################################################
def add_random_spheres_to_scene(number_spheres=1,
                                extent=10):
    """Add a set of random spheres to the scene.

    :param number_spheres:
        Number of spheres to be created in the scene.
    :param extent:
        The extent of the cube where the spheres will be created in Blender units.
    :return
        A list of all the created spheres in the scene.
    """

    # A list of all the created spheres.
    spheres_list = list()

    # Create the spheres and append their reference to the list
    for i in range(number_spheres):

        # Get a random XYZ coordinate
        x = random.uniform(-extent, extent)
        y = random.uniform(-extent, extent)
        z = random.uniform(-extent, extent)

        # Sphere location
        location = Vector((x, y, z))

        # Create a sphere object
        sphere = nmv.mesh.create_uv_sphere(location=location)

        # Append the sphere object to the list
        spheres_list.append(sphere)

    # Return the list of all the created spheres.
    return spheres_list


####################################################################################################
# @is_point_inside_sphere
####################################################################################################
def is_point_inside_sphere(sphere_center, 
                           sphere_radius, 
                           point):
    """Check if a given point is located inside a given sphere or not.

    :param sphere_center:
        Sphere center or location.
    :param sphere_radius:
        Sphere radius.
    :param point:
        A given point in the three-dimensional space.
    :return:
        True or False.
    """

    # Compute the distance between the point and center of the sphere and compare it with the radius
    distance = (sphere_center - point).length
    return True if distance < sphere_radius else False

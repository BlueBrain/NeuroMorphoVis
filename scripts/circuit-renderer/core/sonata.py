####################################################################################################
# Copyright (c) 2016 - 2024, EPFL / Blue Brain Project
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

# System imports
import numpy as np 
import quaternion
from scipy.spatial.transform import Rotation as R

from mathutils import Matrix

####################################################################################################
# @get_positions
####################################################################################################
def get_positions(nodes):
    """
    Extract 3D positions (x, y, z) from a nodes object.

    Args:
        nodes: An object representing nodes, expected to have methods
               `get_attribute(name, selection)` and `select_all()`.

    Returns:
        list of tuple: A list of (x, y, z) coordinates as tuples.
    """
    xs = nodes.get_attribute("x", nodes.select_all())
    ys = nodes.get_attribute("y", nodes.select_all())
    zs = nodes.get_attribute("z", nodes.select_all())
    return [(x, y, z) for x, y, z in zip(xs, ys, zs)]

####################################################################################################
# @get_position
####################################################################################################
def get_position(nodes, gid):
    """
    Retrieves the 3D position (x, y, z) of a node with the given global ID (gid).

    Parameters
    ----------
    nodes : object
        An object that provides access to node attributes via `get_attribute(attribute_name, gid)`.
    gid : int
        Global identifier of the node.

    Returns
    -------
    tuple of float
        A tuple (x, y, z) representing the 3D position of the node.
    """
    x = nodes.get_attribute("x", gid)
    y = nodes.get_attribute("y", gid)
    z = nodes.get_attribute("z", gid)
    return (x, y, z)

####################################################################################################
# @get_orientation
####################################################################################################
def get_orientation(nodes, gid):
    """
    Retrieves the orientation of a node as a 3×3 rotation matrix.

    Parameters
    ----------
    nodes : object
        An object that provides access to node attributes via `get_attribute(attribute_name, gid)`.
    gid : int
        Global identifier of the node.

    Returns
    -------
    np.ndarray
        A 3×3 rotation matrix representing the orientation of the node.
    """
    qx = nodes.get_attribute("orientation_x", gid)
    qy = nodes.get_attribute("orientation_y", gid)
    qz = nodes.get_attribute("orientation_z", gid)
    qw = nodes.get_attribute("orientation_w", gid) 
    q = np.array([qx, qy, qz, qw])  # [x, y, z, w] format expected by scipy
    r = R.from_quat(q)
    return r.as_matrix()

####################################################################################################
# @get_transformation
####################################################################################################
def get_transformation(nodes, gid):
    """
    Constructs a 4×4 homogeneous transformation matrix from a node's position and orientation.

    Parameters
    ----------
    nodes : object
        An object that provides access to node attributes via `get_attribute(attribute_name, gid)`.
    gid : int
        Global identifier of the node.

    Returns
    -------
    np.ndarray
        A 4×4 transformation matrix combining the node's rotation and translation.
    """
    translation_vector = get_position(nodes, gid)
    rotation_matrix = get_orientation(nodes, gid)
    
    transformation_matrix = np.eye(4)
    transformation_matrix[:3, :3] = rotation_matrix
    transformation_matrix[:3, 3] = translation_vector    
    return transformation_matrix

####################################################################################################
# @get_gid_of_nearest_neuron
####################################################################################################
def get_gid_of_nearest_neuron(positions, point):
    """
    Finds the index (GID) of the nearest point in `positions` to the given `point`.

    Parameters
    ----------
    positions : list of np.ndarray
        List of 3D position vectors (one per neuron).
    point : np.ndarray
        A 3D vector representing the query point.

    Returns
    -------
    tuple
        (closest_gid, shortest_distance), where:
            - closest_gid is the index of the closest point in `positions`
            - shortest_distance is the Euclidean distance to that point
    """
    shortest_distance = 1e10
    closest_gid = -1
    for i in range(len(positions)):
        dist = np.linalg.norm(positions[i] - point)
        if dist < shortest_distance:
            shortest_distance = dist
            closest_gid = i
    return closest_gid, shortest_distance

####################################################################################################
# @get_transformed_positions
####################################################################################################
def get_transformed_positions(positions, transformation_matrix):
    """
    Applies the inverse of a transformation matrix to a list of 3D positions.

    Parameters
    ----------
    positions : list of np.ndarray
        List of 3D position vectors to transform.
    transformation_matrix : np.ndarray
        A 4×4 transformation matrix to invert and apply to the positions.

    Returns
    -------
    list of np.ndarray
        The list of transformed 3D positions.
    """
    inverse_matrix = np.linalg.inv(transformation_matrix)
    
    transformed_positions = []
    for pos in positions:
        pos_homogeneous = np.append(pos, 1.0)  # Convert to homogeneous coordinate
        transformed_homogeneous = inverse_matrix @ pos_homogeneous
        transformed_position = transformed_homogeneous[:3]  # Back to 3D
        transformed_positions.append(transformed_position)
    
    return transformed_positions

####################################################################################################
# @get_layers
####################################################################################################
def get_layers(nodes):
    """
    Extract layer information for each node.

    Args:
        nodes: An object representing nodes, expected to have methods
               `get_attribute(name, selection)` and `select_all()`.

    Returns:
        list: A list of layer identifiers corresponding to each node.
    """
    return nodes.get_attribute("layer", nodes.select_all())

####################################################################################################
# @get_layers_positions
####################################################################################################
def get_layers_positions(layers, positions):
    """
    Group positions by their respective layers.

    Args:
        layers (list): List of layer identifiers (assumed to be convertible to int).
        positions (list): List of (x, y, z) position tuples.

    Returns:
        tuple: A tuple of 6 lists, each containing positions belonging to layers 1 to 6.
               Positions with layers outside [1-6] are ignored.
    """
    layer_lists = [[] for _ in range(6)]
    for layer, pos in zip(layers, positions):
        index = int(layer) - 1
        if 0 <= index < 6:
            layer_lists[index].append(pos)
    return tuple(layer_lists)

####################################################################################################
# @get_layers_positions
####################################################################################################
def get_layers_positions(layers, positions):
    """
    Group positions by their respective layers.

    Args:
        layers (list): List of layer identifiers (assumed to be convertible to int).
        positions (list): List of (x, y, z) position tuples.

    Returns:
        tuple: A tuple of 6 lists, each containing positions belonging to layers 1 to 6.
               Positions with layers outside [1-6] are ignored.
    """
    layer_lists = [[] for _ in range(6)]
    for layer, pos in zip(layers, positions):
        index = int(layer) - 1
        if 0 <= index < 6:
            layer_lists[index].append(pos)
    return tuple(layer_lists)

####################################################################################################
# @split_gids_by_layers
####################################################################################################
def split_gids_by_layers(gids, layers):
    """
    Split global identifiers (gids) into separate lists based on their corresponding layers.

    Args:
        gids (list): List of global identifiers.
        layers (list): List of layer identifiers corresponding to each gid.

    Returns:
        tuple: A tuple of 6 lists, each containing gids belonging to layers 1 to 6.
               Gids with layers outside [1-6] are ignored.
    """
    layer_lists = [[] for _ in range(6)]
    for i in range(len(layers)):
        if layers[i] == '1':
            layer_lists[0].append(gids[i])
        elif layers[i] == '2':
            layer_lists[1].append(gids[i])
        elif layers[i] == '3':
            layer_lists[2].append(gids[i])
        elif layers[i] == '4':
            layer_lists[3].append(gids[i])
        elif layers[i] == '5':
            layer_lists[4].append(gids[i])
        elif layers[i] == '6':
            layer_lists[5].append(gids[i])
    return tuple(layer_lists)

####################################################################################################
# @import_circuit
####################################################################################################
def import_circuit(circuit_config):
    """
    Load a circuit configuration using libsonata from a given config file.

    Tries to load a CircuitConfig directly. If that fails, attempts to load
    a SimulationConfig first and then load the circuit from the simulation's network.

    Args:
        circuit_config (str): Path to the circuit or simulation configuration file.

    Returns:
        libsonata.CircuitConfig or None: The loaded circuit configuration object,
                                         or None if loading fails.
    """
    import libsonata
    try:
        return libsonata.CircuitConfig.from_file(circuit_config)
    except:
        try:
            sim_config = libsonata.SimulationConfig.from_file(circuit_config)
            return libsonata.CircuitConfig.from_file(sim_config.network)
        except:
            pass
        
####################################################################################################
# @get_global_inverse_transformation
####################################################################################################
def get_global_inverse_transformation(nodes, central_neuron_gid=0):
    """
    Compute the global inverse transformation matrix for the circuit.

    This function retrieves the transformation for the first node (gid=0) and computes its inverse.

    Args:
        nodes: An object representing nodes, expected to have methods
               `get_attribute(name, selection)` and `select_all()`.

    Returns:
        mathutils.Matrix: The inverted transformation matrix.
    """

    # Get the transformation for the first node (gid=0) 
    return Matrix(get_transformation(nodes, central_neuron_gid).tolist()).inverted()
    

import subprocess, shutil, ntpath
import bpy, bmesh, os, sys, array
import argparse


####################################################################################################
# @WatertightCheck
####################################################################################################
class WatertightCheck:
    def __init__(self):
        self.watertight = False
        self.non_contiguous_edge = 0
        self.non_manifold_edges = 0
        self.non_manifold_vertices = 0 
        self.self_intersections = 0
        

####################################################################################################
# @BoundingBox
####################################################################################################
class BoundingBox:
    def __init__(self):
        x = 0.0
        y = 0.0
        z = 0.0
        diagnoal = 0.0
        
        
####################################################################################################
# @deselect_all
####################################################################################################
def deselect_all():
    """Deselect all the objects in the scene.
    """

    # Set the '.select' flag of all the objects in the scene to False.
    for scene_object in bpy.context.scene.objects:
        scene_object.select = False


####################################################################################################
# @set_active_object
####################################################################################################
def set_active_object(scene_object):
    """Set the active object in the scene to the given one.

    :param scene_object:
        A given object in the scene that is desired to be active.

    :return
        A reference to the active object.
    """

    # Deselects all objects in the scene
    deselect_all()

    # Select the object
    scene_object.select = True

    # Set it active
    bpy.context.scene.objects.active = scene_object

    # Return a reference to the mesh object again for convenience
    return scene_object


####################################################################################################
# @import_obj_file
####################################################################################################
def import_obj_file(file_path):
    """Import an .OBJ file into the scene, and return a reference to it.

    :param input_directory:
        The directory that is supposed to have the mesh.
    :param input_file_name:
        The name of the mesh file.
    :return:
        A reference to the loaded mesh in Blender.
    """

    # Issue an error message if failing
    if not os.path.isfile(file_path):
        print('LOADING ERROR: cannot load [%s]' % file_path)

    # Deselect all the objects in the scene
    deselect_all()

    print('Loading [%s]' % file_path)
    bpy.ops.import_scene.obj(filepath=file_path)

    input_file_name = ntpath.basename(file_path)
    
    # Change the name of the loaded object
    # The object will be renamed based on the file name
    object_name = input_file_name.split('.')[0]

    # The mesh is the only selected object in the scene after the previous deselection operation
    mesh_object = bpy.context.selected_objects[0]
    mesh_object.name = object_name

    # Return a reference to the object
    return mesh_object

    
####################################################################################################
# @import_ply_file
####################################################################################################
def import_ply_file(file_path):
    """Import an .OBJ file into the scene, and return a reference to it.

    :param file_path:
        The mesh path.
    :return:
        A reference to the loaded mesh in Blender.
    """
    
    # Issue an error message if failing
    if not os.path.isfile(file_path):
        print('LOADING ERROR: cannot load [%s]' % file_path)

    # Deselect all the objects in the scene
    deselect_all()

    print('Loading [%s]' % file_path)
    bpy.ops.import_mesh.ply(filepath=file_path)

    input_file_name = ntpath.basename(file_path)
    
    # Change the name of the loaded object
    # The object will be renamed based on the file name
    object_name = input_file_name.split('.')[0]

    # The mesh is the only selected object in the scene after the previous deselection operation
    mesh_object = bpy.context.selected_objects[0]
    mesh_object.name = object_name

    # Return a reference to the object
    return mesh_object


####################################################################################################
# @convert_to_mesh_object
####################################################################################################
def convert_to_mesh_object(bmesh_object,
                           name='mesh'):
    """Converts the bmesh to a new mesh object and rename it. This operation returns a reference to
    the created object.

    :param bmesh_object:
        An input bmesh object.
    :param name:
        The name of the mesh object.
    :return:
        Returns a reference to the converted object.
    """

    # Create a new mesh object and convert the bmesh object to it
    mesh_object = bpy.data.meshes.new(name)
    bmesh_object.to_mesh(mesh_object)

    # Return a reference to the mesh object
    return mesh_object


####################################################################################################
# @convert_from_mesh_object
####################################################################################################
def convert_from_mesh_object(mesh_object):
    """
    Converts the mesh object to a bmesh object and returns a reference to it.

    :param mesh_object: An input mesh object.
    :return: A reference to the bmesh object.
    """

    # Return a reference to the bmesh created from the object.
    return bmesh.from_edit_mesh(mesh_object.data)



     
####################################################################################################
# @check_watertightness
####################################################################################################
def check_watertightness(bm):
    """
    Checks if the mesh is watertight or not.

    :param mesh_object: An input mesh object.
    :return: True or False
    """

    # Set the current object to be the active object
    # set_active_object(mesh_object)
    
    # Switch to geometry or edit mode from the object mode
    # bpy.ops.object.editmode_toggle()
    
    # Convert the mesh into a bmesh
    # bm = convert_from_mesh_object(mesh_object)

    # Watertightness checks
    non_manifold_edges = 0
    non_contiguous_edge = 0
    non_manifold_vertices = 0

    check = WatertightCheck()
    
    # Edges 
    for i, edge in enumerate(bm.edges):
        if not edge.is_manifold:
            non_manifold_edges += 1 
        if not edge.is_contiguous:
            non_contiguous_edge += 1
            
    # Vertices 
    for i, vert in enumerate(bm.verts):
        if not vert.is_manifold:
            non_manifold_vertices += 1
    
    import mathutils
    tree = mathutils.bvhtree.BVHTree.FromBMesh(bm, epsilon=0.00001)
    overlap = tree.overlap(tree)
    faces_error = {i for i_pair in overlap for i in i_pair}
    if len(faces_error) > 0:
        check.self_intersections = len(faces_error)
            
    # bm.free()
    
    # Switch to geometry or edit mode from the object mode
    # bpy.ops.object.editmode_toggle()
    
    check.non_manifold_edges = non_manifold_edges
    check.non_manifold_vertices = non_manifold_vertices
    check.non_contiguous_edge = non_contiguous_edge

    if non_manifold_edges > 0 or non_contiguous_edge > 0 or (non_manifold_vertices > 0):
        check.watertight = False
    else:
        check.watertight = True
    
    # Return the result
    return check


####################################################################################################
# @is_self_intersecting
####################################################################################################
def is_self_intersecting(bm):
    """
    Checks if the mesh is self intersecting or not.
    """
    
    #if not mesh.data.polygons:
    #    return False
        
    # Set the current object to be the active object
    # set_active_object(mesh)
    
    # Switch to geometry or edit mode from the object mode
    # bpy.ops.object.editmode_toggle()
    
    # Convert the mesh into a bmesh
    # bm = convert_from_mesh_object(mesh)

    import mathutils
    tree = mathutils.bvhtree.BVHTree.FromBMesh(bm, epsilon=0.00001)
    overlap = tree.overlap(tree)
    faces_error = {i for i_pair in overlap for i in i_pair}
    if len(faces_error) > 0:
        return True
    return False     

    
####################################################################################################
# @compute_surface_area
####################################################################################################
def compute_surface_area(bm):
    """
    Calculates the surface area of a given mesh
    """
    
    # Set the current object to be the active object
    # set_active_object(mesh)
    
    # Switch to geometry or edit mode from the object mode
    # bpy.ops.object.editmode_toggle()
    
    # Convert the mesh into a bmesh
    # bm = convert_from_mesh_object(mesh)
    
    # Compute teh surface area 
    surface_area = 0.0
    for f in bm.faces:
        surface_area += f.calc_area()    
    
    # Release the bm 
    # bm.free()
    
    # Switch to geometry or edit mode from the object mode
    # bpy.ops.object.editmode_toggle()
    
    # Return the surface area 
    return surface_area
    

####################################################################################################
# @compute_number_polygons
####################################################################################################
def compute_number_polygons(bm):
    """
    Calculates the number of polygons of a given mesh
    """
    
    # Set the current object to be the active object
    # set_active_object(mesh)
    
    # Switch to geometry or edit mode from the object mode
    # bpy.ops.object.editmode_toggle()
    
    # Convert the mesh into a bmesh
    # bm = convert_from_mesh_object(mesh)
    
    # Compute it 
    polygons = len(bm.faces)    
    
    # Release the bm 
    # bm.free()
    
    # Switch to geometry or edit mode from the object mode
    # bpy.ops.object.editmode_toggle()
    
    # Return the polygon count 
    return polygons


####################################################################################################
# @compute_number_vertices
####################################################################################################
def compute_bounding_box(mesh_object):
    """
    Calculates the bounding box
    """
    
    import math 
    
    bbox = BoundingBox()
    bbox.x = mesh_object.dimensions.x
    bbox.y = mesh_object.dimensions.y
    bbox.z = mesh_object.dimensions.z
    bbox.diagonal = math.sqrt((bbox.x * bbox.x) + (bbox.y * bbox.y) + (bbox.z * bbox.z))  
    
    return bbox 
    
    
####################################################################################################
# @compute_number_vertices
####################################################################################################
def compute_number_vertices(bm):
    """
    Calculates the number of polygons of a given mesh
    """
    
    # Set the current object to be the active object
    # set_active_object(mesh)
    
    # Switch to geometry or edit mode from the object mode
    # bpy.ops.object.editmode_toggle()
    
    # Convert the mesh into a bmesh
    # bm = convert_from_mesh_object(mesh)
    
    # Compute it 
    vertices = len(bm.verts)    
    
    # Release the bm 
    # bm.free()
    
    # Switch to geometry or edit mode from the object mode
    # bpy.ops.object.editmode_toggle()
    
    # Return the polygon count 
    return vertices
    
    
####################################################################################################
# @compute_surface_area
####################################################################################################
def compute_volume(bm):
    """Compute the volume of the mesh.
    """
    
    # Set the current object to be the active object
    # set_active_object(mesh)
    
    # Switch to geometry or edit mode from the object mode
    # bpy.ops.object.editmode_toggle()
    
    # Convert the mesh into a bmesh
    # bm = convert_from_mesh_object(mesh)
    
    # Compute the volume 
    volume = bm.calc_volume()
    
    # Free the bmesh 
    # bm.free()
    
    # Switch to geometry or edit mode from the object mode
    # bpy.ops.object.editmode_toggle()
    
    # Return the volume 
    return volume
    
    
####################################################################################################
# @parse_command_line_arguments
####################################################################################################
def parse_command_line_arguments():

    # Create an argument parser, and then add the options one by one
    parser = argparse.ArgumentParser(sys.argv)

    # Morphology directory
    arg_help = 'Input mesh'
    parser.add_argument('--mesh', action='store', help=arg_help)
                        
    # Output directory
    arg_help = 'Output directory'
    parser.add_argument('--output-directory', action='store', default=None, help=arg_help)
                        
    # Parse the arguments, and return a list of them
    return parser.parse_args()

        
####################################################################################################
# @ Run the main function if invoked from the command line.
####################################################################################################
if __name__ == "__main__":

    # Ignore blender extra arguments required to launch blender given to the command line interface
    args = sys.argv
    args = args[args.index("--") + 0:]
    sys.argv = args
    
    # Main
    args = parse_command_line_arguments()

    file_name, file_extension = os.path.splitext(args.mesh)

    # Import the file
    if '.ply' == file_extension:
        mesh_object = import_ply_file(args.mesh)
    elif '.obj' == file_extension:
        mesh_object = import_obj_file(args.mesh)
        
    # Set the current object to be the active object
    set_active_object(mesh_object)
    
    # Compute the bounding box
    bbox = compute_bounding_box(mesh_object)
    
    # Switch to geometry or edit mode from the object mode
    bpy.ops.object.editmode_toggle()
    
    # Convert the mesh into a bmesh
    bm = convert_from_mesh_object(mesh_object)
    
    # Compute the surface area
    print('\tSurface Area')
    surface_area = compute_surface_area(bm)

    # Compute the volume
    print('\tVolume')
    volume = compute_volume(bm)
    
    # Compute the number of polygons 
    print('\tNumber Polygons')
    polygons = compute_number_polygons(bm)

    # Compute the number of vertices
    print('\tVertices') 
    vertices = compute_number_vertices(bm)

    # Is it watertight
    print('\tWatertightness')
    watertight_check = check_watertightness(bm)
    
    # Free the bmesh 
    bm.free()
    
    # Switch to geometry or edit mode from the object mode
    bpy.ops.object.editmode_toggle()

    # Print details
    input_file_name = ntpath.basename(args.mesh)
    
    info_file = open('%s/%s.info' % (args.output_directory, input_file_name), 'w')
    info_file = open('%s/%s.info' % (args.output_directory, input_file_name), 'w')
    info_file.write('Bounding Box Size = %f %f %f \n' % (bbox.x, bbox.y, bbox.z))
    info_file.write('Bounding Box Diagonal = %f \n' % bbox.diagonal)
    info_file.write('Number Polygons = %d \n' % polygons)
    info_file.write('Number Vertices = %d \n' % vertices)
    info_file.write('Surface Area = %f \n' % surface_area)
    info_file.write('Volume = %f \n' % volume)
    info_file.write('Watertight: %s \n' % str(watertight_check.watertight))
    info_file.write('Non Manifold Edges: %s \n' % str(watertight_check.non_manifold_edges))
    info_file.write('Non Manifold Vertices: %s \n' % str(watertight_check.non_manifold_vertices))
    info_file.write('Non Continious Edges: %s \n' % str(watertight_check.non_contiguous_edge))
    info_file.write('Self-intersecting: %s \n' % str(watertight_check.self_intersections))
    info_file.close()




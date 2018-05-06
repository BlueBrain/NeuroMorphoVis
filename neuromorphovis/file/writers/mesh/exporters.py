"""
exporters.py:
    Mesh exporters into different file formats and types.
"""

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2017, Blue Brain Project / EPFL"
__version__     = "0.1.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"

# Blender imports
import bpy

# Internal modules
import neuromorphovis as nmv
import neuromorphovis.scene
import neuromorphovis.utilities


####################################################################################################
# @export_object_to_ply_file
####################################################################################################
def export_object_to_ply_file(mesh_object,
                              output_directory,
                              output_file_name):
    """
    Exports a selected object to a .ply file.

    :param mesh_object: A selected mesh object in the scene.
    :param output_directory: The output directory where the mesh will be saved.
    :param output_file_name: The name of the output mesh.
    """

    # Construct the name of the exported mesh.
    output_file_path = "%s/%s.ply" % (output_directory, str(output_file_name))

    # Deselect all the other objects in the scene
    nmv.scene.ops.deselect_all()

    # Select the target mesh and set it to be the only active object
    nmv.scene.ops.set_active_object(mesh_object)

    # Export the mesh object to an OBJ file
    nmv.logger.log('Exporting [%s]' % output_file_path)
    export_timer = nmv.utilities.Timer()
    export_timer.start()

    bpy.ops.export_mesh.ply(filepath=output_file_path, check_existing=True)

    export_timer.end()
    nmv.logger.log('Exporting done in [%f] seconds' % export_timer.duration())


####################################################################################################
# @export_object_to_obj_file
####################################################################################################
def export_object_to_obj_file(mesh_object,
                              output_directory,
                              output_file_name):
    """
    Exports a selected object to an ascii .obj file.

    :param mesh_object: A selected mesh object in the scene.
    :param output_directory: The output directory where the mesh will be saved.
    :param output_file_name: The name of the output mesh.
    """

    # Construct the name of the exported mesh.
    output_file_path = "%s/%s.obj" % (output_directory, output_file_name)

    # Deselect all the other objects in the scene
    nmv.scene.ops.deselect_all()

    # Select the target mesh and set it to be the only active object
    nmv.scene.ops.set_active_object(mesh_object)

    nmv.logger.log('Exporting [%s]' % output_file_path)
    export_timer = nmv.utilities.Timer()
    export_timer.start()

    bpy.ops.export_scene.obj(filepath=output_file_path, check_existing=True, axis_forward='-Z',
        axis_up='Y', use_selection=True, use_smooth_groups=True,
        use_smooth_groups_bitflags=False, use_normals=True, use_triangles=True,
        path_mode='AUTO')

    export_timer.end()
    nmv.logger.log('Exporting done in [%f] seconds' % export_timer.duration())


####################################################################################################
# @export_object_to_stl_file
####################################################################################################
def export_object_to_stl_file(mesh_object,
                              output_directory,
                              output_file_name):
    """
    Exports a selected object to a binary .stl file.

    :param mesh_object: A selected mesh object in the scene.
    :param output_directory: The output directory where the mesh will be saved.
    :param output_file_name: The name of the output mesh.
    """

    # Construct the name of the exported mesh.
    output_file_path = "%s/%s.stl" % (output_directory, output_file_name)

    # Deselect all the other objects in the scene
    nmv.scene.ops.deselect_all()

    # Select the target mesh and set it to be the only active object
    nmv.scene.ops.set_active_object(mesh_object)

    # Export the mesh object to a binary STL file
    nmv.logger.log('Exporting [%s]' % output_file_path)
    export_timer = nmv.utilities.Timer()
    export_timer.start()

    bpy.ops.export_mesh.stl(filepath=output_file_path, check_existing=True, ascii=False)

    export_timer.end()
    nmv.logger.log('Exporting done in [%f] seconds' % export_timer.duration())


####################################################################################################
# @export_object_to_blend_file
####################################################################################################
def export_object_to_blend_file(mesh_object,
                                output_directory,
                                output_file_name):
    """
    Exports a selected object to a binary .blend file.

    :param mesh_object: A selected mesh object in the scene. If this option is set to None,
    the exported file will contain all the objects that exist in the scene.
    :param output_directory: The output directory where the mesh will be saved.
    :param output_file_name: The name of the output mesh.
    """

    # Construct the name of the exported mesh.
    output_file_path = "%s/%s.blend" % (output_directory, output_file_name)

    # Deselect all the other objects in the scene
    nmv.scene.ops.deselect_all()

    # Select the target mesh and set it to be the only active object if selected
    if mesh_object is not None:
        nmv.scene.ops.set_active_object(mesh_object)

    # Export the mesh object to a binary STL file
    nmv.logger.log('Exporting [%s]' % output_file_path)
    export_timer = nmv.utilities.Timer()
    export_timer.start()

    bpy.ops.wm.save_as_mainfile(filepath=output_file_path, check_existing=True)

    export_timer.end()
    nmv.logger.log('Exporting done in [%f] seconds' % export_timer.duration())


####################################################################################################
# @export_mesh_object
####################################################################################################
def export_mesh_object(mesh_object,
                       output_directory,
                       file_name,
                       obj=False,
                       ply=False,
                       stl=False,
                       blend=False):
    """
    Exports the mesh in one line in different file formats.

    :param mesh_object: An input mesh object to export to a file.
    :param output_directory: Output directory where the meshes will be saved.
    :param file_name: Mesh prefix.
    :param obj: Flag to export to .obj format.
    :param ply: Flag to export to .ply format.
    :param stl: Flag to export to .stl format.
    :param blend: Flag to export to .blend format.
    """

    # To .obj format
    if obj:
        export_object_to_obj_file(mesh_object, output_directory, file_name)

    # To .ply format
    if ply:
        export_object_to_ply_file(mesh_object, output_directory, file_name)

    # .To stl format
    if stl:
        export_object_to_stl_file(mesh_object, output_directory, file_name)

    # To .blend format
    if blend:
        export_object_to_blend_file(mesh_object, output_directory, file_name)


####################################################################################################
# @export_mesh_as_separate_objects
####################################################################################################
def export_mesh_as_separate_objects(soma_mesh,
                                    branches_meshes,
                                    spines_meshes,
                                    output_directory,
                                    output_file_name,
                                    export_ply,
                                    export_obj,
                                    export_stl):
    """
    Exports the neuron meshes as separate objects.

    :param soma_mesh: The mesh of the soma.
    :param branches_meshes: A list of all the meshes of the branches.
    :param spines_meshes: A list of all the meshes of the spines.
    :param output_directory: A directory where all the meshes will be saved to.
    :param output_file_name: File prefix.
    :param export_ply: Save the meshes in ply format.
    :param export_obj: Save the meshes in obj format.
    :param export_stl: Save the meshes in stl format.
    """

    # To .ply format
    if export_ply:

        # Soma
        export_object_to_ply_file(soma_mesh, output_directory, '%s_soma' % output_file_name)

        # Branches
        for i, branch_mesh in branches_meshes:
            mesh_name = '%s_branch_%d' % (output_file_name, i)
            export_object_to_ply_file(branch_mesh, output_directory, mesh_name)

        # Spines
        for i, spine_mesh in spines_meshes:
            mesh_name = '%s_spine_%d' % (output_file_name, i)
            export_object_to_ply_file(spine_mesh, output_directory, mesh_name)

    # To obj. format
    if export_obj:

        # Soma
        export_object_to_obj_file(soma_mesh, output_directory, '%s_soma' % output_file_name)

        # Branches
        for i, branch_mesh in branches_meshes:
            mesh_name = '%s_branch_%d' % (output_file_name, i)
            export_object_to_obj_file(branch_mesh, output_directory, mesh_name)

        # Spines
        for i, spine_mesh in spines_meshes:
            mesh_name = '%s_spine_%d' % (output_file_name, i)
            export_object_to_obj_file(spine_mesh, output_directory, mesh_name)

    # To .stl format
    if export_stl:

        # Soma
        export_object_to_stl_file(soma_mesh, output_directory, '%s_soma' % output_file_name)

        # Branches
        for i, branch_mesh in branches_meshes:
            mesh_name = '%s_branch_%d' % (output_file_name, i)
            export_object_to_stl_file(branch_mesh, output_directory, mesh_name)

        # Spines
        for i, spine_mesh in spines_meshes:
            mesh_name = '%s_spine_%d' % (output_file_name, i)
            export_object_to_stl_file(spine_mesh, output_directory, mesh_name)

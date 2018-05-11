"""soft_body_options.py:
    Soft body physics options.
"""

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2016 - 2017, Blue Brain Project / EPFL"
__version__     = "1.0.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"

# Internal imports
import neuromorphovis as nmv
import neuromorphovis.consts
import neuromorphovis.enums


####################################################################################################
# @SomaOptions
####################################################################################################
class SomaOptions:
    """Soma options
    """

    def __init__(self):
        """Constructor
        """

        # Reconstruction method
        self.method = nmv.enums.Soma.ReconstructionMethod.ARBORS_ONLY

        # Stiffness
        self.stiffness = nmv.consts.SoftBody.GOAL_DEFAULT

        # Subdivision level of the sphere
        self.subdivision_level = nmv.consts.SoftBody.SUBDIVISIONS_DEFAULT

        # Irregular subdivisions for the faces created for extruding the arbors
        self.irregular_subdivisions = False

        # Extrude the arbors from the soma to cover the maximal volume
        self.full_volume_extrusion = True

        # Simulation steps
        self.simulation_steps = nmv.consts.SoftBody.SIMULATION_STEPS_DEFAULT

        # Soma color
        self.soma_color = nmv.enums.Color.SOMA

        # Soma material
        self.soma_material = nmv.enums.Shading.FLAT

        # Reconstruct soma mesh
        self.reconstruct_soma_mesh = False

        # Render projections of the soma mesh
        self.render_soma_mesh = False

        # Render the progressive reconstruction of the soma mesh
        self.render_soma_mesh_progressive = False

        # Render a 360 sequence for the reconstructed soma mesh
        self.render_soma_mesh_360 = False

        # Rendering resolution for the soma images
        self.rendering_resolution = 512

        # Rendering extent in microns
        self.rendering_extent = 20

        # Camera view
        self.camera_view = nmv.enums.Camera.View.FRONT

        # Export soma mesh in .ply format
        self.export_ply = False

        # Export soma mesh in .obj format
        self.export_obj = False

        # Export soma mesh in .stl format
        self.export_stl = False

        # Export soma mesh in .blend format
        self.export_blend = False


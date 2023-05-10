





import bpy


####################################################################################################
# @SomaReconstructionDocumentation
####################################################################################################
class SomaReconstructionDocumentation(bpy.types.Operator):
    """Open the online documentation page of the Soma Reconstruction panel"""

    # Operator parameters
    bl_idname = "nmv.documentation_soma"
    bl_label = "Online User Guide"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):

        import webbrowser
        webbrowser.open('https://github.com/BlueBrain/NeuroMorphoVis/wiki/Soma-Reconstruction')
        return {'FINISHED'}


# System imports
import time

# Internal imports
import nmv.bbox
import nmv.builders
import nmv.consts
import nmv.enums
import nmv.file
import nmv.interface
import nmv.shading
import nmv.scene
import nmv.skeleton
import nmv.utilities
import nmv.rendering
import nmv.geometry


####################################################################################################
# draw_rendering_options
####################################################################################################
def draw_rendering_options(layout,
                          scene,
                          options):
    """Morphology rendering options.

    :param layout:
        Panel layout.
    :param scene:
        Context scene.NMV_
    :param options:
        System options.
    """

    # Quick rendering options
    quick_rendering_row = layout.row()
    quick_rendering_row.label(text='Quick Rendering Options:', icon='RENDER_STILL')

    # Rendering view
    rendering_view_row = layout.row()
    rendering_view_row.prop(scene, 'NMV_MorphologyRenderingView', expand=True)

    # Close up view
    if scene.NMV_MorphologyRenderingView == nmv.enums.Rendering.View.CLOSEUP:

        # Rendering close up option
        render_close_up_row = layout.row()
        render_close_up_row.prop(scene, 'NMV_MorphologyCloseUpDimensions')

        # Frame resolution option
        frame_resolution_row = layout.row()
        frame_resolution_row.label(text='Frame Resolution:')
        frame_resolution_row.prop(scene, 'NMV_MorphologyFrameResolution')
        frame_resolution_row.enabled = True

    # Full morphology view
    else:

        # Rendering type
        rendering_type_row = layout.row()
        rendering_type_row.prop(scene, 'NMV_RenderingType', expand=True)

        # Render at a specific resolution
        if scene.NMV_RenderingType == nmv.enums.Rendering.Resolution.FIXED:

            # Frame resolution option
            frame_resolution_row = layout.row()
            frame_resolution_row.label(text='Frame Resolution:')
            frame_resolution_row.prop(scene, 'NMV_MorphologyFrameResolution')
            frame_resolution_row.enabled = True

        # Otherwise, render to scale
        else:

            # Scale factor option
            scale_factor_row = layout.row()
            scale_factor_row.prop(scene, 'NMV_MorphologyFrameScaleFactor')
            scale_factor_row.enabled = True

    # Image extension
    image_extension_row = layout.row()
    image_extension_row.label(text='Image Format:')
    image_extension_row.prop(scene, 'NMV_MorphologyImageFormat')
    nmv.interface.ui_options.morphology.image_format = scene.NMV_MorphologyImageFormat

    # Scale bar
    scale_bar_row = layout.row()
    scale_bar_row.prop(scene, 'NMV_RenderMorphologyScaleBar')
    nmv.interface.ui_options.rendering.render_scale_bar = scene.NMV_RenderMorphologyScaleBar

    # Render view buttons
    render_view_row = layout.row()
    render_view_row.label(text='Render View:', icon='RESTRICT_RENDER_OFF')
    render_view_buttons_row = layout.row(align=True)
    render_view_buttons_row.operator('nmv.render_morphology_front', icon='AXIS_FRONT')
    render_view_buttons_row.operator('nmv.render_morphology_side', icon='AXIS_SIDE')
    render_view_buttons_row.operator('nmv.render_morphology_top', icon='AXIS_TOP')
    render_view_buttons_row.enabled = True

    # Render animations buttons
    render_animation_row = layout.row()
    render_animation_row.label(text='Render Animation:', icon='CAMERA_DATA')
    render_animations_buttons_row = layout.row(align=True)
    render_animations_buttons_row.operator('nmv.render_morphology_360', icon='FORCE_MAGNETIC')
    render_animations_buttons_row.operator('nmv.render_morphology_progressive',
                                           icon='FORCE_HARMONIC')
    render_animations_buttons_row.enabled = True

    # Progress bar
    progress_bar_row = layout.row()
    progress_bar_row.prop(scene, 'NMV_MorphologyRenderingProgress')
    progress_bar_row.enabled = False

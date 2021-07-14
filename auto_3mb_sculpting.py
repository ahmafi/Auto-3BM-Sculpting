bl_info = {
    "name": "Auto 3BM Sculpting",
    "author": "Amir Hossein Mafi <amir77mafi@gmail.com>",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "description": 'Automatically enables "Emulate 3 Button Mouse" when entering sculpt mode',
    "category": "3D View",
}

import bpy
from bpy.app.handlers import persistent

def callback_mode_change(object, data):
    if bpy.context.active_object.mode == "SCULPT":
        bpy.context.preferences.inputs.use_mouse_emulate_3_button=True
    else:
        bpy.context.preferences.inputs.use_mouse_emulate_3_button=False

owner = object()

def subscribe_mode_change():
    subscribe_to = (bpy.types.Object, "mode")

    bpy.msgbus.subscribe_rna(
        key=subscribe_to,
        owner=owner,
        args=(owner,"mode",),
        notify=callback_mode_change,
    )

def unsubscribe_mode_change():
    bpy.msgbus.clear_by_owner(owner)

@persistent
def load_handler(dummy):
    subscribe_mode_change()

def register():
    bpy.app.handlers.load_post.append(load_handler)
    
    # subscribe for the first time use, so we don't need to restart the blend file
    subscribe_mode_change()

def unregister():
    bpy.app.handlers.load_post.remove(load_handler)

    # unsubscribe after unregister, so we don't need to restart the blend file
    unsubscribe_mode_change()

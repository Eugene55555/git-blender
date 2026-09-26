import bpy
import math

scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 240  # 8 s at 30 fps, loops seamlessly

prefs = bpy.context.preferences.edit
prefs.keyframe_new_interpolation_type = 'LINEAR'

def spin(name, turns):
    obj = bpy.data.objects.get(name)
    e = obj.rotation_euler
    obj.keyframe_insert(data_path="rotation_euler", frame=1)
    e.z = e.z + 2 * math.pi * turns
    obj.keyframe_insert(data_path="rotation_euler", frame=241)

spin("Ring_Cyan", 1.0)
spin("Ring_Magenta", -1.0)
spin("Cable", 2.0)

import os
os.makedirs("/home/kat/hermes-workspace/git-repo/git-blender/scene", exist_ok=True)

bpy.ops.wm.save_as_mainfile(filepath="/home/kat/hermes-workspace/git-repo/git-blender/scene/ai_core.blend")
bpy.ops.export_scene.gltf(
    filepath="/home/kat/hermes-workspace/git-repo/git-blender/scene/ai_core.glb",
    export_format='GLB',
    export_animations=True,
    export_animation_mode='SCENE',
)
print("GLB_EXPORTED")

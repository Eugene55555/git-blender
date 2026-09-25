import bpy

# Экспорт для веба: только сфера + кольца (пол исключаем — в model-viewer будет мягкая тень)
for o in bpy.data.objects:
    o.select_set(False)
keep = [o for o in bpy.data.objects if o.name in ("AI_Core", "Ring_Cyan", "Ring_Magenta", "Cable")]
for o in keep:
    o.select_set(True)

bpy.ops.export_scene.gltf(
    filepath="/home/kat/hermes-workspace/git-repo/git-blender/scene/ai_core.glb",
    export_format='GLB',
    export_animations=True,
    export_animation_mode='SCENE',
    use_selection=True,
)
print("GLB_EXPORTED_NO_FLOOR", len(keep), "objects")

# AI Core demo scene — recreates the style from the reference video (Blender MCP практикум demo)
import bpy
import math

# ---------- clean scene ----------
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)

# ---------- core sphere (dark glossy) ----------
bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, segments=96, ring_count=48, location=(0, 0, 1.15))
core = bpy.context.active_object
core.name = "AI_Core"
bpy.ops.object.shade_smooth()
mcore = bpy.data.materials.new("AI_Core_Shell")
mcore.use_nodes = True
n = mcore.node_tree.nodes["Principled BSDF"]
n.inputs["Base Color"].default_value = (0.015, 0.015, 0.02, 1.0)
n.inputs["Metallic"].default_value = 1.0
n.inputs["Roughness"].default_value = 0.08
core.data.materials.append(mcore)

# ---------- orbit ring 1 (cyan emissive) ----------
bpy.ops.mesh.primitive_torus_add(major_radius=1.55, minor_radius=0.014, location=(0, 0, 1.15), rotation=(math.radians(75), 0, math.radians(15)))
ring1 = bpy.context.active_object
ring1.name = "Ring_Cyan"
bpy.ops.object.shade_smooth()
m1 = bpy.data.materials.new("Cyan_Glow")
m1.use_nodes = True
n = m1.node_tree.nodes["Principled BSDF"]
n.inputs["Base Color"].default_value = (0.1, 0.75, 1.0, 1.0)
n.inputs["Emission Color"].default_value = (0.1, 0.75, 1.0, 1.0)
n.inputs["Emission Strength"].default_value = 20.0
ring1.data.materials.append(m1)

# ---------- orbit ring 2 (magenta emissive) ----------
bpy.ops.mesh.primitive_torus_add(major_radius=1.85, minor_radius=0.012, location=(0, 0, 1.15), rotation=(math.radians(108), 0, math.radians(-22)))
ring2 = bpy.context.active_object
ring2.name = "Ring_Magenta"
bpy.ops.object.shade_smooth()
m2 = bpy.data.materials.new("Magenta_Glow")
m2.use_nodes = True
n = m2.node_tree.nodes["Principled BSDF"]
n.inputs["Base Color"].default_value = (0.75, 0.2, 1.0, 1.0)
n.inputs["Emission Color"].default_value = (0.75, 0.2, 1.0, 1.0)
n.inputs["Emission Strength"].default_value = 16.0
ring2.data.materials.append(m2)

# ---------- thin dark cable ring ----------
bpy.ops.mesh.primitive_torus_add(major_radius=1.3, minor_radius=0.03, location=(0, 0, 1.15), rotation=(math.radians(95), math.radians(12), math.radians(40)))
ring3 = bpy.context.active_object
ring3.name = "Cable"
bpy.ops.object.shade_smooth()
m3 = bpy.data.materials.new("Cable_Dark")
m3.use_nodes = True
n = m3.node_tree.nodes["Principled BSDF"]
n.inputs["Base Color"].default_value = (0.02, 0.02, 0.025, 1.0)
n.inputs["Metallic"].default_value = 0.4
n.inputs["Roughness"].default_value = 0.5
ring3.data.materials.append(m3)

# ---------- floor ----------
bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, 0))
floor = bpy.context.active_object
floor.name = "Floor"
mfloor = bpy.data.materials.new("Floor_Dark")
mfloor.use_nodes = True
n = mfloor.node_tree.nodes["Principled BSDF"]
n.inputs["Base Color"].default_value = (0.008, 0.009, 0.012, 1.0)
n.inputs["Roughness"].default_value = 0.35
floor.data.materials.append(mfloor)

# ---------- lights ----------
bpy.ops.object.light_add(type='AREA', location=(4.2, -2.6, 3.6))
l1 = bpy.context.active_object
l1.name = "cold_cyan_rim_light"
l1.data.energy = 800.0
l1.data.size = 2.6
l1.data.color = (0.22, 0.72, 1.0)
c1 = l1.constraints.new('TRACK_TO')
c1.target = core
c1.track_axis = 'TRACK_NEGATIVE_Z'
c1.up_axis = 'UP_Y'

bpy.ops.object.light_add(type='AREA', location=(-3.6, 2.2, 2.6))
l2 = bpy.context.active_object
l2.name = "magenta_rim_light"
l2.data.energy = 550.0
l2.data.size = 2.2
l2.data.color = (0.72, 0.25, 1.0)
c2 = l2.constraints.new('TRACK_TO')
c2.target = core
c2.track_axis = 'TRACK_NEGATIVE_Z'
c2.up_axis = 'UP_Y'

bpy.ops.object.light_add(type='AREA', location=(0.4, 3.8, 4.2))
l3 = bpy.context.active_object
l3.name = "warm_fill"
l3.data.energy = 260.0
l3.data.size = 3.0
l3.data.color = (1.0, 0.86, 0.72)
c3 = l3.constraints.new('TRACK_TO')
c3.target = core
c3.track_axis = 'TRACK_NEGATIVE_Z'
c3.up_axis = 'UP_Y'

# ---------- world ----------
world = bpy.data.worlds[0] if bpy.data.worlds else bpy.data.worlds.new("World")
bpy.context.scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.004, 0.005, 0.009, 1.0)
bg.inputs[1].default_value = 1.0

# ---------- camera ----------
bpy.ops.object.camera_add(location=(4.4, -4.1, 2.7))
cam = bpy.context.active_object
cam.name = "Camera_AI_Core"
cam.data.lens = 62
cc = cam.constraints.new('TRACK_TO')
cc.target = core
cc.track_axis = 'TRACK_NEGATIVE_Z'
cc.up_axis = 'UP_Y'
bpy.context.scene.camera = cam

# ---------- render settings ----------
sc = bpy.context.scene
sc.render.engine = 'CYCLES'
sc.cycles.device = 'CPU'
sc.cycles.samples = 48
sc.cycles.use_denoising = True
sc.render.resolution_x = 720
sc.render.resolution_y = 720
sc.render.image_settings.file_format = 'PNG'
sc.render.filepath = "/home/kat/hermes-workspace/git-repo/git-blender/renders/ai_core_demo"

# ---------- save ----------
bpy.ops.wm.save_as_mainfile(filepath="/home/kat/hermes-workspace/git-repo/git-blender/scene/ai_core.blend")
print("AI_CORE_SCENE_READY", len(bpy.data.objects), "objects")

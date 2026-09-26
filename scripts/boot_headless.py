"""Blender headless (Xvfb) bootstrap: enable MCP addon + auto-start server."""
import bpy
import addon_utils

NAME = "blender_mcp"
try:
    addon_utils.enable(NAME, default_set=True, persistent=True)
    print("BLENDERMCP: addon enabled:", NAME)
except Exception as e:
    print("BLENDERMCP: enable failed:", repr(e))

scene = bpy.context.scene
print("BLENDERMCP: auto_start =", scene.blendermcp_auto_start_server, "| port =", scene.blendermcp_port)

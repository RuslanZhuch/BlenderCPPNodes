import bpy

from bpy.types import NodeTree

class ScriptingTree(NodeTree):
    bl_idname = 'ScriptingTreeType'
    bl_label = "Scripting"
    bl_icon = 'NODETREE'

_classes = (
    ScriptingTree, 
)

def register():
    for cls in _classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)

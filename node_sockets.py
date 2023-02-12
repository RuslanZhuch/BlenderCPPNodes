import bpy
from bpy.types import NodeTree, Node, NodeSocket

# Custom socket type
class ScriptingNodeAutoSocket(NodeSocket):
    bl_idname = 'AUTO_SCRIPTING_SOKET'
    bl_label = "auto"

    value: None

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    # Socket color
    def draw_color(self, context, node):
        return (0.69, 0.14, 0.43, 0.8)


_classes = (
    ScriptingNodeAutoSocket, 
)

def register():
    for cls in _classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)
import bpy
from bpy.types import NodeTree, Node, NodeSocket

# Custom socket type
class ScriptingNodeAutoSocket(NodeSocket):
    bl_idname = 'AUTO_SCRIPTING_SOKET'
    bl_label = "auto"

    value: None

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0.69, 0.14, 0.43, 0.8)

class ScriptingNodeAutoSocketWeakName(NodeSocket):
    bl_idname = 'AUTO_SCRIPTING_SOKET_WEAK'
    bl_label = "auto"

    def draw(self, context, layout, node, text):
        if len(self.links) == 0:
            layout.label(text=text)
            return

        link = self.links[0]
        layout.label(text=link.to_socket.name)

    def draw_color(self, context, node):
        return (0.69, 0.14, 0.43, 0.8)

_classes = (
    ScriptingNodeAutoSocket, 
    ScriptingNodeAutoSocketWeakName,
)

def register():
    for cls in _classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)
import bpy
from bpy.types import NodeTree, Node, NodeSocket, NodeCustomGroup, StringProperty

class TypesMapper:
    @staticmethod
    def type_to_socket(data_type):
        if data_type == "int":
            return "NodeSocketInt"
        elif data_type == "float":
            return "NodeSocketFloat"
        elif data_type == "bool":
            return "NodeSocketBool"
        elif data_type == "auto":
            return "AUTO_SCRIPTING_SOKET"
        return "NodeSocketInt"

class ScriptingTreeNodeBase(Node):
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'ScriptingTreeType'

def update_sockets(sockets):
        sockets_linked = sum([socket.is_linked for socket in sockets])

        linked_sockets_diff = len(sockets) - sockets_linked 
        if linked_sockets_diff == 0:
            sockets.new("AUTO_SCRIPTING_SOKET_WEAK", "Value")
        elif linked_sockets_diff >= 2:
            last_socket_id = 0
            while linked_sockets_diff > 1:
                while True:
                    if sockets[last_socket_id].is_linked:
                        last_socket_id -= 1
                        continue
                    sockets.remove(sockets[last_socket_id])
                    linked_sockets_diff -= 1
                    break

class InputScriptingNode(ScriptingTreeNodeBase):
    bl_idname = "InputScriptingNode"
    bl_label = "Input"

    def init(self, context):
        self.outputs.new("AUTO_SCRIPTING_SOKET_WEAK", "Value")
        
    def update(self):
        update_sockets(self.outputs)


class OutputScriptingNode(ScriptingTreeNodeBase):
    bl_idname = "OutputScriptingNode"
    bl_label = "Output"

    def init(self, context):
        self.inputs.new("AUTO_SCRIPTING_SOKET_WEAK", "Value")
        
    def update(self):
        update_sockets(self.inputs)
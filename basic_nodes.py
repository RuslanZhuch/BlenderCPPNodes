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

    def set_id(self, node_id):
        self.bl_idname = node_id

    def set_name(self, node_name):
        self.bl_label = node_name

    def add_input_node(self, input_type, name):
        self.inputs.new(input_type, name)

    def add_output_node(self, output_type, name):
        self.outputs.new(output_type, name)

class InputScriptingNode(ScriptingTreeNodeBase):
    bl_idname = "InputScriptingNode"
    bl_label = "Input"
    num_of_links = 0

    def init(self, context):
        self.outputs.new("AUTO_SCRIPTING_SOKET", "Output 1")
        
    def update(self):
        
        sockets_linked = sum([socket.is_linked for socket in self.outputs])

        print("sockets_linked", sockets_linked, self)
        linked_sockets_diff = len(self.outputs) - sockets_linked 
        if linked_sockets_diff == 0:
            print("Need to add socket", self)
            self.outputs.new("AUTO_SCRIPTING_SOKET_WEAK", "Output")
        elif linked_sockets_diff >= 2:
            print("Need to remove socket", self)
            last_socket_id = 0
            while linked_sockets_diff > 1:
                while True:
                    if self.outputs[last_socket_id].is_linked:
                        last_socket_id -= 1
                        continue
                    self.outputs.remove(self.outputs[last_socket_id])
                    linked_sockets_diff -= 1
                    break
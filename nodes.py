import bpy
import json

from bpy.types import NodeTree, Node, NodeSocket, NodeCustomGroup, StringProperty

class ScriptingTree(NodeTree):
    bl_idname = 'ScriptingTreeType'
    bl_label = "Scripting"
    bl_icon = 'NODETREE'

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

class AddMathNode(ScriptingTreeNodeBase, Node):
    bl_idname = 'AddNodeB'
    bl_label = "AddB"

    def init(self, context):
        self.inputs.new('NodeSocketInt', "Left")
        self.inputs.new('NodeSocketFloat', "Right")
        self.outputs.new('NodeSocketFloat', "Result")

import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

class ScriptCategyryBase(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'ScriptingTreeType'

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

class NodesFactory():
    def __init__(self):
        self._nodes = []
        self._node_categories = {}
        self._node_categories_names = {}

        self.blocks_config_path = "D:\Projects\cppParser\output.json"
        self.blocks_config = json.load(open(self.blocks_config_path))
        
    def register_nodes(self):

        if self.blocks_config is None:
            return

        if len(self.blocks_config) == 0:
            return
        
        blocks_namespace = self.blocks_config[0]
        if blocks_namespace["name"] != "Blocks":
            return
        
        for block_category in blocks_namespace["members"]:
            category_name = block_category["name"]
            category_id = str.upper(category_name) + "NODES"

            if self._node_categories.get(category_id) is None:
                self._node_categories[category_id] = []
            self._node_categories_names[category_id] = category_name

            def add_node(arguments, return_data, node_id, node_name):
                print("arguments outer", arguments)
                def init(self, context):
                    print("arguments inner", arguments)
                    for argument in arguments:
                        input_data = argument["type"]
                        input_type = input_data["name"]
                        self.inputs.new(TypesMapper.type_to_socket(input_type), argument["name"] + "(" + input_type + ")")
                    return_type = return_data["name"]
                    self.outputs.new(TypesMapper.type_to_socket(return_type), "Result (" + return_type + ")")

                node_class = type("ScriptingTreeNode" + "Math" + "AddNode", (ScriptingTreeNodeBase, Node, ), {
                    "bl_idname": node_id,
                    "bl_label": node_name,
                    
                    "init": init
                })
                print("class type", type(node_class))

                return node_class

            for node_data in block_category["members"]:
                node_name = node_data["name"]
                node_id = str.upper(node_name) + "NODE"

                return_data = node_data["returnType"]
                arguments = node_data["arguments"]

                self._nodes.append(add_node(arguments, return_data, node_id, node_name))
                self._node_categories[category_id].append(NodeItem(node_id))

    def register_all(self):
        self.register_nodes()

        for n in self._nodes:
            bpy.utils.register_class(n)

        categories = []
        for category_id, category in self._node_categories.items():
            print("append", category_id, category)
            categories.append(
                ScriptCategyryBase(category_id, self._node_categories_names[category_id], items = category)
            )

        nodeitems_utils.register_node_categories('CUSTOM_NODES', categories)


    def unregister_all(self):
        nodeitems_utils.unregister_node_categories('CUSTOM_NODES')

        for n in reversed(self._nodes):
            bpy.utils.unregister_class(n)

nodes_factory = NodesFactory()

_classes = (
    ScriptingTree, 
)

def register():
    for cls in _classes:
        bpy.utils.register_class(cls)

    nodes_factory.register_all()

def unregister():

    nodes_factory.unregister_all()

    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)

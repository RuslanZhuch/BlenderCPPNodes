import bpy
import json
import os
import subprocess
from pathlib import Path

from . import basic_nodes
from . import nodes_meta

from bpy.types import NodeTree, Node, NodeSocket, NodeCustomGroup, StringProperty

import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

class ScriptCategyryBase(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'ScriptingTreeType'

class NodesFactory():
    def __init__(self):
        self._nodes = []
        self._node_categories = {}
        self._node_categories_names = {}
        self._block_configs = []
        self._nodes_meta = nodes_meta.Generator()

    def get_nodes_meta(self):
        return self._nodes_meta

    def fetch_configs(self):
        self._block_configs.clear()
        self._nodes_meta.reset()

        pathlist = Path(bpy.context.scene.cppgen.src_path + "nodes-structures").rglob('*.json')
        for path in pathlist:
            path_in_str = str(path)
            self._nodes_meta.register_include(path.stem + ".h")
            try:
                file = open(path_in_str)
                self._block_configs.append(json.load(file))
            except:
                print("Failed to load config from file", path_in_str)

    def parse_blocks(self, blocks_namespace):
        def add_node(arguments, return_data, node_id, node_name):
            def init(self, context):
                for argument in arguments:
                    input_data = argument["type"]
                    input_type = input_data["name"]
                    self.inputs.new(basic_nodes.TypesMapper.type_to_socket(input_type), argument["name"] + " (" + input_type + ")")
                return_type = return_data["name"]
                self.outputs.new(basic_nodes.TypesMapper.type_to_socket(return_type), "Result (" + return_type + ")")

            node_class = type("ScriptingTreeNode" + node_id, (basic_nodes.ScriptingTreeNodeBase, Node, ), {
                "bl_idname": node_id,
                "bl_label": node_name,
                
                "init": init
            })

            return node_class
        
        for block_group in blocks_namespace["members"]:
            block_group_type = block_group["type"]
            if block_group_type != "namespace":
                continue
            
            category_name = block_group["name"]
            category_id = str.upper(category_name) + "NODES"
            if self._node_categories.get(category_id) is None:
                self._node_categories[category_id] = []
            self._node_categories_names[category_id] = category_name
        
            for node_data in block_group["members"]:
                node_name = node_data["name"]
                node_id = str.upper(node_name) + "NODE"

                return_data = node_data["returnType"]
                arguments = node_data["arguments"]

                self._nodes.append(add_node(arguments, return_data, node_id, node_name))
                self._node_categories[category_id].append(NodeItem(node_id))

                self._nodes_meta.register_group(node_name, "Blocks::" + category_name)

    def parse_types(self, types_namespace):
        category_name = "Types"
        category_id = "TypesNODES"
        for type_category in types_namespace["members"]:
            if self._node_categories.get(category_id) is None:
                self._node_categories[category_id] = []
            self._node_categories_names[category_id] = category_name

            def add_node(outputs_data, node_id, node_name):
                def init(self, context):
                    self.inputs.new(basic_nodes.TypesMapper.type_to_socket("auto"), type_category["name"])
                    print("Outputs data", outputs_data)
                    for output_data in outputs_data:
                        output_name = output_data["name"]
                        output_type = output_data["dataType"]["name"]
                        print("Output data {} {}".format(output_name, output_type))
                        self.outputs.new(basic_nodes.TypesMapper.type_to_socket(output_type), output_name + " (" + output_type + ")")

                node_class = type("ScriptingTreeNode" + node_id, (basic_nodes.ScriptingTreeNodeBase, Node, ), {
                    "bl_idname": node_id,
                    "bl_label": node_name,
                    
                    "init": init
                })

                return node_class

            outputs_data = type_category["members"]

            node_name = type_category["name"]
            node_id = str.upper(node_name) + "NODE"

            self._nodes.append(add_node(outputs_data, node_id, node_name))
            self._node_categories[category_id].append(NodeItem(node_id))
            
            self._nodes_meta.register_group(node_name, category_name)

    def parse_namespace(self, blocks_namespace):
        if blocks_namespace["name"] == "Blocks":
            self.parse_blocks(blocks_namespace)
        elif blocks_namespace["name"] == "Types":
            self.parse_types(blocks_namespace)

    def parse_config(self, block_config):
        if len(block_config) == 0:
            return
        
        for block in block_config:
            if block["type"] == "namespace":
                self.parse_namespace(block)

    def register_nodes(self):
        parser_path = bpy.context.scene.cppgen.src_path + "genschemas.sh"
        try:
            parsed = os.system("{}".format(parser_path))
            print(parsed)
        except FileNotFoundError:
            print("(NodesFactory.register_nodes) Failed to run c++ parser: invalid path")
            return

        self.fetch_configs()

        for block_config in self._block_configs:
            self.parse_config(block_config)

        self._nodes.append(basic_nodes.InputScriptingNode)
        self._nodes.append(basic_nodes.OutputScriptingNode)

        node_meta_json = {
            "nodeGroups" : self._nodes_meta.get_node_groups()
        }

        output_path = bpy.context.scene.cppgen.src_path + "nodesOutput\\nodes_meta.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(node_meta_json, f, ensure_ascii=False, indent=4)     

    def register_all(self):
        self.register_nodes()

        print("register all nodes")
        for n in self._nodes:
            print(n)
            bpy.utils.register_class(n)

        categories = []
        for category_id, category in self._node_categories.items():
            categories.append(
                ScriptCategyryBase(category_id, self._node_categories_names[category_id], items = category)
            )
        categories.append(
            ScriptCategyryBase("ioNODES", "IO", items = [
                NodeItem("InputScriptingNode"),
                NodeItem("OutputScriptingNode"),
            ])
        )

        nodeitems_utils.register_node_categories('CUSTOM_NODES', categories)

    def unregister_all(self):
        try:
            nodeitems_utils.unregister_node_categories('CUSTOM_NODES')
        except Exception as e:
            print("Failed to unregister nodes", e)
            pass

        for n in reversed(self._nodes):
            bpy.utils.unregister_class(n)

        self._nodes.clear()
        self._node_categories.clear()
        self._node_categories_names.clear()

nodes_factory = NodesFactory()

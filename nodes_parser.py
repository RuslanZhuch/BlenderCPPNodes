import bpy
import json

import queue

def find_output_node(nodes):
    for node in nodes:
        if node.name == "Output":
            return node

    return None

def traverse_node(node, nodes_to_traverse_next, nodes_cache, node_groups):
    inputs = node.inputs
    print("Node {} has inputs {}".format(node, inputs))

    node_inputs_data, node_outputs_data = gather_node_schema(node)

    node_group = ""
    if node.name in node_groups:
        node_group = node_groups[node.name]

    node_data = {
        "id": node.bl_idname,
        "name": node.name,
        "group": node_group,
        "inputs": traverse_node_inputs(node, nodes_to_traverse_next, nodes_cache),
        "inputsSchema": node_inputs_data, 
        "outputsSchema": node_outputs_data, 
    }

    return node_data

def gather_node_schema(node):
    def gather_output_data(node):
        splitted_list = [output.name.split(' ') for output in node.outputs]
        splitted_names = [splitted[0] for splitted in splitted_list]

        splitted_types_raw = [splitted[1] if len(splitted) > 1 else "" for splitted in splitted_list]
        splitted_types = [type_raw[1:-1] if len(type_raw) > 2 else "" for type_raw in splitted_types_raw]

        return splitted_names, splitted_types
     
    output_names, output_types = gather_output_data(node)
    node_outputs_data = {
        "names": output_names,
        "types": output_types
    }

    node_inputs_data = {
        "numOfInputs": len(node.inputs)
    }

    return node_inputs_data, node_outputs_data

def traverse_node_inputs(node, nodes_to_traverse_next, nodes_cache):
    node_inputs_data = []

    for node_input in node.inputs:
        print("Process inputs:", node_input)
        print("Is linked", node_input.is_linked)
        if not node_input.is_linked:
            continue

        link = node_input.links[0]
        print("Input's link:", link)

        from_node = link.from_node
        print("From node", from_node)        
        from_output = link.from_socket
        print("From socket", from_output)

        def find_output_socket_id(node_to_find_in, socket_to_find):
            node_outputs = node_to_find_in.outputs
            #TODO: Remake it in python way 
            index = 0
            for output in node_outputs:
                if output == socket_to_find:
                    return index
                index += 1

            return -1

        from_output_index = find_output_socket_id(from_node, from_output)

        print("From socket if", from_output_index)

        node_inputs_data.append({
            "target_node_id": from_node.bl_idname,
            "target_node_name": from_node.name,
            "target_socket_id": from_output_index
        })

        already_in_list = from_node in nodes_cache
        print("Is Node already listed", already_in_list)

        if not already_in_list:
            nodes_cache.add(from_node)
            nodes_to_traverse_next.put(from_node)
            print("Added node {} to list".format(from_node))

    return node_inputs_data
    
def traverse_nodes(node_tree):
    print("-----------------Parse node tree-----------------", node_tree.name)
    nodes = node_tree.nodes

    output_node = find_output_node(nodes)
    print("Output node:", output_node)
    if output_node is None:
        return    

    nodes_to_traverse_next = queue.Queue()
    nodes_to_traverse_next.put_nowait(output_node)
    nodes_cache = set()

    json_data = {
        "version": 1,
        "name": node_tree.name,
        "data":[]
    }

    nodes_groups = []
    try:
        file = open(bpy.context.scene.cppgen.src_path + "nodesOutput//nodes_meta.json")
        nodes_meta = json.load(file)
        nodes_groups = nodes_meta["nodeGroups"]
    except:
        print("Failed to load meta file")
        return
    finally:
        file.close()

    while not nodes_to_traverse_next.empty():
        node_to_traverse = nodes_to_traverse_next.get_nowait()
        print("Node to traverse:", node_to_traverse)

        json_data["data"].append(traverse_node(node_to_traverse, nodes_to_traverse_next, nodes_cache, nodes_groups))

    output_path = bpy.context.scene.cppgen.src_path + "nodesOutput\\temp\\{}.json".format(node_tree.name)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)     

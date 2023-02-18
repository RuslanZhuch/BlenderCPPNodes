import bpy
import json

import queue

def find_output_node(nodes):
    for node in nodes:
        if node.name == "Output":
            return node

    return None

def traverse_node_inputs(node, nodes_to_traverse_next, nodes_cache):
    inputs = node.inputs
    print("Node {} has inputs {}".format(node, inputs))

    node_data = {
        "id": node.bl_idname,
        "name": node.name,
        "inputs": []
    }

    for node_input in inputs:
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

        node_data["inputs"].append({
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

    return node_data
    
def traverse_nodes(node_group):
    nodes = node_group.nodes

    output_node = find_output_node(nodes)
    print("Output node:", output_node)
    if output_node is None:
        return    

    nodes_to_traverse_next = queue.Queue()
    nodes_to_traverse_next.put_nowait(output_node)
    nodes_cache = set()

    json_data = {
        "version": 1,
        "data":[]
    }

    while not nodes_to_traverse_next.empty():
        node_to_traverse = nodes_to_traverse_next.get_nowait()
        print("Node to traverse:", node_to_traverse)

        json_data["data"].append(traverse_node_inputs(node_to_traverse, nodes_to_traverse_next, nodes_cache))

        output_path = bpy.context.scene.cppgen.src_path + "temp\\parsed_nodes.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)     

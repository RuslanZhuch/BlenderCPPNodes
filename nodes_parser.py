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
        print("From щгезге", from_output)

        already_in_list = from_node in nodes_cache
        print("Is Node already listed", already_in_list)

        if not already_in_list:
            nodes_cache.add(from_node)
            nodes_to_traverse_next.put(from_node)
            print("Added node {} to list".format(from_node))
    
def traverse_nodes(node_group):
    nodes = node_group.nodes

    output_node = find_output_node(nodes)
    print("Output node:", output_node)
    if output_node is None:
        return    

    nodes_to_traverse_next = queue.Queue()
    nodes_to_traverse_next.put_nowait(output_node)
    nodes_cache = set()

    while not nodes_to_traverse_next.empty():
        node_to_traverse = nodes_to_traverse_next.get_nowait()
        print("Node to traverse:", node_to_traverse)

        traverse_node_inputs(node_to_traverse, nodes_to_traverse_next, nodes_cache)

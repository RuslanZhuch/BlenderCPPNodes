bl_info = {
    "name": "cppGen",
    "blender": (3, 4, 1),
    "category": "Rising",
}

import bpy

import os
import sys

from . import nodes_tree, node_sockets, basic_nodes, nodes_generator, gui

print("reloaded")

_modules = (
    node_sockets,
    nodes_tree,
    basic_nodes,
    nodes_generator,
    gui,
)

def register():
    
    import importlib
    for mdl in _modules:
        importlib.reload(mdl)
        
    for mdl in _modules:
        if "register" in dir(mdl):
            mdl.register()
        
def unregister():
    for mdl in reversed(_modules):
        if "unregister" in dir(mdl):
            mdl.unregister()
        
if __name__ == '__main__':
    register()
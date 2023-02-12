bl_info = {
    "name": "cppScripts",
    "blender": (3, 4, 1),
    "category": "Rising",
}

import bpy

import os
import sys

from . import nodes, node_sockets, nodes_group

print("reloaded")

_modules = (
    nodes_group,
    node_sockets,
    nodes,
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
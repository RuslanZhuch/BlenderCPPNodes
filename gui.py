import bpy
from bpy.types import NodeTree, Node, NodeSocket, PropertyGroup
from bpy.props import StringProperty, BoolProperty, EnumProperty, IntProperty, CollectionProperty, FloatProperty, PointerProperty

from . import nodes_generator
from . import nodes_parser

from bpy.app.handlers import persistent
from pathlib import Path

directory_subtype = 'DIR_PATH' if bpy.app.version != (3,1,0) else 'NONE' # https://developer.blender.org/T96691
class CommonProps(PropertyGroup):
    src_path : StringProperty(name="source path", description="root folder with header-parser.exe", subtype=directory_subtype)

class CPPGEN_PT_ScriptingPanel(bpy.types.Panel):
    bl_label = "Scripting panel"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        obj = context.object

        row = layout.row()
        row.operator("node.cppgen_generate_nodes")

        row = layout.row()
        row.prop(scene.cppgen, "src_path")

        row = layout.row()
        row.operator("node.cppgen_parse_nodes")

class CPPGEN_OT_GenerateNodes(bpy.types.Operator):
    bl_label = "Generate nodes"
    bl_idname = "node.cppgen_generate_nodes"

    def execute(self, context):
        nodes_generator.nodes_factory.unregister_all()
        nodes_generator.nodes_factory.register_all()

        return {'FINISHED'}

class CPPGEN_OT_ParseNodes(bpy.types.Operator):
    bl_label = "Parse nodes"
    bl_idname = "node.cppgen_parse_nodes"

    def execute(self, context):
        print("--------------- BEGIN PARSING ---------------")
        if bpy.context.scene.cppgen.src_path == "":
            print("(node.cppgen_parse_nodes) Source path is empty")
            return {'FINISHED'}
        temp_path = bpy.context.scene.cppgen.src_path + "nodesOutput\\temp\\"
        [f.unlink() for f in Path(temp_path).glob("*") if f.is_file()] 
        for node_group in bpy.data.node_groups:
            if node_group.bl_idname != "ScriptingTreeType":
                continue
            nodes_parser.traverse_nodes(node_group)
        print("--------------- PARSING COMPLETE ---------------")
        return {'FINISHED'}

_classes = (
    CPPGEN_OT_GenerateNodes,
    CPPGEN_PT_ScriptingPanel,
    CPPGEN_OT_ParseNodes,
    CommonProps,
)

@persistent
def load_handler(dummy):
    nodes_generator.nodes_factory.unregister_all()
    nodes_generator.nodes_factory.register_all()

def register():
    for cls in _classes:
        bpy.utils.register_class(cls)

    def make_pointer(prop_type):
        return PointerProperty(name="settings",type=prop_type)

    bpy.types.Scene.cppgen = make_pointer(CommonProps)
    bpy.app.handlers.load_post.append(load_handler)

def unregister():
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)
        
    del bpy.types.Scene.cppgen
    bpy.app.handlers.load_post.remove(load_handler)
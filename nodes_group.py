import bpy
from bpy.types import NodeTree, Node, NodeSocket

class SriptingPanel(bpy.types.Panel):
    bl_label = "Scripting panel"
    bl_idname = "NODE_PT_SCRIPTING_PANEL"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.operator("node.group_script_nodes")

class NODE_OT_TEST(bpy.types.Operator):
    bl_label = "Group script nodes"
    bl_idname = "node.group_script_nodes"

    @staticmethod
    def create_group(context, operator, group_name):
        new_group = bpy.data.node_groups.new(group_name, 'ScriptingTreeType')
        return new_group

    def execute(self, context):
        print("Executed")

        new_group = self.create_group(self, context, "Testing")
        group_node = context.space_data.edit_tree.nodes.new('NodeCustomGroup')
        group_node.node_tree = bpy.data.node_groups["Testing"]

        return {'FINISHED'}

_classes = (
    SriptingPanel,
    NODE_OT_TEST,
)

def register():
    for cls in _classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)
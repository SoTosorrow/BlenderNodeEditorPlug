import bpy
import time
from .node_system import *

class PearlExecOperator(bpy.types.Operator):
    bl_idname = "pearl.node_exec"
    bl_label = "Apply"

    @classmethod
    def poll(cls, context):
        return getattr(context.space_data, 'tree_type', 'PearlNodeTree') == 'PearlNodeTree'

    def execute(self, context):
        self.executeNodeTree(context)
        return {'FINISHED'}

    def executeNodeTree(self,context):
        # 当前树 ： context.space_data.edit_tree

        start = time.time()

        current_tree = context.space_data.edit_tree
        current_tree.executeNodes()

        end = time.time()
        total_time = (end - start)
        print("------------------")
        print("nodes number: ",len(current_tree.nodes))
        self.report({"INFO"},"finish execute node trees: "+str(total_time)+'s')

        # 单纯传输数据 2000 节点要6.7s
        # 601 节点要 1.8s
        # 10节点要 0.0271s


       




def draw_menu(self, context):
    if context.area.ui_type == 'PearlNodeTree':
        self.layout.separator()
        self.layout.operator(PearlExecOperator.bl_idname, text="Pearl Node Exec")

classes = [
    PearlExecOperator,

]

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.NODE_MT_context_menu.append(draw_menu)

def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)
    bpy.types.NODE_MT_context_menu.remove(draw_menu)

import bpy
from .node_system import *
from .node_socket import *

'''
    NodeSocket_Int,
    NodeSocket_Float,
    NodeSocket_Vector,
    NodeSocket_String,

'''
class Node_OutputFloat(PearlNode):
    bl_idname = "Node_OutputFloat"
    bl_label = "Float Output"

    node_value : bpy.props.FloatProperty(name='Input', default=0.0)

    def init(self, context):
        self.inputs.new(NodeSocket_Float.bl_idname, name="input")
    
    def draw_buttons(self,context,layout):
        layout.prop(self, 'node_value', text='')  

    def process(self):
        print("process: ",self.name)
        if self.tree!=None:
            nodeValueDict = self.tree.tree_values[self.name]
            self.node_value = nodeValueDict[self.inputs[0].name]

        


class Node_OutputVector(PearlNode):
    bl_idname = "Node_OutputVector"
    bl_label = "Vector Output"

    node_value : bpy.props.FloatVectorProperty(name='Vector', default=(0, 0, 0))

    def init(self,context):
        self.inputs.new(NodeSocket_Vector.bl_idname,name="input")

    def draw_buttons(self,context,layout):
        col = layout.column(align=1)
        col.prop(self, 'node_value', text='')

    def process(self):
        self.node_value = self.inputs[0].socket_value







classes = [
    Node_OutputFloat,
    Node_OutputVector,

]


def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)

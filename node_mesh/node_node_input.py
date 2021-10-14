import bpy
from ..node_system import *
from ..node_socket import *
import mathutils

'''
    NodeSocket_Int,
    NodeSocket_Float,
    NodeSocket_Vector,
    NodeSocket_String,

'''
class Node_InputFloat(PearlNode):
    bl_idname = "Node_InputFloat"
    bl_label = "Float Input"

    node_value : bpy.props.FloatProperty(name='Input', default=0.0)

    def init(self, context):
        self.outputs.new(NodeSocket_Float.bl_idname, name="output")
    
    def draw_buttons(self,context,layout):
        layout.prop(self, 'node_value', text='')  

    def process(self):
        print("process: ",self.name)
        if self.tree!=None:
            nodeValueDict = self.tree.tree_values[self.name]
            nodeValueDict[self.outputs[0].name] = self.node_value
        return True

        


class Node_InputVector(PearlNode):
    bl_idname = "Node_InputVector"
    bl_label = "Vector Input"

    node_value : bpy.props.FloatVectorProperty(name='Vector', default=(0, 0, 0))

    def init(self,context):
        self.outputs.new(NodeSocket_Vector.bl_idname,name="output")

    def draw_buttons(self,context,layout):
        col = layout.column(align=1)
        col.prop(self, 'node_value', text='')

    def process(self):
        print("process: ",self.name)
        nodeValueDict = self.tree.tree_values[self.name]

        vec3 = mathutils.Vector(self.node_value)
        nodeValueDict[self.outputs[0].name] = vec3
        return True




classes = [
    Node_InputFloat,
    Node_InputVector,

]


def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)

import bpy
from .node_system import *
from .node_socket import *
import mathutils

'''
    NodeSocket_Int,
    NodeSocket_Float,
    NodeSocket_Vector,
    NodeSocket_String,

'''
class Node_Float2Vector(PearlNode):
    bl_idname = "Node_Float2Vector"
    bl_label = "Float2Vector"

    node_value : bpy.props.FloatVectorProperty(name='Vector', default=(0, 0, 0))


    def init(self, context):
        self.inputs.new(NodeSocket_Float.bl_idname, name="input1")
        self.inputs.new(NodeSocket_Float.bl_idname, name="input2")
        self.inputs.new(NodeSocket_Float.bl_idname, name="input3")
        self.outputs.new(NodeSocket_Vector.bl_idname, name="output")

    
    def draw_buttons(self,context,layout):
        col = layout.column(align=1)
        col.prop(self, 'node_value', text='')

    def process(self):
        print("process: ",self.name)
        nodeValueDict = self.tree.tree_values[self.name]
        # vec3[] = float
        nodeValueDict[self.outputs[0].name] = mathutils.Vector()
        nodeValueDict[self.outputs[0].name][0] = nodeValueDict[self.inputs[0].name] if nodeValueDict[self.inputs[0].name] else 0
        nodeValueDict[self.outputs[0].name][1] = nodeValueDict[self.inputs[1].name] if nodeValueDict[self.inputs[1].name] else 0
        nodeValueDict[self.outputs[0].name][2] = nodeValueDict[self.inputs[2].name] if nodeValueDict[self.inputs[2].name] else 0
        # FloatVectorProperty = mathutils.Vector
        self.node_value = nodeValueDict[self.outputs[0].name]
        return True


        


class Node_Vector2Float(PearlNode):
    bl_idname = "Node_Vector2Float"
    bl_label = "Vector2Float"

    node_value : bpy.props.FloatVectorProperty(name='Vector', default=(0, 0, 0))

    def init(self,context):
        self.inputs.new(NodeSocket_Vector.bl_idname, name="input")
        self.outputs.new(NodeSocket_Float.bl_idname, name="output1")
        self.outputs.new(NodeSocket_Float.bl_idname, name="output2")
        self.outputs.new(NodeSocket_Float.bl_idname, name="output3")

    def draw_buttons(self,context,layout):
        col = layout.column(align=1)
        col.prop(self, 'node_value', text='')

    def process(self):
        print("process: ",self.name)
        nodeValueDict = self.tree.tree_values[self.name]
        # vec3[] = float
        if self.inputs[0].is_linked:
            nodeValueDict[self.outputs[0].name] = nodeValueDict[self.inputs[0].name][0]
            nodeValueDict[self.outputs[1].name] = nodeValueDict[self.inputs[0].name][1]
            nodeValueDict[self.outputs[2].name] = nodeValueDict[self.inputs[0].name][2]
            self.node_value = nodeValueDict[self.inputs[0].name]
        else:
            nodeValueDict[self.outputs[0].name] = self.node_value[0]
            nodeValueDict[self.outputs[1].name] = self.node_value[1]
            nodeValueDict[self.outputs[2].name] = self.node_value[2]
        return True




classes = [
    Node_Float2Vector,
    Node_Vector2Float,

]


def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)

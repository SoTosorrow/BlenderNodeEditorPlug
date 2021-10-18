import bpy
import bmesh
import random

from bpy.ops import mesh
from ..node_system import *
from ..node_socket import *


# 输入顶点序列，随机化其位置
class Node_PointRandomLocation(PearlNode):
    bl_idname = "Node_PointRandomLocation"
    bl_label = "PointRandomLocation"

    node_value : bpy.props.IntProperty(name='seed', default=1)
    node_value2 : bpy.props.FloatProperty(name='scale', default=1)
    
    def draw_buttons(self,context,layout):
        col = layout.column(align=1)
        col.prop(self, 'node_value', text='') 
        col.prop(self, 'node_value2', text='') 

    def process(self):
        print("process: ",self.name)
        nodeValueDict = self.tree.tree_values[self.name]

        def randomPoint(point,scale):
            vec3 = point.copy()
            vec3[0] = random.random() * scale
            vec3[1] = random.random() * scale
            vec3[2] = random.random() * scale
            return vec3

        random.seed(self.node_value)
        verts_list = nodeValueDict[self.inputs[0].name]
        nodeValueDict[self.outputs[0].name] = [randomPoint(vec3,self.node_value2) for vec3 in verts_list]
        
    def init(self, context):
        self.inputs.new(NodeSocket_Verts.bl_idname,name="verts")
        self.outputs.new(NodeSocket_Verts.bl_idname,name='verts')

    # 必须连接vert
    def is_prepared(self):
        if not self.inputs[0].is_linked:
            return False
        return self.link_num == 0


# 输入顶点序列，生成网格实例
# 撤销会导致崩溃
class Node_PointGenerateObj(PearlNode):
    bl_idname = "Node_PointGenerateObj"
    bl_label = "PointGenerateObj"

    node_value : bpy.props.StringProperty(name='obj', default="")
    count = 0
    
    def draw_buttons(self,context,layout):
        col = layout.column(align=1)
        col.prop_search(self, 'node_value', context.scene, "objects", text='Object', icon = "OBJECT_DATA")


    def process(self):
        print("process: ",self.name)
        nodeValueDict = self.tree.tree_values[self.name]

        def generateObj(pos):
            obj = bpy.data.objects.new('obj'+str(self.count),mesh)
            obj.location = pos
            bpy.data.collections[0].objects.link(obj)
            self.count+=1

        self.node_value = nodeValueDict[self.inputs[1].name]
        mesh = bpy.data.objects[self.node_value].data
        random.seed(self.node_value)
        verts_list = nodeValueDict[self.inputs[0].name]
        [generateObj(vec3) for vec3 in verts_list]

        bpy.data.objects[self.node_value].select_set(True)
        

    def init(self, context):
        self.inputs.new(NodeSocket_Verts.bl_idname,name="verts")
        self.inputs.new(NodeSocket_String.bl_idname,name="object")

    # 必须连接vert
    def is_prepared(self):
        if not self.inputs[0].is_linked:
            return False
        return self.link_num == 0


classes = [
    Node_PointRandomLocation,
    Node_PointGenerateObj,

]


def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)





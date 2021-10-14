import bpy
import bmesh
import random
import time
import numpy as np
from ..node_system import *
from ..node_socket import *

'''
    NodeSocket_Int,
    NodeSocket_Float,
    NodeSocket_Vector,
    NodeSocket_String,

    NodeSocket_Verts,
    NodeSocket_Edges,
    NodeSocket_Faces,
    NodeSocket_Object,

'''

def bmesh_verts_to_numpy(bm):
    arr = [x.co for x in bm.verts]
    if len(arr)==0:
        return np.zeros((0,3),dtype=np.float32)
    return np.array(arr,dtype=np.float32)

def bmesh_faces_to_numpy(bm):
    arr = [[y.index for y in x.verts] for x in bm.faces]
    if len(arr)==0:
        return np.zeros((0,3),dtype=np.int32)
    return np.array(arr,dtype=np.int32)


def new_mesh(name, verts=None, edges=None, faces=None):
    if name in bpy.data.meshes:
        bpy.data.meshes.remove(bpy.data.meshes[name])
    mesh = bpy.data.meshes.new(name)
    verts = verts.tolist() if verts is not None else []
    edges = edges.tolist() if edges is not None else []
    faces = faces.tolist() if faces is not None else []
    mesh.from_pydata(verts, edges, faces)
    return mesh

def new_object(name, mesh):
    if name in bpy.data.objects:
        bpy.data.meshes.remove(bpy.data.objects[name])
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    return obj


class Node_InputObject(PearlNode):
    bl_idname = "Node_InputObject"
    bl_label = "Object Input"    

    node_value : bpy.props.StringProperty(name='object', default='')

    def init(self,context):
        self.outputs.new(NodeSocket_String.bl_idname,name="output")

    def draw_buttons(self,context,layout):
        col = layout.column(align=1)
        col.prop_search(self, 'node_value', context.scene, "objects", text='Object', icon = "OBJECT_DATA")

    def process(self):
        print("process: ",self.name)
        if self.tree!=None:
            nodeValueDict = self.tree.tree_values[self.name]
            nodeValueDict[self.outputs[0].name] = self.node_value
        return True


class Node_Object2BMesh(PearlNode):
    bl_idname = "Node_Object2BMesh"
    bl_label = "Object2BMesh"

    
    def process(self):
        print("process: ",self.name)
        nodeValueDict = self.tree.tree_values[self.name]
        # 清空缓冲
        # not need anymore

        # 获取物体bmesh
        bm = bmesh.new()
        obj = bpy.data.objects[nodeValueDict[self.inputs[0].name]]
        bm.from_mesh(obj.data)

        verts_list = []
        edges_list = []
        faces_list = []

        # gc.disable()
        start = time.time()
        for v in bm.verts:
            verts_list.append([i for i in v.co])
        for e in bm.edges:
            edges_list.append([i.index for i in e.verts])
        for f in bm.faces:
            faces_list.append([i.index for i in f.verts])
        end = time.time()
        print("mesh data tolist time:" ,end-start)
        # gc.enable()

        ls1 = time.time()
        if self.tree!=None:
            nodeValueDict[self.outputs[0].name] = {}
            nodeValueDict[self.outputs[0].name]=verts_list
            nodeValueDict[self.outputs[1].name]=edges_list
            nodeValueDict[self.outputs[2].name]=faces_list
        ls2 = time.time()
        print("data to dict:",ls2-ls1)
        # print(nodeValueDict[self.outputs[0].name])
        # print(nodeValueDict[self.outputs[1].name])
        # print(nodeValueDict[self.outputs[2].name])
        bm.free()

          
    def init(self, context):
        self.inputs.new(NodeSocket_String.bl_idname,name="input")
        self.outputs.new(NodeSocket_Verts.bl_idname,name="verts")
        self.outputs.new(NodeSocket_Edges.bl_idname,name="edges")
        self.outputs.new(NodeSocket_Faces.bl_idname,name="faces")





class Node_MeshAppoint(PearlNode):
    bl_idname = "Node_MeshAppoint"
    bl_label = "MeshAppoint"

    node_value : bpy.props.StringProperty(name='object', default='')
    
    def draw_buttons(self,context,layout):
        col = layout.column(align=1)
        col.prop_search(self, 'node_value', context.scene, "objects", text='Object', icon = "OBJECT_DATA")

    def process(self):
        print("process: ",self.name)
        nodeValueDict = self.tree.tree_values[self.name]
        bm = bmesh.new()


        start = time.time()

        verts_list = nodeValueDict[self.inputs[0].name]
        for v in range(len(verts_list)):
            vertex = bm.verts.new()
            vertex.co = [i for i in verts_list[v]]
            vertex.index = v
        bm.verts.ensure_lookup_table()

        if self.inputs[1].is_linked:
            edges_list = nodeValueDict[self.inputs[1].name]
            for e in range(len(edges_list)):
                l = [i for i in edges_list[e]]
                bm.edges.new([bm.verts[l[0]],bm.verts[l[1]]])
 
        if self.inputs[2].is_linked:
            faces_list = nodeValueDict[self.inputs[2].name]
            for f in range(len(faces_list)):
                l = [i for i in faces_list[f]]
                f_list = []
                for i in l:
                    f_list.append(bm.verts[i])
                bm.faces.new(f_list)

        end = time.time()
        print("mesh data appoint time:" ,end-start)



        # 采用bmesh方法不会自动刷新物体显示，使用select_all()来刷新一下
        obj = bpy.data.objects[self.node_value]
        bm.to_mesh(obj.data)
        bm.free()
        bpy.ops.object.select_all()
        nodeValueDict[self.outputs[0].name] = self.node_value

     # 输入点边面数据
    def init(self, context):
        self.inputs.new(NodeSocket_Verts.bl_idname,name="verts")
        self.inputs.new(NodeSocket_Edges.bl_idname,name="edges")
        self.inputs.new(NodeSocket_Faces.bl_idname,name="faces")
        self.outputs.new(NodeSocket_String.bl_idname,name='object')
    # 必须连接vert
    def is_prepared(self):
        if not self.inputs[0].is_linked:
            return False
        return self.link_num == 0



class Node_PointRandomMove(PearlNode):
    bl_idname = "Node_PointRandomMove"
    bl_label = "PointRandomMove"

    node_value : bpy.props.StringProperty(name='object', default='')
    
    def draw_buttons(self,context,layout):
        col = layout.column(align=1)
        col.prop_search(self, 'node_value', context.scene, "objects", text='Object', icon = "OBJECT_DATA")

    def process(self):
        print("process: ",self.name)
        nodeValueDict = self.tree.tree_values[self.name]
        bm = bmesh.new()


        verts_list = nodeValueDict[self.inputs[0].name]
        for v in range(len(verts_list)):
            vertex = bm.verts.new()
            vertex.co = [i for i in verts_list[v]]
            vertex.index = v
        bm.verts.ensure_lookup_table()

        for v in bm.verts:
            v.co.x = random.random()*2
            v.co.y = random.random()*2
            v.co.z = random.random()*2
    
        # 采用bmesh方法不会自动刷新物体显示，使用select_all()来刷新一下
        obj = bpy.data.objects[self.node_value]
        bm.to_mesh(obj.data)
        bm.free()
        # 找到更好的刷新方法
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.select_all(action='DESELECT')
        nodeValueDict[self.outputs[0].name] = self.node_value

     # 输入点边面数据
    def init(self, context):
        self.inputs.new(NodeSocket_Verts.bl_idname,name="verts")
        self.outputs.new(NodeSocket_String.bl_idname,name='object')

    # 必须连接vert
    def is_prepared(self):
        if not self.inputs[0].is_linked:
            return False
        return self.link_num == 0



classes = [
    Node_InputObject,
    Node_Object2BMesh,
    Node_MeshAppoint,
    Node_PointRandomMove,



]


def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)




'''



class Node_MeshAppoint(PearlNode):
    bl_idname = "Node_MeshAppoint"
    bl_label = "MeshAppoint"

    node_value : bpy.props.StringProperty(name='object', default='')
    
    def draw_buttons(self,context,layout):
        col = layout.column(align=1)
        col.prop_search(self, 'node_value', context.scene, "objects", text='Object', icon = "OBJECT_DATA")

    def process(self):
        # 清空缓冲   话说为啥会保留了数据
        from_obj_name = self.inputs[0].socket_value
        to_obj_name = self.node_value

        # 进入编辑模式
        from_obj = bpy.data.objects[from_obj_name]
        from_obj.select_set(True)
        to_obj = bpy.data.objects[to_obj_name]
        to_obj.select_set(True)
        bpy.ops.object.mode_set(mode="EDIT")

        # 获取物体bmesh
        from_obj_bm = bmesh.from_edit_mesh(from_obj.data)
        to_obj_bm = bmesh.from_edit_mesh(to_obj.data)
        to_obj_bm = from_obj_bm.copy()

# why update failed?
        # bmesh.update_edit_mesh(to_obj.data, loop_triangles=True)
        bpy.ops.object.mode_set(mode='OBJECT')
        to_obj_bm.to_mesh(to_obj.data)

        # bm2 = bmesh.new()
        # bm2.from_mesh
        # 回到物体模式
        bpy.ops.object.select_all(False)
          
    def init(self, context):
        self.inputs.new(NodeSocket_String.bl_idname,name="input")


'''

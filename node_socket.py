import bmesh
import time
import bpy
from .node_system import *


# TODO 规范化socket和tree_values数据类型


color_dark = 0.39, 0.39, 0.39
color_gray = 0.63, 0.63, 0.63
color_blue = 0.39, 0.39, 0.78
color_green = 0.39, 0.78, 0.39
color_magenta = 0.78, 0.16, 0.78
color_red = 0.78, 0.39, 0.39
color_yellow = 0.78, 0.78, 0.16
color_cyan = 0.16, 0.78, 0.78



class NodeSocket_Int(PearlNodeSocket):
    bl_idname = 'NodeSocket_Int'
    bl_label = 'NodeSocket_Int'

    socket_color = (0.45, 0.45, 0.45, 1.0)
    socket_value : bpy.props.StringProperty()

class NodeSocket_Float(PearlNodeSocket):
    bl_idname = 'NodeSocket_Float'
    bl_label = 'NodeSocket_Float'

    socket_color = (0.3, 1.0, 0.8, 1.0)
    socket_value : bpy.props.StringProperty()
    


class NodeSocket_Vector(PearlNodeSocket):
    bl_idname = 'NodeSocket_Vector'
    bl_label = 'NodeSocket_Vector'

    socket_color = (1.0, 0.4, 0.2, 1.0)
    socket_value : bpy.props.StringProperty()


class NodeSocket_String(PearlNodeSocket):
    bl_idname = 'NodeSocket_String'
    bl_label = 'NodeSocket_String'

    socket_color = (0.2, 0.7, 1.0, 1)
    socket_value : bpy.props.StringProperty(default='')



class NodeSocket_Verts(PearlNodeSocket):
    bl_idname = 'NodeSocket_Verts'
    bl_label = 'NodeSocket_Verts'

    socket_color = (0.2, 0.7, 1.0, 1)
    socket_value : bpy.props.StringProperty(default='')
class NodeSocket_Edges(PearlNodeSocket):
    bl_idname = 'NodeSocket_Edges'
    bl_label = 'NodeSocket_Edges'

    socket_color = (0.2, 0.7, 1.0, 1)
    socket_value : bpy.props.StringProperty(default='')
class NodeSocket_Faces(PearlNodeSocket):
    bl_idname = 'NodeSocket_Faces'
    bl_label = 'NodeSocket_Faces'

    socket_color = (0.2, 0.7, 1.0, 1)
    socket_value : bpy.props.StringProperty(default='')






classes = [
    NodeSocket_Int,
    NodeSocket_Float,
    NodeSocket_Vector,
    NodeSocket_String,

    NodeSocket_Verts,
    NodeSocket_Edges,
    NodeSocket_Faces
    
]

# register -------
def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)
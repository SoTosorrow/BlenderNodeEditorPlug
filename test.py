# python函数传参是按值还是按引用

# 新的尝试将所有数据储存在nodedtree中，socketvalue只传递节点name，nodetree的字典的key也是节点那么，value为具体储存的值

'''
node-name{
    input-socket-name:value
    output-socket-name:value
}
node-name{
    input-socket-index:value
    output-socket-index:value
}


采用socket name作为key之后，socketvalue似乎没有用了
addExecuteNodes 中的遍历socket似乎也不需要了


TODO:!!!!!
注意！bmesh.loops是循环边的引用
对于顶点来说通过
bm.verts[10].link_loops[3].link_loop_next.vert
的方式可以循环它的循环边和点和面
相邻点和边可以通过link_edges找到
所以需要设计一个类似bmesh的类来储存这些，或者自己建立一个边表
但还需要搞明白loop的设计，与edge区别

好像不是循环边，而是围绕某个面的循环？
是某个面的循环，该顶点连着几个面，就有几个loop
loop可能是按建立顺序来的

TODO:优化： numpy 代替 list


class NewNode(PearlNode):
    bl_idname = "NewNode"
    bl_label = "NewNode"

    # 节点内部值
    node_value : bpy.props.FloatProperty(name='Input', default=0.0)

    # 初始化输入输出
    def init(self, context):
        self.outputs.new(NodeSocket_Float.bl_idname, name="output")
    
    # UI
    def draw_buttons(self,context,layout):
        layout.prop(self, 'node_value', text='')  

    # 节点逻辑
    def process(self):
        print("process: ",self.name)
        
        nodeValueDict = self.tree.tree_values[self.name]
        nodeValueDict[self.outputs[0].name] = self.node_value
        return True


'''



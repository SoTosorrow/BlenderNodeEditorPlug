# NodeEditor
NodeEditor addon for blender  
Reference @atticus-lv  
Will re-write to build model-editor  



## Show

![1](./doc/1.png)



![2](./doc/2.png)



## Current

* 基本框架：自定义的tree-node-socket、tree中的node与socket采用字典查询、基于socket入度的拓扑排序

* 浮点数的输入输出与运算

* Vector的输入输出





## TODO

* 增加更多的节点

* 建模系统、颜色系统

* socket与节点内置值的联动

* socket的节点内值缺省

* 更好的UI和交互

* 节点的UI-update和process-Update

* 优化socket_values的参数传递 与 key

* 节点执行后数据结果的自动刷新问题

* 将入度判断从socket数量的prepare_num改为input-link的num+必须连接的函数判断，link_num为0时执行，会使得没有任何连接的节点执行，prepare函数能否保证不会出问题？检查（已更新，待检查）

* 封装string2list与list2string

* 封装init文件自动加载路径下模块（已完成）

* 让process返回True/False，确定节点是否完成计算，以便决定是否执行transfer

* 如何转递物体信息而不是像现在这样传递object-string，定义mesh用来赋值？要做到连接modifier节点则有相应的修改器，断开节点修改器也没有，或者一直储存一个隐式的object或者mesh，而且这个mesh的修改器不能一直叠加。。。。。反正需要思考很多

* 隐式mesh-object系列虽然能够独立的产生新obj，但是build之后的所有操作本质还是堆栈式的，需要更改，一个方法是每个节点都产生独立的obj，比如每个节点先进行一个new object(input.name+self.name)，但是这种方式显然不是最佳，并且会产生很多冗余，需要思考更好的方式

* ！！！十五万点的物体传递点线面到另一个物体需要221s，性能太低，应该学习zeno转到c++还是？zenoblend是如何储存socket数据的？。检测：append有些慢，但主要性能瓶颈在list2string

  



## Large Change

* 原来socket父类内置有被继承的socket_value，但是由于子类数据类型的变化，父类中的socket_value已经删除，所有的子类必须自己定义socket_value才能满足transfer 传递socket_value的需求（已弃用）
* 原来使用原生list类型用于存储bmesh的点边面数据，但是存在覆盖的问题无法解决，采用转换StringProperty代替



## Develop Need

fake-bpy-module  
Blender Development  



## Reference

Blender/3.0/scripts/templates_py  
https://gitlab.com/AquaticNightmare/rigging_nodes  
https://github.com/atticus-lv/simple_node_tree  
https://github.com/aachman98/Sorcar  
https://github.com/nortikin/sverchok  




## notice

建立object需要mesh，删除object时不会删除mesh,需要清理未使用数据clean  


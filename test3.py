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

'''
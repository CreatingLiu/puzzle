from tkinter.constants import NO


def hash(node):
    """
    获取节点的特征值，用进制方式计算
    """
    h=0
    for i in range(len(node.data)):
        h += node.data[i]*(len(node.data)**i) #进制得到特征值h
    return h

class Node:
    """
    节点的结构
    """
    args = {
        "shape": (3, 3)
    }
    def __init__(self, data,father=None):
        self.data=data #数据
        self.father=father #父节点
        self.shape=self.args["shape"] #规模
        self.hash=hash(self) #特征值
        self.layer=self.father.layer + 1 if self.father else 0

    def __eq__(self, value):
        """
        重写相等运算，支持节点间比较
        """
        return self.hash == value.hash

    def convertPos(self, i):
        """
        坐标和数组索引间转换
        """
        if type(i) == int:
            return i // self.shape[1], i % self.shape[1]
        else:
            return int(i[0] * self.shape[1] + i[1])
    

    def spacePos(self):
        """
        获取空格位置
        """
        return self.data.index(0)

    def swap(self,index1,index2):
        """
        交换两个位置的数，返回副本
        """
        newData = self.data.copy()
        newData[index1], newData[index2] = newData[index2], newData[index1]
        return newData

    def extend(self): 
        """
        节点扩展
        """
        index = self.spacePos()
        position = self.convertPos(index)
        children = []
        if position[0] > 0:  #上移
            data = self.swap(index,self.convertPos((position[0]-1,position[1])))
            children.append(Node(data,self))
        if position[0] < self.shape[0]-1: #下移
            data = self.swap(index,self.convertPos((position[0]+1,position[1])))
            children.append(Node(data,self))
        if position[1] > 0:  #左移
            data = self.swap(index,self.convertPos((position[0],position[1]-1)))
            children.append(Node(data,self))
        if position[1] < self.shape[1]-1:  #右移
            data = self.swap(index,self.convertPos((position[0],position[1]+1)))
            children.append(Node(data,self))
        return children

def tableToList(table):
    """
    从二维数组转到一维数组
    """
    return sum(table, [])

def listToTable(dataList, shape):
    """
    从一维数组转到二维数组
    """
    table = []
    for i in range(shape[0]):
        table.append(dataList[i * shape[1] : (i + 1) * shape[1]])
    return table
    
def getSolvePath(targetNode : Node):
    """
    寻找目标节点的路径
    """
    path = []
    while targetNode:
        path.append(listToTable(targetNode.data, targetNode.shape))
        targetNode = targetNode.father
    path.reverse() #倒置
    return path



        
       



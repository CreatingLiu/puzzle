import heapq
from base import Node

class NodeList:
    def __init__(self):
        self.map={}  #存放特征值和节点，快速找到
        self.heap=[]  #存放结点并排序

    def __contains__(self,node):
        return node.hash in self.map

    def __len__(self):
        return len(self.heap)

    def append(self,node):
        self.map[node.hash]=node
        heapq.heappush(self.heap,node)

    def popMin(self):
        node = heapq.heappop(self.heap)  #输出最小的代价节点
        del self.map[node.hash]  #从map中删除最小节点
        return node

    def setMin(self, node, key="fn"):
        existence = self.map[node.hash]
        if getattr(node, key) < getattr(existence, key):
            self.map[node.hash]=node
            self.heap[self.heap.index(existence)] = node
            heapq.heapify(self.heap)

def gn(node):
    return node.layer

def hn(node: Node,target: Node):
    """
    曼哈顿距离
    """
    if target is None:
        return int("Inf")
    s=0
    for i in range(len(node.data)):
        a = node.convertPos(i) #目前状态的坐标
        b = node.convertPos(target.data.index(node.data[i]))  #目标状态的坐标
        s += abs(b[0]-a[0])+abs(b[1]-a[1])
    return s


def AStar(current,target):
    open=NodeList()
    close=NodeList()
    open.append(current)
    while len(open)>0:
        node=open.popMin()
        close.append(node)
        if node == target:
            return {
                "targetNode": node,
                "layer": node.layer,
                "step": len(close),
                "hn": node.hn,
                "gn": node.gn,
                "fn": node.fn
            }
        else:
            childList=node.extend()
            for child in childList:
                if child in close:
                    continue
                elif child in open:
                    open.setMin(child)
                else:
                    open.append(child)
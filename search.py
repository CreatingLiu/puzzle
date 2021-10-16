from copy import deepcopy

class Node:
    def __init__(self, data):
        self.data = data
        self.father = None
        self.children = []

    def __repr__(self):
        return "Node:" + self.data

def getAnswer(data):
    """
    获取目标棋盘
    生成的棋盘大小等于原棋盘，默认空白在最后一个位置
    @data: 要获取解的棋盘
    @return: 对应的解
    """

    if isinstance(data, tuple):
        size = data
    else:
        size = (len(data), len(data[0]))
    answer = []
    for i in range(size[0]):
        answer.append(list(range(i * size[1] + 1, i * size[1] + 1 + size[1])))

    answer[size[0] - 1][size[1] - 1] = 0
    return answer

def getSpacePos(data):
    """
    获取空格坐标
    @data: 棋盘（二维列表，0表示空格）
    @return: 坐标（(坐标1, 坐标2)）
    """
    for row in data:
        x = 0
        try:
            x = row.index(0)
        except:
            pass
        else:
            return data.index(row), x

def swap(data, a, b):
    """
    交换两个方块
    @data: 要交换的棋盘（不修改原棋盘）
    @a: 要交换的位置a（(pos1, pos2)）
    @b: 要交换的位置b（(pos1, pos2)）
    @return: 交换后的棋盘拷贝
    """
    swapped = deepcopy(data)
    swapped[a[0]][a[1]], swapped[b[0]][b[1]] = swapped[b[0]][b[1]], swapped[a[0]][a[1]]
    return swapped

def move(data):
    """
    移动一次
    @data: 要移动的棋盘
    @return: 移动后的棋盘列表
    """
    spacePos = getSpacePos(data)
    size1 = len(data)
    size2 = len(data[0])
    children = []
    if spacePos[0] > 0: #上
        moved = swap(data, spacePos, (spacePos[0] - 1, spacePos[1]))
        children.append(moved)

    if spacePos[1] > 0: #左
        moved = swap(data, spacePos, (spacePos[0], spacePos[1] - 1))
        children.append(moved)

    if spacePos[0] < size1 - 1: #下
        moved = swap(data, spacePos, (spacePos[0] + 1, spacePos[1]))
        children.append(moved)

    if spacePos[1] < size2 - 1: #右
        moved = swap(data, spacePos, (spacePos[0], spacePos[1] + 1))
        children.append(moved)

    return children

def search(root, target, maxLayer, callback):
    """
    搜索解并返回解的叶子节点
    @root: 根节点
    @target: 目标棋盘
    @maxLayer: 最大搜索层数
    @return: 叶子节点
    """
    arrived = [root.data]
    layer = 0
    thisLayer = [root]
    while True:
        if thisLayer == [] or maxLayer and layer >= maxLayer:
            return None
        nextLayer = []
        for father in thisLayer: #遍历当前层，生成下一层
            moved = move(father.data)
            for i in moved:
                if i in arrived: #跳过已到达过的棋盘
                    continue
                arrived.append(i)
                node = Node(i)
                node.father = father
                father.children.append(node)
                nextLayer.append(node)
                if i == target:
                    return node
        thisLayer = nextLayer
        layer += 1
        if callback:
            callback()
   
def getWay(answerNode):
    """
    从叶子节点获取求解路径
    """
    way = []
    while answerNode:
        way.append(answerNode.data)
        answerNode = answerNode.father
    way.reverse()
    return way

def getRandom(source, step):
    """
    随机移动指定步数
    """
    import random
    way = []
    size1 = len(source)
    size2 = len(source[0])
    source = deepcopy(source)
    for i in range(step):
        action_list = []
        spacePos = getSpacePos(source)
        if spacePos[0] > 0 and swap(source, spacePos, (spacePos[0] - 1, spacePos[1])) not in way: #上
            action_list.append("up")
            
        if spacePos[1] > 0 and swap(source, spacePos, (spacePos[0], spacePos[1] - 1)) not in way: #左
            action_list.append("left")

        if spacePos[0] < size1 - 1 and swap(source, spacePos, (spacePos[0] + 1, spacePos[1])) not in way: #下
            action_list.append("down")

        if spacePos[1] < size2 - 1 and swap(source, spacePos, (spacePos[0], spacePos[1] + 1)) not in way: #右
            action_list.append("right")

        action = action_list[random.randint(0, len(action_list) - 1)]

        if action == "up": #上
            source = swap(source, spacePos, (spacePos[0] - 1, spacePos[1]))

        if action == "left": #左
            source = swap(source, spacePos, (spacePos[0], spacePos[1] - 1))

        if action == "down": #下
            source = swap(source, spacePos, (spacePos[0] + 1, spacePos[1]))

        if action == "right": #右
            source = swap(source, spacePos, (spacePos[0], spacePos[1] + 1))

        way.append(source)
    return source

def solve(data, max_layer = None, callback = None):
    return getWay(search(Node(data), getAnswer(data), max_layer, callback = callback))

if __name__ == "__main__":
    data = [
        [ 1,  2,  3,  4],
        [ 5,  6, 7,  8],
        [ 9, 10,  11,  12],
        [13, 14, 15, 0]
    ]
    print(getAnswer((3, 4)))
    # print(solve(getRandom(data, 10), 15))
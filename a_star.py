import heapq

class NodeList1:
    def __init__(self):
        self.data = {}

    def append(self, node):
        self.data[node.hash] = node

    def popmin(self):
        min_key = min(self.data, key = lambda x : self.data[x].f_cost)
        min_node = self.data[min_key]
        del self.data[min_key]
        return min_node

    def set_min(self, node):
        if node.f_cost < self.data[node.hash].f_cost:
            self.data[node.hash] = node

    def __contains__(self, node):
        return node.hash in self.data

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return repr(self.data)

class NodeList2:
    class MinHeap:
        def __init__(self):
            self.heap = []

        def insert(self, key, value):
            self.heap.append((key, value))
            self.shift_up()

        def pop(self, key, value):
            temp = self.heap.pop()
            if temp == (key, value):
                return temp[1]
            index = self.heap.index((key, value))
            min_data = self.heap[index]
            self.heap[index] = temp
            self.shift_down(index)
            return min_data[1]

        def popmin(self):
            return self.pop(self.heap[0][0], self.heap[0][1])

        def shift_up(self):
            current_id = len(self.heap) - 1
            while current_id > 0:
                parent_id = (current_id - 1) // 2
                if self.heap[parent_id][0] <= self.heap[current_id][0]:
                    break
                else:
                    self.heap[current_id], self.heap[parent_id] = self.heap[parent_id], self.heap[current_id]
                    current_id = parent_id

        def shift_down(self, index):
            current_id = index
            while current_id < len(self.heap) - 1:
                child_id_left = current_id * 2 + 1
                child_id_right = current_id * 2 + 2
                if child_id_left > len(self.heap) - 1:
                    break
                elif child_id_right > len(self.heap) - 1:
                    if self.heap[current_id][0] <= self.heap[child_id_left][0]:
                        break
                    else:
                        self.heap[current_id], self.heap[child_id_left] = self.heap[child_id_left], self.heap[current_id]
                        break
                else:
                    if self.heap[child_id_left][0] < self.heap[child_id_right][0]:
                        min_id = child_id_left
                    else:
                        min_id = child_id_right
                    if self.heap[current_id][0] <= self.heap[min_id][0]:
                        break
                    else:
                        self.heap[current_id], self.heap[min_id] = self.heap[min_id], self.heap[current_id]
                        current_id = min_id


            
    def __init__(self):
        self.map = {}
        self.heap = self.MinHeap()
        
    def append(self, node):
        self.map[node.hash] = node
        self.heap.insert(node.f_cost, node.hash)

    def popmin(self):
        min_hash = self.heap.popmin()
        min_node = self.map[min_hash]
        del self.map[min_hash]
        return min_node

    def set_min(self, node):
        old_node = self.map[node.hash]
        if node.f_cost < old_node.f_cost:
            self.heap.pop(old_node.f_cost, old_node.hash)
            self.heap.insert(node.f_cost, node.hash)
            self.map[node.hash] = node

    def __contains__(self, node):
        return node.hash in self.map

    def __len__(self):
        return len(self.map)

class NodeList3:            
    def __init__(self):
        self.map = {}
        self.heap = []
        
    def append(self, node):
        self.map[node.hash] = node
        heapq.heappush(self.heap, (node.f_cost, node.hash))

    def popmin(self):
        min_hash = heapq.heappop(self.heap)[1]
        min_node = self.map[min_hash]
        del self.map[min_hash]
        return min_node

    def set_min(self, node):
        old_node = self.map[node.hash]
        if node.f_cost < old_node.f_cost:
            self.heap[self.heap.index((old_node.f_cost, old_node.hash))] = (node.f_cost, node.hash)
            heapq.heapify(self.heap)
            self.map[node.hash] = node

    def __contains__(self, node):
        return node.hash in self.map

    def __len__(self):
        return len(self.map)


NodeList = NodeList3


class Node:
    args = {
        "size": None,
        "g_cost": None,
        "h_cost": None,
        "target": None,
        "hash": None
    }

    def __init__(self, data, father = None):
        self.size = self.args['size']
        self.data = data
        self.father = father
        if self.father:
            self.layer = self.father.layer + 1
        else:
            self.layer = 0
        self.h_cost = self.args['h_cost'](self)
        self.g_cost = self.args['g_cost'](self)
        self.f_cost = self.g_cost + self.h_cost
        self.hash = self.args['hash'](self)

    @classmethod
    def init(cls, **args):
        for key, value in args.items():
            cls.args[key] = value

    def __eq__(self, value):
        if isinstance(value, Node):
            return self.hash == value.hash
        else:
            raise TypeError()

def list_to_table(data, size):
    l = []
    for i in range(size[0]):
        l.append(data[i * size[1] : (i + 1) * size[1]])
    return l

def table_to_list(data):
    l = []
    for row in data:
        l += row
    return l

d = 0.03

def g_cost(node):
    if node.father:
        return node.layer * d
    else:
        return 0


def h_cost(node):
    target = node.args['target']
    h = 0
    for i in node.data:
        h += get_distance(get_pos(node.data, node.size, i), get_pos(target, node.size, i))
    return h / len(node.data)


def get_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def node_hash(node):
    h = 0
    for i in range(node.size[0] * node.size[1]):
        h += node.data[i] * ((node.size[0] * node.size[1]) ** i)
    return h

def get_pos(data, size, num):
    data = list_to_table(data, size)
    for row in data:
        x = 0
        try:
            x = row.index(num)
        except:
            pass
        else:
            return data.index(row), x

def get_space_pos(data, size):
    """
    获取空格坐标
    @data: 棋盘（二维列表，0表示空格）
    @return: 坐标（(坐标1, 坐标2)）
    """
    return get_pos(data, size, 0)

def swap(data, shape, a, b):
    """
    交换两个方块
    @data: 要交换的棋盘（不修改原棋盘）
    @a: 要交换的位置a（(pos1, pos2)）
    @b: 要交换的位置b（(pos1, pos2)）
    @return: 交换后的棋盘拷贝
    """
    swapped = data.copy()
    swapped = list_to_table(swapped, shape)
    swapped[a[0]][a[1]], swapped[b[0]][b[1]] = swapped[b[0]][b[1]], swapped[a[0]][a[1]]
    return table_to_list(swapped)

def extend_node(node : Node):
    space_pos = get_space_pos(node.data, node.size)
    table = list_to_table(node.data, node.size)
    shape = node.size
    children = []
    if space_pos[0] > 0: #上
        moved = swap(node.data, node.size, space_pos, (space_pos[0] - 1, space_pos[1]))
        children.append(Node(moved, node))

    if space_pos[1] > 0: #左
        moved = swap(node.data, node.size, space_pos, (space_pos[0], space_pos[1] - 1))
        children.append(Node(moved, node))


    if space_pos[0] < shape[0] - 1: #下
        moved = swap(node.data, node.size, space_pos, (space_pos[0] + 1, space_pos[1]))
        children.append(Node(moved, node))


    if space_pos[1] < shape[1] - 1: #右
        moved = swap(node.data, node.size, space_pos, (space_pos[0], space_pos[1] + 1))
        children.append(Node(moved, node))

    return children

def A_star(start_node, target_node):
    Open = NodeList()
    Close = NodeList()

    Open.append(start_node) #把初始节点放入OPEN表中

    while len(Open) > 0:    #如果OPEN表为空，则问题无解，退出
        n = Open.popmin()
        Close.append(n)     #把Open表的第一个节点取出放入Closed表，并记该节点为n

        
        if n == target_node:#考察节点n是否为目标节点。若是，则找到问题的解，成功退出
            return {
                "solve node": n,
                "open table len": len(Open),
                "close table len": len(Close),
            }

        extend_list = extend_node(n) #扩展节点n，生成其子节点ni(i=1, 2, …),并为每一个子节点设置指向父节点的指针

        for extend in extend_list:  
            if extend in Close:    #将这些子节点放入Open表中
                continue
            elif extend in Open:
                Open.set_min(extend)
            else:
                Open.append(extend)

        # print(n.layer, len(Close))
   
        


def get_random(size, step):
    Node.init(**{
        "size": size,
        "g_cost": g_cost,
        "h_cost": h_cost,
        "target": get_answer(size),
        "hash": node_hash
    })
    import random
    way = NodeList()
    target = Node(get_answer(size))
    for i in range(step):
        space_pos = get_space_pos(target.data, target.size)
        way_list = []
        if space_pos[0] > 0: #上
            node = Node(swap(target.data, target.size, space_pos, (space_pos[0] - 1, space_pos[1])))
            if node not in way:
                way_list.append(node)
            
        if space_pos[1] > 0: #左
            node = Node(swap(target.data, target.size, space_pos, (space_pos[0], space_pos[1] - 1)))
            if node not in way:
                way_list.append(node)

        if space_pos[0] < size[0] - 1: #下
            node = Node(swap(target.data, target.size, space_pos, (space_pos[0] + 1, space_pos[1])))
            if node not in way:
                way_list.append(node)

        if space_pos[1] < size[1] - 1: #右
            node = Node(swap(target.data, target.size, space_pos, (space_pos[0], space_pos[1] + 1)))
            if node not in way:
                way_list.append(node)


        target = way_list[random.randint(0, len(way_list) - 1)]
        way.append(target)

    return target.data

def get_answer(size):
    return list(range(1, size[0] * size[1])) + [0]

def get_solve_list(node):
    l = []
    while node:
        l.append(node.data)
        node = node.father
    l.reverse()
    return l

def search(data, size):
    Node.init(**{
        "size": size,
        "g_cost": g_cost,
        "h_cost": h_cost,
        "target": get_answer(size),
        "hash": node_hash
    })

    solve = A_star(Node(data), Node(get_answer(size)))
    solve_list = get_solve_list(solve['solve node'])
    return solve_list

def get_pair_count(data):
    paircount = 0
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            if data[i] < data[j]:
                paircount += 1
    return paircount

def get_random1(size):
    import random
    while True:
        data = get_answer(size)
        random.shuffle(data)
        test = data.copy()
        test.remove(0)
        if size[1] % 2 == 1:
            if get_pair_count(test) % 2 == 0:
                return data
        else:
            space_pos = get_space_pos(data, size)
            if (get_pair_count(test) + abs(size[0] - 1 - space_pos[0])) % 2 == 0:
                return data
            

    
if __name__ == "__main__":
    from time import time
    # l = NodeList()
    # Node.init(**{
    #     "size": (3, 3),
    #     "g_cost": g_cost,
    #     "h_cost": h_cost,
    #     "target": get_answer((3, 3)),
    #     "hash": node_hash
    # })
    # l.append(Node([1, 2, 3, 4, 5, 6, 7, 8, 0]))
    # l.append(Node([1, 2, 3, 4, 5, 6, 7, 0, 8]))
    
    # l = sorted(l, key = lambda x : x.f_cost)
    # print(l)
    size = (3, 3)
    data = get_random1(size)
    Node.init(**{
        "size": size,
        "g_cost": g_cost,
        "h_cost": h_cost,
        "target": get_answer(size),
        "hash": node_hash
    })

    target = A_star(Node(data), Node(get_answer(size)))
    
    print(target)
    # table = [
    #     [3, 1, 5],
    #     [0, 6, 8],
    #     [4, 2, 7]
    # ]

    # start = time()
    # solve = A_star(Node(data), Node(get_answer(size)))
    # print(len(get_solve_list(solve['solve node'])))
    # print(time() - start)
    # NodeList = NodeList2
    # start = time()
    # A_star(Node(data), Node(get_answer(size)))
    # print(time() - start)
    # for i in range(0, 1200, 100):
    #     d = i / 10000
    #     if d == 0:
    #         continue
    #     solve = A_star(Node(data), Node(get_answer(size)))
    #     print(d, solve['close table len'], len(get_solve_list(solve['solve node'])))
    # print("1")
    # data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0]

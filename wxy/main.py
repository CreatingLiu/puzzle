from AStar import AStar, gn, hn
from base import Node, getSolvePath, tableToList
from BFS import BFS


current = [[0,2,3],
          [1,5,6],
          [4,7,8]]
target = [[1,2,3],
          [4,5,6],
          [7,8,0]]

currentNode = Node(tableToList(current))
targetNode = Node(tableToList(target))

Node.args["gn"] = gn
Node.args["hn"] = hn
Node.args["targetNode"] = targetNode

result = AStar(currentNode, targetNode)
path = getSolvePath(result["targetNode"])
for step in path:
    print(step)
print(f"步数：{result['step']}")
print(f"层数：{result['layer']}")

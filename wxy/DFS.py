from collections import deque


def DFS(current,target):
    open=deque()
    close=deque()
    open.append(current)  #根节点放入open列表
    while len(open) > 0:  #若open表为空则问题无解，退出
        n=open.popleft()  #取出open表的第一个节点，设为n
        close.append(n)
        if n == target:   #如果n为目标节点，则找到目标解，退出
            return {
                "targetNode": n,
                "layer": n.layer,
                "step": len(close)
            }
        else:
            childList=n.extend()
            for child in childList:
                if child in close:
                    continue
                else:
                    open.appendleft(child)

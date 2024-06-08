class Block:
    def __init__(self, start, label):
        # 记录块的起始位置
        self.start = start

        # 记录全部的操作码数组
        self.lines = []

        # 记录所有父节点
        self.pre = []

        # 记录所有子节点
        self.next = []

        # 记录块名（按出块序号排序）
        self.label = label

        # 记录每次进入此块的路径及此时的栈快照
        self.function = []

        self.need = 0

        self.stack = 0

    # 添加父节点（同时添加栈快照）
    def add_pre(self,pre):
        if pre in self.pre:
            return False
        self.pre.append(pre)
        return True

    # 添加子节点
    def add_next(self,next):
        if next in self.next:
            return False
        self.next.append(next)
        return True

    # 计算入路径与出路径的差值
    def pre_next(self):
        return len(self.pre) - len(self.next)

    # 返回是否为交叉路径
    def is_repeat(self):
        return len(self.pre) > 1 or len(self.next) > 1


class Stack:
    def __init__(self, start, label):
        # 记录块的起始位置
        self.data = []

        # 记录全部的操作码数组
        self.record = []

        self.index = 0

    def pop(self,block):
        result = self.data.pop()
        self.index -= 1
        result.end = block
        self.record.append(result)

    def push(self,block,data,kind):
        data = DataOfStack(block,data,kind)
        self.data.append(data)

class DataOfStack:
    def __init__(self, start, data, kind):
        # 记录块的起始位置
        self.start = start

        # 记录全部的操作码数组
        self.end = ""

        self.data = data

        self.kind = kind


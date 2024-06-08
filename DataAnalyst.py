class DataAnalyst:
    def __init__(self,basicBlock):
        self.path = {}
        self.basicBlock = basicBlock

    def getPaths(self,block_start,block_end,path):
        if len(path) >= 50:
            return
        if block_start.label == block_end.label:
            path.append(block_end)
            if self.path.get(block_end.label,'non') == 'non':
                self.path[block_end.label] = []
            self.path[block_end.label].append(path)

        else:
            path.append(block_start)
            for next in block_start.next:
                if next != block_start.label:
                    self.getPaths(self.basicBlock[next],block_end,path)


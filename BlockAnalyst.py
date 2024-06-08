from octopus.analysis.graph import CFGGraph
from octopus.platforms.ETH.cfg import EthereumCFG

from Block import Block


class BlockAnalyst:
    def __init__(self, bytecode):
        self.cfg = None
        self.bytecode = bytecode

        self.basicBlocks = {}

        self.crossBlock = []

    def getCFG(self):
        cfg = EthereumCFG(self.bytecode)
        graph = CFGGraph(cfg)

        self.cfg = cfg
        for basicblock in cfg.basicblocks:
            block = Block(basicblock.start_offset, basicblock.name)
            block.lines = basicblock.instructions
            for edge in cfg.edges:
                if (edge.node_from == block.label):
                    block.next.append(edge.node_to)
                if (edge.node_to == block.label):
                    block.pre.append(edge.node_from)

            self.basicBlocks[block.label] = block

    def getCrossBlock(self):
        for function in self.cfg.functions:
            for basicblock in function.basicblocks:
                self.basicBlocks[basicblock.name].function.append(function.name)

        for key in self.basicBlocks:
            if len(self.basicBlocks[key].function) > 1:
                self.crossBlock.append(self.basicBlocks[key])

    def analystData(self):
        for block in self.basicBlocks:
            stack,need = self.runStack(self.basicBlocks[block])
            self.basicBlocks[block].stack = stack
            self.basicBlocks[block].need = need

    def runStack(self,block):
        stack = 0
        need = 0
        for op in block.lines:
            if op.pops > 0:
                need = min(need,stack - op.pops)
                stack -= op.pops
            if op.pushes > 0:
                stack += op.pushes
        return stack,need



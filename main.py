from octopus.analysis.graph import CFGGraph
from octopus.platforms.ETH.cfg import EthereumCFG

from Block import Block
from BlockAnalyst import BlockAnalyst
from DataAnalyst import DataAnalyst
from Graph import Graph

from collections import defaultdict, deque


class DirectedGraph:
    def __init__(self):
        self.edges = defaultdict(list)

    def add_edge(self, from_node, to_node):
        self.edges[from_node].append(to_node)

    def get_neighbors(self, node):
        return self.edges[node]

    def dfs(self, node, visited):
        visited.add(node)
        for neighbor in self.get_neighbors(node):
            if neighbor not in visited:
                self.dfs(neighbor, visited)

    def find_paths(self, start_node):
        paths = []
        stack = [(start_node, [start_node])]
        while stack:
            (vertex, path) = stack.pop()
            for next_node in set(self.get_neighbors(vertex)) - set(path):
                if not self.get_neighbors(next_node):  # If next_node has no neighbors, it's a leaf node
                    paths.append(path + [next_node])
                else:
                    stack.append((next_node, path + [next_node]))
        return paths

    def find_converging_node(self, start_node):
        paths = self.find_paths(start_node)
        if not paths:
            return None

        last_nodes = [path[-1] for path in paths]
        converging_node = None

        # Check if all paths converge to the same node
        if all(node == last_nodes[0] for node in last_nodes):
            converging_node = last_nodes[0]

        return converging_node, paths


# 示例图结构
graph = DirectedGraph()
graph.add_edge(0, 1)
graph.add_edge(0, 2)
graph.add_edge(1, 3)
graph.add_edge(1, 4)
graph.add_edge(2, 5)
graph.add_edge(3, 6)
graph.add_edge(4, 6)
graph.add_edge(5, 6)

start_node = 0
converging_node, paths = graph.find_converging_node(start_node)

print("Paths from node", start_node, ":", paths)
if converging_node is not None:
    print("All paths converge to node:", converging_node)
else:
    print("No single converging node found.")

def getCrossBlock(bytecode):
    cfg = EthereumCFG()
    graph = CFGGraph(cfg)

    blocks = {}
    for basicblock in cfg.basicblocks:
        block = Block(basicblock.start_offset, basicblock.name)
        block.lines = basicblock.instructions
        for edge in cfg.edges:
            if (edge.node_from == block.label):
                block.next.append(edge.node_to)
            if (edge.node_to == block.label):
                block.pre.append(edge.node_from)

        blocks[block.label] = block

    for function in cfg.functions:
        for basicblock in function.basicblocks:
            blocks[basicblock.name].function.append(function.name)

    crossblock = []
    for key in blocks:
        if len(blocks[key].function) > 1:
            crossblock.append(blocks[key])

    print(len(crossblock))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    block = BlockAnalyst("606060405236156101175763ffffffff60e060020a600035041663083c632381146102b15780630bc1236e146102d357806319ac2756146102fb5780632b093fe91461031d5780632cb3ce8c1461033f57806330adce0e14610361578063421934731461038357806344a5450f146103a557806348cd4cb1146103d15780634a51dcea146103f35780634bb278f314610415578063521eb2731461042757806363b20117146104535780638da5cb5b1461047557806394da0746146104a1578063964ad434146104c3578063ada8938f146104e5578063b391983c14610511578063be82f56b1461053d578063c7f43b5714610561578063ccb07cef14610583578063f0a15f10146105a7578063f2fde38b146105c9575b6102af5b6000805460a060020a900460ff16156101345760006000fd5b6005544310156101445760006000fd5b60065443106101535760006000fd5b66038d7ea4c680003410156101685760006000fd5b691c529a1e8a211018000061017f600354346105e7565b111561018b5760006000fd5b61019760035434610617565b600254604080517f0ecaea73000000000000000000000000000000000000000000000000000000008152600160a060020a033381166004830152602482018590529151939450911691630ecaea739160448082019260009290919082900301818387803b151561020357fe5b6102c65a03f1151561021157fe5b505050610220600354346105e7565b60035560045461023090826105e7565b60045560408051348152602081018390528151600160a060020a033316927f12cb4648cf3058b17ceeb33e579f8b0bc269fe0843f3900b8e24b6c54871703c928290030190a2600154604051600160a060020a03909116903480156108fc02916000818181858888f1935050505015156102aa5760006000fd5b5b5b50565b005b34156102b957fe5b6102c16106a0565b60408051918252519081900360200190f35b34156102db57fe5b6102c1600435602435610617565b60408051918252519081900360200190f35b341561030357fe5b6102c16106a6565b60408051918252519081900360200190f35b341561032557fe5b6102c16106ab565b60408051918252519081900360200190f35b341561034757fe5b6102c16106b7565b60408051918252519081900360200190f35b341561036957fe5b6102c16106bc565b60408051918252519081900360200190f35b341561038b57fe5b6102c16106c2565b60408051918252519081900360200190f35b34156103ad57fe5b6103b56106cd565b60408051600160a060020a039092168252519081900360200190f35b34156103d957fe5b6102c16106dc565b60408051918252519081900360200190f35b34156103fb57fe5b6102c16106e2565b60408051918252519081900360200190f35b341561041d57fe5b6102af6106f0565b005b341561042f57fe5b6103b561088c565b60408051600160a060020a039092168252519081900360200190f35b341561045b57fe5b6102c161089b565b60408051918252519081900360200190f35b341561047d57fe5b6103b56108a1565b60408051600160a060020a039092168252519081900360200190f35b34156104a957fe5b6102c16108b0565b60408051918252519081900360200190f35b34156104cb57fe5b6102c16108bf565b60408051918252519081900360200190f35b34156104ed57fe5b6103b56108cd565b60408051600160a060020a039092168252519081900360200190f35b341561051957fe5b6105246004356108dc565b6040805192835260208301919091528051918290030190f35b341561054557fe5b6102af600160a060020a036004358116906024351661096c565b005b341561056957fe5b6102c1610b00565b60408051918252519081900360200190f35b341561058b57fe5b610593610b0e565b604080519115158252519081900360200190f35b34156105af57fe5b6102c1610b1e565b60408051918252519081900360200190f35b34156105d157fe5b6102af600160a060020a0360043516610b23565b005b6001632321491955600082820161060c8482108015906106075750838210155b610b7c565b8091505b5092915050565b600080808080808087151561062f5760009650610694565b6000955060009450610640896108dc565b909650945061064f868a610b95565b935061065b8489610bb6565b92506106678386610bd8565b91506106856106768a856105e7565b6106808a86610b95565b610617565b905061069182826105e7565b96505b50505050505092915050565b60065481565b60a081565b670de0b6b3a764000081565b605081565b60035481565b66038d7ea4c6800081565b600754600160a060020a031681565b60055481565b691c529a1e8a211018000081565b6000805433600160a060020a0390811691161461070d5760006000fd5b60055443101561071d5760006000fd5b60005460a060020a900460ff16156107355760006000fd5b61074b691c529a1e8a2110180000600354610b95565b905060065443108015610765575066038d7ea4c680008110155b156107705760006000fd5b600254600754604080517f0ecaea73000000000000000000000000000000000000000000000000000000008152600160a060020a0392831660048201526a0422ca8b0a00a425000000602482015290519190921691630ecaea7391604480830192600092919082900301818387803b15156107e757fe5b6102c65a03f115156107f557fe5b5050600254604080517fa69df4b50000000000000000000000000000000000000000000000000000000081529051600160a060020a03909216925063a69df4b591600480830192600092919082900301818387803b151561085257fe5b6102c65a03f1151561086057fe5b50506000805474ff0000000000000000000000000000000000000000191660a060020a179055505b5b50565b600154600160a060020a031681565b60045481565b600054600160a060020a031681565b6a0422ca8b0a00a42500000081565b69069e10de76676d08000081565b600254600160a060020a031681565b600080808069069e10de76676d080000851015610908575069069e10de76676d080000905060a061095c565b690f1678619d523608000085101561092f5750690f1678619d52360800009050607d61095c565b691c529a1e8a21101800008510156109565750691c529a1e8a21101800009050605061095c565b60006000fd5b5b5b8181935093505b5050915091565b60008054819033600160a060020a0390811691161461098b5760006000fd5b600160a060020a03841615156109a15760006000fd5b600160a060020a03831615156109b75760006000fd5b83915081600160a060020a03166370a08231306000604051602001526040518263ffffffff1660e060020a0281526004018082600160a060020a0316600160a060020a03168152602001915050602060405180830381600087803b1515610a1a57fe5b6102c65a03f11515610a2857fe5b50505060405180519050905081600160a060020a031663a9059cbb84836000604051602001526040518363ffffffff1660e060020a0281526004018083600160a060020a0316600160a060020a0316815260200182815260200192505050602060405180830381600087803b1515610a9c57fe5b6102c65a03f11515610aaa57fe5b505060408051600160a060020a0380881682528616602082015280820184905290517feb64d3e0fe21df59e0edd78e9749e4bc9f3cf593a842d487fe40f29ef45fdad692509081900360600190a15b5b50505050565b690f1678619d523608000081565b60005460a060020a900460ff1681565b607d81565b60005433600160a060020a03908116911614610b3f5760006000fd5b600160a060020a038116156102aa576000805473ffffffffffffffffffffffffffffffffffffffff1916600160a060020a0383161790555b5b5b50565b60016323214919558015156102aa5760006000fd5b5b50565b60006001632321491955610bab83831115610b7c565b508082035b92915050565b60006001632321491955818310610bcd5781610bcf565b825b90505b92915050565b6001632321491955600082820261060c8415806106075750838583811515610bfc57fe5b04145b610b7c565b8091505b50929150505600a165627a7a72305820186dc053867706f6478123f8c92c57ef15012a00694594d2e32ad510d89701d90029")

    # block.getCFG()
    # block.getCrossBlock()
    # block.analystData()
    #
    # graph = Graph(block.cfg.edges)
    # data = DataAnalyst(block.basicBlocks)
    # for a in block.crossBlock:
    #     b = graph.get_subgraphs_starting_from(a.label)
    #     for subgraph in b:
    #         if len(block.basicBlocks[subgraph[0]].pre) == len(block.basicBlocks[subgraph[1]].next):
    #             print(subgraph)
    #             data.getPaths(block.basicBlocks[subgraph[0]],block.basicBlocks[subgraph[1]],[])
    #             print(data.path[block.basicBlocks[subgraph[1]].label])
    #
    # for end in data.path:
    #     if len(data.path[end]) == 1:
    #         put_in = 0
    #         put_out = 0
    #         stack = 0
    #         for block in data.path[end][0]:
    #             if stack < block.need:
    #                 put_in += block.need - stack
    #                 stack = 0
    #             stack += block.stack
    #         put_out = stack + put_in
    #         print(end,put_in,put_out)






class Graph:
    def __init__(self,edges):
        self.graph = {}  # 使用邻接表表示的图
        for edge in edges:
            self.add_edge(edge.node_from,edge.node_to)

    def add_edge(self, from_node, to_node):
        if from_node not in self.graph:
            self.graph[from_node] = []
        self.graph[from_node].append(to_node)

    def dfs_paths(self, start_node):
        stack = [(start_node, [start_node])]
        while stack:
            (vertex, path) = stack.pop()
            for next_node in self.graph.get(vertex, []):
                if next_node not in path:
                    new_path = path + [next_node]
                    stack.append((next_node, new_path))
                    if len(new_path) == 2:  # 只考虑长度为2的路径
                        yield new_path

    def get_subgraphs_starting_from(self, start_node):
        subgraphs = []
        for path in self.dfs_paths(start_node):
            subgraphs.append(path)
        return subgraphs

    def get_end_blocks_of_subgraphs(self, start_node):
        end_blocks = []
        for path in self.dfs_paths(start_node):
            if len(path) == 2:  # 只考虑长度为2的路径
                end_blocks.append(path[-1])
        return end_blocks




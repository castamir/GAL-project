from Components import *
import copy


class Magic:
    def __init__(self, nodes, edges):
        if not isinstance(nodes, dict) or not isinstance(nodes, dict):
            raise Exception("Fuj, co jsi mi to dal? Ja chci slovnik s uzly a hranami!!!")
        self.nodes = []
        self.edges = []
        self.components = []  # seznam komponent; komponenta je seznam uzlu
        self.cycles = []
        self.steps = []  # toto mi vratis
        self.current_step = None
        self.next_step()
        self.reset()
        self.time = 0
        self.TransponseEdges = []
        self.TransponseNodes = []
        self.TransponseIndex = []

        for v in nodes:
            node = nodes[v]
            node.name = v
            self.nodes.append(node)
        for e in edges:
            edge = edges[e]
            edge.name = e
            self.add_color(edge, "grey")
            self.edges.append(edge)

    def reset(self):
        for v in self.nodes:
            node = self.nodes[v]
            self.add_color(node, "white")
            node.f = None
            node.d = None

    def add_color(self, element, color):
        element.color = color
        self.current_step[element.name] = color

    def next_step(self):
        self.steps.append({})
        self.current_step = self.steps[-1]

    def detect_cycles_in(self):
        self.SSC()  # step + odbarveni zbytecnych hran
        for c in self.components:
            longest_path = self.find_shortest_path_containing_all_nodes(c)  # step + obarveni nejdelsi cesty
            if len(longest_path) > 1:
                self.cycles.append(longest_path)
                reversed_path = reversed(longest_path)
                for node in reversed_path:
                    for pre in node.Pre:
                        if pre != self.find_pre_in_longest_path(path=reversed_path, node=pre): # step
                            new_cycle = self.find_subcycle_from(path=reversed_path, node_from=node,
                                                                node_pre=pre) #obarveni
                            self.cycles.append(new_cycle)

    def StructInit(self, V, E):
        for node in V:
            node.color = "white"
            node.Adj = []
            for edge in E:
                if edge.start == node:
                    if (edge.end) not in node.Adj:
                        node.Adj.append(edge.end)

    def DFS_visit(self, node):
        node.color = "grey"
        self.time += 1
        node.d = self.time
        for v in node.Adj:
            if v.color == "white":
                self.DFS_visit(v)
        node.color = "black"
        self.time += 1
        node.f = self.time

    def DFS(self, V, E):
        self.time = 0
        for node in V:
            if node.color == "white":
                self.DFS_visit(node)

    def TransponseGraph(self):
        for edge in self.edges:
            self.TransponseEdges.append(Edge(edge.end, edge.start))
        Nodes = {}
        Index = []
        for node in self.nodes:
            Nodes[node.f] = node
            Index.append(node.f)
        Index = sorted(Index, reverse=True)
        for value in Index:
            self.TransponseNodes.append(Nodes[value])

    def FindComponent(self):
        self.components = []

        Nodes = {}
        Index = []
        ordered_nodes = []
        for node in self.TransponseNodes:
            Nodes[node.d] = node
            Index.append(node.d)
        Index = sorted(Index)
        for value in Index:
            ordered_nodes.append(Nodes[value])

        if len(ordered_nodes) == 0:
            return
        while len(ordered_nodes) > 0:
            first = ordered_nodes.pop(0)
            current_component = [first]
            if len(ordered_nodes) > 0:
                while True:
                    if len(ordered_nodes) == 0:
                        break
                    node = ordered_nodes.pop(0)
                    if node.f < first.f:
                        current_component.append(node)
                    else:
                        ordered_nodes.insert(0, node)
                        break
            self.components.append(current_component)

    # todo
    def SSC(self):
        self.StructInit(self.nodes, self.edges)
        self.DFS(self.nodes, self.edges)
        self.TransponseGraph()
        self.StructInit(self.TransponseNodes, self.TransponseEdges)
        self.DFS(self.TransponseNodes, self.TransponseEdges)

        self.FindComponent()
        # nalezeni komponent
        self.add_color_to_components()
        self.next_step()

    # todo
    def find_pre_in_longest_path(self, path, node):
        return Node(0, 0)

    # todo
    def find_subcycle_from(self, path, node_from, node_pre):
        return []

    def add_color_to_components(self):
        for c in self.components:
            edges = self.get_edges_from_component(c)
            for edge in edges:
                self.add_color(edge, "green")

    def find_shortest_path_containing_all_nodes(self, c):
        edges = self.get_edges_from_component(c)
        if len(edges) == 0:
            return []
        return self.__find_path(c[0], c[0], c, edges)

    def print_path(self, path):
        print "path:", [str(s) for s in path]

    def __find_path(self, start_node, curent_node, component, edges, visited_nodes=list(), curent_path=list()):
        for e, edge in enumerate(edges):
            if edge not in curent_path and edge.start == curent_node and edge.end in component:
                if edge.end in visited_nodes:
                    visited = []
                else:
                    visited = [edge.end]
                if len(visited_nodes) + 1 == len(component) and edge.end == start_node:
                    # nasel jsem posledni
                    return curent_path + [edge]
                found = self.__find_path(start_node, edge.end, component, edges, visited_nodes + visited,
                                         curent_path + [edge])
                if found is not None:
                    # tato hrana lezi na spravne ceste, ktera tady jeste nebyla znama cela
                    return found
        return None

    def get_edges_from_component(self, c):
        edges = []
        for edge in self.edges:
            if edge.start in c and edge.end in c:
                edges.append(edge)
        return edges


if __name__ == "__main__":

    V = {"A": Node(0, 0), "B": Node(0, 0), "C": Node(0, 0), "D": Node(0, 0), "E": Node(0, 0), "F": Node(0, 0),
         "G": Node(0, 0)
    }
    E = {
        #0: Edge(V["A"], V["B"]), 2: Edge(V["B"], V["D"]), 4: Edge(V["D"], V["C"]), 1: Edge(V["C"], V["A"]),
        6: Edge(V["A"], V["B"]),
        7: Edge(V["B"], V["C"]),
        9: Edge(V["C"], V["D"]), # mimo
        10: Edge(V["D"], V["A"]),

        11: Edge(V["B"], V["A"]), # vnitrni cyklus

        12: Edge(V["C"], V["E"]), # mimo
        13: Edge(V["E"], V["F"]), # mimo
        8: Edge(V["F"], V["E"]),
    }

    x = Magic(V, E)
    x.SSC()
    for i in x.components:
        for j in i:
            print j.name
        print "xxx"


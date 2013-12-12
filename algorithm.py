from Components import *
import copy


class Magic:
    def __init__(self, nodes, edges):
        if not isinstance(nodes, dict) or not isinstance(nodes, dict):
            raise Exception("Fuj, co jsi mi to dal? Ja chci slovnik s uzly a hranami!!!")
        self.nodes = nodes
        self.edges = edges
        self.components = []  # seznam komponent; komponenta je seznam uzlu
        self.cycles = []
        self.steps = []  # toto mi vratis
        self.current_step = None
        self.next_step()
        self.reset()
        self.time = 0
        self.TransponseEdges = {}
        self.TransponseNodes = {}

        for v in self.nodes:
            node = self.nodes[v]
            node.name = v
        for e in self.edges:
            edge = self.edges[e]
            edge.name = e
            self.add_color(edge, "grey")

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
        for v in V:
            node = V[v]
            node.name = v
            node.color = "white"
            for e in E:
                edge = E[e]
                if edge.start == node:
                    if (edge.end) not in node.Adj:
                        node.Adj.append(edge.end)
        for e in E:
            E[e].name = e

    def DFS_visit(self, u):
        u.color = "grey"
        self.time = self.time +1;
        u.d = self.time
        for v in u.Adj:
            if v.color == "white":
                self.DFS_visit(v)
        u.color = "black"
        self.time = self.time + 1
        u.f = self.time

    def DFS(self, V, E):
        for u in V:
            V[u].Pre = []
        self.time = 0
        for u in V:
            if V[u].color == "white":
                self.DFS_visit(V[u])

    def TransponseGraph(self):
        TransponseIndex = []
        TransponseNames = {}
        Nodes = {}
        for e in self.edges:
            self.TransponseEdges[e]= Edge(self.edges[e].end, self.edges[e].start)

        for v in self.nodes:
            node = self.nodes[v]
            Nodes[node.f] = node
            TransponseNames[node.f] = v
        TransponseIndex = Nodes.keys()
        TransponseIndex.sort()
        TransponseIndex.reverse()
        for i in TransponseIndex:
            self.TransponseNodes[TransponseNames[i]] = Nodes[i]


    # todo
    def SSC(self):
        self.StructInit(self.nodes, self.edges)
        self.DFS(self.nodes, self.edges)

        self.TransponseGraph()

        self.StructInit(self.TransponseNodes, self.TransponseEdges)
        self.DFS(self.TransponseNodes, self.TransponseEdges)

        self.print_path(s.name for s in self.TransponseNodes.values())
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
            for e in self.edges:
                edge = self.edges[e]
                if edge.start in c and edge.end in c:
                    self.add_color(edge, "black")

    def find_shortest_path_containing_all_nodes(self, c):
        edges = self.get_edges_from_component(c)
        print "edges:", [str(s) for s in edges]
        if len(edges) == 0:
            return []
        return self.__find_path(c[0], c[0], c, edges)

    def print_path(self, path):
        print "path:", [str(s) for s in path]

    def __find_path(self, start_node, curent_node, component, edges, visited_nodes=list(), curent_path=list()):
        #print "\ncurent node:", curent_node.name
        #self.print_path(curent_path)
        #print "visited nodes: [", ", ".join([v.name for v in visited_nodes]), "]"
        for e, edge in enumerate(edges):
            if edge not in curent_path and edge.start == curent_node and edge.end in component:
                if edge.end in visited_nodes:
                    #print edge.end.name, "je ve visited"
                    visited = []
                else:
                    #print edge.end.name, "nebyl ve visited"
                    visited = [edge.end]
                if len(visited_nodes)+1 == len(component) and edge.end == start_node:
                    #print "ukoncovaci podminka"
                    # nasel jsem posledni
                    return curent_path + [edge]
                found = self.__find_path(start_node, edge.end, component, edges, visited_nodes + visited, curent_path + [edge])
                if found is not None:
                    #print "druha ukoncovaci podminka - z uzlu", edge.end.name
                    # tato hrana lezi na spravne ceste, ktera tady jeste nebyla znama cela
                    return found
        #print "nebyla nalezena zadna cesta z uzlu", curent_node.name
        return None


    def get_edges_from_component(self, c):
        edges = []
        for e in self.edges:
            edge = self.edges[e]
            if edge.start in c and edge.end in c:
                edges.append(edge)
        return edges

if __name__ == "__main__":
    V = {"A": Node(0, 0), "B": Node(0, 0), "C": Node(0, 0), "D": Node(0, 0), "E": Node(0, 0)}
    E = {
        #0: Edge(V["A"], V["B"]), 2: Edge(V["B"], V["D"]), 4: Edge(V["D"], V["C"]), 1: Edge(V["C"], V["A"]),
         6: Edge(V["A"], V["B"]),
         7: Edge(V["B"], V["C"]),
         8: Edge(V["C"], V["D"]),
         9: Edge(V["C"], V["E"]),  # mimo
         10: Edge(V["E"], V["A"]),
         11: Edge(V["B"], V["A"]),  # vnitrni cyklus
    }

    x = Magic(V, E)
    x.SSC()
    # c = [V["A"], V["B"], V["C"], V["E"]]
    # path = x.find_shortest_path_containing_all_nodes(c)
    # if path is not None:
    #    x.print_path(path)


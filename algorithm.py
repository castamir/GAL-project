from Components import *
import copy


class Magic:
    def __init__(self, nodes, edges):
        if not isinstance(nodes, dict) or not isinstance(nodes, dict):
            raise Exception("Fuj, co jsi mi to dal? Ja chci slovnik s uzly a hranami!!!")
        self.nodes = []
        self.edges = []
        self.components = []  # seznam komponent; komponenta je seznam uzlu
        self.cycles = [] #posloupnost hran
        self.steps = []  # toto mi vratis
        self.current_step = None
        self.next_step()
        self.reset()
        self.time = 0
        self.TransponseEdges = []
        self.TransponseNodes = []

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

    def edgesFromNodes(self, nodes, edges):
        newEdges = []
        s = nodes.pop(0)
        while len(nodes) > 0:
            en = nodes.pop(0)
            for e in edges:
                if e.start == s and en == e.end:
                    newEdges.append(e)
            s = en
        return newEdges

    def DetErrCycle(self, path, node):
        for i in range(0, len(path) - 1):
            if path[i] == node:
                for j in range(i + 1, len(path) - 1):
                    if path[j] == node:
                        if path[i + 1] == path[j + 1]:
                            return True

        return False

    def detectPrePath(self, start, det, path): #detekce podle predchudcu
        for node in start.Pre:
            if node == det:
                return [node]
            if self.DetErrCycle(path, node):
                return []
            return [node] + self.detectPrePath(node, det, path + [node])
        return []

    def cycle(self, start, path, edges, init):
        for node in start.Adj:
            node.Pre = []
            node.Pre.append(start)
            if node in path:
                nodes = self.detectPrePath(node, node, path) #detekuju pozpatku
                if nodes == []:
                    continue
                nodes = [node] + nodes
                cycleEdges = self.edgesFromNodes(nodes[::-1], edges)
                self.cycles.append(cycleEdges)
            if node != init:
                self.cycle(node, path + [node], edges, init)


    def detect_cycles_in(self):
        self.SSC()  # step + odbarveni zbytecnych hran
        for c in self.components:
            edges = self.get_edges_from_component(c)
            self.cycle(c[0], [c[0]], edges, c[0])

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

    def add_color_to_components(self):
        for c in self.components:
            edges = self.get_edges_from_component(c)
            for edge in edges:
                self.add_color(edge, "green")

    def find_path_containing_all_nodes_from_component(self, c):
        edges = self.get_edges_from_component(c)
        print "edges from component:"
        print [str(e) for e in edges]
        if len(edges) == 0:
            return []

        return self.__find_path(c[0], c[0], c, edges)

    def print_path(self, path):
        print "path:", [str(s) for s in path]

    def __find_path(self, start_node, curent_node, component, edges, visited_nodes=list(), curent_path=list()):
        #print "starting node", str(curent_node)
        for edge in edges:
            if edge not in curent_path and edge.start == curent_node and edge.end in component:
                #print "good edge", str(edge)
                if edge.end in visited_nodes:
                    visited = []
                else:
                    visited = [edge.end]
                missing = self.__get_missing_elements_from_component(component, visited_nodes)
                #print [str(m) for m in missing]
                if (len(missing) == 1 and missing[0] == start_node or len(missing) == 0) and edge.end == start_node:
                    # nasel jsem posledni
                    #print "ending node", str(curent_node), "because last was found"
                    return curent_path + [edge]
                found = self.__find_path(start_node, edge.end, component, edges, visited_nodes + visited,
                                         curent_path + [edge])
                if found is not None:
                    # tato hrana lezi na spravne ceste, ktera tady jeste nebyla znama cela
                    #print "ending node", str(curent_node), "good path"
                    return found
                else:
                    #print "continue with", str(curent_node)
                    pass
        #print "ending node", str(curent_node), "nothing found"
        return None

    def __get_missing_elements_from_component(self, c, visited_nodes):
        missing = []
        for node in c:
            if node not in visited_nodes:
                missing.append(node)
        return missing

    def get_edges_from_component(self, c):
        for node in c:
            node.Pre = []
            node.Adj = []
            #   node.Checked = []
        edges = []
        for edge in self.edges:
            if edge.start in c and edge.end in c:
                edges.append(edge)
                edge.start.Adj.append(edge.end)
        return edges


if __name__ == "__main__":

    V = {
        "A": Node(0, 0), "B": Node(0, 0), "C": Node(0, 0),
         "D": Node(0, 0), "E": Node(0, 0), "F": Node(0, 0), "G": Node(0, 0), "H": Node(0, 0)
    }
    E = {
        #0: Edge(V["A"], V["B"]), 2: Edge(V["B"], V["D"]), 4: Edge(V["D"], V["C"]), 1: Edge(V["C"], V["A"]),
        6: Edge(V["A"], V["B"]),
        7: Edge(V["B"], V["C"]),
        9: Edge(V["C"], V["B"]),
        10: Edge(V["B"], V["A"]),

        11: Edge(V["D"], V["E"]),
        12: Edge(V["E"], V["F"]),
        13: Edge(V["F"], V["G"]),
        14: Edge(V["G"], V["D"]),
        15: Edge(V["E"], V["G"]),
        16: Edge(V["E"], V["H"]),
        17: Edge(V["H"], V["E"]),
    }

    x = Magic(V, E)
    x.SSC()
    #x.detect_cycles_in()
    #print len(x.cycles)
    #for i in x.cycles:
    #    for e in i:
    #        print e.name
    #print e.start, "->", e.end
    #print "---------------"

    for c in x.components:
        print "new component:"
        print [str(n) for n in c]
        path = x.find_path_containing_all_nodes_from_component(c)
        #print "=================================="
        if path is not None:
            print "longest path:"
            print [str(e) for e in path]

            print "\n"
        else:
            print "problem"





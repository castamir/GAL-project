from Components import *

class Magic:
    def __init__(self, nodes, edges):
        if not isinstance(nodes, dict) or not isinstance(nodes, dict):
            raise Exception("Fuj, co jsi mi to dal? Ja chci slovnik s uzly a hranami!!!")
        self.__nodes = []
        self.__edges = []
        self._components = []  # seznam komponent; komponenta je seznam uzlu
        self.cycles = [] #posloupnost hran
        self.steps = []  # toto mi vratis
        self._current_step = None
        self.next_step()
        self.reset()
        self.__time = 0
        self.__TransponseEdges = []
        self.__TransponseNodes = []

    ################################################## revision ########################################################
        self.blocked = {}
        self.B = {}
        self.stack = []
    ################################################## revision end ####################################################
        for v in nodes:
            node = nodes[v]
            node.name = v
            self.__nodes.append(node)
        for e in edges:
            edge = edges[e]
            edge.name = e
            self.add_color(edge, "grey")
            self.__edges.append(edge)

    def reset(self):
        for v in self.__nodes:
            node = self.__nodes[v]
            self.add_color(node, "white")
            node.f = None
            node.d = None

    def add_color(self, element, color):
        element.color = color
        self._current_step[element.name] = color

    def next_step(self):
        self.steps.append({})
        self._current_step = self.steps[-1]


    def __is_in_cycles(self, tmp):
        num = len(tmp)
        while num > 0:
            tmp.append(tmp.pop(0))
            num -= 1
            if tmp in self.cycles:
                return True
        return False

    def __walkthrow(self, find, start, tmp, out):
        for p in start.Pre:
            if p == find:
                if tmp[:] + [p] not in out:
                    out.append(tmp[:] + [p])
            else:
                if p not in tmp:
                    self.__walkthrow(find, p, tmp + [p], out)
    #################################################### revision ######################################################
    def unblock(self, node, comp):
        self.blocked[comp.index(node)] = False
        for w in self.B[comp.index(node)]:
            if(self.blocked[comp.index(w)]):
                self.unblock(w, comp)

    def nFindCycles(self, v, s, comp):
        f = False
        self.stack.append(v)
        self.blocked[comp.index(v)] = True

        for i in v.Adj:
            if i == s:
                cycle = []
                for j in self.stack:
                    cycle.append(j)
                self.cycles.append(cycle[:])
                f = True
            elif not self.blocked[comp.index(i)]:
                if self.nFindCycles(i,s,comp):
                    f = True

        if f:
            self.unblock(v, comp)
        else:
            for i in v.Adj:
                if v not in self.B[comp.index(i)]:
                    self.B[comp.index(i)].append(v)
        self.stack.remove(v)
        return f

    def getElementaryCycles(self, comp):
        self.blocked = {}
        self.B = {}
        ind = 0
        while True:
            edges = self.__get_edges_from_component(comp)
            if edges != []:
                s = comp[ind]
                for i in s.Adj:
                    self.blocked[comp.index(i)] = False
                    self.B[comp.index(i)] = []
                self.nFindCycles(s, s, comp)
                ind += 1
            else:
                break

    def detect_cycles(self):
        self.SSC()
        for i in self._components:
            self.B = {}
            self.blocked = {}
            for j in i:
                self.blocked[i.index(j)] = False
                self.B[i.index(j)] = []

            self.__get_edges_from_component(i)
            self.nFindCycles(i[0],i[0],i) # zde to mozna bude potreba volat pro kazdy uzel

    ################################################## revision end ####################################################
    def detect_cycles_in(self):
        self.SSC()
        out = []
        output = []
        for c in self._components:
            edges = self.__get_edges_from_component(c)
            for v in c:
                to_expand = [v]
                expanded = []
                while len(to_expand) > 0:
                    node = to_expand.pop(0)
                    for n in node.Adj:
                        n.Pre.append(node)
                        if n == v:
                            self.__walkthrow(v, n,[n], out)
                            continue
                        else:
                            if n not in expanded and n != node:
                                to_expand.append(n)
                    expanded.append(node)

                for o in out:
                    if o not in output:
                        output.append(o)

            for i in output:
                newEdges = self.find_path_from_nodes(i[::-1], edges)
                if not self.__is_in_cycles(newEdges):
                    self.cycles.append(newEdges[:])

    def find_path_from_nodes(self, nodes, edges):
        newEdges = []
        current_node = nodes.pop(0)
        for node in nodes:
            for edge in edges:
                if edge.start == current_node and edge.end == node:
                    newEdges.append(edge)
                    break
            current_node = node
        return newEdges

    def _StructInit(self, V, E):
        for node in V:
            node.color = "white"
            node.Adj = []
            for edge in E:
                if edge.start == node:
                    if edge.end not in node.Adj:
                        node.Adj.append(edge.end)

    def __DFS_visit(self, node):
        node.color = "grey"
        self.__time += 1
        node.d = self.__time
        for v in node.Adj:
            if v.color == "white":
                self.__DFS_visit(v)
        node.color = "black"
        self.__time += 1
        node.f = self.__time

    def DFS(self, V, E):
        self.__time = 0
        for node in V:
            if node.color == "white":
                self.__DFS_visit(node)

    def __TransponseGraph(self):
        for edge in self.__edges:
            self.__TransponseEdges.append(Edge(edge.end, edge.start))
        Nodes = {}
        Index = []
        for node in self.__nodes:
            Nodes[node.f] = node
            Index.append(node.f)
        Index = sorted(Index, reverse=True)
        for value in Index:
            self.__TransponseNodes.append(Nodes[value])

    def __FindComponent(self):
        self._components = []

        Nodes = {}
        Index = []
        ordered_nodes = []
        for node in self.__TransponseNodes:
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
            self._components.append(current_component)

    # todo
    def SSC(self):
        self._StructInit(self.__nodes, self.__edges)
        self.DFS(self.__nodes, self.__edges)
        self.__TransponseGraph()
        self._StructInit(self.__TransponseNodes, self.__TransponseEdges)
        self.DFS(self.__TransponseNodes, self.__TransponseEdges)

        self.__FindComponent()
        # nalezeni komponent
        self.add_color_to_components()
        self.next_step()

    def add_color_to_components(self):
        for c in self._components:
            edges = self.__get_edges_from_component(c)
            for edge in edges:
                self.add_color(edge, "green")


    def print_path(self, path):
        print "path:", [str(s) for s in path]


    def __get_edges_from_component(self, c):
        for node in c:
            node.Pre = []
            node.Adj = []
        edges = []
        for edge in self.__edges:
            if edge.start in c and edge.end in c:
                edges.append(edge)
                edge.start.Adj.append(edge.end)
        return edges


if __name__ == "__main__":

    # V = {
    #     "A": Node(0, 0), "B": Node(0, 0), "C": Node(0, 0),
    #     "D": Node(0, 0), "E": Node(0, 0), "F": Node(0, 0), "G": Node(0, 0), "H": Node(0, 0)
    # }
    # E = {
    #     #0: Edge(V["A"], V["B"]), 2: Edge(V["B"], V["D"]), 4: Edge(V["D"], V["C"]), 1: Edge(V["C"], V["A"]),
    #     6: Edge(V["A"], V["B"]),
    #     7: Edge(V["B"], V["C"]),
    #     9: Edge(V["C"], V["B"]),
    #     10: Edge(V["B"], V["A"]),
    #
    #     11: Edge(V["D"], V["E"]),
    #     12: Edge(V["E"], V["F"]),
    #     13: Edge(V["F"], V["G"]),
    #     14: Edge(V["G"], V["D"]),
    #     15: Edge(V["E"], V["G"]),
    #     16: Edge(V["E"], V["H"]),
    #     17: Edge(V["H"], V["E"]),
    # }

    V = {
        "A": Node(0, 0), "B": Node(0, 0), "C": Node(0, 0),
        "D": Node(0, 0), "E": Node(0, 0), "Z": Node(0, 0),
    }
    E = {


        11: Edge(V["A"], V["B"]),
        12: Edge(V["B"], V["C"]),
        13: Edge(V["C"], V["D"]),
        14: Edge(V["D"], V["A"]),

        15: Edge(V["B"], V["D"]),
        16: Edge(V["D"], V["E"]),
        17: Edge(V["E"], V["D"]),

        18: Edge(V["A"], V["Z"]),
        19: Edge(V["Z"], V["A"]),

        # druhej priklad

        # 6: Edge(V["A"], V["B"]),
        # 7: Edge(V["B"], V["C"]),
        # 5: Edge(V["C"], V["B"]),
        # 4: Edge(V["B"], V["A"]),
    }

    x = Magic(V, E)
    x.detect_cycles()






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

        self.__blocked = {}
        self.__B = {}
        self.__stack = []
        self.component_steps = []
        self.cycle_steps = []

        for v in nodes:
            node = nodes[v]
            node.name = v
            self.__nodes.append(node)
        for e in edges:
            edge = edges[e]
            edge.name = e
            self.add_color(edge, "grey")
            self.__edges.append(edge)

    def get_all_steps(self):
        return self.component_steps[:] + self.cycle_steps[:]

    def get_component_steps(self):
        return self.component_steps[:]

    def get_cycle_steps(self):
        return self.cycle_steps[:]

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

    def color_edges(self, nodes, color):
        for n in range(0,len(nodes)-1):
            for e in self.__edges:
                if e.start == nodes[n] and e.end == nodes[n+1]:
                    self.add_color(e,color)

    def __unblock(self, node, comp):
        self.__blocked[comp.index(node)] = False
        for w in self.__B[comp.index(node)]:
            self.__B[comp.index(node)].remove(w)
            if(self.__blocked[comp.index(w)]):
                self.__unblock(w, comp)

    def __find_cycles(self, v, s, comp, From):
        f = False
        self.__stack.append(v)
        self.__blocked[comp.index(v)] = True
        self.add_color(v, "green")

        for i in v.Adj:
            self.color_edges([v]+[i],"red")
            prev = i.color
            self.add_color(i, "red")
            self.next_step()
            if i == s:
                cycle = []
                for j in self.__stack:
                    cycle.append(j)
                    self.add_color(j, "yellow")

                self.color_edges(cycle[:] + [s], "blue")
                self.next_step()
                self.color_edges(cycle[:] + [s], "red")
                for j in self.__stack:
                    self.add_color(j, "green")
                self.add_color(v, "red")
                self.next_step()
                self.cycles.append(cycle[:] + [s])
                f = True
            elif not self.__blocked[comp.index(i)]:
                if self.__find_cycles(i, s, comp, v):
                    f = True
                
            self.color_edges([v]+[i],"grey")
            if i.color != prev:
                self.add_color(i, prev)
                self.next_step()

        self.add_color(v, "red")
        self.next_step()
        if f:
            self.__unblock(v, comp)
        else:
            for i in v.Adj:
                if v not in self.__B[comp.index(i)]:
                    self.__B[comp.index(i)].append(v)
        self.__stack.remove(v)
        if From != None:
            self.color_edges([From]+[v],"grey")
        if s != v:
            self.add_color(v, "white")
        else:
            self.add_color(v, "grey")
        self.next_step()
        return f

    def detect_cycles(self):
        self.SSC()
        for e in self.__edges:
            self.add_color(e, "grey")
        for n in self.__nodes:
            self.add_color(n, "white")

        for i in self._components:
            tmp = i[:]
            self.__blocked = {}
            self.__B = {}
            self.__stack = []
            for j in tmp:

                self.__get_edges_from_component(i)
                for k in i:
                    self.__blocked[i.index(k)] = False
                    self.__B[i.index(k)] = []
                    self.add_color(k, "white")
                self.add_color(j, "green")
                self.next_step()
                self.__find_cycles(j,j,i,None)
                i.remove(j)
            i = tmp[:]
        self.cycle_steps = self.steps[len(self.component_steps):]
        
        tmp = []
        for i in self.cycles:
            tmp.append(self.find_path_from_nodes(i,self.__edges))
        self.cycles = []
        self.cycles = tmp

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

    def __struct_init(self, V, E):
        for node in V:
           # node.color = "white"

            self.add_color(node,"white")
            node.Adj = []
            for edge in E:
                if edge.start == node:
                    if edge.end not in node.Adj:
                        node.Adj.append(edge.end)
        self.next_step()

    def __DFS_visit(self, node):
        #node.color = "grey"
        self.add_color(node,"grey")
        self.next_step()
        self.__time += 1
        node.d = self.__time
        for v in node.Adj:
            if v.color == "white":
                self.__DFS_visit(v)
        #node.color = "black"
        self.add_color(node,"black")
        self.next_step()
        self.__time += 1
        node.f = self.__time

    def DFS(self, V, E):
        self.__time = 0
        for node in V:
            if node.color == "white":
                self.__DFS_visit(node)

    def __transponse_graph(self):
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

    def __find_component(self):
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


    def SSC(self):
        self.__struct_init(self.__nodes, self.__edges)
        self.DFS(self.__nodes, self.__edges)
        self.__transponse_graph()
        self.__struct_init(self.__TransponseNodes, self.__TransponseEdges)
        self.DFS(self.__TransponseNodes, self.__TransponseEdges)

        self.__find_component()
        # nalezeni komponent
        self.add_color_to_components_edges()
        self.next_step()
        self.component_steps = self.steps[:]

    def add_color_to_components_edges(self):
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

        15: Edge(V["B"], V["A"]),
        16: Edge(V["C"], V["B"]),
        17: Edge(V["D"], V["C"]),

        18: Edge(V["A"], V[""]),
        19: Edge(V["Z"], V["A"]),

        # druhej priklad

        # 6: Edge(V["A"], V["B"]),
        # 7: Edge(V["B"], V["C"]),
        # 5: Edge(V["C"], V["B"]),
        # 4: Edge(V["B"], V["A"]),
    }

    x = Magic(V, E)
    x.detect_cycles()

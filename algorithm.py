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




    def detect_cycles_in(self):
        self.SSC()  # step + odbarveni zbytecnych hran
        for c in self.components:
            edges = self.get_edges_from_component(c)
            #print [str(e) for e in edges]
            longestPath = self.find_path_containing_all_nodes_from_component(c)
            if longestPath == []:
                continue

            zkratky = []
            for edge in longestPath:
                for e in edges:
                    if e.start == edge.start and e.end != edge.end and e not in zkratky:
                        zkratky.append(e)
            print [str(e) for e in zkratky]
            visit = []
            #for e in longestPath:

            longestCopy = longestPath[:]
            for z in zkratky:

                while longestCopy[0].start != z.end:
                    longestCopy.append(longestCopy.pop(0))
                print z,"long",[str(x) for x in longestCopy]
               # print z,":::",[str(x) for x in longestCopy]

                for e in longestCopy:
                    if e.end not in visit:
                        if z.end == e.start:
                            path = []
                            for i in range(longestCopy.index(e), len(longestCopy)):
                                path.append(longestCopy[i])
                                if longestCopy[i].end == z.start:
                                    tmp = [z] + path[:]
                                    num = len(tmp)
                                    flag = False
                                    while num > 0:
                                        tmp.append(tmp.pop(0))
                                        num = num - 1
                                        if tmp in self.cycles:
                                            flag = True
                                    if  not flag:
                                        self.cycles.append([z] + path[:])

            visit.append(e.start)
# ##############################
# for hrana in nejdelsi_cesta:
    # seznam_zkratek = []  # z hrana.start
    # for zkratka in seznam_zkratek:
    #     if zkratka != hrana:
    #         for hrana_na_zbytku_cesty_od_zkratky_dal in nejdelsi_cesta:
    #             if hrana_na_zbytku_cesty_od_zkratky_dal.start == zkratka.end:
    #                 # pro vsechny vyskyty zkratka.start (tedy hranu H) ve zbytku nejdelsi cesty od "hrana_na_zbytku_cesty_od_zkratky_dal"
    #                     # pridame cyklus (cestu) slouzenou ze zkratky (jedna hrana) a vsech hrany mezi H a "hrana_na_zbytku_cesty_od_zkratky_dal" vcetne
# ##############################


    def StructInit(self, V, E):
        for node in V:
            node.color = "white"
            node.Adj = []
            for edge in E:
                if edge.start == node:
                    if edge.end not in node.Adj:
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
        #print "edges from component:"
        #print [str(e) for e in edges]
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

    # V = {
    #     "A": Node(0, 0), "B": Node(0, 0), "C": Node(0, 0),
    #     "D": Node(0, 0), "E": Node(0, 0), "Z": Node(0, 0),
    # }
    # E = {
    #
    #
    #     11: Edge(V["A"], V["B"]),
    #     12: Edge(V["B"], V["C"]),
    #     13: Edge(V["C"], V["D"]),
    #     14: Edge(V["D"], V["A"]),
    #
    #     15: Edge(V["B"], V["D"]),
    #     16: Edge(V["D"], V["E"]),
    #     17: Edge(V["E"], V["D"]),
    #
    #     18: Edge(V["A"], V["Z"]),
    #     19: Edge(V["Z"], V["A"]),
    #
    #     # druhej priklad
    #
    #     # 6: Edge(V["A"], V["B"]),
    #     # 7: Edge(V["B"], V["C"]),
    #     # 5: Edge(V["C"], V["B"]),
    #     # 4: Edge(V["B"], V["A"]),
    #
    #
    # }

    x = Magic(V, E)
   # x.SSC()
    #x.detect_cycles_in()
    #print len(x.cycles)
    #for i in x.cycles:
    #    for e in i:
    #        print e.name
    #print e.start, "->", e.end
    #print "---------------"

    # for c in x.components:
    #     print "new component:"
    #     print [str(n) for n in c]
    #     path = x.find_path_containing_all_nodes_from_component(c)
    #     #print "=================================="
    #     if path is not None:
    #         print "longest path:"
    #         print [str(e) for e in path]
    #
    #         print "\n"
    #     else:
    #         print "problem"

    x.detect_cycles_in()


    for cycle in x.cycles:
        print "-------------------"
        print "cycle:", [str(i) for i in cycle]
        print "-------------------"

    print "cycle", len(x.cycles), "comp", len(x.components)





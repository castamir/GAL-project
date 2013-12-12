from Components import *
import copy


class core:
    def __init__(self):
        self.output = []
        self.count = 0

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

    def DetectCycle(self, u, v, f):
        for x in u.Pre:
            f2 = copy.deepcopy(f)
            f2.append(x)
            if x == v: #detekoval jsem smycku
                self.output.append(reversed(f2)) # reverze retezce
            else:
                self.DetectCycle(x, v, f2)

    def DFS_Visit(self, u):
        u.color = "grey"
        for v in u.Adj:
            if v.color == "white":
                v.Pre.append(u)
                self.DFS_Visit(v)
            else: # natrefil jsem na neco kde jsem uz byl budu hledat predka

                self.DetectCycle(u, v, [v, u]) #jedu od konce
        u.color = "black"

    def DFS(self, V, E):
        for v in V:
            print v
            node = V[v]
            if node.color == "white":
                self.DFS_Visit(node)
            print "-"

    def GetResult(self):
        return self.output


if __name__ == "__main__":
    core = core()
    V = {"A": Node(0, 0), "B": Node(0, 0), "C": Node(0, 0), "D": Node(0, 0)}
    E = {0: Edge(V["A"], V["B"]), 2: Edge(V["B"], V["D"]), 4: Edge(V["D"], V["C"]), 1: Edge(V["C"], V["A"]),
         6: Edge(V["A"], V["D"]),
         5: Edge(V["B"], V["C"]),
         #3: Edge(V["C"], V["D"]),
    }

    core.StructInit(V, E)

    for v in V:
        node = V[v]
        sousede = []
        for u in node.Adj:
            sousede.append(u.name)
        print v, "sousede:", ", ".join(sousede)


    core.DFS(V, E)
    r = core.GetResult()
    for i in r:
        for j in i:
            print j.name
        print "-------"

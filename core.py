import Components
import Magic
import copy
import pprint

class core:
    def __init__(self):
        self.output = []
        self.count = 0

    def StructInit(self, V, E):
        for v in V :
            v.color = "white"
            for e in E:
                if e.start == v:
                    if (e.end) not in v.Adj:
                        v.Adj.append(e.end)

    def DetectCycle(self, u, v, f):
        for x in u.Pre:
            f2 = copy.deepcopy(f)
            f2.append(x)
            if x == v: #detekoval jsem smycku
                self.output.append(reversed(f2)) # reverze retezce
            else:
                self.DetectCycle(x,v, f2)


    def DFS_Visit(self, u):
        u.color = "grey"
        for v in u.Adj:
            if v.color == "white":
                v.Pre.append(u)
                self.DFS_Visit(v)
            else: # natrefil jsem na neco kde jsem uz byl budu hledat predka
                self.DetectCycle(u, v, [v,u]) #jedu od konce
        u.color = "black"


    def DFS(self, V, E):
        self.StructInit(V, E)
        for v in V:
            if v.color == "white":
                self.DFS_Visit(v)

    def GetResult(self):
        return self.output



if __name__ == "__main__":
    core = core()
    V = [Components.Node(0,0,"A"), Components.Node(0,0,"B"), Components.Node(0,0,"C"), Components.Node(0,0,"D")]
    E = [Components.Edge(V[0],V[1]),Components.Edge(V[0],V[3]),Components.Edge(V[1],V[2]),Components.Edge(V[1],V[3]),
         Components.Edge(V[2],V[0]),Components.Edge(V[3],V[2])]

    core.DFS(V, E)
    r = core.GetResult()
    #print len(r)
    #for i in r:
    #    for j in i:
    #        print j.name
    #    print "\n"
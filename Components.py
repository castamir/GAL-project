
NODE_SIZE = 50


class Edge:
    def __init__(self, start, end):
        if not isinstance(start, Node):
            pass
        if not isinstance(end, Node):
            pass
        self.start = start
        self.end = end


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = int(NODE_SIZE / 2)
        self.color = "blue"
        self.Adj = []
        self.Pre = []

    def get_coord(self):
        return self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r

NODE_SIZE = 50
DEFAULT_COLOR = "blue"


class Edge:
    def __init__(self, start, end):
        if not isinstance(start, Node):
            pass
        if not isinstance(end, Node):
            pass
        self.name = None
        self.start = start
        self.end = end
        self.color = DEFAULT_COLOR

    def __str__(self):
        return "%s -> %s" % (self.start.name, self.end.name)

class Node:
    def __init__(self, x, y):
        self.name = None
        self.x = x
        self.y = y
        self.r = int(NODE_SIZE / 2)
        self.color = DEFAULT_COLOR
        self.Adj = []
        self.Pre = []
        self.d = None
        self.f = None
        self.checked = []

    def get_coord(self):
        return self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r

    def __str__(self):
        return self.name


NODE_SIZE = 50
DEFAULT_COLOR = "blue"


class Edge:
    def __init__(self, start, end, is_curve=False):
        if not isinstance(start, Node):
            pass
        if not isinstance(end, Node):
            pass
        self.name = None
        self.start = start
        self.end = end
        self.color = DEFAULT_COLOR
        self.is_curve = is_curve

    def __str__(self):
        return "%s -> %s" % (self.start.name, self.end.name)

    def get_coords(self):
        return [
            (self.start.x, self.start.y),
            (self.start.x, self.start.y - 75),
            (self.start.x + 75, self.start.y),
            (self.start.x + 25, self.start.y),
        ]


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

    def get_coord(self):
        return self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r

    def __str__(self):
        return self.name


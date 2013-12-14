from Tkinter import *
import math
from Components import *
from algorithm import *

HEIGHT = 450
WIDTH = 600


class GAL:
    def __init__(self):
        self.locked = False
        self.window = Tk()
        self.window.title("kuk")
        self.canvas = None
        self.buttons = {}
        self.nodes = {}
        self.edges = {}
        self.render_canvas()
        self.render_buttons()
        self.active_node = None
        self.active_edge = None
        self.start = None
        self.x = None
        self.y = None

    def repaint(self):
        for e in self.edges:
            edge = self.edges[e]
            self.canvas.itemconfigure(e, fill=edge.color)
        for v in self.nodes:
            node = self.nodes[v]
            self.canvas.itemconfigure(v, fill=node.color)

    def render_buttons(self):
        self.buttons['start'] = b = Button(self.window, text="Start", compound=LEFT)
        b.bind('<Button-1>', self.event_start)
        b.pack(side=RIGHT, padx=5, pady=5)
        self.buttons['reset'] = b = Button(self.window, text="Reset", compound=LEFT)
        b.pack(side=RIGHT, padx=5, pady=5)

    def event_start(self, event):
        x = Magic(self.nodes, self.edges)
        x.detect_cycles_in()
        for i in x.cycles:
            print [str(e) for e in i]

        self.repaint()
        #c = [self.nodes[v] for v in self.nodes]

    def render_canvas(self):
        self.canvas = Canvas(self.window, height=HEIGHT, width=WIDTH, relief=RAISED, borderwidth=1)
        self.canvas.bind('<Double-Button-1>', self.event_add_node)
        self.canvas.bind('<Button-1>', self.event_add_edge_start)
        self.canvas.bind('<B1-Motion>', self.event_add_edge_move)
        self.canvas.bind('<ButtonRelease-1>', self.event_add_edge_end)
        self.canvas.bind('<Button-3>', self.event_move_node_start)
        self.canvas.bind('<B3-Motion>', self.event_move_node)
        self.canvas.pack(fill='both', expand='yes')

    def run(self):
        self.window.mainloop()

    def _activate_node(self, id):
        self._deactivate_node()
        if id in self.nodes:
            self.active_node = id

    def _deactivate_node(self):
        self.active_node = None

    def event_add_edge_start(self, event):
        self.x = event.x
        self.y = event.y

    def event_add_edge_move(self, event):
        if self.active_edge is None:
            self.active_edge = self.canvas.create_line(self.x, self.y, event.x, event.y, arrow="last", width=2)
        else:
            x1, y1, x2, y2 = self.canvas.coords(self.active_edge)
            self.canvas.coords(self.active_edge, x1, y1, event.x, event.y)

    def event_add_edge_end(self, event):
        if self.active_edge is None:
            return
        x1, y1, x2, y2 = self.canvas.coords(self.active_edge)
        start = self._get_node_from_position(x1, y1)
        end = self._get_node_from_position(x2, y2)
        if start is None or end is None or start == end:
            self.canvas.delete(self.active_edge)
        else:
            x, y = self._calculate_edge_end_from_nodes(start, end)
            self.canvas.coords(self.active_edge, start.x, start.y, x, y)
            self.canvas.tag_lower(self.active_edge, self.nodes.keys()[0])
            edge = Edge(start, end)
            self.edges[self.active_edge] = edge
        self.active_edge = None
        self.x = None
        self.y = None

    def event_move_node_start(self, event):
        id = self._get_id_from_position(event.x, event.y)
        if id is None:
            return
        self._activate_node(id)
        self.x = event.x
        self.y = event.y

    def event_move_node(self, event):
        id = self.active_node
        if id is None:
            return
        deltax = event.x - self.x
        deltay = event.y - self.y
        self.canvas.move(id, deltax, deltay)
        self.x = event.x
        self.y = event.y
        coord = self.canvas.coords(id)
        self.nodes[self.active_node].x = (coord[2] - coord[0]) / 2 + coord[0]
        self.nodes[self.active_node].y = (coord[3] - coord[1]) / 2 + coord[1]
        self._repair_edge_starting_in_node(self.nodes[self.active_node])
        self._repair_edge_ending_in_node(self.nodes[self.active_node])

    def _repair_edge_ending_in_node(self, node):
        list_of_edge_ids = []
        for edge_id in self.edges:
            edge = self.edges[edge_id]
            if edge.end == node:
                list_of_edge_ids.append(edge_id)
        for edge_id in list_of_edge_ids:
            edge = self.edges[edge_id]
            x, y = self._calculate_edge_end_from_nodes(edge.start, edge.end)
            self.canvas.coords(edge_id, edge.start.x, edge.start.y, x, y)

    def _repair_edge_starting_in_node(self, node):
        list_of_edge_ids = []
        for edge_id in self.edges:
            edge = self.edges[edge_id]
            if edge.start == node:
                list_of_edge_ids.append(edge_id)
        for edge_id in list_of_edge_ids:
            edge = self.edges[edge_id]
            x, y = self._calculate_edge_end_from_nodes(edge.start, edge.end)
            self.canvas.coords(edge_id, edge.start.x, edge.start.y, x, y)
            #self.canvas.itemconfigure(edge_id, fill="black")

    def _calculate_edge_end_from_nodes(self, start_node, end_node):
        diffx = end_node.x - start_node.x
        diffy = end_node.y - start_node.y
        distance = math.sqrt(diffx ** 2 + diffy ** 2)
        if distance > 0:
            ratio = NODE_SIZE / 2 / distance
            x = end_node.x - diffx * ratio
            y = end_node.y - diffy * ratio
            return x, y
        return end_node.x, end_node.y


    def _get_id_from_position(self, x, y, reverse=False):
        overlaping = self.canvas.find_overlapping(x, y, x, y)
        if len(overlaping) > 0:
            if reverse:
                return overlaping[-1]
            else:
                return overlaping[0]
        else:
            return None

    def _get_node_from_position(self, x, y):
        id = self._get_id_from_position(x, y)
        if id is not None and id in self.nodes:
            return self.nodes[id]
        else:
            return None

    def event_add_node(self, event):
        id = self._get_id_from_position(event.x, event.y, reverse=True)
        if id is None or id not in self.nodes:
            self.add_node(event.x, event.y)

    def add_node(self, x, y):
        node = Node(x, y)
        id = self.canvas.create_oval(node.get_coord(), fill="blue")
        self.nodes[id] = node


if __name__ == "__main__":
    gal = GAL()
    gal.run()

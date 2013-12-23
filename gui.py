#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import Tk, Text, BOTH, W, N, E, S, Canvas, Menu, END, RIGHT, LEFT, DISABLED
from ttk import Frame, Button, Label, Style
import tkFileDialog
import tkMessageBox as box
from pygraphml.GraphMLParser import *
from pygraphml.Graph import *

import math, os
from algorithm import *

HEIGHT = 450
WIDTH = 600


class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent

        self.buttons = {}
        self.nodes = {}
        self.edges = {}
        self.active_node = None
        self.active_edge = None
        self.start = None
        self.x = None
        self.y = None
        self.steps = None
        self.step_index = None

        self.parent.title("Windows")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, pad=7)

        self.label = Label(self, text="graf1.graphml")
        self.label.grid(sticky=W, pady=4, padx=5)

        self.canvas = Canvas(self)
        self.canvas.bind('<Double-Button-1>', self.event_add_node)
        self.canvas.bind('<Button-1>', self.event_add_edge_start)
        self.canvas.bind('<B1-Motion>', self.event_add_edge_move)
        self.canvas.bind('<ButtonRelease-1>', self.event_add_edge_end)
        self.canvas.bind('<Button-3>', self.event_move_node_start)
        self.canvas.bind('<B3-Motion>', self.event_move_node)
        self.canvas.pack()
        self.canvas.grid(row=1, column=0, columnspan=2, rowspan=5,
                         padx=5, sticky=E + W + S + N)

        self.buttons['start'] = b = Button(self, text="Vyhledat cykly", width=15)
        b.bind('<Button-1>', self.event_start)
        b.grid(row=1, column=3)

        self.buttons['next'] = b = Button(self, text=">>", width=15, state=DISABLED)
        b.bind('<Button-1>', self.event_next_step)
        b.grid(row=2, column=3, pady=4)

        self.buttons['prev'] = b = Button(self, text="<<", width=15, state=DISABLED)
        b.bind('<Button-1>', self.event_prev_step)
        b.grid(row=3, column=3, pady=4)

        self.buttons['reset'] = b = Button(self, text="Reset", width=15)
        b.bind('<Button-1>', self.event_reset)
        b.grid(row=5, column=3)

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Načíst", command=self.onLoad)
        fileMenu.add_command(label="Uložit", command=self.onSave)
        fileMenu.add_separator()
        fileMenu.add_command(label="Konec", command=self.onExit)
        menubar.add_cascade(label="Soubor", menu=fileMenu)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label="O aplikaci", command=self.onAbout)
        menubar.add_cascade(label="Nápověda", menu=fileMenu)

    def onExit(self):
        self.quit()

    def onLoad(self):
        fileTypes = [('Soubory typu GraphML', '*.graphml')]

        dialog = tkFileDialog.Open(self, filetypes=fileTypes)
        filename = dialog.show()

        if filename != '':
            text = self.readFile(filename)
            #self.txt.insert(END, text)
            print text

    def onSave(self):
        fileTypes = [('GraphML files', '*.graphml')]

        dialog = tkFileDialog.SaveAs(self, filetypes=fileTypes)
        filename = dialog.show()

        if not filename.endswith(".graphml"):
            filename += ".graphml"

        self.writeFile(filename)


    def onAbout(self):
        box.showinfo("O aplikaci",
                     "Demonstrace algoritmu nalezení elementárních cyklů v orientovaném grafu podle D. B. Johnsona. \n\n"
                     "Autoři:\n"
                     "Paulík Miroslav\n"
                     "Pavlů Igor\n"
                     "FIT VUT v Brně 2013")


    def readFile(self, filename):
        self.reset()

        parser = GraphMLParser()
        g = parser.parse(filename)

        try:
            nodeMap = {}
            for gnode in g.nodes():
                nodeMap[gnode.id] = self.__add_node(int(gnode['x']), int(gnode['y']))
            for gedge in g.edges():
                start = nodeMap[gedge.node1.id]
                end = nodeMap[gedge.node2.id]
                isCurve = start == end
                self.__add_edge(start, end, isCurve)
            self.label.configure(text=os.path.basename(filename))
        except KeyError:
            self.reset()


        self.repaint()


    def writeFile(self, filename):
        g = Graph()

        for i in self.nodes:
            node = self.nodes[i]
            node.name = str(i)
            gnode = g.add_node(i)
            gnode['label'] = i
            gnode['x'] = node.x
            gnode['y'] = node.y

        for i in self.edges:
            edge = self.edges[i]
            edge.name = i
            print g.add_edge_by_label(edge.start.name, edge.end.name)

        parser = GraphMLParser()
        parser.write(g, filename)


    def repaint(self):
        for e in self.edges:
            edge = self.edges[e]
            self.canvas.itemconfigure(e, fill=edge.color)
        for v in self.nodes:
            node = self.nodes[v]
            self.canvas.itemconfigure(v, fill=node.color)

    def reset_colors(self):
        for n in self.nodes:
            self.nodes[n].color = "white"
        for e in self.edges:
            self.edges[e].color = "grey"

    def reset(self):
        self.nodes = {}
        self.edges = {}
        self.canvas.delete("all")
        self.buttons['prev'].config(state=DISABLED)
        self.buttons['next'].config(state=DISABLED)


    def event_reset(self, event):
        self.reset()

    def event_prev_step(self, event):
        if str(self.buttons['prev'].cget("state")) != str(DISABLED):
            self.algorithm_step_move(-1)

    def event_next_step(self, event):
        if str(self.buttons['next'].cget("state")) != str(DISABLED):
            self.algorithm_step_move(1)

    def event_start(self, event):
        x = Magic(self.nodes, self.edges)
        x.detect_cycles()
        self.step_index = 0
        self.steps = x.get_all_steps()

        self.algorithm_step_move(0)

        if len(self.steps) > 0:
            self.buttons['prev'].config(state=1)
            self.buttons['next'].config(state=1)

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
        start = self.__get_node_from_position(x1, y1)
        end = self.__get_node_from_position(x2, y2)
        if start is None or end is None:
            self.canvas.delete(self.active_edge)
        elif start == end:
            self.canvas.delete(self.active_edge)
            edge = Edge(start, start, True)
            points = edge.get_coords()
            self.active_edge = self.canvas.create_line(points, width=2, smooth=True, arrow="last")
            self.canvas.tag_lower(self.active_edge, min(self.nodes.keys()))
            self.edges[self.active_edge] = edge
        else:
            x, y = self.__calculate_edge_end_from_nodes(start, end)
            self.canvas.coords(self.active_edge, start.x, start.y, x, y)
            self.canvas.tag_lower(self.active_edge, min(self.nodes.keys()))
            edge = Edge(start, end)
            self.edges[self.active_edge] = edge
        self.active_edge = None
        self.x = None
        self.y = None

    def event_move_node_start(self, event):
        id = self.__get_id_from_position(event.x, event.y)
        if id is None:
            return
        self.__activate_node(id)
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
        self.__repair_edge_starting_in_node(self.nodes[self.active_node])
        self.__repair_edge_ending_in_node(self.nodes[self.active_node])

    def event_add_node(self, event):
        id = self.__get_id_from_position(event.x, event.y, reverse=True)
        if id is None or id not in self.nodes:
            self.__add_node(event.x, event.y)

    def __repair_edge_ending_in_node(self, node):
        list_of_edge_ids = []
        for edge_id in self.edges:
            edge = self.edges[edge_id]
            if edge.end == node:
                list_of_edge_ids.append(edge_id)
        for edge_id in list_of_edge_ids:
            edge = self.edges[edge_id]
            x, y = self.__calculate_edge_end_from_nodes(edge.start, edge.end)
            if edge.is_curve:
                coords = edge.get_coords()
                self.canvas.coords(edge_id, coords[0][0], coords[0][1], coords[1][0], coords[1][1], coords[2][0],
                                   coords[2][1], coords[3][0], coords[3][1])
            else:
                self.canvas.coords(edge_id, edge.start.x, edge.start.y, x, y)

    def __repair_edge_starting_in_node(self, node):
        list_of_edge_ids = []
        for edge_id in self.edges:
            edge = self.edges[edge_id]
            if edge.start == node:
                list_of_edge_ids.append(edge_id)
        for edge_id in list_of_edge_ids:
            edge = self.edges[edge_id]
            x, y = self.__calculate_edge_end_from_nodes(edge.start, edge.end)
            if edge.is_curve:
                coords = edge.get_coords()
                self.canvas.coords(edge_id, coords[0][0], coords[0][1], coords[1][0], coords[1][1], coords[2][0],
                                   coords[2][1], coords[3][0], coords[3][1])
            else:
                self.canvas.coords(edge_id, edge.start.x, edge.start.y, x, y)

    def __calculate_edge_end_from_nodes(self, start_node, end_node):
        diffx = end_node.x - start_node.x
        diffy = end_node.y - start_node.y
        distance = math.sqrt(diffx ** 2 + diffy ** 2)
        if distance > 0:
            ratio = NODE_SIZE / 2 / distance
            x = end_node.x - diffx * ratio
            y = end_node.y - diffy * ratio
            return x, y
        return end_node.x, end_node.y

    def __activate_node(self, id):
        self.__deactivate_node()
        if id in self.nodes:
            self.active_node = id

    def __deactivate_node(self):
        self.active_node = None

    def __get_id_from_position(self, x, y, reverse=False):
        overlaping = self.canvas.find_overlapping(x, y, x, y)
        if len(overlaping) > 0:
            if reverse:
                return overlaping[-1]
            else:
                return overlaping[0]
        else:
            return None

    def __get_node_from_position(self, x, y):
        id = self.__get_id_from_position(x, y)
        if id is not None and id in self.nodes:
            return self.nodes[id]
        else:
            return None

    def __add_node(self, x, y):
        node = Node(x, y)
        id = self.canvas.create_oval(node.get_coord(), fill="blue")
        self.nodes[id] = node
        return node

    def __add_edge(self, start, end, is_curve=False):
        edge = Edge(start, end)
        if is_curve:
            id = self.canvas.create_line(edge.get_coords(), width=2, smooth=True, arrow="last")
        else:
            id = self.canvas.create_line(start.x, start.y, end.x, end.y, arrow="last", width=2)
        self.edges[id] = edge
        self.canvas.tag_lower(id, min(self.nodes.keys()))
        self.__repair_edge_starting_in_node(start)
        return edge

    def algorithm_step_move(self, move):
        if (self.step_index + move) < len(self.steps) and self.step_index + move >= 0:
            self.step_index += move
            self.reset_colors()
            for i in range(self.step_index + 1):
                colors = self.steps[i]
                for id in colors:
                    if id in self.nodes.keys():
                        self.nodes[id].color = colors[id]
                    elif id in self.edges.keys():
                        self.edges[id].color = colors[id]
            self.repaint()
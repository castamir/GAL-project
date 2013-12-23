#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import Tk, Text, BOTH, W, N, E, S, Canvas, Menu, END
from ttk import Frame, Button, Label, Style
import tkFileDialog
import tkMessageBox as box
from pygraphml.GraphMLParser import *
from pygraphml.Graph import *


class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent

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
        self.canvas.grid(row=1, column=0, columnspan=2, rowspan=5,
                         padx=5, sticky=E + W + S + N)

        abtn = Button(self, text="Vyhledat cykly")
        abtn.grid(row=1, column=3)

        cbtn = Button(self, text=">>")
        cbtn.grid(row=2, column=3, pady=4)

        cbtn = Button(self, text="<<")
        cbtn.grid(row=3, column=3, pady=4)

        #hbtn = Button(self, text="Help")
        #hbtn.grid(row=5, column=0, padx=5)
        #
        obtn = Button(self, text="Reset")
        obtn.grid(row=5, column=3)

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
        print filename

        self.writeFile(filename)


    def onAbout(self):
        box.showinfo("O aplikaci",
                     "Demonstrace algoritmu nalezení elementárních cyklů v orientovaném grafu podle D. B. Johnsona. \n\n"
                     "Autoři:\n"
                     "Paulík Miroslav\n"
                     "Pavlů Igor\n"
                     "FIT VUT v Brně 2013")


    def readFile(self, filename):
        f = open(filename, "r")
        text = f.read()
        return text


    def writeFile(self, filename):
        g = Graph()

        n1 = g.add_node("A")
        n2 = g.add_node("B")
        n3 = g.add_node("C")
        n4 = g.add_node("D")
        n5 = g.add_node("E")
        n5['x'] = 5
        n5['y'] = 199

        g.add_edge(n1, n3)
        g.add_edge(n2, n3)
        g.add_edge(n3, n4)
        g.add_edge(n3, n5)

        parser = GraphMLParser()
        parser.write(g, filename)

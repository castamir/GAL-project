#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import Tk, Text, BOTH, W, N, E, S, Canvas, Menu, END
from ttk import Frame, Button, Label, Style
import tkFileDialog


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
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)

        self.area = Canvas(self)
        self.area.grid(row=1, column=0, columnspan=2, rowspan=4,
                       pady=3,
                       padx=5, sticky=E + W + S + N)

        self.abtn = Button(self, text="Activate")
        self.abtn.grid(row=1, column=3)

        self.cbtn = Button(self, text="Close")
        self.cbtn.grid(row=2, column=3, pady=4)

        self.hbtn = Button(self, text="Help")
        self.hbtn.grid(row=5, column=0, padx=5)

        self.obtn = Button(self, text="OK")
        self.obtn.grid(row=5, column=3)

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Load", command=self.onLoad)
        fileMenu.add_command(label="Save", command=self.onSave)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=self.onExit)
        menubar.add_cascade(label="File", menu=fileMenu)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label="About", command=self.onAbout)
        menubar.add_cascade(label="Help", menu=fileMenu)


    def onExit(self):
        self.quit()

    def onLoad(self):
        fileTypes = [('GraphML files', '*.xml')]

        dialog = tkFileDialog.Open(self, filetypes=fileTypes)
        filename = dialog.show()

        if filename != '':
            text = self.readFile(filename)
            #self.txt.insert(END, text)
            print text

    def onSave(self):
        pass


    def onAbout(self):
        pass


    def readFile(self, filename):
        f = open(filename, "r")
        text = f.read()
        return text

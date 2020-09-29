# -*- coding: UTF-8 -*-
from tkinter import Tk, Canvas
from tkinter import *
import _thread

width = 600
height = 600
sq_length = 8


class CA_draw():
    lock = []

    def __init__(self, space):
        # self.space = space
        # self.root = Tk()
        # self.root.title = 'CA'
        # self.frame = Frame(self.root)
        # self.cv = Canvas(self.frame, bg='white', width=width, height=height, scrollregion=(0, 0, 800, 800))
        # self.frame.grid(row=0, column=0)
        # hbar = Scrollbar(self.frame, orient=HORIZONTAL)
        # hbar.pack(side=BOTTOM, fill=X)
        # hbar.config(command=self.cv.xview)
        # vbar = Scrollbar(self.frame, orient=VERTICAL)
        # vbar.pack(side=RIGHT, fill=Y)
        # vbar.config(command=self.cv.yview)
        # self.cv.config(width=300, height=300)
        # self.cv.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        # self.cv.pack(side=LEFT, fill=BOTH, expand=YES)
        # self.root.bind("<Configure>", self.changeSize)
        # self.drawByRow(space)
        # self.root.mainloop()
        self.space = space
        self.root = Tk()
        self.root.title = 'CA'
        l = len(space)
        self.cv = Canvas(self.root, bg='white', width=l * sq_length, height=l * sq_length,
                         scrollregion=(0, 0, 800, 800))
        hbar = Scrollbar(self.root, orient=HORIZONTAL)
        hbar.pack(side=BOTTOM, fill=X)
        hbar.config(command=self.cv.xview)
        vbar = Scrollbar(self.root, orient=VERTICAL)
        vbar.pack(side=RIGHT, fill=Y)
        vbar.config(command=self.cv.yview)
        self.cv.config(width=300, height=300)
        self.cv.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        # self.cv.pack(side=LEFT, fill=BOTH, expand=YES)
        self.cv.pack()
        # self.root.bind("<Configure>", self.changeSize)
        self.drawByRow(space)
        self.root.mainloop()


    def drawByRow(self, space):
        x1 = 0
        y1 = height - sq_length
        x2 = x1 + sq_length
        y2 = height
        for i, row in enumerate(space):
            for j, char in enumerate(row):
                if char == '1':
                    self.cv.create_rectangle(x1 + sq_length * j, y1 - sq_length * i, x2 + sq_length * j,
                                             y2 - sq_length * i, width=None, fill='blue', outline='blue')
                if char == '0':
                    self.cv.create_rectangle(x1 + sq_length * j, y1 - sq_length * i, x2 + sq_length * j,
                                             y2 - sq_length * i, width=None, fill='white', outline='white')


if __name__ == '__main__':
    space = []
    n = 50
    for i in range(n):
        tm = []
        for j in range(n):
            if i == j or i == j * 2 or i == j * 3:
                tm.append('1')
            else:
                tm.append('0')
        space.append(tm)
    CA_draw(space)

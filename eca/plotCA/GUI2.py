# -*- coding: UTF-8 -*-
from tkinter import Tk, Canvas
from tkinter import *
import _thread

width = 600
height = 600
sq_length = 4
ll = 900
cv = None


def changeSize(event):
    global height
    for item in cv.find(ALL):
        cv.move(item, 0, event.height - height)
    height = event.height


def drawPoints(space, cv):
    # sq_length = 800 / len(space[0])
    x1 = 0
    y1 = height - sq_length
    x2 = x1 + sq_length
    y2 = height
    for i, row in enumerate(space):
        for j, char in enumerate(row):
            if char == '1':
                cv.create_rectangle(x1 + sq_length * j, y1 - sq_length * i, x2 + sq_length * j,
                                    y2 - sq_length * i, width=None, fill='blue', outline='blue')
            # if char == '0':
            #     cv.create_rectangle(x1 + sq_length * j, y1 - sq_length * i, x2 + sq_length * j,
            #                         y2 - sq_length * i, width=None, fill='white', outline='white')


def drawByRow(space):
    root = Tk()
    root.title = 'CA'
    l = len(space)
    global width, height
    width = l * sq_length
    height = l * sq_length
    root.geometry(str(width if width < ll else ll) + "x" + str(height if height < 800 else 800))
    global cv
    cv = Canvas(root, bg='white', width=width, height=height, scrollregion=(0, 0, width, height))
    # cv = Canvas(root, bg='white', width=width, height=height)
    hbar = Scrollbar(root, orient=HORIZONTAL)
    hbar.pack(side=BOTTOM, fill=X)
    hbar.config(command=cv.xview)
    vbar = Scrollbar(root, orient=VERTICAL)
    vbar.pack(side=RIGHT, fill=Y)
    vbar.config(command=cv.yview)
    cv.config(width=width, height=height)
    cv.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    cv.pack(side=LEFT, fill=BOTH, expand=YES)
    # cv.pack()
    drawPoints(space, cv)
    root.bind("<Configure>", changeSize)
    root.mainloop()


if __name__ == '__main__':
    space = []
    n = 500
    for i in range(n):
        tm = []
        for j in range(n):
            if i == j or i == j * 2 or i == j * 3:
                tm.append('1')
            else:
                tm.append('0')
        space.append(tm)
    drawByRow(space)

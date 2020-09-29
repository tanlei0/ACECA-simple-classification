# -*- coding: UTF-8 -*-
from tkinter import Tk, Canvas
import threading

width = 600
height = 600
sq_length = 8


class CA_draw():
    def __init__(self, space):
        self.root = Tk()
        self.root.title = 'CA'
        self.root.geometry(str(width) + 'x' + str(height))
        self.cv = Canvas(self.root, bg='white', width=width, height=height)
        self.cv.pack()
        self.drawByRow(space)
        # self.root.mainloop()

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


def show(cc):
    cc.root.mainloop()


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
    cc = CA_draw(space)
    t = threading.Thread(target=show, args=(cc, ))
    t.start()
    # t.join()

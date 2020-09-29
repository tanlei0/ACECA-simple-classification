# -*- coding: UTF-8 -*-
from tkinter import Tk, Canvas
import matplotlib.pyplot as plt
from tkinter import *
import numpy as np
import matplotlib.patches as mp
from PyQt5 import QtGui
import pyqtgraph as pg

width = 600
height = 600
sq_length = 8


class CA_draw():
    def __init__(self, space):
        global sq_length
        sq_length = len(space[0]) / 800
        self.space = space
        # self.plotCA(self.space)
        self.drawByRow(space)
    def drawByRow(self, space):
        ones_x = []
        ones_y = []
        zeros_x = []
        zeros_y = []
        plt.xlim(0, len(space))
        plt.ylim(0, len(space[0]))
        for i in range(len(space)):
            for j in range(len(space[0])):
                if space[i][j] == '1':
                    ones_x.append(i)
                    ones_y.append(j)
                else:
                    zeros_x.append(i)
                    zeros_y.append(j)
        plt.scatter(ones_x, ones_y, s=0.6, c='b', marker='s')
        # plt.scatter(zeros_x, zeros_y, s=1, c='w', marker='s')
        plt.legend(['1', '0'])
        plt.show()

    def test(self, space):
        ones_x = []
        ones_y = []
        zeros_x = []
        zeros_y = []
        plt.xlim(0, len(space))
        plt.ylim(0, len(space[0]))
        for i in range(len(space)):
            for j in range(len(space[0])):
                if space[i][j] == '1':
                    ones_x.append(i)
                    ones_y.append(j)
                else:
                    zeros_x.append(i)
                    zeros_y.append(j)
        app = QtGui.QApplication([])
        w = QtGui.QWidget()
        pg.setConfigOption('background', 'w')
        QtGui.QPainter.drawPoints(ones_x, ones_y)
        # plot = pg.plot(ones_x, ones_y, pen=pg.mkPen('r', width=0.1), symbol='s')
        # plot.plot(zeros_x, zeros_y, pen=pg.mkPen('w', width=0.1), symbol='s')
        layout = QtGui.QGridLayout()
        w.setLayout(layout)
        layout.addWidget(plot, 0, 1, 3, 1)
        w.show()
        app.exec_()

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

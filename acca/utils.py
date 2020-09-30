# -*- coding: utf-8 -*-
# @Time : 2020/8/7 pm3:11
# @Author : cmk
# @File : utils.py.py

import pickle
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import imageio
from tqdm import tqdm
import re
import numpy as np
import math
from enum import Enum
import random
import multiprocessing

random.seed(2020)

plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']

light_gray_code = 0.3
dark_gray_code = 0.8
while_code = 0
black_code = 1
# color map
colors_dict_ = {
    '000': 0,
    '001': 0,
    '002': 0,

    '010': 0.8,
    '012': 0.8,
    '011': 0.8,

    '100': 0.3,
    '102': 0.3,
    '101': 0.3,

    '110': 1,
    '111': 1,
    '112': 1,
}


class Flag(Enum):
    UNUSED = 0
    BLACK = 1
    WHITE = 2


def save_data(data, file_path=""):
    with open(file_path, "wb") as file:
        pickle.dump(data, file, True)


def read_data(file_path=""):
    with open(file_path, "rb") as file:
        data = pickle.load(file)
    return data


def get_color2space(colors_dict=None, gap=None, datas=None):
    """
    assign colors to matrix
    """
    if gap is None:
        gap = [1]
    if colors_dict is None:
        # (curr, prev, t)
        colors_dict = colors_dict_
    datas = read_data("./sim_data/temp.pkl") if datas is None else datas
    datas = [datas[i] for i in range(0, len(datas), gap)]
    space = [[] for _ in range(len(datas))]
    for i in range(len(datas)):
        for data in datas[i]:
            cell = data['cell']
            # (curr, prev, t)
            space[i].append(colors_dict[cell['curr'] + cell['prev'] + str(cell['t'])])
    return np.asarray(space)


def plot_space(title='', colors_dict=None, gaps=None, datas=None, save_=False, show=True):
    if colors_dict is None:
        # (curr, prev, t)
        colors_dict = colors_dict_
    if gaps is None:
        gaps = [1]
    for gap in gaps:
        space = get_color2space(colors_dict, gap, datas=datas)

        cmap = plt.get_cmap('Greys')
        plt.xticks([])
        plt.yticks([])
        plt.tight_layout()
        plt.imshow(space, interpolation='none', cmap=cmap)
        if save_:
            plt.savefig("./result/{}_run={}_cell={}_gap={}.jpeg".format(title, len(datas), len(datas[0]), gap),
                        dpi=300)
        if show:
            plt.show()


def getInitState(n_cell, d_ini):
    init_state = ''
    for i in range(0, n_cell):
        rand = np.random.rand()
        if rand >= d_ini:
            init_state += '0'
        else:
            init_state += '1'
    return init_state


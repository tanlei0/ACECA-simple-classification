# -*- coding: utf-8 -*-
# @Time : 2020/8/7 下午2:44
# @Author : cmk
# @File : plot_ACCA.py

import numpy as np
from utils.utils import *
import matplotlib.pyplot as plt
from tqdm import tqdm

plt.rcParams[u'font.sans-serif'] = ['Noto Sans CJK JP']
plt.rcParams['axes.unicode_minus'] = False


if __name__ == "__main__":
    colors_dict = [
        {'00': 1,
         '10': 0,
         '01': 1,
         '02': 1,
         '11': 0,
         '12': 0},
        {'00': 0,
         '10': 1,
         '01': 0,
         '02': 0,
         '11': 1,
         '12': 1},
        {'00': 0,
         '10': 1,
         '01': 0.2,
         '02': 0.4,
         '11': 0.8,
         '12': 0.6}
    ]
    # gaps = [1, 2, 4, 8, 12]
    gaps = [1]
    c = 2
    for gap in gaps:
        space = get_color2space(colors_dict[c], gap)
        # fig = plt.figure(figsize=(19.2, 10.8))
        plt.figure(figsize=(10, 10))
        plt.title("run=2000, cell=400,每隔{}取一次".format(gap))
        plt.text(x=0, y=-50, s=str(colors_dict[c]), size=10)
        cmap = plt.get_cmap('Greys')
        plt.imshow(space, interpolation='none', cmap=cmap)
        # plt.savefig('./result/{}-result.png'.format(gap), dpi=300)
        plt.savefig('./result/ACCA_90_.png'.format(gap), dpi=300)
        plt.show()

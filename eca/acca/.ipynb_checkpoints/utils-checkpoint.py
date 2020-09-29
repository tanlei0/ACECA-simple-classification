# -*- coding: utf-8 -*-
# @Time : 2020/8/7 下午3:11
# @Author : cmk
# @File : utils.py.py

import pickle
import matplotlib.pyplot as plt
import os
import imageio
from tqdm import tqdm
import re
import numpy as np
import math
from enum import Enum
import random
random.seed(2020)

plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']

# 颜色设置规则
# 0时刻curr为0, 则whilte
# 1时刻curr或prev有一个为1,则darkgray，否则为lightgray
# 2时刻curr为1，则darkgray, 否则为lightgray
colors_dict_ = {
    # 00 white
    '010': 0,
    '000': 0,
    # 10 black
    '100': 1,
    '110': 1,

    # lightgray
    '001': 0.5,
    '012': 0.5,
    '002': 0.5,

    # darkgray
    '011': 0.8,
    '101': 0.8,
    '111': 0.8,
    '102': 0.8,
    '112': 0.8,
}


class Flag(Enum):
    UNUSED = 0
    BLACK = 1
    WHITE = 2


# ####### 操作pkl文件####

def save_data(data, file_path=""):
    with open(file_path, "wb") as file:
        pickle.dump(data, file, True)


def read_data(file_path=""):
    with open(file_path, "rb") as file:
        data = pickle.load(file)
    return data


# #######################


def delete_dir_contents(img_dir):
    """
    删除目录下所有文件
    :param img_dir: 图片目录
    :return:
    """
    if not os.path.exists(img_dir):
        print("该目录不存在")
    else:
        # 循环删除之前的文件
        files = os.listdir(img_dir)
        for file in files:
            os.remove(os.path.join(img_dir, file))
        print("文件删除完毕！")


def create_gif(img_dir, save_gif_path="./acca.gif", duration=0.5):
    """
    将多张图片保存为gif动态图
    每张图片的格式为img_num.jpg，num为图片编号
    图片编号需要连续,img_1.jpg, img_2.jpg ... img_12.jpg
    :param duration: gif播放速度
    :param img_dir: 图片目录
    :param save_gif_path: gif保存位置
    :return:
    """

    # 递归获取指定目录下所有文件的绝对路径（非目录）
    def get_all(path):
        dir_list = os.listdir(path)
        image_list = [''] * len(dir_list)
        for img_name in dir_list:
            img_path = os.path.join(path, img_name)
            if os.path.isdir(img_path):
                raise IsADirectoryError('图片目录下不能有子目录')
            else:  # 此时sub_dir是文件的绝对路径
                # 提取路径中图片的编号
                index = int(re.match(r".*img_(.*).jpg", img_path).group(1))
                image_list[index] = img_path

        return image_list

    image_list = get_all(img_dir)
    # 将每一帧图片存起来
    frames = []
    for image_path in image_list:
        frames.append(imageio.imread(image_path))
    # 将所有帧保存为gif动图
    imageio.mimsave(save_gif_path, frames, 'GIF', duration=duration)
    print("gif文件保存在", save_gif_path)


# 将一维展开为二维
def to_2D(space):
    w = int(math.sqrt(len(space[0])))
    if w * w != len(space[0]):
        raise ValueError("一维数据的长度不能整开方")
    # 对space中的每一行展开为二维
    td_space = [np.asarray(s).reshape(w, w) for s in space]
    return np.asarray(td_space)


# 绘制动图gif
def draw_gif(space, img_dir='./tmp/'):
    """
    绘制动图gif
    :param space: 每一轮迭代的状态对应的颜色
    :param img_dir: 图片的临时保存路径
    :return:
    """
    if not os.path.exists(img_dir):
        os.mkdir(img_dir)
    else:
        delete_dir_contents(img_dir)
    space = to_2D(space)
    print("绘制每一帧图片...")
    for i in tqdm(range(len(space))):
        cmap = plt.get_cmap('Greys')
        plt.title("iter" + str(i))
        plt.imshow(space[i], interpolation='none', cmap=cmap)
        plt.savefig(os.path.join(img_dir, "img_" + str(i) + ".jpg"), dpi=96)
    create_gif(img_dir=img_dir)


def get_color2space(colors_dict=None, gap=None, datas=None):
    """
    给矩阵上色
    :param colors_dict: 每种状态对应的颜色
    :param gap: 间隔
    :return:
    """
    if gap is None:
        gap = [1]
    if colors_dict is None:
        # (curr, prev, t) 三元组
        colors_dict = colors_dict_
    datas = read_data("./sim_data/temp.pkl") if datas is None else datas
    datas = [datas[i] for i in range(0, len(datas), gap)]
    space = [[] for _ in range(len(datas))]
    for i in range(len(datas)):
        for data in datas[i]:
            cell = data['cell']
            # (curr, prev, t) 三元组
            space[i].append(colors_dict[cell['curr'] + cell['prev'] + str(cell['t'])])
    return np.asarray(space)


def plot_space(title='', colors_dict=None, gaps=None, datas=None, save_=False):
    if colors_dict is None:
        # (curr, prev, t) 三元组
        colors_dict = colors_dict_
    if gaps is None:
        gaps = [1]
    for gap in gaps:
        space = get_color2space(colors_dict, gap, datas=datas)
        plt.figure(figsize=(10, 10))
        plt.title("{}, run={}, cell={},每隔{}取一次".format(title, len(datas), len(datas[0]), gap))
        cmap = plt.get_cmap('Greys')
        plt.imshow(space, interpolation='none', cmap=cmap)
        if save_:
            plt.savefig("./result/run={}_cell={}_每隔{}取一次.jpg".format(len(datas), len(datas[0]), gap), dpi=300)
        plt.show()


# def get_dense(datas=None):
#     datas = read_data("./sim_data/temp.pkl") if datas is None else datas
#     cell_type = ['100', '110', '111', '101', '102', '112']
#     # cell_type = ['100', '110', '011', '111', '102', '112']
#     quantities = [0] * len(datas)
#     for i in range(len(datas)):
#         for data in datas[i]:
#             cell = data['cell']
#             if cell['curr'] + cell['prev'] + str(cell['t']) in cell_type:
#                 quantities[i] += 1
#     density = np.asarray(quantities) / len(datas[0])
#     return density


def get_dense(datas=None):
    datas = read_data("./sim_data/temp.pkl") if datas is None else datas
    cell_type = ['100', '110', '111', '101', '102', '112']
    # cell_type = ['100', '110', '011', '111', '102', '112']
    quantities = [0] * len(datas)
    ct = {}
    for i in range(len(datas)):
        for data in datas[i]:
            cell = data['cell']
            g = cell['curr'] + cell['prev'] + str(cell['t'])
            ct[g] = ct.get(g, 0) + 1
            if g in cell_type:
                quantities[i] += 1
    # density = np.asarray(quantities) / len(datas[0])
    density = np.asarray(quantities)
    step = 260
    partsl = int(len(density) / step)
    density_step = []
    for i in range(partsl):
        density_step.append(density[i * step: i * step + step].sum(axis=0) / step)
    return density_step


def plot_dense(datas=None, title="ACCA", save_path="./result/density.jpg"):
    density = get_dense(datas=datas)
    plt.figure(figsize=(19.2, 10.8))
    plt.plot(range(len(density)), density, label='nums(cells_1)/nums(cells)')
    plt.title(title)
    plt.xlabel('Time step')
    plt.ylabel('Density')
    plt.legend()
    plt.savefig(save_path, dpi=144)
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


if __name__ == '__main__':
    plt.subplot(121)
    plt.imshow(plt.imread("./result/ECA_density.jpg"))
    plt.subplot(122)
    plt.imshow(plt.imread("./result/ECA_density.jpg"))
    plt.show()

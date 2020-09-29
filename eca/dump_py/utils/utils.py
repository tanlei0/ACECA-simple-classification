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


def create_gif(img_dir, save_gif_path=None, duration=0.5):
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
                index = int(re.match(r"img_(.*).jpg", 'img_02.jpg').group(1))
                image_list[index] = img_path
        return image_list

    image_list = get_all(img_dir)
    # 将每一帧图片存起来
    frames = []
    for image_name in image_list:
        frames.append(imageio.imread(image_name))
    # 将所有帧保存为gif动图
    imageio.mimsave(save_gif_path, frames, 'GIF', duration=duration)


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
    :param space: 每一轮迭代的状态
    :param img_dir: 图片的临时保存路径
    :return:
    """
    if not os.path.exists(img_dir):
        os.mkdir(img_dir)
    else:
        delete_dir_contents(img_dir)
    for i in tqdm(range(len(space))):
        cmap = plt.get_cmap('Greys')
        plt.title("iter" + str(i))
        plt.imshow(space[i], interpolation='none', cmap=cmap)
        plt.savefig(os.path.join(img_dir, "img_" + str(i) + ".jpg"), dpi=96)


def get_color2space(colors_dict, gap):
    """
    给矩阵上色
    :param colors_dict: 每种状态对应的颜色
    :param gap: 间隔
    :return:
    """
    datas = read_data("./temp.pkl")
    datas = [datas[i] for i in range(0, len(datas), gap)]
    space = [[] for _ in range(len(datas))]
    for i in range(len(datas)):
        for data in datas[i]:
            cell = data['cell']
            space[i].append(colors_dict[cell['curr'] + str(cell['t'])])
    return np.asarray(space)


if __name__ == '__main__':
    temp = [[1, 2, 3, 4], [5, 6, 7, 8]]
    print(to_2D(temp))

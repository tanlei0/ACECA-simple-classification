# -*- coding: UTF-8 -*-
import matplotlib.pyplot as plt
import imageio
import os
import matplotlib.patches as patches
from tqdm import tqdm


class CA_draw():
    def __init__(self, space, sq_length=1, title="fig", draw=False):
        self.sq_length = sq_length
        self.title = title
        if draw:
            self.drawByRow(space)

    def drawByRow(self, space, save_path=None, file_name=None, show=True):
        fig1 = plt.figure(num=self.title, figsize=(6, 10), dpi=144, facecolor='#FFFFFF', edgecolor='#FF0000')
        plt.xticks([])  # 去掉x轴
        plt.yticks([])  # 去掉y轴
        ax = plt.gca()
        y = len(space)
        x = len(space[0])
        plt.xlim(0, x)
        plt.ylim(0, y)
        for i in range(y):
            for j in range(x):
                if space[i][j] == '1':
                    ax.add_patch(plt.Rectangle((x - j, y - i), self.sq_length, self.sq_length, facecolor='black', edgecolor='r', linewidth=0.1))
                    # ax.add_patch(patches.Rectangle((x - j, y - i), self.sq_length, self.sq_length, color='darkgray', edgecolor='r'))
        if show:
            plt.show()
        if save_path is not None:
            plt.savefig(os.path.join(save_path, file_name))

    @staticmethod
    def delete_dir_contents(img_dir):
        if not os.path.exists(img_dir):
            print("该目录不存在")
        else:
            # 循环删除之前的文件
            files = os.listdir(img_dir)
            for file in files:
                os.remove(os.path.join(img_dir, file))
            print("文件删除完毕！")

    @staticmethod
    def create_gif(img_dir, save_gif_path=None, duration=0.5):
        """
        将多张图片保存为gif动态图
        :param image_list: 图片路径列表
        :param gif_name: 生成的gif文件名
        :return:
        """
        def get_all(path):  # 递归获取指定目录下所有文件的绝对路径（非目录）
            image_list = []
            dir_list = os.listdir(path)
            for i in dir_list:
                sub_dir = os.path.join(path, i)
                if os.path.isdir(sub_dir):
                    get_all(sub_dir)
                else:  # 此时sub_dir是文件的绝对路径
                    image_list.append(sub_dir)
            return image_list

        tmp = get_all(img_dir)
        image_list = []
        for i in tqdm(range(len(tmp))):
            image_list.append(img_dir + "img_" + str(i) + ".jpg")
        frames = []
        for image_name in image_list:
            frames.append(imageio.imread(image_name))
        print(len(frames))
#         frames.reverse()
        imageio.mimsave(save_gif_path, frames, 'GIF', duration=duration)


def generate():
    space = []
    n = 100
    for i in range(n):
        tm = []
        for j in range(n):
            if i == j or i == j * 2 or i == j * 3:
                tm.append('1')
            else:
                tm.append('0')
        space.append(tm)
    return space


if __name__ == '__main__':
    space = generate()
    CA_draw(space, draw=True)

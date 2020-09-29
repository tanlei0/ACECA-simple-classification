# -*- coding: utf-8 -*-
# @Time : 2020/8/19 下午4:46
# @Author : cmk
# @File : acca_asy.py

# ACCA实现异步CA

import copy
import random
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt

from utils import save_data, Flag, getInitState

random.seed(2020)


class Cell:
    def __init__(self, state):
        self.state = state
        # 时间-1, 1, 0 ==> unuse, black flag, white flag
        self.flag = Flag.UNUSED

    def to_dict(self):
        d = {'state': self.state, 'flag': self.flag}
        return d


class EACcell:
    def __init__(self, lcell, cell, rcell, mode):
        self.cell = cell
        self.lcell = lcell
        self.rcell = rcell
        # 模式 B L U
        self.mode = mode

    def group(self):
        return self.lcell.state + self.cell.state + self.rcell.state

    def to_dict(self):
        return {'mode': self.mode, 'cell': self.cell.to_dict(), 'lbuff': self.lcell.to_dict(),
                'rbuff': self.rcell.to_dict()}


class ACCA_ASY(object):
    def __init__(self, rule, init_state='0' * 2 + '1' + '0' * 2, run_num=100):
        """Initialize the CA with the given rule and initial state."""
        # transform the rule number to a binary code (Example: rule 90 is 01011010 in binary code)
        self.binary = f'{rule:08b}'
        self.rule = rule
        self.dict = {
            "111": (self.binary[0]),
            "110": (self.binary[1]),
            "101": (self.binary[2]),
            "100": (self.binary[3]),
            "011": (self.binary[4]),
            "010": (self.binary[5]),
            "001": (self.binary[6]),
            "000": (self.binary[7])
        }

        self.n_cell = len(init_state)

        # 细胞栈，每个cell都有一个栈，每次cell进行no-trival的U时，入栈
        # 输出时，按照列输出，每一列表示该列的所有细胞的U次数相同
        self.state_stack = [[] for _ in range(self.n_cell)]
        self.state_in_sim = []

        # for ring data
        self.init_state = init_state[:-1] + init_state[0]

        self.EACcells = []

        # 初始化细胞
        self.__initCell(self.init_state)

        self.run_num = run_num

        # 用于记录迭代过程中的一些数据
        self.sim_datas = []

    # 初始化细胞
    def __initCell(self, init_state):
        """
        初始化细胞，初始的模式都是B
        :param init_state: 初始的状态
        :return:
        """
        for i in range(0, self.n_cell):
            nei = self.__get_nei_index(i)
            LCell = Cell(init_state[nei[0]])
            cell = Cell(init_state[i])
            RCell = Cell(init_state[nei[1]])
            EACC = EACcell(LCell, cell, RCell, mode='B')
            self.EACcells.append(EACC)

            # 将初始状态添加到栈中
            self.state_stack[i].append(cell.state)

    # 获取邻居的下标
    def __get_nei_index(self, i):
        if i == 0:
            return [self.n_cell - 1, i + 1]
        elif i == self.n_cell - 1:
            return [i - 1, 0]
        else:
            return [i - 1, i + 1]

    # 为细胞随机分配一个模式（L或B或U）
    def __cell_mode_change(self, i):
        """
        为细胞随机分配一个模式
        :param cell: 细胞
        :return:
        """
        mode = ''.join(random.sample('BLU', 1))
        self.EACcells[i].mode = mode

    # ============ L模式 begin ================

    # 修改buff的状态
    def __cell_buff_change(self, i):
        ACcell = self.EACcells[i]
        nei = self.__get_nei_index(i)
        if ACcell.mode == 'L':
            # 左
            if self.EACcells[nei[0]].mode == 'B':
                ACcell.lcell = copy.deepcopy(self.EACcells[nei[0]].cell)
            # 右
            if self.EACcells[nei[1]].mode == 'B':
                ACcell.rcell = copy.deepcopy(self.EACcells[nei[1]].cell)

    # ============ L模式 end ================

    # ============ U模式 begin ================
    # 判断buff是否在某个时间范围
    def __buff_in_ts(self, ACcell, ts, one=False):
        """
        判断buff是否在某个时间范围
        :param ACcell: 细胞
        :param ts: 时间范围
        :return:
        """
        if not one:
            if ACcell.lcell.flag in ts and ACcell.rcell.flag in ts:
                return True
        else:
            if ACcell.lcell.flag in ts or ACcell.rcell.flag in ts:
                return True
        return False

    # 细胞状态改变-U模式 2m2
    def __cell_state_change(self, i):
        ACcell = self.EACcells[i]
        # (1) 加BLACK
        if ACcell.cell.flag == Flag.UNUSED and self.__buff_in_ts(ACcell=ACcell, ts=[Flag.UNUSED], one=False):
            ACcell.cell.flag = Flag.BLACK
        # (2) 加WHITE
        elif ACcell.cell.flag == Flag.UNUSED and self.__buff_in_ts(ACcell=ACcell, ts=[Flag.BLACK], one=True):
            ACcell.cell.flag = Flag.WHITE
        # (3) 去BLACK，更新状态
        elif ACcell.cell.flag == Flag.BLACK and self.__buff_in_ts(ACcell=ACcell, ts=[Flag.WHITE], one=False):
            ACcell.cell.state = self.dict[ACcell.group()]
            ACcell.cell.flag = Flag.UNUSED
        # (4) 去WHITE
        elif ACcell.cell.flag == Flag.WHITE and self.__buff_in_ts(ACcell=ACcell, ts=[Flag.WHITE, Flag.UNUSED],
                                                                  one=False):
            ACcell.cell.flag = Flag.UNUSED
        # (5) 去BLACK
        elif ACcell.cell.flag == Flag.BLACK and self.__buff_in_ts(ACcell=ACcell, ts=[Flag.BLACK], one=True):
            ACcell.cell.flag = Flag.UNUSED
        # (6)
        else:
            pass

    # ============ U模式 end ================

    # ============ 迭代 begin ================
    # 执行一轮迭代
    def __next(self):
        self.current_state = ''

        # 1. 更新模式
        for i in range(self.n_cell):
            self.__cell_mode_change(i)
        # if isPrint:
        #     self.__print_AC(text="")

        # 2. 执行模式
        iter_datas = []
        for i in range(self.n_cell):
            ACcell = self.EACcells[i]
            iter_datas.append(ACcell.to_dict())
            # ### 根据相应的模式执行操作 ###
            # broadcast
            if ACcell.mode == 'B':
                pass
            # listen
            elif ACcell.mode == 'L':
                self.__cell_buff_change(i)
            # update
            elif ACcell.mode == 'U':
                self.__cell_state_change(i)
            self.current_state += ACcell.cell.state
        # 保存中间结果
        self.sim_datas.append(iter_datas)
        return self.current_state

    # 运行
    def run(self, isPrint=True, print_stack=False):
        print("m3...")
        for i in tqdm(range(0, self.run_num)):
            state = self.__next()
            self.state_in_sim.append(state)
        print("")
        # 执行完所有迭代后，再输出迭代结果
        if isPrint:
            if print_stack:
                self.print_stack()
            else:
                for s in self.state_in_sim:
                    print(s.replace("0", " ").replace("1", "*"))

    # ============ 迭代 end ================

    # 打印cell栈
    def print_stack(self):
        l = len(self.state_stack)
        self.ss = []
        min_ = 1000
        for i in range(l):
            min_ = min_ if min_ < len(self.state_stack[i]) else len(self.state_stack[i])
        for i in range(min_):
            state = ""
            for j in range(l):
                state += self.state_stack[j][i]
            print(state.replace("0", " ").replace("1", "*"))
            self.ss.append(state)
        print('最小的U次数：', min_)
        return min_


def get_color2space(colors_dict=None, gap=None, datas=None):
    """
    给矩阵上色
    :param colors_dict: 每种状态对应的颜色
    :param gap: 间隔
    :return:
    """
    if gap is None:
        gap = [1]
    datas = [datas[i] for i in range(0, len(datas), gap)]
    space = [[] for _ in range(len(datas))]
    for i in range(len(datas)):
        for data in datas[i]:
            cell = data['cell']
            # (curr, prev, t) 三元组
            space[i].append(colors_dict[cell['state'] + str(cell['flag'].value)])
    return np.asarray(space)


def plot_space(colors_dict=None, gaps=None, datas=None, save_=False):
    if gaps is None:
        gaps = [1]
    for gap in gaps:
        space = get_color2space(colors_dict, gap, datas=datas)
        plt.figure(figsize=(10, 10))
        plt.title("ACCA_ASY_run={}, cell={},每隔{}取一次".format(len(datas), len(datas[0]), gap))
        cmap = plt.get_cmap('Greys')
        plt.imshow(space, interpolation='none', cmap=cmap)
        if save_:
            plt.savefig("./result/run={}_cell={}_每隔{}取一次.jpg".format(len(datas), len(datas[0]), gap), dpi=300)
        print("plot")
        plt.show()


if __name__ == "__main__":
    colors_dict = {
        # 00 white
        '00': 0,
        '10': 1,
        # 10 black
        '11': 0.8,
        '12': 0.8,

        # lightgray
        '01': 0.5,
        '02': 0.5,
    }
    # init_state = '0' * 48 + '1' + '0' * 48
    init_state = getInitState(100, d_ini=0.5)
    rule = 90
    run_num = 2000
    aceca = ACCA_ASY(rule=90, init_state=init_state, run_num=run_num)
    aceca.run(isPrint=True, print_stack=False)
    # 保存迭代结果
    # save_data(aceca.sim_datas, "./sim_data/rule={}_run={}_cell={}.pkl".format(rule, run_num, len(init_state)))
    plot_space(colors_dict=colors_dict, datas=aceca.sim_datas, gaps=[12], save_=False)

    # 绘制密度
    # plot_dense(datas=aceca.sim_datas, title='m3', save_path="./result/m3_density.jpg")

    # 创建动态图
    # space = get_color2space(colors_dict=None, gap=1, datas=aceca.sim_datas)
    # draw_gif(space=space[:10], img_dir='./tmp/')

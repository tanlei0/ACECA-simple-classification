# -*- coding: utf-8 -*-
# @Time : 2020/7/22 下午6:23
# @Author : cmk
# @File : ECA_ACECA.py
import math

import pandas as pd
from dump_py.ECA_ import *
from plotCA.plot_ca_space import *

random.seed(100)

# todo randomly in every itorate ? independent clocks with mean period and standard deviation ?
class Cell:
    def __init__(self, state, t=0):
        self.curr_state = state
        self.prev_state = state
        self.t = t


class EACcell:
    def __init__(self, lcell, cell, rcell, mode):
        self.cell = cell
        self.lcell = lcell
        self.rcell = rcell
        # 模式 B L U
        self.mode = mode
        self.isCheck = False

    def group(self):
        lstate = self.lcell.curr_state if self.lcell.t == self.cell.t else self.lcell.prev_state
        rstate = self.rcell.curr_state if self.rcell.t == self.cell.t else self.rcell.prev_state
        return lstate + self.cell.state + rstate


class ECA_ACECA:
    def __init__(self, rule, init_state='0' * 50 + '1' + '0' * 50, alpha=1.0, d_ini=0.5, k=0, Ttrs=0, Tsample=100,
                 run_num=100):
        """Initialize the CA with the given rule and initial state."""
        self.binary = f'{rule:08b}'  # transform the rule number to a binary code (Example: rule 90 is 01011010 in binary code)
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

        # for ring data
        self.init_state = init_state[:-1] + init_state[0]

        self.EACcells = []
        # self.__initRandomModel()
        # 存储模式空间
        self.modeSpace = []
        # 初始时期所有细胞为B模式
        self.__initBModel()

        # 初始化细胞
        self.__initCell(self.init_state)

        self.run_num = run_num
        self.alpha = alpha
        self.d_ini = d_ini
        self.k = k
        self.preEACcells = []

        # para for paper
        self.n_1 = []
        self.n_1.append(self.init_state.count('1'))
        self.space = []
        self.space.append(self.init_state)

        self.Ttrs = Ttrs
        self.Tsample = Tsample

    def __initRandomModel(self):
        """
        初始化随机模式
        :return:
        """
        self.init_mode = ''
        for i in range(0, self.n_cell):
            rand = ''.join(random.sample('UBL', 1))
            self.init_mode += rand
        self.current_mode = self.init_mode
        self.modeSpace.append(self.current_mode)

    def __initBModel(self):
        """
        初始化为同一模式B
        :return:
        """
        self.init_mode = ''
        for i in range(0, self.n_cell):
            self.init_mode += 'B'
        self.current_mode = self.init_mode
        self.modeSpace.append(self.current_mode)

    def __initCell(self, init_state):
        for i in range(0, self.n_cell):
            if i == 0:
                LCell = Cell(init_state[self.n_cell - 1])
                cell = Cell(init_state[i])
                RCell = Cell(init_state[i + 1])
            elif i == self.n_cell - 1:
                LCell = Cell(init_state[i - 1])
                cell = Cell(init_state[i])
                RCell = Cell(init_state[i])
            else:
                LCell = Cell(init_state[i - 1])
                cell = Cell(init_state[i])
                RCell = Cell(init_state[i + 1])
            EACC = EACcell(LCell, cell, RCell, mode=self.init_mode[i])
            self.EACcells.append(EACC)

    def __next(self):
        # 保存上一轮迭代的细胞
        self.preEACcells = self.EACcells.copy()
        n_EACcells = len(self.EACcells)
        self.current_state = ''

        for i in range(0, n_EACcells):
            ACcell = self.EACcells[i]
            randNum = np.random.random()

            # print("turn "+str(i)+": ACECA the randNum is "+ str(randNum))

            if randNum >= self.alpha:
                ACcell.isCheck = False
                self.current_state += ACcell.cell.state
            else:
                # 根据模式改变细胞状态
                ACcell.isCheck = True
                if ACcell.cell.mode == 'B':
                    pass
                if ACcell.cell.mode == 'L':
                    self.__cell_buff_change(i)
                if ACcell.cell.mode == 'U':
                    self.__cell_state_change(ACcell)
                self.current_state += ACcell.cell.state
            # 添加字符
        self.n_1.append(self.current_state.count('1'))
        self.space.append(self.current_state)
        return self.current_state

    # 当时为了统一接口用的
    def Next4Turn(self, randN):
        self.preEACcells = self.EACcells.copy()
        n_EACcells = len(self.EACcells)
        self.current_state = ''

        if randN.shape != (self.n_cell,):
            print("randN shape Error")
            return

        for i in range(0, n_EACcells):
            ACcell = self.EACcells[i]
            # print("turn "+str(i)+": ACECA the randNum is "+ str(randNum))

            if randN[i] >= self.alpha:
                ACcell.isCheck = False
                self.current_state += ACcell.cell.state
            else:
                ACcell.isCheck = True
                if ACcell.cell.mode == 'B':
                    pass
                if ACcell.cell.mode == 'L':
                    self.__cell_buff_change(i)
                if ACcell.cell.mode == 'U':
                    self.__cell_state_change(i)
                self.current_state += ACcell.cell.state
            # 添加字符
        self.n_1.append(self.current_state.count('1'))
        self.space.append(self.current_state)
        return self.current_state

    def ALL_MODEL_CHANGE(self):
        self.__all_mode_change()

    # todo modeSpace
    def __cell_mode_change(self, cell):
        """
        为细胞随机分配一个模式
        :param cell: 细胞
        :return:
        """
        mode = ''.join(random.sample('UBL', 1))
        cell.mode = mode

    def __cell_buff_change(self, i):
        ACcell = self.EACcells[i]
        # 需要判断左右邻居的时间差距
        if ACcell.mode == 'L':
            if i == 0:
                if self.preEACcells[self.n_cell - 1].mode == 'B':
                    if self.preEACcells[self.n_cell - 1].t > ACcell.t:
                        # 左buffer的state为左邻居之前的state
                        self.EACcells[i].lcell.state = self.preEACcells[self.n_cell - 1].cell.prev_state
                        self.EACcells[i].lcell.t = (self.EACcells[i].lcell.t + 1) % 3
                    else:
                        # 左buffer的state为左邻居的当前state
                        self.EACcells[i].rcell.state = self.preEACcells[self.n_cell - 1].cell.curr_state
                        self.EACcells[i].rcell.t = (self.EACcells[i].rcell.t + 1) % 3
                if self.preEACcells[i + 1].mode == 'B':
                    if self.preEACcells[i + 1].t > ACcell.t:
                        self.EACcells[i].lcell.state = self.preEACcells[i - 1].cell.prev_state
                        self.EACcells[i].lcell.t = (self.EACcells[i].lcell.t + 1) % 3
                    else:
                        self.EACcells[i].rcell.state = self.preEACcells[i - 1].cell.curr_state
                        self.EACcells[i].rcell.t = (self.EACcells[i].rcell.t + 1) % 3
            elif i == self.n_cell - 1:
                if self.preEACcells[i - 1].mode == 'B':
                    if self.preEACcells[i - 1].t > ACcell.t:
                        self.EACcells[i].lcell.state = self.preEACcells[i - 1].cell.prev_state
                        self.EACcells[i].lcell.t = (self.EACcells[i].lcell.t + 1) % 3
                    else:
                        self.EACcells[i].rcell.state = self.preEACcells[i - 1].cell.curr_state
                        self.EACcells[i].rcell.t = (self.EACcells[i].rcell.t + 1) % 3
                if self.preEACcells[0].mode == 'B':
                    if self.preEACcells[0].t > ACcell.t:
                        self.EACcells[i].lcell.state = self.preEACcells[0].cell.prev_state
                        self.EACcells[i].lcell.t = (self.EACcells[i].lcell.t + 1) % 3
                    else:
                        self.EACcells[i].rcell.state = self.preEACcells[0].cell.curr_state
                        self.EACcells[i].rcell.t = (self.EACcells[i].rcell.t + 1) % 3
            else:
                if self.preEACcells[i - 1].mode == 'B':
                    if self.preEACcells[i - 1].t > ACcell.t:
                        self.EACcells[i].lcell.state = self.preEACcells[i - 1].cell.prev_state
                        self.EACcells[i].lcell.t = (self.EACcells[i].lcell.t + 1) % 3
                    else:
                        self.EACcells[i].rcell.state = self.preEACcells[i - 1].cell.curr_state
                        self.EACcells[i].rcell.t = (self.EACcells[i].rcell.t + 1) % 3
                if self.preEACcells[i + 1].mode == 'B':
                    if self.preEACcells[i + 1].t > ACcell.t:
                        self.EACcells[i].lcell.state = self.preEACcells[i + 1].cell.prev_state
                        self.EACcells[i].lcell.t = (self.EACcells[i].lcell.t + 1) % 3
                    else:
                        self.EACcells[i].rcell.state = self.preEACcells[i + 1].cell.curr_state
                        self.EACcells[i].rcell.t = (self.EACcells[i].rcell.t + 1) % 3

    def __cell_state_change(self, i):
        ACcell = self.EACcells[i]
        if ACcell.cell.mode == 'U':
            if ACcell.delta1 < 1 and ACcell.delta2 < 1 \
                    and self.dict[ACcell.group()] == self.eca.space[ACcell.target[0], ACcell.target[1]]:
                # 目标值坐标改变
                self.EACcells[i] = [ACcell.target[0] + 1, ACcell.target[0]]
                # 保存变化之前的值
                self.EACcells[i].v0 = ACcell.cell.state
                # 更新当前细胞的值
                self.EACcells[i].Cell.state = self.dict[ACcell.group()]
                # 更新时间点
                self.EACcells[i].t = (self.EACcells[i].t + 1) % 3
                # 更新左右之间的差距
                if i == 0:
                    delta1 = math.fabs(self.preEACcells[self.n_cell - 1].t - ACcell.t)
                    delta2 = math.fabs(self.preEACcells[i + 1].t - ACcell.t)
                    self.EACcells[i].delta1 = delta1
                    self.EACcells[i].delta2 = delta2
                    self.preEACcells[self.n_cell - 1].delta2 = delta1
                    self.preEACcells[i + 1].delta1 = delta2
                elif i == self.n_cell - 1:
                    delta1 = math.fabs(self.preEACcells[i - 1].t - ACcell.t)
                    delta2 = math.fabs(self.preEACcells[0].t - ACcell.t)
                    self.EACcells[i].delta1 = delta1
                    self.EACcells[i].delta2 = delta2
                    self.preEACcells[i - 1].delta2 = delta1
                    self.preEACcells[0].delta1 = delta2
                else:
                    delta1 = math.fabs(self.preEACcells[i - 1].t - ACcell.t)
                    delta2 = math.fabs(self.preEACcells[i + 1].t - ACcell.t)
                    self.EACcells[i].delta1 = delta1
                    self.EACcells[i].delta2 = delta2
                    self.preEACcells[i - 1].delta2 = delta1
                    self.preEACcells[i + 1].delta1 = delta2

    def __all_mode_change(self):
        self.current_mode = ''
        for ACcell in self.EACcells:
            if ACcell.isCheck is True:
                # 为细胞随机分配一个模式
                self.__cell_mode_change(ACcell.cell)
            self.current_mode += ACcell.cell.mode

        self.modeSpace.append(self.current_mode)

    def __all_mode_change_2(self):
        # 'B'->'L'->'U'
        pass

    def __isFitTarget(self):
        for i in range(0, len(self.EACcells)):
            if self.EACcells[i].LCell.target != self.EACcells[i].LCell.state:
                return False
            if self.EACcells[i].Cell.target != self.EACcells[i].Cell.state:
                return False
            if self.EACcells[i].RCell.target != self.EACcells[i].RCell.state:
                return False
            return True

    def run(self, isPrint=True):
        if isPrint is True:
            print(self.init_state.replace("0", " ").replace("1", "*"))  # print the first line
        while True:
            if isPrint is True:
                print(self.__next().replace("0", " ").replace("1", "*"))
            else:
                self.__next()
            # 为细胞随机分配模式
            self.__all_mode_change()
            if self.__isFitTarget():
                break

    def getu(self):
        # run_num 个时间的密度 den
        den = np.array(self.n_1) / self.n_cell
        u = 1.0 / self.Tsample * den[self.Ttrs:self.Ttrs + self.Tsample].sum()
        return u

    def getModelRatio(self, isDraw=False):
        modeRatio = []
        for row in self.modeSpace:
            mode_B = row.count('B') / self.n_cell
            mode_L = row.count('L') / self.n_cell
            mode_U = row.count("U") / self.n_cell
            modeRatio.append({'B': mode_B, 'L': mode_L, 'U': mode_U})
        if isDraw is True:
            df = pd.DataFrame(modeRatio)
            fig = df.plot.line()
            fig.lines[0].set_linestyle('-')
            fig.lines[1].set_linestyle('--')
            fig.lines[2].set_linestyle('-.')
            plt.xlabel("Iteration")
            plt.ylabel("Ratio")
            plt.plot([0, 100], [1 / 3, 1 / 3], linestyle=':')
            plt.legend(["B", 'L', 'U', 'ratio=0.3333'])
        return modeRatio

    def reset(self, **kargs):
        if "alpha" in kargs.keys():
            self.alpha = kargs['alpha']

        if "init_state" in kargs.keys():
            init_state = kargs['init_state']
            self.n_cell = len(init_state)
            self.init_state = init_state[:-1] + init_state[0]

            self.EACcells = []

            self.modeSpace = []
            self.__initBModel()

            self.__initCell(self.init_state)

        if "rule" in kargs.keys():
            rule = kargs['rule']
            self.binary = f'{rule:08b}'
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
        if "run_num" in kargs.keys():
            self.run_num = kargs['run_num']

        # clear and re assign
        self.preEACcells = []

        self.n_1 = []
        self.n_1.append(self.init_state.count('1'))
        self.space = []
        self.space.append(self.init_state)


def getInitState(n_cell, d_ini):
    init_state = ''
    for i in range(0, n_cell):
        rand = np.random.rand()
        if rand >= d_ini:
            init_state += '0'
        else:
            init_state += '1'
    return init_state


if __name__ == "__main__":
    # init_state = getInitState(100, d_ini=0.5)
    init_state = '0' * 2 + '1' + '0' * 2
    # init_state = '0' * 48 + '1' + '0' * 48
    aceca = ECA_ACECA(90, init_state=init_state, alpha=1)
    # aceca.run()
    # space = aceca.space
    # aceca.eca.run(isPrint=False)
    # CA_draw(aceca.eca.space)
    aceca.run(isPrint=True)

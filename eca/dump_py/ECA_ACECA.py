# -*- coding: utf-8 -*-
# @Time : 2020/7/22 下午6:23
# @Author : cmk
# @File : ECA_ACECA.py
import math

import pandas as pd
from dump_py.ECA_ import *
from plotCA.plot_ca_space import *


# todo randomly in every itorate ? independent clocks with mean period and standard deviation ?
class Cell:
    def __init__(self, state, t=0, mode=0):
        self.state = state
        self.t = t
        self.mode = mode


class EACcell:
    def __init__(self, LCell, Cell, RCell):
        self.LCell = LCell
        self.Cell = Cell
        self.RCell = RCell

    def group(self):
        return self.LCell.state + self.Cell.state + self.RCell.state


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

        # 创建ECA
        # self.eca = ECA(rule=rule, init_state=init_state, alpha=alpha, d_ini=d_ini, k=k, Ttrs=Ttrs, Tsample=Tsample, run_num=run_num, ACECA=True)

        self.n_cell = len(init_state)

        # for ring data 
        self.init_state = init_state[:-1] + init_state[0]

        # # 创建ECA
        self.eca = ECA(rule=rule, init_state=self.init_state, alpha=alpha, d_ini=d_ini, k=k, Ttrs=Ttrs, Tsample=Tsample,
                       ACECA=True)
        self.eca.run(isPrint=False)

        self.EACcells = []
        # self.__initRandomModel()
        # 存储模式空间
        self.modelSpace = []
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
        self.init_model = ''
        for i in range(0, self.n_cell):
            rand = ''.join(random.sample('UBL', 1))
            self.init_model += rand
        self.current_model = self.init_model
        self.modelSpace.append(self.current_model)

    def __initBModel(self):
        """
        初始化为同一模式B
        :return:
        """
        self.init_model = ''
        for i in range(0, self.n_cell):
            self.init_model += 'B'
        self.current_model = self.init_model
        self.modelSpace.append(self.current_model)

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
            EACC = EACcell(LCell, cell, RCell, model=self.init_model[i], j=i)
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
                self.current_state += ACcell.Cell.state
            else:
                # 根据模式改变细胞状态
                ACcell.isCheck = True
                if ACcell.Cell.model == 'B':
                    pass
                if ACcell.Cell.model == 'L':
                    self.__cell_buff_change(i)
                if ACcell.Cell.model == 'U':
                    self.__cell_state_change(ACcell)
                self.current_state += ACcell.Cell.state
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
                self.current_state += ACcell.Cell.state
            else:
                ACcell.isCheck = True
                if ACcell.Cell.model == 'B':
                    pass
                if ACcell.Cell.model == 'L':
                    self.__cell_buff_change(i)
                if ACcell.Cell.model == 'U':
                    self.__cell_state_change(i)
                self.current_state += ACcell.Cell.state
            # 添加字符
        self.n_1.append(self.current_state.count('1'))
        self.space.append(self.current_state)
        return self.current_state

    def ALL_MODEL_CHANGE(self):
        self.__all_model_change()

    # todo modelSpace
    def __cell_model_change(self, cell):
        """
        为细胞随机分配一个模式
        :param cell: 细胞
        :return:
        """
        model = ''.join(random.sample('UBL', 1))
        cell.model = model

    def __cell_buff_change(self, i):
        ACcell = self.EACcells[i]
        # 需要判断左右邻居的时间差距
        if ACcell.model == 'L':
            if i == 0:
                if self.preEACcells[self.n_cell - 1].model == 'B':
                    if self.preEACcells[self.n_cell - 1].t > ACcell.t:
                        self.EACcells[i].LCell.state = self.preEACcells[self.n_cell - 1].v0
                    else:
                        self.EACcells[i].LCell.state = self.preEACcells[self.n_cell - 1].Cell.state
                if self.preEACcells[i + 1].model == 'B':
                    if self.preEACcells[i + 1].t > ACcell.t:
                        self.EACcells[i].RCell.state = self.preEACcells[i - 1].v0
                    else:
                        self.EACcells[i].RCell.state = self.preEACcells[i - 1].Cell.state
            elif i == self.n_cell - 1:
                if self.preEACcells[i - 1].model == 'B':
                    if self.preEACcells[i - 1].t > ACcell.t:
                        self.EACcells[i].LCell.state = self.preEACcells[i - 1].v0
                    else:
                        self.EACcells[i].LCell.state = self.preEACcells[i - 1].Cell.state
                if self.preEACcells[0].model == 'B':
                    if self.preEACcells[0].t > ACcell.t:
                        self.EACcells[i].RCell.state = self.preEACcells[0].v0
                    else:
                        self.EACcells[i].RCell.state = self.preEACcells[0].Cell.state
            else:
                if self.preEACcells[i - 1].model == 'B':
                    if self.preEACcells[i - 1].t > ACcell.t:
                        self.EACcells[i].LCell.state = self.preEACcells[i - 1].v0
                    else:
                        self.EACcells[i].LCell.state = self.preEACcells[i - 1].Cell.state
                if self.preEACcells[i + 1].model == 'B':
                    if self.preEACcells[i + 1].t > ACcell.t:
                        self.EACcells[i].RCell.state = self.preEACcells[i + 1].v0
                    else:
                        self.EACcells[i].RCell.state = self.preEACcells[i + 1].Cell.state

                # if self.preEACcells[i - i].model == 'B':
                #     self.EACcells[i].LCell.state = self.preEACcells[i - 1].Cell.state
                # if self.preEACcells[i + 1].Cell.model == 'B':
                #     self.EACcells[i].RCell.state = self.preEACcells[i + 1].Cell.state

    def __cell_state_change(self, i):
        ACcell = self.EACcells[i]
        if ACcell.Cell.model == 'U':
            # 细胞达到最终目标后，不再改变
            if ACcell.target[0] > len(self.eca.space) - 1:
                self.EACcells[i].isFinal = True
                return
            if ACcell.delta1 < 1 and ACcell.delta2 < 1 \
                    and self.dict[ACcell.group()] == self.eca.space[ACcell.target[0], ACcell.target[1]]:
                # 目标值坐标改变
                self.EACcells[i] = [ACcell.target[0] + 1, ACcell.target[0]]
                # 保存变化之前的值
                self.EACcells[i].v0 = ACcell.Cell.state
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

    def __all_model_change(self):
        self.current_model = ''
        for ACcell in self.EACcells:
            if ACcell.isCheck is True:
                # 为细胞随机分配一个模式
                self.__cell_model_change(ACcell.Cell)
            self.current_model += ACcell.Cell.model

        self.modelSpace.append(self.current_model)

    def __all_model_change_2(self):
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
        for i in range(1, len(self.eca.space)):
            while True:
                if isPrint is True:
                    print(self.__next().replace("0", " ").replace("1", "*"))
                else:
                    self.__next()
                # 为细胞随机分配模式
                self.__all_model_change()
                if self.__isFitTarget():
                    break

    def getu(self):
        # run_num 个时间的密度 den
        den = np.array(self.n_1) / self.n_cell
        u = 1.0 / self.Tsample * den[self.Ttrs:self.Ttrs + self.Tsample].sum()
        return u

    def getModelRatio(self, isDraw=False):
        modelRatio = []
        for row in self.modelSpace:
            model_B = row.count('B') / self.n_cell
            model_L = row.count('L') / self.n_cell
            model_U = row.count("U") / self.n_cell
            modelRatio.append({'B': model_B, 'L': model_L, 'U': model_U})
        if isDraw is True:
            df = pd.DataFrame(modelRatio)
            fig = df.plot.line()
            fig.lines[0].set_linestyle('-')
            fig.lines[1].set_linestyle('--')
            fig.lines[2].set_linestyle('-.')
            plt.xlabel("Iteration")
            plt.ylabel("Ratio")
            plt.plot([0, 100], [1 / 3, 1 / 3], linestyle=':')
            plt.legend(["B", 'L', 'U', 'ratio=0.3333'])
        return modelRatio

    def reset(self, **kargs):
        if "alpha" in kargs.keys():
            self.alpha = kargs['alpha']

        if "init_state" in kargs.keys():
            init_state = kargs['init_state']
            self.n_cell = len(init_state)
            self.init_state = init_state[:-1] + init_state[0]

            self.EACcells = []

            self.modelSpace = []
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
    init_state = getInitState(100, d_ini=0.5)
    aceca = ECA_ACECA(50, init_state=init_state, alpha=1)
    # aceca.run()
    # space = aceca.space
    # aceca.eca.run(isPrint=False)
    # CA_draw(aceca.eca.space)
    aceca.run(isPrint=True)

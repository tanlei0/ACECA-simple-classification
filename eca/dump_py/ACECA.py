# -*- coding: utf-8 -*-
# @Time    : 2019/5/29 23:27
# @Author  : tanlei0
# @FileName: ACECA.py
#
import numpy
import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt

random.seed(100)

# todo randomly in every itorate ? independent clocks with mean period and standard deviation ?
class Cell:
    def __init__(self, state, model):
        self.state = state
        self.model = model


class ACcell:
    def __init__(self, LCell, Cell, RCell):
        self.LCell = LCell
        self.Cell = Cell
        self.RCell = RCell
        self.isCheck = True

    def group(self):
        return self.LCell.state + self.Cell.state + self.RCell.state


class ACECA:
    def __init__(self, rule, init_state='0' * 48 + '1' + '0' * 48, alpha=1.0, d_ini=0.5, k=0, Ttrs=0, Tsample=100,
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

        self.ACcells = []
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
        self.preACcells = []

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
                LCell = Cell(init_state[self.n_cell - 1], model=self.init_model[self.n_cell - 1])
                cell = Cell(init_state[i], model=self.init_model[i])
                RCell = Cell(init_state[i + 1], model=self.init_model[i + 1])
            elif i == self.n_cell - 1:
                LCell = Cell(init_state[i - 1], model=self.init_model[i - 1])
                cell = Cell(init_state[0], model=self.init_model[0])
                RCell = Cell(init_state[0], model=self.init_model[0])
            else:
                LCell = Cell(init_state[i - 1], model=self.init_model[i - 1])
                cell = Cell(init_state[i], model=self.init_model[i])
                RCell = Cell(init_state[i + 1], model=self.init_model[i + 1])
            ACC = ACcell(LCell, cell, RCell)
            self.ACcells.append(ACC)

    def __next(self):
        # 保存上一轮迭代的细胞
        self.preACcells = self.ACcells.copy()
        n_ACcells = len(self.ACcells)
        self.current_state = ''

        for i in range(0, n_ACcells):
            ACcell = self.ACcells[i]
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
        ACcell = self.ACcells[i]
        if ACcell.Cell.model == 'L':
            if i == 0:
                if self.preACcells[self.n_cell - 1].Cell.model == 'B':
                    ACcell.LCell = self.preACcells[self.n_cell - 1].Cell
                if self.preACcells[i + 1].Cell.model == 'B':
                    ACcell.RCell = self.preACcells[i + 1].Cell
            elif i == self.n_cell - 1:
                if self.preACcells[i - i].Cell.model == 'B':
                    ACcell.LCell = self.preACcells[i - 1].Cell
                if self.preACcells[0].Cell.model == 'B':
                    ACcell.RCell = self.preACcells[0].Cell
            else:
                if self.preACcells[i - i].Cell.model == 'B':
                    ACcell.LCell = self.preACcells[i - 1].Cell
                if self.preACcells[i + 1].Cell.model == 'B':
                    ACcell.RCell = self.preACcells[i + 1].Cell

    def __cell_state_change(self, ACcell):
        if ACcell.Cell.model == 'U':
            ACcell.Cell.state = self.dict[ACcell.group()]

    def __all_model_change(self):
        self.current_model = ''
        for ACcell in self.ACcells:
            # 模式已经用过，则分配新模式，否则沿用旧模式
            if ACcell.isCheck is True:
                # 为细胞随机分配一个模式
                self.__cell_model_change(ACcell.Cell)
            self.current_model += ACcell.Cell.model

        self.modelSpace.append(self.current_model)

    def __all_model_change_2(self):
        # 'B'->'L'->'U'
        pass

    def run(self, isPrint=True):
        if isPrint is True:
            print(self.init_state.replace("0", " ").replace("1", "*"))  # print the first line
        for i in range(1, self.run_num):
            if isPrint is True:
                print(self.__next().replace("0", " ").replace("1", "*"))
            else:
                self.__next()
            # 为细胞随机分配模式
            self.__all_model_change()

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

            self.ACcells = []

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
        self.preACcells = []

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
    # init_state = '0' * 2 + '1' + '0' * 2
    init_state = '0' * 48 + '1' + '0' * 48
    aceca = ACECA(rule=90, init_state=init_state, alpha=1, run_num=300)
    # aceca = ACECA(rule=90)
    aceca.run(isPrint=True)
    space = [[int(s) for s in sp] for sp in aceca.space]
    # plt.figure(figsize=(19.2, 10.8))
    cmap = plt.get_cmap('Greys')
    plt.title("ACA")
    plt.imshow(space, interpolation='none', cmap=cmap)
    plt.show()

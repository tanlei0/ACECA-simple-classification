import pandas as pd
from dump_py.ECA_ import *
from plotCA.plot_ca_space import *

random.seed(100)


# todo randomly in every itorate ? independent clocks with mean period and standard deviation ?
class Cell:
    def __init__(self, state, t=0):
        self.curr_state = state
        # -1代表停用该状态
        self.prev_state = -1
        # 时间0, 1, 2
        self.t = t


class EACcell:
    def __init__(self, lcell, cell, rcell, mode):
        self.cell = cell
        self.lcell = lcell
        self.rcell = rcell
        # 模式 B L U
        self.mode = mode

    def group(self):
        # lstate = self.lcell.curr_state if self.lcell.t == self.cell.t else self.lcell.prev_state
        # rstate = self.rcell.curr_state if self.rcell.t == self.cell.t else self.rcell.prev_state
        # 对于buff来说，只保留curr_state
        lstate = self.lcell.curr_state
        rstate = self.rcell.curr_state
        return lstate + self.cell.curr_state + rstate


class ECA_ACECA:
    def __init__(self, rule, init_state='0' * 2 + '1' + '0' * 2, alpha=1.0, d_ini=0.5, k=0, Ttrs=0, Tsample=100,
                 run_num=200):
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

        # for ring data
        self.init_state = init_state[:-1] + init_state[0]

        self.EACcells = []
        # self.__initRandomModel()
        # 存储模式空间
        self.modeSpace = []
        # 初始时期所有细胞为B模式
        self.__initBMode()

        # 初始化细胞
        self.__initCell(self.init_state)

        self.run_num = run_num
        self.alpha = alpha
        self.d_ini = d_ini
        self.k = k
        self.preEACcells = []
        self.cells_in_process = []

        self.space = []
        self.space.append(self.init_state)
        self.len = len(self.space[0])
        self.Ttrs = Ttrs
        self.Tsample = Tsample

        self.ucount = [0 for i in range(self.n_cell)]
        self.lock_step = 1

    # 初始化B模式
    def __initBMode(self):
        """
        初始化为同一模式B
        :return:
        """
        self.init_mode = ''
        for i in range(0, self.n_cell):
            self.init_mode += 'B'
        self.current_mode = self.init_mode
        self.modeSpace.append(self.current_mode)

    # 初始化细胞
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

    # 为细胞随机分配一个模式（L或B）
    def __cell_mode_change(self, i):
        """
        为细胞随机分配一个模式
        :param cell: 细胞
        :return:
        """
        mode = ''.join(random.sample('BL', 1))
        self.EACcells[i].mode = mode

    # 修改某个具体的buff
    def __change_buff(self, neiACell, buff):
        """
        根据邻居修改buff, 邻居的时间要>buff
        :param neiACell: 邻居细胞
        :param buff: 当前细胞的buff
        :return: 修改后的buff
        """
        if neiACell.cell.t > buff.t:
            prev = neiACell.cell.prev_state
            curr = neiACell.cell.curr_state
            # 更新buffer的状态
            # 做邻居有prev则取prev，否则取curr
            # buff.curr_state = curr if prev == -1 else prev
            buff.curr_state = curr if prev == -1 else prev
            # 更新buffer的时间
            buff.t = (buff.t + 1) % 3
        return buff

    def __get_nei_index(self, i):
        if i == 0:
            return [self.n_cell - 1, i + 1]
        elif i == self.n_cell - 1:
            return [i - 1, 0]
        else:
            return [i - 1, i + 1]

    # 修改某个细胞的左右buff
    def __cell_buff_change(self, i):
        ACcell = self.EACcells[i]
        nei = self.__get_nei_index(i)
        # 需要判断左右邻居和buff的时间差距
        if ACcell.mode == 'L':
            # 左
            if self.EACcells[nei[0]].mode == 'B':
                ACcell.lcell = self.__change_buff(self.EACcells[nei[0]], ACcell.lcell)
            # 右
            if self.EACcells[nei[1]].mode == 'B':
                ACcell.rcell = self.__change_buff(self.EACcells[nei[1]], ACcell.rcell)

    # cell_buff_change.bak
    # def __cell_buff_change(self, i):
    #     ACcell = self.EACcells[i]
    #     # 需要判断左右邻居和buff的时间差距
    #     if ACcell.mode == 'L':
    #         if i == 0:
    #             # 左
    #             if self.EACcells[self.n_cell - 1].mode == 'B':
    #                 ACcell.lcell = self.__change_buff(self.EACcells[self.n_cell - 1], ACcell.lcell)
    #             # 右
    #             if self.EACcells[i + 1].mode == 'B':
    #                 ACcell.rcell = self.__change_buff(self.EACcells[i + 1], ACcell.rcell)
    #         elif i == self.n_cell - 1:
    #             # 左
    #             if self.EACcells[i - 1].mode == 'B':
    #                 ACcell.lcell = self.__change_buff(self.EACcells[i - 1], ACcell.lcell)
    #             # 右
    #             if self.EACcells[0].mode == 'B':
    #                 ACcell.rcell = self.__change_buff(self.EACcells[0], ACcell.rcell)
    #         else:
    #             # 左
    #             if self.EACcells[i - 1].mode == 'B':
    #                 ACcell.lcell = self.__change_buff(self.EACcells[i - 1], ACcell.lcell)
    #             # 右
    #             if self.EACcells[i + 1].mode == 'B':
    #                 ACcell.rcell = self.__change_buff(self.EACcells[i + 1], ACcell.rcell)

    # U模式时，改变细胞的当前状态

    def __cell_state_change(self, i):
        ACcell = self.EACcells[i]
        nei = self.__get_nei_index(i)
        if abs(ACcell.cell.t - self.EACcells[nei[0]].cell.t) <= 1 and abs(ACcell.cell.t - self.EACcells[nei[1]].cell.t) <= 1 \
                and abs(ACcell.cell.t - ACcell.lcell.t) <= 1 and abs(ACcell.cell.t - ACcell.rcell.t) <= 1:
            ACcell.cell.t = (ACcell.cell.t + 1) % 3
            # t为1时，保留先前的状态
            ACcell.cell.prev_state = -1 if ACcell.cell.t != 1 else ACcell.cell.curr_state
            ACcell.cell.curr_state = self.dict[ACcell.group()]

    # 执行一轮迭代
    def __next(self):
        # 保存上一轮迭代的细胞
        self.preEACcells = self.EACcells.copy()
        self.cells_in_process.append(self.preEACcells)
        n_EACcells = len(self.EACcells)
        self.current_state = ''

        for i in range(0, n_EACcells):
            ACcell = self.EACcells[i]

            # ### 判断时间，更改模式 ###
            # buffer和cell的时间相等，则更改细胞的模式为U
            # 否则为细胞在L和B中随机选择一个模式
            if self.ucount[i] == self.lock_step:
                ACcell.mode = "B"
            else:
                if ACcell.lcell.t == ACcell.cell.t and ACcell.cell.t == ACcell.rcell.t:
                    ACcell.mode = "U"
                else:
                    # B和L中随机选择一个
                    self.__cell_mode_change(i)

            # # ### 根据相应的模式执行操作 ###
            # # broadcast
            # if ACcell.mode == 'B':
            #     pass
            # # listen
            # if ACcell.mode == 'L':
            #     self.__cell_buff_change(i)
            # # update
            # if ACcell.mode == 'U':
            #     self.__cell_state_change(i)
            # self.current_state += ACcell.cell.curr_state
        for i in range(0, n_EACcells):
            ACcell = self.EACcells[i]
            # ### 根据相应的模式执行操作 ###
            # broadcast
            if ACcell.mode == 'B':
                pass
            # listen
            if ACcell.mode == 'L':
                self.__cell_buff_change(i)
            # update
            if ACcell.mode == 'U':
                self.__cell_state_change(i)
                self.ucount[i] += 1
            self.current_state += ACcell.cell.curr_state
        self.space.append(self.current_state)
        return self.current_state

    # 运行
    def run(self, isPrint=True):
        if isPrint is True:
            print(self.init_state.replace("0", " ").replace("1", "*"))  # print the first line
        for i in range(1, self.run_num):
            if isPrint is True:
                count = 0
                for k in range(self.n_cell):
                    if self.ucount[k] == self.lock_step:
                        count += 1
                if count == self.n_cell:
                    self.ucount = [0 for _ in range(self.n_cell)]
                    print(self.__next().replace("0", " ").replace("1", "*"))
                else:
                    self.__next()
            else:
                self.__next()
            # 为细胞随机分配模式
            # self.__all_mode_change()

    # ################### 暂时未用到的方法 #######################

    def ALL_MODEL_CHANGE(self):
        self.__all_mode_change()

    def __all_mode_change(self):
        self.current_mode = ''
        for ACcell in self.EACcells:
            if ACcell.isCheck is True:
                # 为细胞随机分配一个模式
                self.__cell_mode_change(ACcell.Cell)
            self.current_mode += ACcell.Cell.mode

        self.modeSpace.append(self.current_mode)

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

    @staticmethod
    def getInitState(n_cell, d_ini):
        init_state = ''
        for i in range(0, n_cell):
            rand = np.random.rand()
            if rand >= d_ini:
                init_state += '0'
            else:
                init_state += '1'
        return init_state

    def __initRandomMode(self):
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

    # ################### end #######################


if __name__ == "__main__":
    # init_state = ECA_ACECA.getInitState(100, d_ini=0.5)
    # aceca = ECA_ACECA(rule=50, init_state=init_state, alpha=1)
    aceca = ECA_ACECA(rule=90, alpha=1)
    # print(aceca.dict)
    # aceca.run()
    # space = aceca.space
    # aceca.eca.run(isPrint=False)
    # CA_draw(aceca.eca.space)
    aceca.run(isPrint=True)
    print(aceca.ucount)

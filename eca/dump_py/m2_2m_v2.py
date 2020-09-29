import copy
import random


# ######### 和m2_2m.py的区别 ######
# 在EACcell.group方法中考虑了时间差异，
# 即buffer大于当前细胞则取prev，否则取curr
# ################################
from tqdm import tqdm

random.seed(2020)
from utils import save_data, plot_space, plot_dense


class Cell:
    def __init__(self, state, t=0):
        self.curr_state = state
        self.prev_state = state
        # 时间0, 1, 2
        self.t = t

    # ## 记录中间结果使用
    def to_string(self):
        return "({},{},{})".format(self.prev_state, self.curr_state, self.t)

    # ## 记录中间结果使用
    def to_dict(self):
        d = {'curr': self.curr_state, 'prev': self.prev_state, 't': self.t}
        return d


class EACcell:
    def __init__(self, lcell, cell, rcell, mode):
        self.cell = cell
        self.lcell = lcell
        self.rcell = rcell
        # 模式 B L U
        self.mode = mode

    def group(self):
        # buff和cell同时间取curr，否则取prev
        lstate = str(self.lcell.curr_state if self.lcell.t == self.cell.t else self.lcell.prev_state)
        rstate = str(self.rcell.curr_state if self.rcell.t == self.cell.t else self.rcell.prev_state)
        return lstate + self.cell.curr_state + rstate

    # ## 记录中间结果使用
    def to_string(self):
        return "([{},{},{}],{})".format(self.lcell.to_string(), self.cell.to_string(), self.rcell.to_string(),
                                        self.mode)

    # ## 记录中间结果使用
    def to_dict(self):
        return {'mode': self.mode, 'cell': self.cell.to_dict(), 'lbuff': self.lcell.to_dict(),
                'rbuff': self.rcell.to_dict()}


class ECA_ACECA_M2_V2:
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
            self.state_stack[i].append(cell.curr_state)

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

    # 修改某个具体的buff
    def __change_buff(self, neiACell, buff):
        """
        根据邻居修改buff, 邻居的时间要>buff
        :param neiACell: 邻居细胞
        :param buff: 当前细胞的buff
        :return: 修改后的buff
        """
        buff = copy.deepcopy(neiACell.cell)
        return buff

    # 判断buff是否在某个时间范围
    def __buff_in_ts(self, ACcell, ts):
        """
        判断buff是否在某个时间范围
        :param ACcell: 细胞
        :param ts: 时间范围
        :return:
        """
        if ACcell.lcell.t in ts and ACcell.rcell.t in ts:
            return True
        return False

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

    # ============ U模式 begin ===============
    # m2 + 2m
    def __cell_state_change(self, i):
        ACcell = self.EACcells[i]
        if ACcell.cell.t == 0 and self.__buff_in_ts(ACcell, [0, 1]):
            ACcell.cell.curr_state = ACcell.cell.curr_state
            ACcell.cell.prev_state = self.dict[ACcell.group()]
            ACcell.cell.t = (ACcell.cell.t + 1) % 3
            # no-trival的U，添加到相应的栈中
            self.state_stack[i].append(ACcell.cell.curr_state)
        elif ACcell.cell.t == 1 and self.__buff_in_ts(ACcell, [1, 2]):
            ACcell.cell.curr_state = ACcell.cell.prev_state
            ACcell.cell.t = (ACcell.cell.t + 1) % 3
            # no-trival的U，添加到相应的栈中
            self.state_stack[i].append(ACcell.cell.curr_state)
        elif ACcell.cell.t == 2 and self.__buff_in_ts(ACcell, [2, 0]):
            ACcell.cell.t = (ACcell.cell.t + 1) % 3
            # no-trival的U，添加到相应的栈中
            self.state_stack[i].append(ACcell.cell.curr_state)

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
        temp = []
        for i in range(self.n_cell):
            ACcell = self.EACcells[i]
            temp.append(ACcell.to_dict())
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
            self.current_state += ACcell.cell.curr_state
        self.sim_datas.append(temp)
        return self.current_state

    # 运行
    def run(self, isPrint=True, print_stack=False):
        print("\nm2_2m_v2...")
        for i in tqdm(range(0, self.run_num)):
            state = self.__next()
            self.state_in_sim.append(state)

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
        # 记录用空格和*替换后的状态
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


if __name__ == "__main__":
    # init_state = '0' * 50 + '1' + '0' * 49
    init_state = '0' * 48 + '1' + '0' * 48
    rule = 90
    run_num = 2000
    aceca = ECA_ACECA_M2_V2(rule=90, init_state=init_state, run_num=run_num)
    aceca.run(isPrint=True, print_stack=True)
    # 保存迭代结果
    # save_data(aceca.sim_datas, "./sim_data/rule={}_run={}_cell={}.pkl".format(rule, run_num, len(init_state)))
    plot_space(title='m2+2m_v2', datas=aceca.sim_datas, gaps=[12], save_=False)

    # 绘制密度
    # plot_dense(datas=aceca.sim_datas, title='m2+2m_v2', save_path="./result/m2+2m_v2_density.jpg")

    # 创建动态图 init_state长要符合 len = N x N
    # space = get_color2space(colors_dict=None, gap=1, datas=aceca.sim_datas)
    # draw_gif(space=space[:10], img_dir='./tmp/')

import copy
import random

from utils import *

# ######### 和m2_2m ######
# ################################


class Cell:
    def __init__(self, state, t=0):
        self.curr_state = state
        self.prev_state = state
        # time: 0, 1, 2
        self.t = t

    def to_string(self):
        return "({},{},{})".format(self.prev_state, self.curr_state, self.t)

    def to_dict(self):
        d = {'curr': self.curr_state, 'prev': self.prev_state, 't': self.t}
        return d


class EACcell:
    def __init__(self, lcell, cell, rcell, mode):
        self.cell = cell
        self.lcell = lcell
        self.rcell = rcell
        # mode: B L U
        self.mode = mode

    def group(self):
        lstate = self.lcell.curr_state
        rstate = self.rcell.curr_state
        return lstate + self.cell.curr_state + rstate

    def to_string(self):
        return "([{},{},{}],{})".format(self.lcell.to_string(), self.cell.to_string(), self.rcell.to_string(),
                                        self.mode)

    def to_dict(self):
        return {'mode': self.mode, 'cell': self.cell.to_dict(), 'lbuff': self.lcell.to_dict(),
                'rbuff': self.rcell.to_dict()}


class ECA_ACECA_M2:
    def __init__(self, rule, init_state='0' * 2 + '1' + '0' * 2, run_num=100, alpha=1., clean=False):
        self.clean = clean
        random.seed(2020)
        """Initialize the CA with the given rule and initial state."""
        # transform the rule number to a binary code (Example: rule 90 is 01011010 in binary code)
        self.iter_nums = 0
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
        self.alpha = alpha
        self.n_cell = len(init_state)

        self.state_stack = [[] for _ in range(self.n_cell)]
        self.state_in_sim = []

        # for ring data
        self.init_state = init_state[:-1] + init_state[0]

        self.EACcells = []

        self.__initCell(self.init_state)

        self.run_num = run_num

        self.sim_datas = []

    # initiate cells
    def __initCell(self, init_state):
        """
        the initial modes of all cells are 'B'
        :param init_state:
        :return:
        """
        for i in range(0, self.n_cell):
            nei = self.__get_nei_index(i)
            LCell = Cell(init_state[nei[0]])
            cell = Cell(init_state[i])
            RCell = Cell(init_state[nei[1]])
            EACC = EACcell(LCell, cell, RCell, mode='B')
            self.EACcells.append(EACC)

            # push initial states to stack
            self.state_stack[i].append(cell.curr_state)

    # get neighboorhood's index
    def __get_nei_index(self, i):
        if i == 0:
            return [self.n_cell - 1, i + 1]
        elif i == self.n_cell - 1:
            return [i - 1, 0]
        else:
            return [i - 1, i + 1]

    # assign a random mode
    def __cell_mode_change(self, i):
        mode = ''.join(random.sample('BLU', 1))
        self.EACcells[i].mode = mode

    # ============ L begin ================

    def __change_buff(self, neiACell, buff):
        buff = copy.deepcopy(neiACell.cell)
        return buff

    def __buff_in_ts(self, ACcell, ts):
        if ACcell.lcell.t in ts and ACcell.rcell.t in ts:
            return True
        return False

    def __cell_buff_change(self, i):
        ACcell = self.EACcells[i]
        nei = self.__get_nei_index(i)
        if ACcell.mode == 'L':
            # left
            if self.EACcells[nei[0]].mode == 'B':
                ACcell.lcell = copy.deepcopy(self.EACcells[nei[0]].cell)
            # right
            if self.EACcells[nei[1]].mode == 'B':
                ACcell.rcell = copy.deepcopy(self.EACcells[nei[1]].cell)

    # ============ L end ================

    # ============ U begin ===============
    # m2 + 2m
    def __cell_state_change(self, i):
        ACcell = self.EACcells[i]
        if ACcell.cell.t == 0 and self.__buff_in_ts(ACcell, [0, 1]):
            ACcell.cell.curr_state = ACcell.cell.curr_state
            ACcell.cell.prev_state = self.dict[ACcell.group()]
            ACcell.cell.t = (ACcell.cell.t + 1) % 3
            # no-trival U
            self.state_stack[i].append(ACcell.cell.curr_state)
        elif ACcell.cell.t == 1 and self.__buff_in_ts(ACcell, [1, 2]):
            ACcell.cell.curr_state = ACcell.cell.prev_state
            ACcell.cell.t = (ACcell.cell.t + 1) % 3
        elif ACcell.cell.t == 2 and self.__buff_in_ts(ACcell, [2, 0]):
            ACcell.cell.t = (ACcell.cell.t + 1) % 3

    # ============ U end ================

    # ============ iterate begin ================
    def __next(self):
        self.current_state = ''
        randNum = random.random()
        # 1. update mode
        for i in range(self.n_cell):
            if randNum >= self.alpha:
                continue
            self.__cell_mode_change(i)

        # 2. execute mode
        temp = []
        for i in range(self.n_cell):
            ACcell = self.EACcells[i]
            if not self.clean:
                temp.append(ACcell.to_dict())
            if randNum >= self.alpha:
                continue
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
        if not self.clean:
            self.sim_datas.append(temp)
        return self.current_state

    def run(self, isPrint=True, print_stack=False):
        print("m2_2m...")
        while True:
            state = self.__next()
            if not self.clean:
                self.state_in_sim.append(state)
            self.iter_nums += 1
            if self.get_stack_min() == self.run_num:
                print("alpha: {}, non-trival nums: {}, iter_nums: {}".format(self.alpha, self.run_num, self.iter_nums))
                break

        if isPrint:
            if print_stack:
                self.print_stack()
            else:
                for s in self.state_in_sim:
                    print(s.replace("0", " ").replace("1", "*"))

    # ============ iterate end ================

    # print stack of cells
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
        print('Minimum times of no-trival U：', min_)
        return min_

    def get_stack_min(self):
        l = len(self.state_stack)
        min_ = 1000
        for i in range(l):
            min_ = min_ if min_ < len(self.state_stack[i]) else len(self.state_stack[i])
        return min_


if __name__ == "__main__":
    init_state = '0' * 100 + '1' + '0' * 100
    rule = 90
    run_num = 100
    aceca = ECA_ACECA_M2(rule=rule, init_state=init_state, run_num=run_num)
    aceca.run(isPrint=True, print_stack=True)
    plot_space(title='m2+2m_alpha=1.0', datas=aceca.sim_datas, gaps=[12], save_=True)

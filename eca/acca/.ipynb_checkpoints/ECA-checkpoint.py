import numpy as np
import random
import time
import threading
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

sns.set(style="darkgrid")


class ECA:
    """Elementary Cellular Automaton - by Paul Panaitescu
    Represents a range 1, 3-cell neighbourhood elementary cellular automaton."""

    def __init__(self, rule, init_state='0' * 50 + '1' + '0' * 50, alpha=1.0, d_ini=0.5, k=0, Ttrs=0, Tsample=100,
                 run_num=100, ConvergeMode=0):
        """Initialize the CA with the given rule and initial state."""
        self.binary = f'{rule:08b}'  # transform the rule number to a binary code (Example: rule 90 is 01011010 in binary code)
        self.rule = rule
        self.dict = {
            # make a dictionary to store the 8 possible pairs of 3 neighbourhood elements (with values 1 and 0)
            "111": (self.binary[0]),
            # assign to each key, a value equivalent to a character from the binary code (from index 0 to index 7)
            "110": (self.binary[1]),
            "101": (self.binary[2]),
            "100": (self.binary[3]),
            "011": (self.binary[4]),
            "010": (self.binary[5]),
            "001": (self.binary[6]),
            "000": (self.binary[7])
        }
        # for ring data
        self.init_state = init_state
        self.n_cell = len(init_state)

        self.current_state = ""
        self.run_num = run_num
        self.alpha = alpha
        self.d_ini = d_ini
        self.k = k
        self.n_1 = []
        self.n_1.append(self.init_state.count('1'))
        self.space = []
        self.space.append(self.init_state)
        # paramters for convergence
        self.ConvergeMode = ConvergeMode
        if self.ConvergeMode == 1 or self.ConvergeMode == 2:
            self.runStop = False
            self.K_stop = int(1 / self.alpha)

        self.Ttrs = Ttrs
        self.Tsample = Tsample

    def printDict(self):
        print(self.dict)

    def __state(self):
        """Returns the current state."""
        return self.current_state

    def __asyNext(self):
        self.init_state = self.init_state[-1] + self.init_state + self.init_state[0]
        self.current_state = ''
        group = ''
        for i in range(1, len(self.init_state) - 1):

            randNum = np.random.random()

            # print("turn "+str(i)+": ECA the randNum is "+ str(randNum))

            if randNum >= self.alpha:
                self.current_state += self.init_state[i]
            else:
                for j in range(i - 1, i + 2):  # get groups of 3 elements (left, center, right)
                    group += self.init_state[j]  # add elemnts to group
                #             print(group)
                self.current_state += self.dict[
                    group]  # add value (1 or 0) in self.current_state, after corresponding dictionary value of the 3 group characters
                group = ''

                # consider the convergence
        if self.ConvergeMode == 1:
            if len(self.space) >= self.K_stop:
                K_sliced = self.space[-self.K_stop:]
                K_sliced.append(self.current_state)
                if len(set(K_sliced)) == 1:
                    self.runStop = True
                    self.init_state = self.__state()  # prepare self.init_state for next itteration
                    return self.current_state

        if self.ConvergeMode == 2:
            if self.__SyncNext(self.init_state) == self.current_state:
                self.runStop = True
                self.init_state = self.__state()  # prepare self.init_state for next itteration
                return self.current_state

        self.n_1.append(self.current_state.count('1'))
        self.space.append(self.current_state)

        self.init_state = self.__state()  # prepare self.init_state for next itteration
        return self.current_state

    def __SyncNext(self, config):
        current_state = ""
        group = ''
        for i in range(1, len(config) - 1):
            for j in range(i - 1, i + 2):  # get groups of 3 elements (left, center, right)
                group += config[j]  # add elemnts to group
            current_state += self.dict[
                group]  # add value (1 or 0) in self.current_state, after corresponding dictionary value of the 3 group characters
            group = ''
        return current_state

    def run(self, isPrint=True):
        """Progress and print num states.
        0s are replaced by spaces, and 1s are replaced by * for pretty printing."""
        if isPrint is True:
            print(self.init_state.replace("0", " ").replace("1", "*"))  # print the first line
        for i in tqdm(range(1, self.run_num)):
            if isPrint is True:
                print(i, self.__asyNext().replace("0", " ").replace("1", "*"))
            else:
                self.__asyNext()

            if self.ConvergeMode == 1 or self.ConvergeMode == 2:
                if self.runStop:
                    break

    def getu(self):
        # run_num 个时间的密度 den
        den = np.array(self.n_1) / self.n_cell
        u = 1.0 / self.Tsample * den[self.Ttrs:self.Ttrs + self.Tsample].sum()

        return u

    def reset(self, **kargs):
        if "alpha" in kargs.keys():
            self.alpha = kargs['alpha']

        if "init_state" in kargs.keys():
            self.init_state = kargs['init_state']
            self.n_cell = len(self.init_state) + 2

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

        self.current_state = ""

        self.n_1 = []
        self.n_1.append(self.init_state.count('1'))
        self.space = []
        self.space.append(self.init_state)

    def getDwithA(self, alpha, init_state, cell=10000, run_num=10000):
        n_cell = 10000
        # for uniform distribution
        init_state = getInitState(n_cell=n_cell, d_ini=0.5)
        start = 0.02
        end = 1
        precision = 100
        Alpha = np.linspace(start, end, (end - start) * precision + 1)
        sd_l = []
        for alpha in Alpha:

            if alpha < 0.1:
                run_num = 100000
            else:
                run_num = int(10000 / alpha)
            ti = time.time()
            self.reset(alpha=alpha, init_state=init_state, run_num=run_num)
            self.run(isPrint=False)
            print("alpha: ", str(alpha), ". spend: ", str(time.time() - ti), 's')
            sd = np.mean(np.array(self.n_1[int(self.run_num / 2):]) / (self.n_cell - 2))
            sd_l.append(sd)

        return sd_l


def plot_space(space):
    space = [[int(s) for s in sp] for sp in space]
    plt.figure(figsize=(19.2, 10.8))
    cmap = plt.get_cmap('Greys')
    plt.title("ACA_run{}_cell{}_rule{}".format(run_num, len(init_state), rule))
    plt.imshow(space, interpolation='none', cmap=cmap)
    plt.show()


def plot_dense(density, title=""):
    plt.plot(range(len(density)), density, label="1")
    plt.xlabel("Time step")
    plt.ylabel("Density")
    plt.title(title)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    init_state = '0' * 49 + '1' + '0' * 48  # yes 98
    # init_state = '0' * 49 + '1' + '0' * 49  # yes 99
    # init_state = '0' * 49 + '1' + '0' * 50 # no 100
    # init_state = '0' * 50 + '1' + '0' * 50 # yes 101
    # init_state = '0' * 51 + '1' + '0' * 50 # no 102
    # init_state = '0' * 50 + '1' + '0' * 51  # no 102
    run_num = 300
    rule = 90
    ca = ECA(rule=rule, init_state=init_state, run_num=run_num)
    ca.run(isPrint=False)

    # 绘制图形
    plot_space(space=ca.space)

    # 绘制密度
#     # steps = [20, 40, 60, 80, 100, 120, 140, 160, 180]
#     steps = [1, 10]
#     # steps = range(20, 220, 20)
#     for step in steps:
#         partsl = int(run_num / step)
#         n_1 = np.asarray(ca.n_1)
#         density = []
#         for i in range(partsl):
#             e = i * step + step
#             e = e if e < len(n_1) else len(n_1)
#             density.append(n_1[i * step: e].sum(axis=0) / step)
#         # density = np.asarray(aceca.n_1) / aceca.n_cell
#         plot_dense(density=density, title="CA_run{}_rule{}_cell{}".format(ca.run_num, ca.rule, ca.n_cell))

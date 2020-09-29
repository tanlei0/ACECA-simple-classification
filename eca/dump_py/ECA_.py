import numpy as np
import random
import time
import matplotlib.pyplot as plt

random.seed(100)


class ECA:
    """Elementary Cellular Automaton - by Paul Panaitescu
    Represents a range 1, 3-cell neighbourhood elementary cellular automaton."""

    def __init__(self, rule, init_state='0' * 2 + '1' + '0' * 2, alpha=1.0, d_ini=0.5, k=0, Ttrs=0, Tsample=100,
                 run_num=100, ConvergeMode=0, ACECA=False):
        """
        Initialize the CA with the given rule and initial state.
        :param rule: 规则
        :param init_state: 初始状态
        :param alpha: 概率值
        :param d_ini: 0和1的数量比例
        :param k:
        :param Ttrs:
        :param Tsample:
        :param run_num: 运行次数
        :param ConvergeMode:
        """
        self.ACECA = ACECA
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
        # self.init_state = init_state
        # for ring data
        self.init_state = init_state[:-1] + init_state[0]
        # 细胞数量
        if ACECA:
            self.n_cell = len(init_state)
        else:
            self.n_cell = len(init_state) + 2
        self.current_state = ""
        self.run_num = run_num
        self.alpha = alpha
        self.d_ini = d_ini
        self.k = k
        # 存储迭代过程中状态里面1的个数
        self.n_1 = []
        self.n_1.append(self.init_state.count('1'))
        # 存储迭代过程中的状态
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

    def run_next(self):
        # 左右添加0
        self.current_state = ''
        group = ''
        # 左右两边添加的0
        for i in range(0, len(self.init_state)):

            randNum = np.random.random()

            # print("turn "+str(i)+": ECA the randNum is "+ str(randNum))

            # 当大于等于alpha概率时，细胞不发生改变
            if randNum >= self.alpha:
                self.current_state += self.init_state[i]
            # 当小于alpha概率时，细胞按照规则发生改变
            else:
                if i == 0:
                    group = self.init_state[len(self.init_state) - 1] + self.init_state[i] + self.init_state[i + 1]
                elif i == len(self.init_state) - 1:
                    group = self.init_state[i - 1] + self.init_state[i] + self.init_state[i]
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
            # 当下一轮和当前轮结果一样的时，迭代停止
            if self.__SyncNext(self.init_state) == self.current_state:
                self.runStop = True
                self.init_state = self.__state()  # prepare self.init_state for next itteration
                return self.current_state
        # 统计当前状态1的数量
        self.n_1.append(self.current_state.count('1'))
        # 将当前状态添加到状态空间
        self.space.append(self.current_state)

        self.init_state = self.__state()  # prepare self.init_state for next itteration
        return self.current_state

    def __asyNext(self):
        """
        一轮遍历
        :return:
        """
        # # 左右添加0
        self.init_state = '0' + self.init_state + '0'
        self.current_state = ''
        group = ''
        # 左右两边添加的0不用遍历
        for i in range(1, len(self.init_state) - 1):

            randNum = np.random.random()

            # print("turn "+str(i)+": ECA the randNum is "+ str(randNum))

            # 当大于等于alpha概率时，细胞不发生改变
            if randNum >= self.alpha:
                self.current_state += self.init_state[i]
            # 当小于alpha概率时，细胞按照规则发生改变
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
            # 当下一轮和当前轮结果一样的时，迭代停止
            if self.__SyncNext(self.init_state) == self.current_state:
                self.runStop = True
                self.init_state = self.__state()  # prepare self.init_state for next itteration
                return self.current_state
        # 统计当前状态1的数量
        self.n_1.append(self.current_state.count('1'))
        # 将当前状态添加到状态空间
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
        for i in range(1, self.run_num):
            if isPrint is True:
                if self.ACECA:
                    print(self.run_next().replace("0", " ").replace("1", "*"))
                else:
                    print(self.__asyNext().replace("0", " ").replace("1", "*"))
            else:
                if self.ACECA:
                    self.run_next()
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


def getInitState(n_cell, d_ini):
    """
    生成由0和1构成的状太
    :param n_cell: 细胞数量
    :param d_ini: 细胞中0和1的比例
    :return:
    """
    init_state = ''
    for i in range(0, n_cell):
        rand = np.random.rand()
        if rand >= d_ini:
            init_state += '0'
        else:
            init_state += '1'
    return init_state


if __name__ == '__main__':
    # init_state = '0' * 2 + '1' + '0' * 2
    init_state = '0' * 48 + '1' + '0' * 48
    run_num = 500
    ca = ECA(rule=90, init_state=init_state, run_num=run_num)
    print(ca.binary)
    ca.printDict()
    ca.run()
    ca.n_1 = np.asarray(ca.n_1) / len(init_state)
    plt.figure(figsize=(19.2, 10.8))
    plt.plot(range(run_num), ca.n_1, label='nums(cells_1)/nums(cells)')
    plt.title('ECA')
    plt.xlabel('Time step')
    plt.ylabel('Density')
    plt.xticks([])
    plt.legend()
    plt.tight_layout()
    plt.savefig("./ECA_density.jpg", dpi=144)
    plt.show()

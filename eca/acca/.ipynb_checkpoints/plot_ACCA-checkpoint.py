# -*- coding: utf-8 -*-
# @Time : 2020/8/7 下午2:44
# @Author : cmk
# @File : plot_ACCA.py

from utils import *
import matplotlib.pyplot as plt
from m3 import ECA_ACECA_M3
from m2_2m import ECA_ACECA_M2
from dump_py.m2_2m_v2 import ECA_ACECA_M2_V2
from dump_py.ECA_ import ECA

plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']


# 绘制1的密度
def plot_dense():
    init_state = '0' * 48 + '1' + '0' * 48
    run_num = 500
    eca_run_num = 500
    rule = 90

    eca = ECA(rule=rule, init_state=init_state, run_num=eca_run_num)
    eca.run(isPrint=False)

    m3 = ECA_ACECA_M3(rule=rule, init_state=init_state, run_num=run_num)
    m3.run(isPrint=False, print_stack=False)

    m2_v2 = ECA_ACECA_M2_V2(rule=rule, init_state=init_state, run_num=run_num)
    m2_v2.run(isPrint=False, print_stack=False)

    m2 = ECA_ACECA_M2(rule=rule, init_state=init_state, run_num=run_num)
    m2.run(isPrint=False, print_stack=False)

    plt.figure(figsize=(19.2, 10.8))
    plt.xlabel('Time step')
    plt.ylabel("Density")

    plt.subplot(221)
    plt.title("ECA")
    plt.plot(range(eca_run_num), np.asarray(eca.n_1) / len(init_state), label='nums(cells_1)/nums(cells)')

    plt.subplot(222)
    plt.title("m3")
    plt.plot(range(run_num), get_dense(m3.sim_datas), label='nums(cells_1)/nums(cells)')

    plt.subplot(223)
    plt.title("m2")
    plt.plot(range(run_num), get_dense(m2.sim_datas), label='nums(cells_1)/nums(cells)')

    plt.subplot(224)
    plt.title("m2_v2")
    plt.plot(range(run_num), get_dense(m2_v2.sim_datas), label='nums(cells_1)/nums(cells)')

    plt.show()


if __name__ == "__main__":
    plot_dense()

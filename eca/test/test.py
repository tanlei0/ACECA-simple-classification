import time
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool, Manager, cpu_count
import random
import json


# 定义装饰器
def time_calc(func):
    def wrapper(*args, **kargs):
        start_time = time.time()
        f = func(*args, **kargs)
        exec_time = time.time() - start_time
        print(exec_time)
        return f

    return wrapper


# 使用装饰器
@time_calc
def add(a, b):
    return a + b


@time_calc
def sub(a, b):
    return a - b


def func(msg, da, lock):
    lock.acquire()
    try:
        da[msg] = "set"
        print(msg)
    finally:
        lock.release()


def plot_line(path=None, acca_type="m2"):
    with open(path, 'r') as load_f:
        load_dict = json.load(load_f)

    print(load_dict)

    def get_m_data(load_dict, acca_type):
        acca_data = load_dict['acca_run_nums'][acca_type]
        x = load_dict['ca_run_nums']
        alphas = load_dict['alphas']
        y = {}
        for alpha in alphas:
            y[str(alpha)] = []

        for key in y:
            for xi in x:
                y[key].append(acca_data[key][str(xi)])
        return y

    m2_data = get_m_data(load_dict, 'm2')
    m3_data = get_m_data(load_dict, 'm3')
    print(m2_data)
    print(m3_data)
    alphas = load_dict['alphas']
    colors = ['r', 'y', 'b']
    x = load_dict['ca_run_nums']
    plt.tight_layout()
    plt.xlabel("ECA run times")
    plt.ylabel("ACCA run times")
    for i in range(len(alphas)):
        plt.plot(x, m2_data[str(alphas[i])], c=colors[i], linestyle=':')
        plt.plot(x, m3_data[str(alphas[i])], c=colors[i])

    # plt.legend()
    plt.savefig("../acca/result/acca-aca-run-times.jpeg", dpi=300)
    plt.show()


if __name__ == "__main__":
    path = "../acca/result/multi_data.json"
    # with open(path, 'r') as load_f:
    #     load_dict = json.load(load_f)
    # acca_type = 'm3'
    # print(load_dict)
    # m2_data = load_dict['acca_run_nums'][acca_type]
    # x = load_dict['ca_run_nums']
    # alphas = load_dict['alphas']
    # print(m2_data)
    # m2_y = {}
    # for alpha in alphas:
    #     m2_y[str(alpha)] = []
    #
    # for key in m2_y:
    #     for xi in x:
    #         m2_y[key].append(m2_data[key][str(xi)])
    # print(m2_y)
    # plt.xlabel("ECA run times")
    # plt.ylabel("ACCA run times")
    # if acca_type == 'm2':
    #     title = "$m^{}+2m$".format(acca_type[1])
    # else:
    #     title = "$m^{}$".format(acca_type[1])
    # # plt.title(title)
    # for key in m2_y:
    #     # plt.plot(x, m2_y[key], label="$\\alpha={}$".format(key))
    #     plt.plot(x, m2_y[key], linestyle="--")
    # # plt.legend()
    # plt.savefig("../acca/result/acca-{}-aca-run-times.jpeg".format(acca_type), dpi=300)
    # plt.show()
    plot_line(path)

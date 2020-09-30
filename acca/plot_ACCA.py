# -*- coding: utf-8 -*-
# @Time : 2020/8/7 pm 2:44
# @Author : cmk
# @File : plot_ACCA.py
import json
import pandas as pd
import platform

from utils import *
import matplotlib.pyplot as plt
from m3 import ECA_ACECA_M3
from m2_2m import ECA_ACECA_M2
from ECA import ECA
import gc
import copy
from tqdm import tqdm
from multiprocessing import Pool, Manager, cpu_count
import time


# plt.rcParams['font.family'] = ['sans-serif']
# plt.rcParams['font.sans-serif'] = ['SimHei']


def plot_all_space():
    alphas = [1., 0.5, 0.2]
    ca_run_num = 50
    rule = 90
    init_state = '0' * 100 + '1' + '0' * 100
    m2_gap = [12, 24, 60]
    m3_gap = [8, 16, 40]
    for i in range(len(alphas)):
        print(alphas[i])
        m2 = ECA_ACECA_M2(rule=rule, init_state=init_state, run_num=ca_run_num, alpha=alphas[i])
        m2.run(isPrint=False, print_stack=False)
        plot_space(title='m2_alpha={}_carunnum={}_runnum={}'.format(m2.alpha, m2.run_num, m2.iter_nums),
                   datas=m2.sim_datas,
                   gaps=[m2_gap[i]], save_=True, show=False)
        del m2
        gc.collect()
        m3 = ECA_ACECA_M3(rule=rule, init_state=init_state, run_num=ca_run_num, alpha=alphas[i])
        m3.run(isPrint=False, print_stack=False)
        plot_space(title='m3_alpha={}_carunnum={}_runnum={}'.format(m3.alpha, m3.run_num, m3.iter_nums),
                   datas=m3.sim_datas,
                   gaps=[m3_gap[i]], save_=True, show=False)
        del m3
        gc.collect()
    print("ECA...")
    ca = ECA(rule=rule, init_state=init_state, run_num=ca_run_num)
    ca.run(isPrint=False)
    ca.plot_space(space=ca.space, save_=True, show=False)


def dict2jsonfile(dict_data=None, json_path=""):
    jsObj = json.dumps(dict_data, indent=4)
    fileObject = open(json_path, 'w')
    fileObject.write(jsObj)
    fileObject.close()


# use multi thread to speed up
# only in unix system
def get_run_datas_multi(save_path=None):
    processes = cpu_count()
    # processes = 4
    st = time.time()
    alphas = [1., 0.5, 0.2]
    ca_run_nums = range(50, 200, 5)
    rule = 90
    init_state = '0' * 100 + '1' + '0' * 100
    m2_gap = [12, 24, 60]
    m3_gap = [8, 16, 40]
    res = {'alphas': alphas, 'ca_run_nums': list(ca_run_nums), 'acca_run_nums': {}}
    manager = Manager()
    pool = Pool(processes=processes)
    lock = manager.Lock()
    template_ = manager.dict()
    template_['m2'] = manager.dict()
    template_['m3'] = manager.dict()
    for alpha in alphas:
        template_['m2'][alpha] = manager.dict()
        template_['m3'][alpha] = manager.dict()
    print(template_['m2'])
    for ca_run_num in ca_run_nums:
        pool.apply_async(run_func,
                         (alphas, template_, rule, init_state, ca_run_num,
                          lock))
    pool.close()
    pool.join()
    new_temp = {'m2': {}, 'm3': {}}
    for k in template_:
        for ki in dict(template_[k]):
            new_temp[k][ki] = dict(template_[k][ki])
    print(new_temp)
    res['acca_run_nums'] = new_temp
    print(res)
    print("times: {}".format(time.time() - st))
    if save_path is None:
        save_path = "./result/relation.json"
    dict2jsonfile(res, save_path)


def run_func(alphas: list, template_, rule, init_state, ca_run_num, lock):
    for i in range(len(alphas)):
        m2 = ECA_ACECA_M2(rule=rule, init_state=init_state, run_num=ca_run_num, alpha=alphas[i], clean=True)
        m2.run(isPrint=False, print_stack=False)
        m3 = ECA_ACECA_M3(rule=rule, init_state=init_state, run_num=ca_run_num, alpha=alphas[i], clean=True)
        m3.run(isPrint=False, print_stack=False)
        lock.acquire()
        try:
            template_['m2'][alphas[i]][ca_run_num] = m2.iter_nums
            template_['m3'][alphas[i]][ca_run_num] = m3.iter_nums
            print("{} ----> {}".format(ca_run_num, alphas[i]))
        finally:
            lock.release()
        del m2
        del m3
        gc.collect()


def get_run_datas(save_path=None):
    st = time.time()
    alphas = [1., 0.5, 0.2]
    # ca_run_nums = range(50, 150, 5)
    ca_run_nums = [10, 20]
    rule = 90
    init_state = '0' * 100 + '1' + '0' * 100
    m2_gap = [12, 24, 60]
    m3_gap = [8, 16, 40]
    res = {'ca_run_nums': ca_run_nums, 'acca_run_nums': {}}
    template_ = {'m2': {}, 'm3': {}}
    for alpha in alphas:
        template_['m2'][alpha] = []
        template_['m3'][alpha] = []
    for ca_run_num in ca_run_nums:
        for i in range(len(alphas)):
            print(alphas[i])
            m2 = ECA_ACECA_M2(rule=rule, init_state=init_state, run_num=ca_run_num, alpha=alphas[i])
            m2.run(isPrint=False, print_stack=False)
            template_['m2'][alphas[i]].append(m2.iter_nums)
            del m2
            gc.collect()
            m3 = ECA_ACECA_M3(rule=rule, init_state=init_state, run_num=ca_run_num, alpha=alphas[i])
            m3.run(isPrint=False, print_stack=False)
            template_['m3'][alphas[i]].append(m3.iter_nums)
            del m3
            gc.collect()

    res['acca_run_nums'] = template_
    if save_path is None:
        save_path = "./result/relation.json"
    dict2jsonfile(res, save_path)
    print(res)
    print("time: {}".format(time.time() - st))
    plot_line(save_path, acca_type='m3')
    return res


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
    colors = ['r', 'g', 'b']
    x = load_dict['ca_run_nums']
    plt.tight_layout()
    plt.xlabel("ECA run times")
    plt.ylabel("ACCA run times")
    for i in range(len(alphas)):
        plt.plot(x, m2_data[str(alphas[i])], c=colors[i], linestyle='--')
        plt.plot(x, m3_data[str(alphas[i])], c=colors[i])

    plt.legend()
    plt.savefig("./result/acca-aca-run-times.jpeg", dpi=300)
    plt.show()


def json2excel(json_path=""):
    with open(json_path, 'r') as load_f:
        load_dict = json.load(load_f)
    ca_run_nums = load_dict['ca_run_nums']
    alphas = load_dict['alphas']
    acca_types = ['m2', 'm3']
    i = 0
    acca_data = load_dict['acca_run_nums']
    y = {}
    for alpha in alphas:
        for i in range(len(acca_types)):
            y["{}_{}".format(acca_types[i], str(alpha))] = []

    for key in y:
        for xi in ca_run_nums:
            y[key].append(acca_data[key[:2]][key[3:]][str(xi)])
    df = pd.DataFrame(y)
    df.insert(0, 'ca_run_nums', ca_run_nums)
    print(df.head())
    df.to_excel('./result/data.xls')


if __name__ == "__main__":
    # =========== plot CA space ==============
    plot_all_space()
    # =========== plot CA space ==============

    # =========== plot CA run times ===================
    # if platform.system() == "Windows":
    #     get_run_datas(save_path="./result/multi_data.json")
    # else:
    #     get_run_datas_multi(save_path="./result/multi_data.json")
    # plot_line(path="./result/multi_data.json")
    # =========== plot CA run times ===================

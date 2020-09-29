# -*- coding: utf-8 -*-
# @Time : 2020/8/18 下午4:52
# @Author : cmk
# @File : create_gif.py

# ####### 创建gif动画 ###############
##################################
from acca.utils import get_color2space, draw_gif
from m3 import ECA_ACECA_M3
from utils import *

if __name__ == '__main__':
    colors_dict = {
        # 00 white
        '010': 0,
        '000': 0,
        # 10 black
        '100': 1,
        '110': 1,

        # lightgray
        '001': 0.5,
        '012': 0.5,
        '002': 0.5,

        # darkgray
        '011': 0.8,
        '101': 0.8,
        '111': 0.8,
        '102': 0.8,
        '112': 0.8,
    }
    init_state = '0' * 50 + '1' + '0' * 49
    rule = 90
    run_num = 50
    aceca = ECA_ACECA_M3(rule=90, init_state=init_state, run_num=run_num)
    aceca.run(isPrint=False, print_stack=False)
    space = get_color2space(colors_dict=colors_dict, gap=1, datas=aceca.sim_datas)
    draw_gif(space[:10])

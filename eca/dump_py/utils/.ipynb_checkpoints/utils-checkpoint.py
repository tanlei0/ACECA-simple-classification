# -*- coding: utf-8 -*-
# @Time : 2020/8/7 下午3:11
# @Author : cmk
# @File : utils.py.py

import pickle


def save_data(data, file_path=""):
    with open(file_path, "wb") as file:
        pickle.dump(data, file, True)


def read_data(file_path=""):
    with open(file_path, "rb") as file:
        data = pickle.load(file)
    return data

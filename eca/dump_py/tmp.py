# -*- coding: utf-8 -*-
# @Time : 2020/8/14 下午6:04
# @Author : cmk
# @File : tmp.py

import platform

print(platform.system())

if platform.system() == 'Windows':
    print('Windows系统')
elif platform.system() == 'Linux':
    print('Linux系统')
else:
    print('其他')

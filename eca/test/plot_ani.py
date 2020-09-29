# -*- coding: utf-8 -*-
# @Time : 2020/8/22 上午10:34
# @Author : cmk
# @File : plot_ani.py

import matplotlib.pyplot as plt
import numpy as np

# 数据集：X轴数据固定；Y轴的数据更新
X = np.arange(0, 10, 0.01)  # X shape： (N,)
Ys = [np.sin(X + k / 10) for k in range(100)]  # Ys shape： (k, N)

plt.ion()
plt.show()
for i in range(len(Ys)):
    plt.cla()

    plt.title('y = sin(x + k/10)')
    plt.xlim(0, 10)
    plt.ylim(-1, 1)

    plt.plot(X, Ys[i], 'r', alpha=0.7, linewidth=0.7)
    plt.text(1, 1, 'k: %d' % i)

    plt.draw()
    plt.pause(0.05)  # 间隔时间，s
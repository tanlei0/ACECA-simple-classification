# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 23:51:49 2020

@author: Qin Lei
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

rule_list1 = [90, 73, 18, 26, 152]


ACECA_SURFACE = 'data/aceca_surface/'
ECA_SURFACE = 'data/ECAsurface_new/'


dval = np.linspace(0.2, 0.8, 7)
A = np.linspace(0.2, 1, 9)
fig = plt.figure()
title_list = ["ECA 90","ECA 73","ECA 18","ECA 26","ECA 152"]
for i,rule in enumerate(rule_list1):
    eca_surface_path = ECA_SURFACE+str(rule)+'.csv'
    aceca_surface_path = ACECA_SURFACE+str(rule)+'.csv'
    u1 = pd.read_csv(aceca_surface_path)
    u2 = pd.read_csv(eca_surface_path)
    x = dval
    y = A
    X, Y = np.meshgrid(x, y)
    Z = u1
    
    ax = fig.add_subplot(1,5,i+1,projection='3d')
    ax.plot_wireframe(X, Y, Z, color='r',label="ACECA")
    Z = u2
    ax.plot_wireframe(X,Y,Z, color= 'k', label="AECA")
    ax.set_zlim(0,1)
    ax.set_zlabel("u")
    ax.set_xlabel("initial density")
    ax.set_ylabel("synchrony rate")
    ax.set_title(title_list[i])

plt.legend()
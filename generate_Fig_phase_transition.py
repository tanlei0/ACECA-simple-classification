# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 22:05:24 2020

@author: tanlei0
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


dic1 = np.load("ACECAph_dic_dpAll.npy",allow_pickle=True)
dic2 = np.load("ACECA_dic.npy",allow_pickle=True)
df1 = pd.DataFrame(columns = ["rule", "alpha","sd"])
df2 = pd.DataFrame(columns = ["rule", "alpha","sd"])

for row in dic1:
    df1 = df1.append(pd.Series(row), ignore_index=True)

for row in dic2:
    df2 = df2.append(pd.Series(row), ignore_index=True)

# In[1]
title_list = ["(a) ECA 58","(b) ECA 106","(c) ECA 146"]
rule_list = [58,106,146]
fig, ax_list = plt.subplots(1,3, sharey="all")
alpha = df1.alpha.unique().tolist()
for i,rule in enumerate(rule_list):
    
    ax_list[i].plot(alpha, (df1[df1.rule == rule].sd).tolist(),color = "r",label= "After modification")
    ax_list[i].plot(alpha, (df2[df2.rule == rule].sd).tolist(),color = "b",label= "Before modification")
    #ax_list.plot(alpha, df.sd.tolist())
    ax_list[i].set_xlim([0,1])
    ax_list[i].set_ylim([0,1])
    ax_list[i].set_title(title_list[i])
    ax_list[i].set_xlabel("alpha")
    if i == 0 :
        ax_list[i].set_ylabel("density")

plt.legend()
plt.show()
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 17:57:54 2022

@author: Jonas
"""

import os
import pandas as pd
import glob
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.patches as patch
import numpy as np

# filepath_examplesetups = path.join(path.dirname(path.abspath(__file__)),
#                                    "testSetupsWithoutOGS/*.xml")

pj = 'default'

if not os.path.exists('fig_sum/' + pj):

    os.makedirs('fig_sum/' + pj)

outputs = glob.glob(pj + r"\*.csv")

datas = []

for output in outputs:
    datas.append(pd.read_csv(output, sep='\t'))



all_datas = pd.concat(datas)

all_datas = all_datas.sort_values("time")
all_datas['species'] = all_datas['plant'].str.slice(0,11)
all_datas['volume_ag'] = np.pi * all_datas['r_ag']**2 * all_datas['h_ag']
all_datas['volume_bg'] = np.pi * all_datas['r_bg']**2 * all_datas['h_bg']
all_datas['volume'] = all_datas['volume_ag'] + all_datas['volume_bg']

time = all_datas['time'].drop_duplicates(ignore_index=True)

l_sector = 25
n_sectors = 4
mean_all = []
means = [[], [], [], []]
means_1 = [[], [], [], []]
means_2 = [[], [], [], []]
means_3 = [[], [], [], []]
means_4 = [[], [], [], []]
stds = [[], [], [], []]

sectors = []

for k in range(n_sectors):
    sectors.append(all_datas[(all_datas['x'] > k * l_sector) & (all_datas['x'] < (
        (k+1) * l_sector))])

for n in time:

    data = all_datas[all_datas['time'] == n].sort_values('h_ag',
                                                         ignore_index=True)
    mean_all.append(data['volume'].mean(skipna=True))
    mean = []
    std = []
    n = 0
    for k in range(n_sectors):
        print(n)
        df = data[(data['x'] > k * l_sector) & (data['x'] < (
            (k+1) * l_sector))]
        means[n].append(df['volume'].mean(skipna=True))
        stds[n].append(df['volume'].std(skipna=True))
        df_1 = df[df['species'] == 'Saltmarsh_1']
        df_2 = df[df['species'] == 'Saltmarsh_2']
        df_3 = df[df['species'] == 'Saltmarsh_3']
        df_4 = df[df['species'] == 'Saltmarsh_4']
        means_1[n].append(df_1['volume'].mean(skipna=True))
        means_2[n].append(df_2['volume'].mean(skipna=True))
        means_3[n].append(df_3['volume'].mean(skipna=True))
        means_4[n].append(df_4['volume'].mean(skipna=True))
        n += 1

fig = plt.figure(figsize=(16, 9), constrained_layout=False)

gs = GridSpec(7, 8)

ax1 = fig.add_subplot(gs[4:7, 0:2])
ax2 = fig.add_subplot(gs[4:7, 2:4])
ax3 = fig.add_subplot(gs[4:7, 4:6])
ax4 = fig.add_subplot(gs[4:7, 6:8])
ax5 = fig.add_subplot(gs[0:3, :])

time = time / 86400

ax1.plot(time, means[0])
ax2.plot(time, means[1])
ax3.plot(time, means[2])
ax4.plot(time, means[3])

ax1.plot(time, means_1[0], label='Saltmarsh 1', color='peru')
ax2.plot(time, means_1[1], label='Saltmarsh 1', color='peru')
ax3.plot(time, means_1[2], label='Saltmarsh 1', color='peru')
ax4.plot(time, means_1[3], label='Saltmarsh 1', color='peru')

ax1.plot(time, means_2[0], label='Saltmarsh 2', color='blue')
ax2.plot(time, means_2[1], label='Saltmarsh 2', color='blue')
ax3.plot(time, means_2[2], label='Saltmarsh 2', color='blue')
ax4.plot(time, means_2[3], label='Saltmarsh 2', color='blue')

ax1.plot(time, means_3[0], label='Saltmarsh 3', color='red')
ax2.plot(time, means_3[1], label='Saltmarsh 3', color='red')
ax3.plot(time, means_3[2], label='Saltmarsh 3', color='red')
ax4.plot(time, means_3[3], label='Saltmarsh 3', color='red')

ax1.plot(time, means_4[0], label='Saltmarsh 4', color='yellow')
ax2.plot(time, means_4[1], label='Saltmarsh 4', color='yellow')
ax3.plot(time, means_4[2], label='Saltmarsh 4', color='yellow')
ax4.plot(time, means_4[3], label='Saltmarsh 4', color='yellow')
ax4.legend()

ax5.plot(time, mean_all)

y_max = 0.2

ax1.set(ylim=(0, y_max))
ax2.set(yticks=[],
        ylim=(0, y_max))
ax3.set(yticks=[],
        ylim=(0, y_max))
ax4.set(yticks=[],
        ylim=(0, y_max))

fig.savefig('fig_sum/' + pj + '/sectors_3_t.png')

fig = plt.figure(figsize=(16, 9), constrained_layout=False)

gs = GridSpec(7, 8)

ax1 = fig.add_subplot(gs[4:7, 0:2])
ax2 = fig.add_subplot(gs[4:7, 2:4])
ax3 = fig.add_subplot(gs[4:7, 4:6])
ax4 = fig.add_subplot(gs[4:7, 6:8])
ax5 = fig.add_subplot(gs[0:3, :])

# ax1.plot(time, means[0])
# ax2.plot(time, means[1])
# ax3.plot(time, means[2])
# ax4.plot(time, means[3])

t = 25

ax1.bar(1, means_1[0][t], label='Saltmarsh 1', color='peru', width=0.5)
ax2.bar(1, means_1[1][t], label='Saltmarsh 1', color='peru', width=0.5)
ax3.bar(1, means_1[2][t], label='Saltmarsh 1', color='peru', width=0.5)
ax4.bar(1, means_1[3][t], label='Saltmarsh 1', color='peru', width=0.5)

ax1.bar(2, means_2[0][t], label='Saltmarsh 2', color='blue', width=0.5)
ax2.bar(2, means_2[1][t], label='Saltmarsh 2', color='blue', width=0.5)
ax3.bar(2, means_2[2][t], label='Saltmarsh 2', color='blue', width=0.5)
ax4.bar(2, means_2[3][t], label='Saltmarsh 2', color='blue', width=0.5)

ax1.bar(3, means_3[0][t], label='Saltmarsh 3', color='red', width=0.5)
ax2.bar(3, means_3[1][t], label='Saltmarsh 3', color='red', width=0.5)
ax3.bar(3, means_3[2][t], label='Saltmarsh 3', color='red', width=0.5)
ax4.bar(3, means_3[3][t], label='Saltmarsh 3', color='red', width=0.5)

ax1.bar(4, means_3[0][t], label='Saltmarsh 4', color='yellow', width=0.5)
ax2.bar(4, means_3[1][t], label='Saltmarsh 4', color='yellow', width=0.5)
ax3.bar(4, means_3[2][t], label='Saltmarsh 4', color='yellow', width=0.5)
ax4.bar(4, means_3[3][t], label='Saltmarsh 4', color='yellow', width=0.5)

ax4.legend()

ax5.plot(time, mean_all)

y_max = 0.015

ax1.set(ylim=(0, y_max),
        xlim=(0.5, 4.5))
ax2.set(yticks=[],
        ylim=(0, y_max),
        xlim=(0.5, 4.5))
ax3.set(yticks=[],
        ylim=(0, y_max),
        xlim=(0.5, 4.5))
ax4.set(yticks=[],
        ylim=(0, y_max),
        xlim=(0.5, 4.5))

fig.savefig('fig_sum/' + pj + '/sectors_3.png')

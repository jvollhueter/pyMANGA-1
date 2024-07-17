# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 12:48:29 2023

@author: Jonas
"""

import os
import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.patches as patch
from scipy.interpolate import griddata
import matplotlib.patches as patch


def legend_without_duplicate_labels(ax):
    handles, labels = ax.get_legend_handles_labels()
    unique = [(h, l) for i, (h, l) in enumerate(zip(handles,
                                                    labels)
                                                ) if l not in labels[:i]]
    ax.legend(*zip(*unique), framealpha=1, shadow=False, loc=1)


result_files_1 = glob.glob(r'70\1\*.csv')
result_files_2 = glob.glob(r'70\2\*.csv')
result_files_3 = glob.glob(r'70\3\*.csv')
result_files_4 = glob.glob(r'70\4\*.csv')

pj = 'ini'

if not os.path.exists('fig/70'):

    os.makedirs('fig/70')


files_avi = []
files_rhi = []
salt_lims = []
files_1 = []
files_2 = []
files_3 = []
files_4 = []

for result_file in result_files_1:
    file = pd.read_csv(result_file, sep='\t')
    files_1.append(file)

for result_file in result_files_2:
    file = pd.read_csv(result_file, sep='\t')
    files_2.append(file)

for result_file in result_files_3:
    file = pd.read_csv(result_file, sep='\t')
    files_3.append(file)

for result_file in result_files_4:
    file = pd.read_csv(result_file, sep='\t')
    files_4.append(file)

x, y = np.meshgrid(np.linspace(0, 50, 51), np.linspace(0, 10, 11))

all_trees_1 = pd.concat(files_1)
all_trees_1['time'] = all_trees_1['time'] / 3600 / 24
all_trees_1['biovolume_ag'] = np.pi * all_trees_1['r_ag']**2 * all_trees_1['h_ag']
all_trees_1['biovolume_bg'] = np.pi * all_trees_1['r_bg']**2 * all_trees_1['h_bg']
all_trees_1['biovolume'] = all_trees_1['biovolume_ag'] + all_trees_1['biovolume_bg']

all_trees_2 = pd.concat(files_2)
all_trees_2['time'] = all_trees_2['time'] / 3600 / 24
all_trees_2['biovolume_ag'] = np.pi * all_trees_2['r_ag']**2 * all_trees_2['h_ag']
all_trees_2['biovolume_bg'] = np.pi * all_trees_2['r_bg']**2 * all_trees_2['h_bg']
all_trees_2['biovolume'] = all_trees_2['biovolume_ag'] + all_trees_2['biovolume_bg']

all_trees_3 = pd.concat(files_3)
all_trees_3['time'] = all_trees_3['time'] / 3600 / 24
all_trees_3['biovolume_ag'] = np.pi * all_trees_3['r_ag']**2 * all_trees_3['h_ag']
all_trees_3['biovolume_bg'] = np.pi * all_trees_3['r_bg']**2 * all_trees_3['h_bg']
all_trees_3['biovolume'] = all_trees_3['biovolume_ag'] + all_trees_3['biovolume_bg']

all_trees_4 = pd.concat(files_4)
all_trees_4['time'] = all_trees_4['time'] / 3600 / 24
all_trees_4['biovolume_ag'] = np.pi * all_trees_4['r_ag']**2 * all_trees_4['h_ag']
all_trees_4['biovolume_bg'] = np.pi * all_trees_4['r_bg']**2 * all_trees_4['h_bg']
all_trees_4['biovolume'] = all_trees_4['biovolume_ag'] + all_trees_4['biovolume_bg']

n = 1

for result_file in result_files_1:

    fig = plt.figure(figsize=(10, 16), constrained_layout=False)

    gs = GridSpec(23, 8)

    ax1 = fig.add_subplot(gs[0:5, :])
    ax2 = fig.add_subplot(gs[6:11, :])
    ax3 = fig.add_subplot(gs[12:17, :])
    ax4 = fig.add_subplot(gs[18:23, :])

    ax1.plot(all_trees_1['time'], all_trees_1['h_ag'])
    ax1.plot(all_trees_2['time'], all_trees_2['h_ag'])
    ax1.plot(all_trees_3['time'], all_trees_3['h_ag'])
    ax1.plot(all_trees_4['time'], all_trees_4['h_ag'])
    ax1.set_title('$h_{ag}$')
    ax1.set(ylabel='l [m]')

    ax2.plot(all_trees_1['time'], all_trees_1['r_ag'])
    ax2.plot(all_trees_2['time'], all_trees_2['r_ag'])
    ax2.plot(all_trees_3['time'], all_trees_3['r_ag'])
    ax2.plot(all_trees_4['time'], all_trees_4['r_ag'])
    ax2.set_title('$r_{ag}$')
    ax2.set(ylabel='l [m]')

    ax3.plot(all_trees_1['time'], all_trees_1['h_bg'])
    ax3.plot(all_trees_2['time'], all_trees_2['h_bg'])
    ax3.plot(all_trees_3['time'], all_trees_3['h_bg'])
    ax3.plot(all_trees_4['time'], all_trees_4['h_bg'])
    ax3.set_title('$h_{bg}$')
    ax3.set(ylabel='l [m]')

    ax4.plot(all_trees_1['time'], all_trees_1['r_bg'])
    ax4.plot(all_trees_2['time'], all_trees_2['r_bg'])
    ax4.plot(all_trees_3['time'], all_trees_3['r_bg'])
    ax4.plot(all_trees_4['time'], all_trees_4['r_bg'])
    ax4.set_title('$r_{bg}$')
    ax4.set(xlabel='t [d]',
            ylabel='l [m]')

    fig.savefig('fig/70/geometries.png')
    # plt.close('all')

res_min = np.nanmin([
    np.nanmin(
        [np.nanmin(all_trees_1['ag_factor']),
        np.nanmin(all_trees_1['bg_factor'])]
        ),
    np.nanmin(
        [np.nanmin(all_trees_2['ag_factor']),
        np.nanmin(all_trees_2['bg_factor'])]
        ),
    np.nanmin(
        [np.nanmin(all_trees_3['ag_factor']),
        np.nanmin(all_trees_3['bg_factor'])]
        ),
    np.nanmin(
        [np.nanmin(all_trees_4['ag_factor']),
        np.nanmin(all_trees_4['bg_factor'])]
        )],
    )
res_max = np.nanmax([
    np.nanmax(
        [np.nanmax(all_trees_1['ag_factor']),
        np.nanmax(all_trees_1['bg_factor'])]
        ),
    np.nanmax(
        [np.nanmax(all_trees_2['ag_factor']),
        np.nanmax(all_trees_2['bg_factor'])]
        ),
    np.nanmax(
        [np.nanmax(all_trees_3['ag_factor']),
        np.nanmax(all_trees_3['bg_factor'])]
        ),
    np.nanmax(
        [np.nanmax(all_trees_4['ag_factor']),
        np.nanmax(all_trees_4['bg_factor'])]
        )],
    )

bv_min = np.nanmin([
    np.nanmin(
        [np.nanmin(all_trees_1['biovolume']),
        np.nanmin(all_trees_1['biovolume'])]
        ),
    np.nanmin(
        [np.nanmin(all_trees_2['biovolume']),
        np.nanmin(all_trees_2['biovolume'])]
        ),
    np.nanmin(
        [np.nanmin(all_trees_3['biovolume']),
        np.nanmin(all_trees_3['biovolume'])]
        ),
    np.nanmin(
        [np.nanmin(all_trees_4['biovolume']),
        np.nanmin(all_trees_4['biovolume'])]
        )],
    )
bv_max = np.nanmax([
    np.nanmax(
        [np.nanmax(all_trees_1['biovolume']),
        np.nanmax(all_trees_1['biovolume'])]
        ),
    np.nanmax(
        [np.nanmax(all_trees_2['biovolume']),
        np.nanmax(all_trees_2['biovolume'])]
        ),
    np.nanmax(
        [np.nanmax(all_trees_3['biovolume']),
        np.nanmax(all_trees_3['biovolume'])]
        ),
    np.nanmax(
        [np.nanmax(all_trees_4['biovolume']),
        np.nanmax(all_trees_4['biovolume'])]
        )],
    )

fig = plt.figure(figsize=(10, 12), constrained_layout=False)

gs = GridSpec(18, 8)

ax1 = fig.add_subplot(gs[0:5, :])
ax1_1 = ax1.twinx()
ax2 = fig.add_subplot(gs[6:11, :])
ax3 = fig.add_subplot(gs[12:17, :])

ax1.plot(all_trees_1['time'], all_trees_1['biovolume'], label='Saltmarsh 1')
ax1.plot(all_trees_2['time'], all_trees_2['biovolume'], label='Saltmarsh 2')
ax1.plot(all_trees_3['time'], all_trees_3['biovolume'], label='Saltmarsh 3')
ax1.plot(all_trees_4['time'], all_trees_4['biovolume'], label='Saltmarsh 4')
ax1.set_title('Biovolume')
ax1.legend()

ax2.plot(all_trees_1['time'], all_trees_1['bg_factor'],
         all_trees_2['time'], all_trees_2['bg_factor'],
         all_trees_3['time'], all_trees_3['bg_factor'],
         all_trees_4['time'], all_trees_4['bg_factor'])
ax2.set_title('BG factor')

ax3.plot(all_trees_1['time'], all_trees_1['growth'],
         all_trees_2['time'], all_trees_2['growth'],
         all_trees_3['time'], all_trees_3['growth'],
         all_trees_4['time'], all_trees_4['growth'])

ax3.set_title('growth factor')

plt.savefig('fig/70/all_types.png')

i = 1
for n in [all_trees_1,
          all_trees_2,
          all_trees_3,
          all_trees_4]:

    all_trees_1 = n

    fig = plt.figure(figsize=(10, 12), constrained_layout=False)

    gs = GridSpec(18, 8)

    ax1 = fig.add_subplot(gs[0:5, :])
    ax1_1 = ax1.twinx()
    ax2 = fig.add_subplot(gs[6:11, :])
    ax3 = fig.add_subplot(gs[12:17, :])

    lns1 = ax1.plot(all_trees_1['time'], all_trees_1['growth'], label='growth',
             color='g')
    lns2 = ax1_1.plot(all_trees_1['time'], all_trees_1['maint'], label='maint',
               color='r')

    lns = lns1 + lns2
    labs = [l.get_label() for l in lns]

    ax1.legend(lns, labs, loc=0)
    ax1.set_title('Growth and Maintanance')
    ax1.set(ylabel='[-]')

    ax2.plot(all_trees_1['time'], all_trees_1['ag_factor'], label='Aboveground')
    ax2.plot(all_trees_1['time'], all_trees_1['bg_factor'], label='Belowground')
    ax2.set_ylim(res_min - res_min * 0.05, res_max + res_max * 0.05)
    ax2.legend()
    ax2.set_title('Resources')
    ax2.set(ylabel='[-]')

    ax3.plot(all_trees_1['time'], all_trees_1['biovolume'], label='total biovolume')
    ax3.plot(all_trees_1['time'], all_trees_1['biovolume_ag'], label='AG biovolume')
    ax3.plot(all_trees_1['time'], all_trees_1['biovolume_bg'], label='BG biovolume')
    ax3.legend()
    ax3.set_title('Biovolume')
    ax3.set_ylim(bv_min - bv_min * 0.05, bv_max + bv_max * 0.05)
    ax3.set(ylabel='m³')

    i += 1

    plt.savefig('fig/70/grow_maint_res_bvol_'+str(i)+'.png')
    # plt.close('all')

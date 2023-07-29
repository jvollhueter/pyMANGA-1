# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 12:48:29 2023

@author: Jonas
"""

import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.patches as patch
from scipy.interpolate import griddata


def legend_without_duplicate_labels(ax):
    handles, labels = ax.get_legend_handles_labels()
    unique = [(h, l) for i, (h, l) in enumerate(zip(handles,
                                                    labels)
                                                ) if l not in labels[:i]]
    ax.legend(*zip(*unique), framealpha=1, shadow=False, loc=1)


result_files =\
    glob.glob(
    r'*.csv')
result_files_avi = glob.glob('*.csv')
#result_files_rhi = glob.glob('R*.csv')

files_avi = []
files_rhi = []
salt_lims = []
files = []

# for result_file in result_files_avi:
#     file = pd.read_csv(result_file, sep='\t')
#     files_avi.append(file)
#     salt_lims.append((min(file['salinity']), max(file['salinity'])))

# for result_file in result_files_rhi:
#     file = pd.read_csv(result_file, sep='\t')
#     files_rhi.append(file)
#     salt_lims.append((min(file['salinity']), max(file['salinity'])))


# all_trees = pd.concat([pd.concat(files_rhi),
#                        pd.concat(files_avi)]).sort_values('time',
#                                                           ignore_index=True)

for result_file in result_files:
    file = pd.read_csv(result_file, sep='\t')
    files.append(file)
    salt_lims.append((min(file['salinity']), max(file['salinity'])))

salt_lim = (np.nanmin(salt_lims), np.nanmax(salt_lims))
levels = np.linspace(np.nanmin(salt_lims),
                     np.nanmax(salt_lims), num=11).round(3)

x, y = np.meshgrid(np.linspace(0, 50, 51), np.linspace(0, 10, 11))

all_trees = pd.concat(files)

ts = all_trees.time.unique().tolist()

time_max = max(ts) / 3600 / 24 / 365.25

salt_lim = (np.nanmin(salt_lims), np.nanmax(salt_lims))

levels = np.linspace(np.nanmin(salt_lims),
                     np.nanmax(salt_lims), num=11).round(3)

x, y = np.meshgrid(np.linspace(0, 50, 51), np.linspace(0, 10, 11))

ts_n = 0

for time in ts:

    trees = all_trees[all_trees["time"] == time]

    time = round((time / 86400 / 365.25), 4)
    trees = trees.sort_values(by='h_stem', ascending=True)

    fig = plt.figure(figsize=(12, 7),
                     constrained_layout=False)

    gs = GridSpec(15, 8)

    ax1 = fig.add_subplot(gs[0:4, :])
    ax2 = fig.add_subplot(gs[5:9, :])
    axc = fig.add_subplot(gs[11, 1:7])
    ax3 = fig.add_subplot(gs[14, 1:7])
    ax1.set(
        aspect='equal',
        xlim=(0, 50),
        ylim=(0, 10),
        xticklabels=[],
        ylabel='y [m]')

    ax2.set(
        aspect='equal',
        xlim=(0, 50),
        ylim=(0, 10),
        xlabel='x [m]',
        ylabel='y [m]')

    ax3.set(
        xlim=(0, time_max),
        ylim=(0, 1),
        xlabel=('t [a]'),
        yticklabels=[])

    for n in trees.index:
        if trees['tree'][n][0] == 'A':
            c = 'yellowgreen'
            label = 'Avicennia'
        elif trees['tree'][n][0] == 'R':
            c = 'green'
            label = 'Rizophora'
        elif trees['tree'][n][0] == 'I':
            c = 'green'
            label = 'Saltmarsh'
        circle = patch.Circle((trees['x'][n], trees['y'][n]),
                              radius=trees['r_crown'][n],
                              color=c,
                              ec='black',
                              label=label)
        ax1.add_patch(circle)
    legend_without_duplicate_labels(ax1)

    trees = trees.dropna(subset=['salinity'])

    try:
        salt = griddata((trees['x'],
                         trees['y']),
                        trees['salinity'],
                        (x, y),
                        method='nearest')

        salinity = ax2.contourf(x,
                                y,
                                salt,
                                levels=levels)
        cbar = fig.colorbar(salinity,
                            cax=axc,
                            orientation='horizontal',
                            label='Salinity [ppt]')
        cbar.ax.set_ylabel('Salinity')

    except:
        pass

    ax3.barh(0.5, time, 1)

    fig.savefig(r'fig/ts_' + str(ts_n))
    plt.close('all')
    ts_n += 1

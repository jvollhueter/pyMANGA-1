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


result_file = 'Population_t_0028512000.0.csv'


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

result_files = glob.glob(r'*.csv')

ts = 0

for file_n in result_files:

    file = pd.read_csv(file_n, sep='\t')
    
    file['salinity'] = (1 - file['bg_resources']) * 10
    salt_lim = (file['salinity'])
    levels = np.linspace(np.nanmin(salt_lim),
                         np.nanmax(salt_lim), num=11).round(3)
    
    x, y = np.meshgrid(np.linspace(0, 50, 51), np.linspace(0, 10, 11))
    
    all_trees = file
    
    ts = all_trees.time.unique().tolist()
    
    time_max = max(ts) / 3600 / 24 / 365.25
    
    time = ts[0]
    
    salt_lim = (np.nanmin(salt_lim), np.nanmax(salt_lim))
    
    # levels = np.linspace(np.nanmin(salt_lim),
    #                      np.nanmax(salt_lim), num=11).round(3)
    
    levels = np.linspace(0, 6, num=7).round(3)
    
    x, y = np.meshgrid(np.linspace(0, 50, 51), np.linspace(0, 10, 11))
    
    ts_n = 0
    
    
    trees = all_trees
    
    
    time = round((time / 86400 / 30.5), 4)
    trees = trees.sort_values(by='h_ag', ascending=True)
    
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
        xlim=(0, 12),
        ylim=(0, 1),
        xlabel=('t [month]'),
        yticklabels=[])
    
    for n in trees.index:
        if trees['plant'][n][0] == 'A':
            c = 'yellowgreen'
            label = 'Avicennia'
        elif trees['plant'][n][0] == 'R':
            c = 'green'
            label = 'Rizophora'
        elif trees['plant'][n][0] == 'I':
            c = 'green'
            label = 'Saltmarsh'
        circle = patch.Circle((trees['x'][n], trees['y'][n]),
                              radius=trees['r_ag'][n],
                              color=c,
                              ec='black',
                              label=label)
        ax1.add_patch(circle)
    legend_without_duplicate_labels(ax1)
    
    trees = trees.dropna(subset=['salinity'])
    
    
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
                        label='Salinity [%]')
    cbar.ax.set_ylabel('Salinity')
    
    
    ax3.barh(0.5, time, 1)
    
    fig.savefig(r'fig/ts_' + str(time) + '.png', dpi=1080)
    plt.close('all')
    ts_n += 1

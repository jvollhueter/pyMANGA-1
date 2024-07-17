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


result_files =\
    glob.glob(r'C:\Users\Jonas\Documents\MASCOT\SourceCode\pyMANGA-1\MyModel\Outputs\OnePlant\default\*.csv')

pj = 'default'

# if not os.path.exists('fig_OnePlant/' + pj):

#     os.makedirs('fig/OnePlant_maint/' + pj)


files_avi = []
files_rhi = []
salt_lims = []
files = []

for result_file in result_files:
    file = pd.read_csv(result_file, sep='\t')
    files.append(file)

x, y = np.meshgrid(np.linspace(0, 50, 51), np.linspace(0, 10, 11))

all_trees = pd.concat(files)

all_trees['time'] = all_trees['time'] / 3600 / 24

n = 1

for result_file in result_files:

    fig = plt.figure(figsize=(10, 16), constrained_layout=False)

    gs = GridSpec(23, 8)

    ax1 = fig.add_subplot(gs[0:5, :])
    ax2 = fig.add_subplot(gs[6:11, :])
    ax3 = fig.add_subplot(gs[12:17, :])
    ax4 = fig.add_subplot(gs[18:23, :])

    ax1.plot(all_trees['time'], all_trees['h_ag'])
    ax1.set_title('$h_{ag}$')
    ax1.set(ylabel='l [m]')

    ax2.plot(all_trees['time'], all_trees['r_ag'])
    ax2.set_title('$r_{ag}$')
    ax2.set(ylabel='l [m]')

    ax3.plot(all_trees['time'], all_trees['h_bg'])
    ax3.set_title('$h_{bg}$')
    ax3.set(ylabel='l [m]')

    ax4.plot(all_trees['time'], all_trees['r_bg'])
    ax4.set_title('$r_{bg}$')
    ax4.set(xlabel='t [d]',
            ylabel='l [m]')

    fig.savefig('fig/OnePlant_maint/geometries_' + pj + '.png')
    plt.close('all')

    fig = plt.figure(figsize=(10, 8), constrained_layout=False)

    gs = GridSpec(12, 8)

    ax1 = fig.add_subplot(gs[0:5, :])
    ax2 = fig.add_subplot(gs[6:11, :])

    ax1.plot(all_trees['time'], all_trees['growth'], label='growth')
    ax1.plot(all_trees['time'], all_trees['maint'], label='maint')
    ax1.legend()
    ax1.set_title('Growth and Maintanance')
    ax1.set(ylabel='[-]')

    ax2.plot(all_trees['time'], all_trees['ag_factor'], label='Aboveground')
    ax2.plot(all_trees['time'], all_trees['bg_factor'], label='Belowground')
    ax2.legend()
    ax2.set_title('Resources')
    ax2.set(ylabel='[-]')

    n += 1

    #plt.savefig('fig/OnePlant_maint/growth_' + pj + '.png')
    #plt.close('all')

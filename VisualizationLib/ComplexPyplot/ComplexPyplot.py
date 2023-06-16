#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
from matplotlib import patches as patch
from matplotlib import pyplot as plt
from VisualizationLib.Visualization import Visualization
import pandas as pd
import numpy as np
from matplotlib.gridspec import GridSpec
from scipy.interpolate import griddata

class ComplexPyplot(Visualization):


    def __init__(self, args):
        self.case = args.find("type").text

        print("Initiate visualization of type " + self.case + ".")
        try:
            self._pause = float(args.find("max_fps").text)
        except AttributeError:
            self._pause = 3
            print("Tag 'max_fps' in '" + self.case +
                  "' visualization is missing! Figure is shown for 3 s.")

        self.fig = plt.figure(figsize=(8, 8),
                         constrained_layout=False)
        gs = GridSpec(8, 8)
        self._ax1 = self.fig.add_subplot(gs[0:3, :])
        self._ax2 = self.fig.add_subplot(gs[3:6, :])
        self._axc = self.fig.add_subplot(gs[7, 2:6])


    def update(self, plant_groups, time):
        def legend_without_duplicate_labels(ax):

            handles, labels = ax.get_legend_handles_labels()
            unique = [(h, l) for i, (h, l) in enumerate(zip(handles,
                                                            labels)
                                                        ) if l not in labels[:i]]
            ax.legend(*zip(*unique), framealpha=1, shadow=False, loc=1)

        max_x = []
        min_x = []
        max_y = []
        min_y = []
        plants = []
        random = True

        for group_name, plant_group in plant_groups.items():

            if plant_group.distribution_type == 'Random':

                if random is True:
                    max_x.append(plant_group.x_1 + plant_group.l_x)
                    min_x.append(plant_group.x_1)
                    max_y.append(plant_group.y_1 + plant_group.l_y)
                    min_y.append(plant_group.y_1)
                else:
                    random = False
            else:
                random = False

            species = plant_group.species
            n = []
            x = []
            y = []
            r = []
            s = []
            h = []
            c = []

            for plant in plant_group.getPlants():
                n.append(group_name)
                if species == 'Avicennia':
                    color = 'darkolivegreen'
                elif species == 'Rhizophora':
                    color = 'greenyellow'
                else:
                    color = 'black'

                xx, yy = plant.getPosition()
                x.append(xx)
                y.append(yy)
                r.append(plant.getGeometry()["r_crown"])
                h.append(plant.getGeometry()["h_stem"])
                c.append(color)
                try:
                    s.append(plant.getGrowthConceptInformation()['salinity'])
                except:
                    s.append(np.nan)
            plants.append(pd.DataFrame(list(zip(n, x, y, r, s, h, c)),
                         columns=['name', 'x', 'y', 'r', 's', 'h', 'c']))

        for group in plants:

            if random is False:
                max_x.append(max(group['x']))
                min_x.append(min(group['x']))
                max_y.append(max(group['y']))
                min_y.append(min(group['y']))

        all_plants = pd.concat(plants).sort_values(by='h', ignore_index=True)

        for n in all_plants.index:
            circle = patch.Circle((all_plants['x'][n], all_plants['y'][n]),
                                  radius=all_plants['r'][n],
                                  label=all_plants['name'][n],
                                  color=all_plants['c'][n])
            self._ax1.add_patch(circle)

        legend_without_duplicate_labels(self._ax1)

        levels = np.linspace(np.nanmin(all_plants['s']),
                             np.nanmax(all_plants['s']), num=11).round(3)

        try:
            x, y = np.meshgrid(np.linspace(0, 50, 51), np.linspace(0, 20, 21))
            salt = griddata((all_plants['x'],
                             all_plants['y']),
                            all_plants['s'],
                            (x, y),
                            method='nearest')

            salinity = self._ax2.contourf(x,
                                          y,
                                          salt,
                                          levels=levels)
            cbar = self.fig.colorbar(salinity,
                                     cax=self._axc,
                                     orientation='horizontal',
                                     label='Salinity [ppt]')
            cbar.ax.set_ylabel('Salinity')

        except:
             pass

        max_x = max(max_x) + 2
        min_x = min(min_x) - 2
        max_y = max(max_y) + 2
        min_y = min(min_y) - 2

        self._ax1.set(
            aspect='equal',
            xlim=(min_x, max_x),
            ylim=(min_y, max_y),
            xticks=[],
            ylabel='y [m]',
            title='Time: ' + self.createTimestring(time))

        self._ax2.set(
            aspect='equal',
            xlim=(min_x, max_x),
            ylim=(min_y, max_y),
            xlabel='x [m]',
            ylabel='y [m]')

        self._axc.set(
            aspect=0.2)

        plt.draw()
        plt.pause(self._pause)


    def show(self, time):

        pass


    def createTimestring(self, arg):

        timestring = ""
        if (type(arg) == float):
            arg = arg / (60 * 60 * 24 * 365.25)
            timestring = "%2.2f" % arg + ' a'
        else:
            timestring = str(arg)
        return timestring
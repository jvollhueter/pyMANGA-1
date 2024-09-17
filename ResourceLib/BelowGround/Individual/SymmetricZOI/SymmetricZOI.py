#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from ResourceLib import ResourceModel


class SymmetricZOI(ResourceModel):
    """
    SymmetricZOI below-ground resource concept.
    """
    def __init__(self, args):
        """
        Args:
            args (lxml.etree._Element): below-ground module specifications from project file tags
        """
        case = args.find("type").text
        self.getInputParameters(args)
        super().makeGrid()


    def calculateBelowgroundResources(self):
        """
        Calculate a growth reduction factor for each plant based on competition with neighboring plants.
        Sets:
            numpy array with shape(number_of_plants)
        """
        # Numpy array of shape [res_x, res_y, n_plants]
        for i in range(len(self.xe)):
            distance = (((self.my_grid[0] - np.array(self.xe)[i])**2 +
                         (self.my_grid[1] - np.array(self.ye)[i])**2)**0.5)
            min_distance = np.min(distance)

            # Array of shape distance [res_x, res_y, n_plants], indicating which
            # cells are occupied by plant root plates
            root_radius = np.array([self.r_root[i]])
            # If root radius < mesh size, set it to mesh size
            root_radius[np.where(root_radius < min_distance)] = min_distance
            plants_present = root_radius >= distance

            # Count all nodes, which are occupied by plants
            # returns array of shape [n_plants]
            # BETTINA ODD 2017: variable 'countbelow'
            plant_counts = plants_present.sum(axis=(0, 1))
            print('plant_counts:')
            print(plant_counts)

            # Calculate reciprocal of cell-own variables (array to count wins)
            # BETTINA ODD 2017: variable 'compete_below'
            # [res_x, res_y]
            denom = plants_present.sum(axis=-1)
            print(plants_present)
            plants_present_reci = np.divide(1, denom, where=denom != 0)

            # Sum up wins of each plant = plants_present_reci[plant]
            n_plants = len(plants_present[0, :])
            plant_wins = np.zeros(n_plants)

        for i in range(n_plants):
            plant_wins[i] = np.sum(plants_present_reci[np.where(plants_present[:, i])])
        self.belowground_resources = plant_wins / plant_counts
        print('bg_resources:')
        print(self.belowground_resources)


    def getInputParameters(self, args):
        tags = {
            "prj_file": args,
            "required": ["type", "domain", "x_1", "x_2", "y_1", "y_2", "x_resolution", "y_resolution"],
            "optional": ["allow_interpolation"]
        }
        super().getInputParameters(**tags)
        self._x_1 = self.x_1
        self._x_2 = self.x_2
        self._y_1 = self.y_1
        self._y_2 = self.y_2
        self.x_resolution = int(self.x_resolution)
        self.y_resolution = int(self.y_resolution)

        self.allow_interpolation = super().makeBoolFromArg("allow_interpolation")


    def prepareNextTimeStep(self, t_ini, t_end):
        self.xe = []
        self.ye = []
        self.r_root = []
        self.t_ini = t_ini
        self.t_end = t_end

    def addPlant(self, plant):
        x, y = plant.getPosition()
        geometry = plant.getGeometry()
        # ToDo: resolve when all geometries are renamed
        try:
            r_root = geometry["r_root"]
        except KeyError:
            r_root = geometry["r_bg"]
        if r_root < (self.mesh_size * 1 / 2**0.5):
            if not hasattr(self, "allow_interpolation") or not self.allow_interpolation:
                print("ERROR: mesh too course for below-ground module!")
                print("Please refine mesh or increase initial root radius above " +
                      str(self.mesh_size) + "m or allow interpolation.")
                exit()

        self.xe.append(x)
        self.ye.append(y)
        self.r_root.append(r_root)

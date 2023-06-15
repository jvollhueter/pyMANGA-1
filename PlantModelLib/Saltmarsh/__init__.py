#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 15:25:03 2018

@author: bathmann
"""

from .Saltmarsh import Saltmarsh
import numpy as np


class Saltmarsh(PlantModel):
    def __init__(self, args):
        """
        Plant model concept.
        Args:
            args: Bettina module specifications from project file tags
        """
        print("Growth and death dynamics of type Saltmarsh.")
        super().iniMortalityConcept(args)

    def prepareNextTimeStep(self, t_ini, t_end):
        """
        Prepare next time step by initializing relevant variables.
        Args:
            t_ini (int): start of current time step in seconds
            t_end (int): end of current time step in seconds
        """
        self.time = t_end - t_ini

    def progressPlant(self, tree, aboveground_resources, belowground_resources):
        """
        Manage growth procedures for a timestep --- read tree geometry and parameters,
        schedule computations, and update tree geometry and survival.
        Args:
            tree (dict): tree object
            aboveground_resources (float): aboveground resource growth reduction factor
            belowground_resources (float): belowground resource growth reduction factor
        """
        geometry = tree.getGeometry()
        growth_concept_information = tree.getGrowthConceptInformation()
        self.parameter = tree.getParameter()
        self.r_ag = geometry["r_ag"]
        self.r_bg = geometry["r_bg"]
        self.h_ag = geometry["h_ag"]
        self.h_bg = geometry["h_bg"]
        self.survive = 1

        self.treeVolume()

        # Define variables that are only required for specific Mortality
        # concepts
        super().setMortalityVariables(growth_concept_information)

        self.treeMaintenance()
        self.bgResources(belowground_resources)
        self.agResources(aboveground_resources)
        self.growthResources()
        self.treeGrowthWeights()
        self.treeGrowth()

        geometry["r_ag"] = self.r_ag
        geometry["r_bg"] = self.r_bg
        geometry["h_ag"] = self.h_ag
        geometry["h_bg"] = self.h_bg
        growth_concept_information[
            "root_surface_resistance"] = self.root_surface_resistance
        growth_concept_information["xylem_resistance"] = self.xylem_resistance
        growth_concept_information["ag_resources"] = self.ag_resources
        growth_concept_information["bg_resources"] = self.bg_resources
        growth_concept_information["growth"] = self.grow
        growth_concept_information["available_resources"] = (
            self.available_resources)
        psi_zero = self.deltaPsi()
        growth_concept_information["psi_zero"] = psi_zero
        growth_concept_information["salinity"] = (
            (belowground_resources * psi_zero - psi_zero) / 85000000.)
        growth_concept_information["weight_ag"] = \
            self.weight_girthgrowth
        growth_concept_information["weight_bg"] = \
            self.weight_stemgrowth

        # Get Mortality-related variables
        super().getMortalityVariables(growth_concept_information)

        tree.setGeometry(geometry)
        tree.setGrowthConceptInformation(growth_concept_information)
        if self.survive == 1:
            tree.setSurvival(1)
        else:
            tree.setSurvival(0)

    def treeGrowth(self):
        """
        Update tree geometry.

        For equation formulation, see Peters, Olagoke and Berger
        ([2018](https://doi.org/10.1016/j.ecolmodel.2018.10.005)), Appendix B (Bettina ODD), section 7.2,
        heading 'increase of allometric measures'.
        Sets:
            multiple float
        """
        self.r_ag = self.r_ag * self.grow
        self.r_bg = self.r_bg * self.grow
        self.h_ag = self.h_ag * self.grow
        self.h_bg = self.h_bg * self.grow

    def treeGrowthWeights(self):
        """
        Calculate the growth weights for distributing biomass increment to the tree geometries.

        For equation formulation, see Peters, Olagoke and Berger
        ([2018](https://doi.org/10.1016/j.ecolmodel.2018.10.005)), Appendix B (Bettina ODD), section 7.2,
        heading 'weights'.
        Sets:
            multiple float
        """
        self.weight_ag = np.nan
        self.weight_bg = np.nan


    def treeMaintenance(self):
        """
        Calculate the resource demand for biomass maintenance.

        For parameter reference, see Peters, Olagoke and Berger
        ([2018](https://doi.org/10.1016/j.ecolmodel.2018.10.005)), Appendix B (Bettina ODD), section 2.5.
        Sets:
            float
        """
        self.maint = self.volume * self.parameter["maint_factor"] * self.time


    ## This function calculates the total tree volume.
    def plantVolume(self):
        """
        Calculate the total tree volume.

        For equation formulation, see Peters, Olagoke and Berger
        ([2018](https://doi.org/10.1016/j.ecolmodel.2018.10.005)), Appendix B (Bettina ODD), section 7.2,
        heading 'volume of plant components'.
        Sets:
            float
        """
        self.volume_ag = 1
        self.volume_bg = 1
        self.volume = self.volume_ag + self.volume_bg

    def agResources(self, aboveground_resources):
        """
        Calculate the available aboveground resources (intercepted light measured equivalent to respective water uptake).

        For equation formulation, see Peters, Olagoke and Berger
        ([2018](https://doi.org/10.1016/j.ecolmodel.2018.10.005)), Appendix B (Bettina ODD), section 7.2,
        heading 'resistances'.
        Args:
            aboveground_resources (float): aboveground resource growth reduction factor
        Sets:
            float
        """
        self.ag_resources = aboveground_resources * (
            np.pi * self.r**2 * self.parameter["sun_c"] * self.time)

    def bgResources(self, belowground_resources):
        """
        Calculate the available belowground resources (m³ water per time step).

        For equation formulation, see Peters, Olagoke and Berger
        ([2018](https://doi.org/10.1016/j.ecolmodel.2018.10.005)), Appendix B (Bettina ODD), section 7.2,
        heading 'resistances'.
        Args:
            belowground_resources (float): belowground resource growth reduction factor
        Sets:
            float
        """
        self.rootSurfaceResistance()
        self.xylemResistance()
        self.bg_resources = belowground_resources * (
            (-self.time * self.deltaPsi() /
             (self.root_surface_resistance + self.xylem_resistance) / np.pi))

    def rootSurfaceResistance(self):
        """
        Calculate the root surface resistance.

        For equation formulation, see Peters, Olagoke and Berger
        ([2018](https://doi.org/10.1016/j.ecolmodel.2018.10.005)), Appendix B (Bettina ODD), section 7.2,
        heading 'resistances'.
        Sets:
            float
        """
        self.root_surface_resistance = (1 / self.parameter["lp"] /
                                        self.parameter["k_geom"] / np.pi /
                                        self.r_bg**2 / self.h_bg)

    def xylemResistance(self):
        """
        Calculate the xylem resistance.

        For equation formulation, see Peters, Olagoke and Berger
        ([2018](https://doi.org/10.1016/j.ecolmodel.2018.10.005)), Appendix B (Bettina ODD), section 7.2,
        heading 'resistances'.
        Sets:
            float
        """
        self.xylem_resistance = (self.flow_length / self.parameter["kf_sap"] /
                                 np.pi / self.r_stem**2)

    def deltaPsi(self):
        """
        Calculate the water potential gradient with soil water potential = 0.

        For equation formulation, see Peters, Olagoke and Berger
        ([2018](https://doi.org/10.1016/j.ecolmodel.2018.10.005)), Appendix B (Bettina ODD), section 7.2,
        heading 'resources'.
        Returns:
            float
        """
        return (self.parameter["leaf_water_potential"] +
                (2 * self.r_ag + self.h_stem) * 9810)

    def growthResources(self):
        """
        Calculate the available resources and the biomass increment.

        For equation formulation, see Peters, Olagoke and Berger
        ([2018](https://doi.org/10.1016/j.ecolmodel.2018.10.005)), Appendix B (Bettina ODD), section 7.2,
        heading 'resources'.
        Sets:
            multiple float
        """
        self.available_resources = min(self.ag_resources, self.bg_resources)
        self.grow = (self.parameter["growth_factor"] *
                     (self.available_resources - self.maint))
        # Check if trees survive based on selected mortality concepts
        super().setTreeKiller()
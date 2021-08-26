#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""

from pyMANGA.TreeModelLib.AbovegroundCompetition.AbovegroundCompetition import AbovegroundCompetition
from pyMANGA.TreeModelLib.BelowgroundCompetition.BelowgroundCompetition import BelowgroundCompetition
from pyMANGA.TreeModelLib.GrowthAndDeathDynamics.GrowthAndDeathDynamics import GrowthAndDeathDynamics
from pyMANGA.VisualizationLib.Visualization import Visualization
from pyMANGA.TreeOutputLib.TreeOutput import TreeOutput
from pyMANGA.PopulationLib.Population import Population
from pyMANGA.TimeLoopLib.TreeDynamicTimeLoop import TreeDynamicTimeLoop
import numpy as np


## Class to store and manage all information necessary for a MANGA model run.
class MangaProject:
    ## Parent class for MangaProjects.
    def argsToProject(self):
        self.iniNumpyRandomSeed()
        self.iniAbovegroundCompetition()
        self.iniBelowgroundCompetition()
        self.iniDeathAndGrowthConcept()
        self.iniPopulation()
        self.iniTreeTimeLoop()
        self.iniVisualization()
        self.iniTreeOutput()

    def getBelowgroundCompetition(self):
        return self.belowground_competition

    def iniNumpyRandomSeed(self):
        if self.args["random_seed"] is not None:
            print("Setting seed for random number generator.")
            _seed = int(self.args["random_seed"].text.strip())
            np.random.seed(_seed)

    def iniBelowgroundCompetition(self):
        arg = self.args["belowground_competition"]
        self.belowground_competition = (BelowgroundCompetition(arg))

    def getAbovegroundCompetition(self):
        return self.aboveground_competition

    def iniAbovegroundCompetition(self):
        arg = self.args["aboveground_competition"]
        self.aboveground_competition = (AbovegroundCompetition(arg))

    def getDeathAndGrowthConcept(self):
        return self.growth_and_death_dynamics

    def iniDeathAndGrowthConcept(self):
        arg = self.args["tree_growth_and_death"]
        self.growth_and_death_dynamics = (GrowthAndDeathDynamics(arg))

    def iniPopulation(self):
        arg = self.args["initial_population"]
        self.population = (Population(arg))

    def getPopulation(self):
        return self.population

    def iniTreeTimeLoop(self):
        arg = self.args["tree_time_loop"]
        self.tree_time_stepping = (TreeDynamicTimeLoop(arg))

    def getTreeTimeStepping(self):
        return self.tree_time_stepping

    def iniVisualization(self):
        arg = self.args["visualization"]
        self.visualization = Visualization(arg)

    def getVisualization(self):
        return self.visualization

    ## Constructor for tree output
    def iniTreeOutput(self):
        arg = self.args["tree_output"]
        ## Containing configuration on tree_output
        self.tree_output = TreeOutput(arg)

    ## Returns tree output defined for the project
    def getTreeOutput(self):
        return self.tree_output

    def runProject(self, time_stepping):
        self.tree_time_stepping.runTimeLoop(time_stepping)

    def getProjectArguments(self):
        return self.args

    def getProjectArgument(self, key):
        return self.args[key]

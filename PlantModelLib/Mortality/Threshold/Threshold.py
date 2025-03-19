#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from PlantModelLib.Mortality.NoGrowth import NoGrowth
from PlantModelLib.PlantModel import PlantModel


class Threshold(NoGrowth):
    """
    Threshold mortality module.
    """
    def __init__(self, args):
        """
        Args:
            args: module specification from project file tags
            case: "Threshold" (module name)
        """
        super().__init__(args)
        # Read input parameters from xml file
        self.getInputParameters(args)

    def setSurvive(self, plant_module):
        self._survive = 1

        if self.threshold_type == "biovolume":
            if plant_module.volume < self.threshold:
                self._survive = 0
            try:
                if self.age > 3.154e+7 and self.volume < 0.01:
                    self._survive = 0
            except:
                pass
        else:
            AttributeError("Threshold type not implemented.")

    def getSurvive(self):

        return self._survive

    def getInputParameters(self, args):

        tags = {
            "prj_file": args,
            "optional": ["type", "mortality", "threshold", "threshold_type"]
        }
        print("tags: ", tags)
        super().getInputParameters(**tags)

        # Set default values if no inputs are given
        if not hasattr(self, "threshold_type"):
            self.threshold_type = "biovolume"
            print("> Set mortality parameter 'threshold_type' to default:", self.threshold_type)

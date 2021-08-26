#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2018-Today
@author: jasper.bathmann@ufz.de
"""
from pyMANGA.TreeOutputLib.TreeOutput import TreeOutput
import os


## Output class. This class creates one file per timestep at a defined
#  location. A line containing time, position, desired geometric measures and
#  desired parameters is written at every nth timestep.
class OneTimestepOneFile(TreeOutput):
    ## Constructor of dummy objects in order to drop output
    #  @param args xml element parsed from project to this constructor.
    def __init__(self, args):
        ## Directory, where output is saved. Please make sure it exists and is
        #  empty.
        self.output_dir = self.checkRequiredKey("output_dir", args)
        ## N-timesteps between two outputs
        self.output_each_nth_timestep = int(
            self.checkRequiredKey("output_each_nth_timestep", args))
        ## Check if overwrite of previous output is allowed
        allow_previous_output = args.find("allow_previous_output")
        if allow_previous_output is not None:
            allow_previous_output = eval(allow_previous_output.text)
        else:
            allow_previous_output = False

        ## Geometric measures included in output
        self.geometry_outputs = []
        ## Parameters included in output
        self.parameter_outputs = []
        ## Parameters included in output
        self.growth_outputs = []
        ## Network information included in output
        self.network_outputs = []
        ## Counter for output generation
        self._output_counter = 0
        for key in args.iterchildren("geometry_output"):
            self.geometry_outputs.append(key.text.strip())
        for key in args.iterchildren("parameter_output"):
            self.parameter_outputs.append(key.text.strip())
        for key in args.iterchildren("growth_output"):
            self.growth_outputs.append(key.text.strip())
        for key in args.iterchildren("network_output"):
            self.network_outputs.append(key.text.strip())
        try:
            dir_files = len(os.listdir(self.output_dir))
        except FileNotFoundError:
            print("No such directory: '" + self.output_dir +
                  "' as defined in the project file." +
                  " Creating directory...")
            os.mkdir(self.output_dir)
            dir_files = 0
        if (dir_files > 0 and allow_previous_output == False):
            raise ValueError("Output directory '" + self.output_dir +
                             "' is not empty.")
        print(
            "Output to '" + self.output_dir + "' of tree positions, the " +
            "parameters ", self.parameter_outputs,
            " and geometric" + " measures ", self.geometry_outputs,
            " at every " + str(self.output_each_nth_timestep) +
            " timesteps initialized.")

    ## Writes output to predefined folder
    #  For each timestep a file is created throughout the simulation.
    #  This function is only able to work, if the output directory exists and
    #  is empty at the begin of the model run
    def writeOutput(self, tree_groups, time):
        self._output_counter = (self._output_counter %
                                self.output_each_nth_timestep)

        if self._output_counter == 0:
            delimiter = "\t"
            filename = ("Population_t_%012.1f" % (time) + ".csv")
            file = open(os.path.join(self.output_dir, filename), "w")
            string = ""
            string += 'tree' + delimiter + 'time' + delimiter + 'x' + \
                      delimiter + 'y'
            for geometry_output in self.geometry_outputs:
                string += delimiter + geometry_output
            for parameter_output in self.parameter_outputs:
                string += delimiter + parameter_output
            for growth_output in self.growth_outputs:
                string += delimiter + growth_output
            for network_output in self.network_outputs:
                string += delimiter + network_output
            string += "\n"
            file.write(string)
            for group_name, tree_group in tree_groups.items():
                for tree in tree_group.getTrees():
                    growth_information = tree.getGrowthConceptInformation()
                    string = ""
                    string += (group_name + "_" + "%09.0d" % (tree.getId()) +
                               delimiter + str(time) + delimiter +
                               str(tree.x) + delimiter + str(tree.y))
                    if (len(self.geometry_outputs) > 0):
                        geometry = tree.getGeometry()
                        for geometry_output in self.geometry_outputs:
                            string += delimiter + str(
                                geometry[geometry_output])
                    if (len(self.parameter_outputs) > 0):
                        parameter = tree.getParameter()
                        for parameter_output in self.parameter_outputs:
                            string += delimiter + str(
                                parameter[parameter_output])
                    if (len(self.growth_outputs) > 0):
                        for growth_output_key in self.growth_outputs:
                            try:
                                string += delimiter + str(
                                    growth_information[growth_output_key])
                            except KeyError:
                                growth_information[growth_output_key] = "NaN"
                                string += delimiter + str(
                                    growth_information[growth_output_key])
                                print(
                                    "Key " + growth_output_key +
                                    " might be not available in growth "+
                                    "concept!" +
                                    " Please read growth concept documentation."
                                )
                    if len(self.network_outputs) > 0:
                        network = tree.getNetwork()
                        for network_output in self.network_outputs:
                            string += delimiter + str(network[network_output])
                    string += "\n"
                    file.write(string)
                    for growth_output in self.growth_outputs:
                        del(growth_information[growth_output])
            file.close()
        self._output_counter += 1

    ## This function checks if a key exists and if its text content is empty.
    #  Raises key-errors, if the key is not properly defined.
    #  @param key Name of the key to be checked
    #  @param args args parsed from project. Xml-element
    def checkRequiredKey(self, key, args):
        tmp = args.find(key)
        if tmp is None:
            raise KeyError("Required key '" + key + "' in project file at " +
                           "position MangaProject__tree_output is missing.")
        elif tmp.text.strip() == "":
            raise KeyError("Key '" + key + "' in project file at position " +
                           "MangaProject__tree_output needs to be specified.")
        return tmp.text

    ## This function returns the output directory
    def getOutputDir(self):
        return self.output_dir
